"""
This only works for the wines.json file, not for general json-to-db conversion purposes

Author: Ari Wisenburn
"""

import json
import mysql.connector


def find_max_value_of_everything_clunky( wines ):
    values = [ 0 ] * 22
    for wine in wines:
        # id
        if not (wine[ 'general' ][ 'id' ] == None or wine[ 'general' ][ 'id' ] == 'None') and wine[ 'general' ][
            'id' ] > values[ 0 ]:
            values[ 0 ] = wine[ 'general' ][ 'id' ]
        # id_without_vintage
        if not (wine[ 'general' ][ 'id_without_vintage' ] == None or wine[ 'general' ][
            'id_without_vintage' ] == 'None') and wine[ 'general' ][ 'id_without_vintage' ] > values[
            1 ]:
            values[ 1 ] = wine[ 'general' ][ 'id_without_vintage' ]
        # wine
        if not (wine[ 'general' ][ 'wine' ] == None or wine[ 'general' ][ 'wine' ] == 'None') and len(
                wine[ 'general' ][ 'wine' ] ) > values[ 2 ]:
            values[ 2 ] = len( wine[ 'general' ][ 'wine' ] )
        # winery
        if not (wine[ 'general' ][ 'winery' ] == None or wine[ 'general' ][ 'winery' ] == 'None') and len(
                wine[ 'general' ][ 'winery' ] ) > values[ 3 ]:
            values[ 3 ] = len( wine[ 'general' ][ 'winery' ] )
        # wine_description
        if not (wine[ 'general' ][ 'wine_description' ] == None or wine[ 'general' ][
            'wine_description' ] == 'None') and len( wine[ 'general' ][ 'wine_description' ] ) > values[
            4 ]:
            values[ 4 ] = len( wine[ 'general' ][ 'wine_description' ] )
        # grape_list
        if not (wine[ 'general' ][ 'grape_list' ] == None or wine[ 'general' ][ 'grape_list' ] == 'None') and len(
                wine[ 'general' ][ 'grape_list' ] ) > values[ 5 ]:
            values[ 5 ] = len( wine[ 'general' ][ 'grape_list' ] )
        # region
        if not (wine[ 'general' ][ 'region' ] == None or wine[ 'general' ][ 'region' ] == 'None') and len(
                wine[ 'general' ][ 'region' ] ) > values[ 6 ]:
            values[ 6 ] = len( wine[ 'general' ][ 'region' ] )
        # country
        if not (wine[ 'general' ][ 'country' ] == None or wine[ 'general' ][ 'country' ] == 'None') and len(
                wine[ 'general' ][ 'country' ] ) > values[ 7 ]:
            values[ 7 ] = len( wine[ 'general' ][ 'country' ] )
        # rating
        if not (wine[ 'general' ][ 'rating' ] == None or wine[ 'general' ][ 'rating' ] == 'None') and wine[ 'general' ][
            'rating' ] > values[ 8 ]:
            values[ 8 ] = wine[ 'general' ][ 'rating' ]
        # price
        if not (wine[ 'general' ][ 'price' ] == None or wine[ 'general' ][ 'price' ] == 'None') and wine[ 'general' ][
            'price' ] > values[ 9 ]:
            values[ 9 ] = wine[ 'general' ][ 'price' ]
        # image_link
        if not (wine[ 'general' ][ 'image_link' ] == None or wine[ 'general' ][ 'image_link' ] == 'None') and len(
                wine[ 'general' ][ 'image_link' ] ) > values[ 10 ]:
            values[ 10 ] = len( wine[ 'general' ][ 'image_link' ] )
        
        # food_list
        if not (wine[ 'traits' ][ 'food_list' ] == None or wine[ 'traits' ][ 'food_list' ] == 'None') and len(
                wine[ 'traits' ][ 'food_list' ] ) > values[ 11 ]:
            values[ 11 ] = len( wine[ 'traits' ][ 'food_list' ] )
        # alcohol_content
        if not (wine[ 'traits' ][ 'alcohol_content' ] == None or wine[ 'traits' ][ 'alcohol_content' ] == 'None') and \
                wine[ 'traits' ][ 'alcohol_content' ] > values[ 12 ]:
            values[ 12 ] = wine[ 'traits' ][ 'alcohol_content' ]
        # sweetness
        if not (wine[ 'traits' ][ 'sweetness' ] == None or wine[ 'traits' ][ 'sweetness' ] == 'None') and \
                wine[ 'traits' ][ 'sweetness' ] > values[ 13 ]:
            values[ 13 ] = wine[ 'traits' ][ 'sweetness' ]
        # style_description
        if not (wine[ 'traits' ][ 'style_description' ] == None or wine[ 'traits' ][
            'style_description' ] == 'None') and len( wine[ 'traits' ][ 'style_description' ] ) > values[
            14 ]:
            values[ 14 ] = len( wine[ 'traits' ][ 'style_description' ] )
        # style_blurb
        if not (wine[ 'traits' ][ 'style_description' ] == None or wine[ 'traits' ][
            'style_description' ] == 'None') and len( wine[ 'traits' ][ 'style_description' ] ) > values[
            15 ]:
            values[ 15 ] = len( wine[ 'traits' ][ 'style_description' ] )
        # body
        if not (wine[ 'traits' ][ 'body' ] == None or wine[ 'traits' ][ 'body' ] == 'None') and wine[ 'traits' ][
            'body' ] > values[ 16 ]:
            values[ 16 ] = wine[ 'traits' ][ 'body' ]
        # body_description
        if not (wine[ 'traits' ][ 'body_description' ] == None or wine[ 'traits' ][
            'body_description' ] == 'None') and len(
            wine[ 'traits' ][ 'body_description' ] ) > values[
            17 ]:
            values[ 17 ] = len( wine[ 'traits' ][ 'body_description' ] )
        # acidity
        if not (wine[ 'traits' ][ 'acidity' ] == None or wine[ 'traits' ][ 'acidity' ] == 'None') and wine[ 'traits' ][
            'acidity' ] > values[ 18 ]:
            values[ 18 ] = wine[ 'traits' ][ 'acidity' ]
        # acidity_description
        if not (wine[ 'traits' ][ 'acidity_description' ] == None or wine[ 'traits' ][
            'acidity_description' ] == 'None') and len( wine[ 'traits' ][ 'acidity_description' ] ) > \
                values[ 19 ]:
            values[ 19 ] = len( wine[ 'traits' ][ 'acidity_description' ] )
        # oak
        if not (wine[ 'traits' ][ 'oak' ] == None or wine[ 'traits' ][ 'oak' ] == 'None') and wine[ 'traits' ][
            'oak' ] > \
                values[ 20 ]:
            values[ 20 ] = wine[ 'traits' ][ 'oak' ]
        # notes
        if not (wine[ 'traits' ][ 'notes' ] == None or wine[ 'traits' ][ 'notes' ] == 'None') and len(
                wine[ 'traits' ][ 'notes' ] ) > values[ 21 ]:
            values[ 21 ] = len( wine[ 'traits' ][ 'notes' ] )
    
    print( values )


