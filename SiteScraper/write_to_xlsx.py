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
    # flavor_ws.sheet_properties.tabColor = '4C00C5' mmm we don't need fun colors rn
    
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


def main():
    # Get all the flavors
    flavors = all_flavors.get_flavor_dictionary()
    
    # initialize flavors workbook
    flavors_wb = Workbook()
    
    # initialize and populate worksheet for foods and which flavors they have, then save
    flavors_ws = flavors_wb.active
    initialize_flavor_ws( flavors_ws )
    populate_flavor_ws( flavors_ws, flavors )
    flavors_wb.save( 'ExcelFiles/flavors.xlsx' )


main()
