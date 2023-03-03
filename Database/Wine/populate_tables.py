"""
Populates tables in wine_db that were created in create_tables.py
"""

"""
Helper functions
"""


# checks if value passed in is any number of ways of expressing null/no value.
# this is how we normalize naturally inconsistent data passed in
def null( value ):
    if value is None or value == '0' or value == 0 or value == '' or value == 'None' or value == 'None.':
        return True
    return False


# generate representation of value to pass in with statement
# adds quotes around a value so it's friendly to pass in for SQL
# finds null values and standardizes how they present to execute in MySQL
def generate_value_statement( dictionary, value ):
    return ("'" + str( dictionary[ value ] ) + "'") if (not null( dictionary[ value ] )) else 'NULL'


# removes html formatting
# removes apostrophes and mid-text single quotes, which caused a lot of problems with automating table insertion
# makes sure text that's returned begins and ends with a single quote
def parse_description( text ):
    # remove all breaks for human readability - they're always next to '\r's anyway, so we're preserving the newline
    while '<br>' in text:
        index = text.index( '<br>' )
        if index != 0:
            text = text[ 0:index ] + text[ index + 4: ]
        else:
            text = text[ index + 4: ]
    
    # remove all \u201x occurrences (where x can be any character)
    while '\\u201' in text:
        index = text.index( '\\u201' )
        text = text[ 0:index ] + text[ index + 6: ]
    
    # remove or replace all escape sequence characters
    while '\\' in text:
        index = text.index( '\\' )
        new_text = text[ 0:index ]
        
        # replace new lines
        if text[ index + 1 ] == 'n' or text[ index + 1 ] == 'r':
            new_text += '\n'  # maybe change later depending on OS and how it prints - carriage return vs new line
        # remove apostrophe
        elif text[ index + 1 ] == "'":
            pass
        # if not a newline or apostrophe, replace with a space and move on
        else:
            new_text += ' '
        
        new_text += text[ index + 2: ]
        text = new_text
    
    # loop through and make sure there are no plain ' s or ` s or ’ s
    i = 0
    while i < len( text ):
        if (text[ i ] == "'" or text[ i ] == "’" or text[ i ] == "`") and i > 0 and text[ i - 1 ] != '\\':
            text = text[ 0:i ] + text[ i + 1: ]
            # don't increment i since we removed a character, it's like we moved forward 1 anyway
        else:
            i += 1
    
    # make sure there's a ' at the beginning and end of the string
    prefix = ''
    suffix = ''
    if text[ 0 ] != "\'":
        prefix = "'"
    if text[ len( text ) - 1 ] != "\'":
        suffix = "'"
    
    final_str = prefix + text + suffix
    words = final_str.split()
    
    value = ""
    for word in words:
        value += word + " "
    
    return value


"""
Generating MySQL statements to populate the tables
"""


# we have to populate wine_info and note_categories first bc of primary keys
def add_to_wine_info_table( wine ):
    """
    insert general wine info into wine_info table
    :param wine: JSON object representing a wine
    :return: MySQL statement to insert row representing wine into wine_info table
    """
    info = wine[ 'general' ]
    statement = 'INSERT INTO wine_info VALUES ('
    # id INT UNSIGNED NOT NULL - we're not using generate_value_statement() here bc it can't be null
    statement += str( info[ 'id' ] ) + ', '
    # id_without_vintage MEDIUMINT UNSIGNED - no quotes around it, since it's an int
    statement += (str( info[ 'id_without_vintage' ] ) if (
        not null( info[ 'id_without_vintage' ] )) else 'NULL') + ', '
    # wine VARCHAR(69)
    statement += parse_description(
        generate_value_statement( info, 'wine' ) ) + ', '  # remove apostrophes from wine name
    # winery VARCHAR(51)
    statement += parse_description(
        generate_value_statement( info, 'winery' ) ) + ', '  # remove apostrophes from winery name
    # type ENUM('Red wine', 'White wine', 'Sparkling wine', 'Dessert wine', 'Rosé wine', 'Fortified Wine')
    statement += "'" + info[ 'type' ] + "', "  # never null
    # wine_description VARCHAR(1137)
    statement += (parse_description( info[ 'wine_description' ] ) if not null(
        info[ 'wine_description' ] ) else "'NULL'") + ', '
    # winery_description VARCHAR(3723)
    statement += (parse_description( info[ 'winery_description' ] ) if not null(
        info[ 'winery_description' ] ) else "'NULL'") + ', '
    # region VARCHAR(43)
    statement += parse_description(
        generate_value_statement( info, 'region' ) ) + ', '  # remove apostrophes from region name
    # country VARCHAR(31)
    statement += parse_description(
        generate_value_statement( info, 'country' ) ) + ', '  # remove apostrophes from country name
    # rating DECIMAL(2, 1) - decimals cannot be null
    statement += (str( info[ 'rating' ] ) + ', ') if (not null( info[ 'rating' ] )) else '0, '
    # price DECIMAL(4, 2)
    statement += (str( info[ 'price' ] ) + ', ') if (not null( info[ 'price' ] )) else '0, '
    # image_link VARCHAR(59)
    statement += generate_value_statement( info, 'image_link' ) + ')'
    
    return statement