def read_wine_json():
    path = './wines.json'
    file = open( path, 'r' )
    content = file.read()
    separator = '},\n{'
    
    wines_as_json = [ ]
    
    while separator in content:
        index = content.index( separator )
        
        # the index is where the string starts, but we want to separate at the ',\n' and remove that.
        wines_as_json.append( json.loads( content[ 0: index + 1 ] ) )
        content = content[ index + 3: ]
    
    wines_as_json.append( json.loads( content ) )
    return wines_as_json


# Prints lines to create tables in mysql server - I pasted these lines in the terminal for debugging, until I got it
def create_tables():
    wine_info = 'CREATE TABLE wine_info ('
    wine_info += 'id INT UNSIGNED NOT NULL, '
    wine_info += 'id_without_vintage MEDIUMINT UNSIGNED, '
    wine_info += 'wine VARCHAR(69), '
    wine_info += 'winery VARCHAR(51), '
    
    wine_info += "type ENUM('Red wine', 'White wine', 'Sparkling wine', 'Dessert wine', 'Rosé wine', 'Fortified "
    wine_info += "Wine'), "
    
    wine_info += 'wine_description VARCHAR(1137), '
    wine_info += 'winery_description VARCHAR(3723), '
    wine_info += 'region VARCHAR(43), '
    wine_info += 'country VARCHAR(31), '
    wine_info += 'rating DECIMAL(2, 1), '
    wine_info += 'price DECIMAL(4, 2), '
    wine_info += 'image_link VARCHAR(59), '
    wine_info += 'PRIMARY KEY (id)'
    wine_info += ')'
    
    print( wine_info )
    
    grapes_table = 'CREATE TABLE grapes ('
    grapes_table += 'id INT UNSIGNED NOT NULL, '
    grapes_table += 'grape VARCHAR(28), '
    grapes_table += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    
    print( grapes_table )
    
    wine_traits = 'CREATE TABLE wine_traits ('
    wine_traits += 'id INT UNSIGNED NOT NULL, '
    wine_traits += 'style_description VARCHAR(1490), '
    wine_traits += 'style_blurb VARCHAR(1490), '
    wine_traits += 'alcohol_content DECIMAL(4, 2), '
    wine_traits += 'sweetness TINYINT, '
    wine_traits += 'body TINYINT, '
    wine_traits += "body_description ENUM('Full-bodied', 'Very full-bodied', 'Medium-bodied', 'Light-bodied', " \
                   "'Very light-bodied', 'None'), "
    wine_traits += 'acidity TINYINT, '
    wine_traits += "acidity_description ENUM('High', 'Medium', 'Low', 'None'), "
    wine_traits += 'oak TINYINT, '
    wine_traits += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    
    print( wine_traits )
    
    suggested_foods = 'CREATE TABLE suggested_foods ('
    suggested_foods += 'id INT UNSIGNED NOT NULL, '
    suggested_foods += 'food VARCHAR(28), '
    suggested_foods += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    
    print( suggested_foods )
    
    notes = 'CREATE TABLE notes ( '
    notes += 'id INT UNSIGNED NOT NULL, '
    notes += 'note VARCHAR(23), '  # TODO: change after comma-separation
    notes += 'category VARCHAR(11), '
    notes += 'line TINYINT UNSIGNED, '
    notes += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    
    print( notes )


