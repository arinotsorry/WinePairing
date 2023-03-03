"""
This only works for the wines.json file, not for general json-to-db conversion purposes

Author: Ari Wisenburn
"""
import getopt
import json
import sys
import time

import mysql.connector

from Database.Wine.create_tables import create_tables
from Database.Wine.populate_tables import populate_tables

"""
Temporary utility functions:
- Drop all tables: drop table wine_info, note_categories, wine_traits, grapes, suggested_food_pairings, notes;
"""

"""
Read from JSON file
"""


# Read in wine JSON information and convert it to a usable JSON
def read_wine_json():
    """
    Reads the scraped wine information stored in the json file and converts it to a usable JSON object we can use later
    :return: a list of all the wines, each as a JSON object
    """
    path = 'wines.json'
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


def main( argv ):
    """
    :param argv: -h host -u user -p password -d database, all optional
    :return: nothing, created and populated tables in your MySQL server
    """
    # initialize default database connection values
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'wine_db'
    
    # handle arguments
    opts, args = getopt.getopt( argv, "h:u:p:d:", [ 'host', 'user', 'password', 'database' ] )
    for opt, arg in opts:
        if opt in ('-h', '--host'):
            host = arg
        elif opt in ('-u', '--user'):
            user = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-d', '--database'):
            database = arg
    
    # create mysql connector
    wine_db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    
    # drop all tables
    cursor = wine_db.cursor( buffered = True )
    cursor.execute( 'drop table wine_info, note_categories, wine_traits, grapes, suggested_food_pairings, notes' )
    
    # read wines from json
    wines = read_wine_json()
    
    # create tables
    create_tables( wine_db )
    
    # populate tables with wine info
    for wine in wines:
        populate_tables( wine_db, wine )
        time.sleep( 0.5 )  # this is stupid if it works


main( sys.argv )
