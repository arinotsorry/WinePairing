'''
Author: Ari Wisenburn
Date: January 23, 2023
'''

# modification for xlsx files
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment, Font

# stupid long dictionary
import all_flavors

'''
normally, I'd run scraper.py and then stick the results directly in here, but I don't want to scrape the whole website
every time I run/debug this file
'''


def initialize_flavor_ws( flavor_ws ):
    flavor_ws.title = 'Flavors'

    flavor_ws[ 'A1' ] = 'Food'
    b = flavor_ws[ 'A1' ]
    b.font = Font( bold = True )
    
    flavor_ws[ 'B1' ] = 'Cocktail'
    b = flavor_ws[ 'B1' ]
    b.font = Font( bold = True )
    
    flavor_ws[ 'C1' ] = 'Savory'
    c = flavor_ws[ 'C1' ]
    c.font = Font( bold = True )
    
    flavor_ws[ 'D1' ] = 'Sweet'
    d = flavor_ws[ 'D1' ]
    d.font = Font( bold = True )
    
    return flavor_ws


def populate_flavor_ws( flavor_ws, flavors ):
    counter = 2 # when excel indexing starts at 2 lol
    for food in flavors:
        food_flavors = flavors[ food ]  # get all the flavors associated with that specific food
        flavor_ws[ 'A' + str(counter) ] = food  # assign food name to first column
        flavor_ws[ 'A' + str( counter ) ].font = Font( bold = True )  # make font bold for readability
        
        # populates Cocktail, Savory, and Sweet for one food row in flavor worksheet
        for flavor in food_flavors:
            cell = ('B' if flavor == 'cocktail' else 'C' if flavor == 'savory' else 'D') + str(counter)
            flavor_ws[ cell ] = 'No' if food_flavors[ flavor ] is None else 'Yes'
        
        counter += 1


def populate_food_ws( wb, food, food_flavors ):
    """
    wb: workbook
    food: string of food being looked at
    food_flavors: dictionary containing { 'cocktail' : None or list (tuples), 'savory' : None | list, 'sweet' : ... }
    """
    
    # create worksheet for food, where title = food name.
    food_ws = wb.create_sheet( food )
    
    # create Rank column
    food_ws[ 'A1' ] = 'Rank'
    food_ws[ 'A1' ].font = Font( bold=True ) # column title bold for readability
    
    col = 'B'  # subtract 1 from row for iteration number
    for flavor in food_flavors:
        flavor_pair_list = food_flavors[ flavor ]
        if flavor_pair_list is not None:
            # now we know we have a list for this flavor, so we need to create a new column for the list
            # create pair_food column title
            food_ws[ col + '1' ] = chr(ord( flavor[0] ) - 32) + flavor[1:]
            food_ws[ col + '1' ].font = Font( bold=True )  # column title bold for readability
            # create pair_food_category column title
            food_ws[ chr( ord( col ) + 1 ) + '1' ] = 'Category'
            food_ws[ chr( ord( col ) + 1 ) + '1' ].font = Font( bold=True ) # column title bold for readability
    
            row = 2  # subtract 1 from row for iteration number
            for pair_food in flavor_pair_list:
                # Write rank
                food_ws[ 'A' + str( row ) ] = row - 1
                # Write food
                food_ws[ col + str( row ) ] = pair_food[ 0 ]
                # Write food's category
                food_ws[ chr( ord( col ) + 1 ) + str( row ) ] = pair_food[ 1 ]
                # increment row
                row += 1
            
            # increment column by 2 for food category
            col = chr( ord( col ) + 2 )  # TODO: do I really need to do all this casting?
        
    wb.save( './TableCreation/ExcelFiles/Flavors.xlsx' )
        

def main():
    # Get all the flavors
    flavors = all_flavors.get_flavor_dictionary()

    # initialize flavors workbook
    flavors_wb = Workbook()
    
    # initialize and populate worksheet for foods and which flavors they have, then save
    flavors_ws = flavors_wb.active
    initialize_flavor_ws( flavors_ws )
    populate_flavor_ws( flavors_ws, flavors )
    flavors_wb.save( './TableCreation/ExcelFiles/Flavors.xlsx' )
    
    # populate worksheet for each food
    count = 1
    for food in flavors:
        populate_food_ws( flavors_wb, food, flavors[ food ] )
        # print percentage, poor (or impatient) man's loading bar
        print("{:.2f}".format( 100 * count / len( flavors )) + ' %')
        count += 1


main()
