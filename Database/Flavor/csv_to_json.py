"""
one-time use: convert all the CSV files I have to one json file I can upload to the github and repeatedly read from
"""

import json

"""
Reading flavor master csv
"""


def read_flavor_csv():
    """
    Read csv with flavor information
    The first line is 'Food,Cocktail,Savory,Sweet' - column titles
    the rest of the lines are formatted 'Food,bool,bool,bool\n', where bool is whether the food has
    cocktail/savory/sweet pairings
    :return: flavor dictionary, where flavor_dict[food: str] = (cocktail: bool, savory: bool, sweet: bool)
    """
    
    flavor_csv = open( '../../TableCreation/CsvFiles/Flavors.csv', 'r' )
    flavor_dict = { }
    
    # lines: list of string like 'Absinthe,Yes,No,No\n'
    # lines[0]: column titles: food, cocktail, savory, sweet
    lines = flavor_csv.readlines()
    food_table_file_names = [ ]
    
    # good practice I guess
    flavor_csv.close()
    
    # add flavor table's column names to lines list
    rows = [ line.strip().split( ',' ) for line in lines[ 1: ] ]
    
    for row in rows:
        # set booleans
        cocktail = 1 if row[ 1 ] == 'Yes' else 0
        savory = 1 if row[ 2 ] == 'Yes' else 0
        sweet = 1 if row[ 3 ] == 'Yes' else 0
        
        # create dictionary entry for food, where food maps to (cocktail, savory, sweet) tuple
        flavor_dict[ row[ 0 ] ] = { 'bools': (cocktail, savory, sweet) }
    
    return flavor_dict


"""
Reading all the food csv files and adding their info to the dictionary
"""


def try_adding_food_category( flavor_dict, food, category ):
    if food in flavor_dict and 'category' not in list( flavor_dict[ food ].keys() ):
        flavor_dict[ food ][ 'category' ] = category


def read_food_files( flavor_dict ):
    food_file_names = list( flavor_dict.keys() )
    
    for food_file_name in food_file_names:
        # open file in 'read' mode
        food_file = open( '../../TableCreation/CsvFiles/' + food_file_name + '.csv', 'r' )
        food_lines = food_file.readlines()
        
        # create lists for food pairs
        cocktail_pairs, savory_pairs, sweet_pairs = [ ], [ ], [ ]
        
        # cycle through each partner that pairs with the file's namesake food
        # food_lines[0] = 'Rank,Table,Category,Table,Category', with up to 3 tables and categories
        # food_lines[1:] = 'int,food,category,food,category', with up to 3 foods and categories
        for food_line in food_lines[ 1: ]:
            # we don't care about the rank, food_line[0]
            row = food_line.strip().split( ',' )
            
            # get booleans for whether cocktail, savory, and sweet pairings exist with this food
            cocktail, savory, sweet = flavor_dict[ food_file_name ][ 'bools' ]
            
            # insert pair information into the dictionary
            index = 1
            if cocktail:
                if row[ index ]:  # if the file ran out of cocktail pairs to give, row[ index ] = ''
                    # add food to list of cocktail pairs
                    cocktail_pairs.append( (row[ index ]) )
                    # try adding food category to dictionary
                    try_adding_food_category( flavor_dict, row[ index ], row[ index + 1 ] )
                
                index += 2  # increment 2 even if cocktail is blank - this is just a quirk in the file
            
            if savory:
                if row[ index ]:  # if the file ran out of savory pairs to give, row[ index ] = ''
                    # add food to list of savory pairs
                    savory_pairs.append( (row[ index ]) )
                    # try adding food category to dictionary
                    try_adding_food_category( flavor_dict, row[ index ], row[ index + 1 ] )
                
                index += 2  # increment 2 even if cocktail is blank - this is just a quirk in the file
            
            if sweet:
                if row[ index ]:  # if the file ran out of sweet pairs to give, row[ index ] = ''
                    # add food to list of savory pairs
                    sweet_pairs.append( (row[ index ]) )
                    # try adding food category to dictionary
                    try_adding_food_category( flavor_dict, row[ index ], row[ index + 1 ] )
            
            # stick these pair lists in the dictionary
            if cocktail:
                flavor_dict[ food_file_name ][ 'cocktail' ] = cocktail_pairs
            if savory:
                flavor_dict[ food_file_name ][ 'savory' ] = savory_pairs
            if sweet:
                flavor_dict[ food_file_name ][ 'sweet' ] = sweet_pairs


def main():
    # generate initial flavor dictionary
    flavor_dict = read_flavor_csv()
    
    # generate list of files
    read_food_files( flavor_dict )
    
    # flavor_dict now has all information about every food and its pairs
    # write this to a json file
    json_file = open( './foods.json', 'w' )
    json.dump( flavor_dict, json_file, indent = 2 )
    json_file.close()


main()
