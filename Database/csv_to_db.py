import mysql.connector

''' FLAVORS TABLE '''
''' One-Stop Shop to create flavor table '''


def create_flavor_table( flavors_cursor ):
    # get lines to populate table
    lines = interpret_flavors_csv()[ 0 ]
    
    # create table with columns Food, Cocktail, Savory, Sweet - the info stored at lines[ 0 ]
    statement = 'CREATE TABLE flavors (food VARCHAR(25) NOT NULL, cocktail BOOL, savory BOOL,'
    statement += 'sweet BOOL, PRIMARY KEY (food)) '
    
    flavors_cursor.execute( statement )
    
    # populate flavor table with food information
    for line in lines[ 1: ]:
        statement = 'INSERT INTO flavors VALUES (\'' + line[ 0 ] + '\''
        for word in line[ 1: ]:
            statement += ', ' + str( word )
        statement += ')'
        flavors_cursor.execute( statement )


''' Utility functions '''


def interpret_flavors_csv():
    file = open( '../TableCreation/CsvFiles/Flavors.csv', 'r' )
    file_lines = file.readlines()
    file_names = [ ]
    
    # add column names to list
    lines = [ file_lines[ 0 ].strip().split( ',' ) ]
    
    # format food and add to list, one mini-list per food item
    for file_line in file_lines[ 1: ]:
        line = file_line.strip().split( ',' )
        
        # record file name
        file_names.append( line[ 0 ] )
        
        # insert title
        line[ 0 ] = make_safe( line[ 0 ] )
        
        # create booleans from 'Yes' and 'No'
        for index in range( 1, len( line ) ):
            line[ index ] = 1 if line[ index ] == 'Yes' else 0
        
        lines.append( line )
    
    return lines, file_names


def make_safe( title ):
    # substitute underscore for space
    if ' ' in title:
        words = title.split( ' ' )
        title = words[ 0 ]
        for word in words[ 1: ]:
            title += '_' + word
    
    # remove apostrophes
    if '\'' in title or '.' in title:
        words = title.split( '\'' )
        title = ''
        for word in words:
            notdot_words = word.split( '.' )
            for notdot_word in notdot_words:
                title += notdot_word
    
    return title.lower()


''' END FLAVOR TABLE FUNCTIONS'''

''' FOOD TABLES '''
''' One function to create food tables '''


def create_food_tables( flavors_cursor ):
    # get list of food csv file names
    file_names = interpret_flavors_csv()
    file_names = file_names[ len( file_names ) - 1 ]
    
    # get list of food
    statement = 'SELECT * FROM flavors'
    flavors_cursor.execute( statement )
    list_of_data = flavors_cursor
    
    # create table for each food
    # we have to store the queries instead of executing them within the helper functions because new queries would
    # flush whatever's in the buffer - namely, the list of foods
    file_names_index = 0
    queries = [ ]
    for (food, cocktail, savory, sweet) in list_of_data:
        file_name = file_names[ file_names_index ]
        queries.append( create_food_table( flavors_cursor, food, cocktail, savory, sweet ) )
        queries += populate_food_table( flavors_cursor, food, file_name )
        file_names_index += 1
    
    for query in queries:
        print( query )
        flavors_cursor.execute( query )


''' Utility functions '''


def create_food_table( flavors_cursor, title, cocktail, savory, sweet ):
    # CREATE TABLE          Flavors (food VARCHAR(25), cocktail BOOL, savory BOOL, sweet BOOL)
    #                       CREATE TABLE absinthe ( rank INT(48),  cocktail VARCHAR(25), cocktail_category VARCHAR(25) )
    
    statement = 'CREATE TABLE ' + title + ' ('
    appendix = ''
    if cocktail:
        statement += ' cocktail VARCHAR(25), cocktail_category VARCHAR(25)'
        appendix += ' FOREIGN KEY (cocktail) REFERENCES flavors(food)'
        if savory | sweet:
            statement += ','
            appendix += ','
    if savory:
        statement += ' savory VARCHAR(25), savory_category VARCHAR(25)'
        appendix += ' FOREIGN KEY (savory) REFERENCES flavors(food)'
        if sweet:
            statement += ','
            appendix += ','
    if sweet:
        statement += ' sweet VARCHAR(25), sweet_category VARCHAR(25)'
        appendix += ' FOREIGN KEY (sweet) REFERENCES flavors(food)'
    
    statement += ',' + appendix + ' )'
    return statement


def populate_food_table( flavors_cursor, food, file_name ):
    # open csv file
    file = open( r'../TableCreation/CsvFiles/' + file_name + '.csv', 'r' )
    file_text = file.readlines()
    
    # prepare file text
    lines = [
        text.strip().split( ',' ) for text in file_text
    ]
    
    # create list of statements
    statements = []
    for line in lines[ 1: ]:
        # rank, <cocktail>, <cocktail_category>, <savory>, ..., <sweet_category>
        statement = 'INSERT INTO ' + food + ' VALUES ( '
        statement += '\'' + make_safe( line[ 1 ] ) + '\'' if line[ 1 ] != '' else 'NULL'
        
        for value in line[ 2: ]:
            statement += ', ' + ('\'' + make_safe( value ) + '\'' if value != '' else 'NULL')
        statement += ' )'
        
        statements.append(statement)
    
    return statements


''' General functions '''


def get_table_names( flavors_cursor ):
    flavors_cursor.execute( 'SHOW TABLES' )
    return [ table for table in flavors_cursor ]


def drop_table( flavors_cursor, table ):
    flavors_cursor.execute( 'DROP TABLE ' + table )


def drop_all_tables( flavors_cursor ):
    flavors_cursor.execute( 'SHOW TABLES' )
    
    statements = [ ]
    for table in flavors_cursor:
        if table[0] != 'flavors':
            statements.append( 'DROP TABLE ' + str(table[0]) )
    
    for statement in statements:
        print(statement)
        flavors_cursor.execute( statement )


def main():
    # connect to mysql
    flavors_db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'flavors_db'
    )
    
    # create cursor, to interact/send commands to db
    flavors_cursor = flavors_db.cursor( buffered = True )
    
    ''' Flavor Table '''
    # create
    # create_flavor_table( flavors_cursor )
    
    ''' Food Tables '''
    # drop_all_tables( flavors_cursor )
    create_food_tables( flavors_cursor )
    
    flavors_db.commit()


main()
