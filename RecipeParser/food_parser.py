"""
scan the words in the recipe to find foods that are in the food database, and gather their flavors
"""

import re

import mysql.connector


def preliminary_food_sweep( lines, cursor ):
    """
    Get all the sentences with flavor information from the file. Return a list with sentence information and the
    foods that were found.
    :param lines: a list of sentences that make up the file contents
    :param cursor: cursor to connect to the flavor_db
    :return: a list of (food, sentence) tuples with sentences that contain foods
    """
    # get list of foods - it's faster to search the recipe for foods we have info for than querying the db for every
    # word in the recipe - less buggy/more consistent too
    cursor.execute( "SELECT food FROM flavors WHERE food LIKE '% %'" )
    two_word_foods = [ food[ 0 ] for food in cursor.fetchall() ]
    cursor.execute( "SELECT food FROM flavors WHERE food NOT LIKE '% %'" )
    one_word_foods = [ food[ 0 ] for food in cursor.fetchall() ]
    
    relevant_lines = [ ]
    for line in lines:
        found = False
        for food in two_word_foods:
            # look through all the two word foods first, so in a recipe, for example, we find 'smoked salmon' before
            # we find 'salmon'
            food_str = "[ -\'\"]" + food + "[\ns ,:;)\'\"\.?!-]"
            result = re.search( r"" + food_str, line )  # returns None if there are no matches
            if result:
                # check if there are two-word foods that match the
                relevant_lines.append( (food, line) )
                found = True
                break
        if not found:
            for food in one_word_foods:
                # we have to define a separate string to look for so that we don't look for foods that happen to be
                # nested in other words, like 'date' in 'updated'
                # sometimes food has
                food_str = "[ -\'\"]" + food + "[\ns ,:;)\'\"\.?!-]"
                result = re.search( r"" + food_str, line )  # returns None if there are no matches
                if result:
                    # check if there are two-word foods that match the
                    relevant_lines.append( (food, line) )
                    break
    
    print( relevant_lines )
    return relevant_lines


def get_recipe_lines():
    """
    
    :return: tokens, a list of lower case tokens parsed from the recipe, with stopwords removed
    """
    file = open( '../Recipes/Grilled Salmon.txt', 'r' )
    content = file.readlines()
    stripped_lines = [ ]
    
    for line in content:
        stripped_lines += line.strip().split( '. ' )  # separate all the sentences in a file
    
    return stripped_lines


def process_ingredients( food_lines, cursor ):
    pass


def main():
    # get the tokens from the recipe
    lines = get_recipe_lines()
    
    # create the mysql connector
    # TODO: make these the default values to args we can pass in, like in the Database directory
    flavor_db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'flavor_db'
    )
    flavor_cursor = flavor_db.cursor( buffered = True )
    
    # compare words in recipe with words in flavor table
    # get a list of (food, sentence) pairs
    food_lines = preliminary_food_sweep( lines, flavor_cursor )
    
    # get a list of ingredients along with category
    ingredients = process_ingredients( food_lines, flavor_cursor )


main()
