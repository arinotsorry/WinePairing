"""
insert json information into MySQL tables
"""


# modify the food name so it's safe to pass in
def make_safe( food ):
    # remove apostrophes and periods
    if '\'' in food or '.' in food:
        words = food.split( '\'' )
        food = ''
        for word in words:
            notdot_words = word.split( '.' )
            for notdot_word in notdot_words:
                food += notdot_word
    
    return food.lower()


def populate_flavor_table( foods_json, cursor ):
    # loop through every food we have info on in the dictionary
    statements = [ ]
    for food_name in foods_json:
        # flavor table columns are
        # food, category, cocktail, savory, sweet
        food = foods_json[ food_name ]
        statement = 'INSERT INTO flavors VALUES ('
        # food
        statement += "'" + make_safe( food_name ) + "', "
        # category
        statement += "'" + make_safe( food[ 'category' ] ) + "', "
        # cocktail
        statement += str( food[ 'bools' ][ 0 ] ) + ', '
        # savory
        statement += str( food[ 'bools' ][ 1 ] ) + ', '
        # sweet
        statement += str( food[ 'bools' ][ 2 ] ) + ')'
        
        cursor.execute( statement )


def populate_pairing_table( table, food, list_of_pairs, cursor ):
    for pair in list_of_pairs:
        # check if the pair already exists, because pairs are undirected and work both ways, reduce redundancy
        cursor.execute(
            'SELECT COUNT(*) FROM ' + table + " WHERE partner = '" + make_safe( food ) + "' and food = '" + make_safe(
                pair ) + "'" )
        already_there = cursor.fetchone()
        already_there = already_there[ 0 ]  # if the pair is already uploaded, it'll return 1, else 0
        
        if not already_there:
            # insert into the table
            statement = 'INSERT INTO ' + table + ' VALUES ('
            statement += "'" + make_safe( food ) + "', "
            statement += "'" + make_safe( pair ) + "')"
            cursor.execute( statement )


def populate_pairing_tables( foods_json, cursor ):
    for food_name in foods_json:
        food = foods_json[ food_name ]
        
        # populate cocktail
        if food[ 'bools' ][ 0 ] == 1:
            populate_pairing_table( 'cocktail', food_name, food[ 'cocktail' ], cursor )
        
        # populate savory
        if food[ 'bools' ][ 1 ] == 1:
            populate_pairing_table( 'savory', food_name, food[ 'savory' ], cursor )
        
        # populate sweet table
        if food[ 'bools' ][ 2 ] == 1:
            populate_pairing_table( 'sweet', food_name, food[ 'sweet' ], cursor )


def populate_tables( foods_json, cursor ):
    # populate flavor table
    populate_flavor_table( foods_json, cursor )
    
    # populate pairing tables
    populate_pairing_tables( foods_json, cursor )