"""
+-------------------+
| Tables_in_wine_db |
+-------------------+
| grapes            |
| notes             |
| suggested_foods   |
| wine_info         |
| wine_traits       |
+-------------------+
"""


def null( value ):
    if value is None or value == '0' or value == 0 or value == '':
        return True
    return False


def generate_value_statement( dictionary, value ):
    return ("'" + str( dictionary[ value ] ) + "'") if (not null( dictionary[ value ] )) else 'NULL'


def parse_description( text ):
    # remove all breaks for human readability - they're always next to '\r's anyway, so we're preserving the newline
    while '<br>' in text:
        index = text.index( '<br>' )
        new_text = text[ 0:index ] + text[ index + 4: ]
        text = new_text
    
    # remove all backslashes
    while '\\' in text:
        index = text.index( '\\' )
        new_text = text[ 0:index ]
        if text[ index + 1 ] == 'n' or text[ index + 1 ] == 'r':
            new_text += '\r\n'  # maybe change later depending on OS and how it prints - carriage return vs new line
        else:
            new_text += ' '
        new_text += text[ index + 2: ]
        text = new_text
    print( "Formatted:\n", text )
    return text


def add_to_general_table( wine ):
    info = wine[ 'general' ]
    statement = 'INSERT INTO TABLE wine_info VALUES ('
    # id INT UNSIGNED NOT NULL - we're not using generate_value_statement() here bc it can't be null
    statement += str( info[ 'id' ] ) + ', '
    # id_without_vintage MEDIUMINT UNSIGNED - no quotes around it, since it's an int
    statement += (str( info[ 'id_without_vintage' ] ) if (not null( info[ 'id_without_vintage' ] )) else 'NULL') + ', '
    # wine VARCHAR(69)
    statement += generate_value_statement( info, 'wine' ) + ', '
    # winery VARCHAR(51)
    statement += generate_value_statement( info, 'winery' ) + ', '
    # type ENUM('Red wine', 'White wine', 'Sparkling wine', 'Dessert wine', 'Rosé wine', 'Fortified Wine')
    statement += "'" + info[ 'type' ] + "', "  # never null
    # wine_description VARCHAR(1137)
    statement += parse_description( generate_value_statement( info, 'wine_description' ) ) + ', '
    # winery_description VARCHAR(3723)
    statement += parse_description( generate_value_statement( info, 'winery_description' ) ) + ', '
    # region VARCHAR(43)
    statement += generate_value_statement( info, 'region' ) + ', '
    # country VARCHAR(31)
    statement += generate_value_statement( info, 'country' ) + ', '
    # rating DECIMAL(2, 1) - decimals cannot be null
    statement += (str( info[ 'rating' ] ) + ', ') if (not null( info[ 'rating' ] )) else '0, '
    # price DECIMAL(4, 2)
    statement += (str( info[ 'price' ] ) + ', ') if (not null( info[ 'price' ] )) else '0, '
    # image_link VARCHAR(59)
    statement += generate_value_statement( info, 'image_link' ) + ')'
    print( "Statement:\n", statement )


def add_to_grapes_table( wine ):
    for grape in wine[ ]
    # id INT UNSIGNED NOT NULL
    # grape VARCHAR(28)
    pass


def add_to_traits_table():
    # id INT UNSIGNED NOT NULL, style_description VARCHAR(1490), style_blurb VARCHAR(1490), alcohol_content DECIMAL(
    # 4, 2), sweetness TINYINT, body TINYINT, body_description ENUM('Full-bodied', 'Very full-bodied',
    # 'Medium-bodied', 'Light-bodied', 'Very light-bodied', 'None'), acidity TINYINT, acidity_description ENUM(
    # 'High', 'Medium', 'Low', 'None'), oak TINYINT
    pass


def main():
    # create mysql connector
    wine_db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'wine_db'
    )
    
    # create cursor, to interact/send commands to wine db
    cursor = wine_db.cursor( buffered = True )
    
    wines = read_wine_json()
    print( wines[ 0 ] )
    for wine in wines:
        add_to_general_table( wine )


main()

# num of wines: 9238
# Max value/length for:
# id: 172831218
# id_without_vintage: 11062103
# wine: 69
# winery: 51
# wine_description: 1137
# winery_description: 3723
# grape_list: 9 (individual len max:
# region: 43
# country: 31
# rating: 4.6
# price: 54.99
# image_link: 59

# food_list: 11
# alcohol_content: 20
# sweetness: 8
# style_description: 1490
# style_blurb: 1490
# body: 5
# body_description: 17
# acidity: 3
# acidity_description: 6
# oak: 120
# notes: 13