def add_to_note_categories_table( wine, cursor ):
    """
    :param wine: JSON object representing a wine
    :return: list of MySQL statements to insert notes into table
    """
    statements = [ ]
    note_cards = wine[ 'traits' ][ 'notes' ]
    
    # get notes already in the table so we don't duplicate primary keys
    cursor.execute( 'SELECT note FROM note_categories' )
    notes_already_there_unprocessed = cursor.fetchall()
    notes_already_there = [ note[ 0 ] for note in notes_already_there_unprocessed ]
    
    if not null( note_cards ):
        for note_card in note_cards:
            # each note card is something like ['vanilla, cinnamon, allspice', 'toasty']
            notes = note_card[ 0 ].split( ',' )
            for note in notes:
                # each wine id (PK) is guaranteed to be unique, but not every note is, so we have to make sure we don't
                # already have info about that note
                if null( notes_already_there ) or note.strip() not in notes_already_there:
                    note = parse_description( note.strip() )  # remove apostrophes from note
                    
                    category = note_card[ 1 ] if note_card[ 1 ][ 0 ] == '\'' else '\'' + note_card[ 1 ]
                    category += '\'' if note_card[ 1 ][ -1 ] != '\'' else ''
                    
                    # creating statement
                    statements.append( 'INSERT INTO note_categories VALUES (' + note + ', ' + category + ')' )
    
    return statements


# now all the tables with foreign keys
def add_to_wine_traits_table( wine ):
    """
    :param wine: JSON object representing a wine
    :return: a MySQL statement to insert row representing wine into wine_info table
    """
    info = wine[ 'traits' ]
    statement = 'INSERT INTO wine_traits VALUES ('
    # id INT UNSIGNED NOT NULL - we're not using generate_value_statement() here bc it can't be null
    statement += str( wine[ 'general' ][ 'id' ] ) + ', '
    # style_description VARCHAR(1490)
    statement += parse_description( generate_value_statement( info, 'style_description' ) ) + ', '
    # style_blurb VARCHAR(1490)
    statement += parse_description( generate_value_statement( info, 'style_blurb' ) ) + ', '
    # alcohol_content DECIMAL(4, 2)
    statement += (str( info[ 'alcohol_content' ] ) + ', ') if (not null( info[ 'alcohol_content' ] )) else '0, '
    # sweetness TINYINT
    statement += (str( info[ 'sweetness' ] ) + ', ') if (not null( info[ 'sweetness' ] )) else '0, '
    # body TINYINT
    statement += (str( info[ 'body' ] ) + ', ') if (not null( info[ 'body' ] )) else '0, '
    # body_description ENUM('Full-bodied', 'Very full-bodied', 'Medium-bodied', 'Light-bodied', 'Very light-bodied',
    # 'None')
    statement += ("'" + info[ 'body_description' ] + "', ") if not null( info[ 'body_description' ] ) else "'None', "
    # acidity TINYINT
    statement += (str( info[ 'acidity' ] ) + ', ') if (not null( info[ 'acidity' ] )) else '0, '
    # acidity_description ENUM('High', 'Medium', 'Low', 'None')
    statement += ("'" + info[ 'acidity_description' ] + "', ") if not null(
        info[ 'acidity_description' ] ) else "'None', "
    # oak TINYINT
    statement += (str( info[ 'oak' ] ) if (not null( info[ 'oak' ] )) else '0') + ')'
    
    return statement


def add_to_grapes_table( wine ):
    """
    :param wine: JSON object representing a wine
    :return: list of MySQL statements to insert grapes into table
    """
    statements = [ ]
    
    if not null( wine[ 'general' ][ 'grape_list' ] ):
        for grape in wine[ 'general' ][ 'grape_list' ]:
            if not null( grape ):
                statement = 'INSERT INTO grapes VALUES ('
                # id INT UNSIGNED NOT NULL
                statement += str( wine[ 'general' ][ 'id' ] ) + ', '
                # grape VARCHAR(28)
                statement += parse_description( grape ) + ")"  # remove apostrophe from grape name
                statements.append( statement )
    
    return statements


def add_to_suggested_food_pairings_table( wine ):
    """
    :param wine: JSON object representing a wine
    :return: list of MySQL statements to insert food matches into table
    """
    statements = [ ]
    
    if not null( wine[ 'traits' ][ 'food_list' ] ):
        for food in wine[ 'traits' ][ 'food_list' ]:
            if not null( food ):
                statement = 'INSERT INTO suggested_food_pairings VALUES ('
                # id INT UNSIGNED NOT NULL
                statement += str( wine[ 'general' ][ 'id' ] ) + ', '
                # food VARCHAR(28)
                statement += "'" + food + "')"
                statements.append( statement )
    
    return statements


def add_to_notes_table( wine ):
    """
    associate wine with just its notes - note categories can be found in the note_categories table
    :param wine: JSON object representing a wine
    :return: list of MySQL statements to insert notes into table
    """
    statements = [ ]
    note_cards = wine[ 'traits' ][ 'notes' ]
    
    if not null( note_cards ):
        for note_card in note_cards:
            # each note card is something like ['vanilla, cinnamon, allspice', 'toasty']
            notes = note_card[ 0 ].split( ',' )
            for note in notes:
                note = parse_description( note.strip() )  # remove all apostrophes from note
                
                statements.append(
                    'INSERT INTO notes VALUES (' + str(
                        wine[ 'general' ][ 'id' ] ) + ", " + note + ")" )
    
    return statements


def populate_tables( wine_db, wine, cursor ):
    # create a cursor to create tables in the wine database passed in
    # cursor = wine_db.cursor( buffered = True )
    
    # create the two with primary keys - also populate these first
    wine_info_statement = add_to_wine_info_table( wine )
    note_categories_statements = add_to_note_categories_table( wine, cursor )
    
    # create tables with only 1 foreign key (id)
    wine_traits_statement = add_to_wine_traits_table( wine )
    grapes_statements = add_to_grapes_table( wine )
    suggested_food_pairings_statements = add_to_suggested_food_pairings_table( wine )
    
    # this table has two foreign keys! (id and note)
    notes_table_statements = add_to_notes_table( wine )
    
    # make sure that we don't already have the wine
    cursor.execute( 'SELECT id FROM wine_info' )
    unprocessed_ids = cursor.fetchall()
    wine_ids = [ idnum[ 0 ] for idnum in unprocessed_ids ]
    
    # if wine isn't already in the db, create the tables
    if wine[ 'general' ][ 'id' ] not in wine_ids:
        # execute the statements to create the tables
        cursor.execute( wine_info_statement )
        wine_db.commit()
        
        if len( note_categories_statements ) > 0:
            for row in note_categories_statements:
                cursor.execute( row )
        
        cursor.execute( wine_traits_statement )
        if len( grapes_statements ) > 0:
            for row in grapes_statements:
                cursor.execute( row )
        
        if len( suggested_food_pairings_statements ) > 0:
            for row in suggested_food_pairings_statements:
                cursor.execute( row )
        
        if len( notes_table_statements ) > 0:
            for row in notes_table_statements:
                cursor.execute( row )
        
        # commit changes to the database - don't forget this step or else you won't save!
        wine_db.commit()
