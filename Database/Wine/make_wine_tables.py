"""
This only works for the wines.json file, not for general json-to-db conversion purposes

Author: Ari Wisenburn
"""
import json

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
    path = 'Wine/wines.json'
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


# drop already-instantiated tables if you're retrying to create/populate tables in one shot
def drop_tables( cursor ):
    cursor.execute( 'SHOW TABLES' )
    tables = cursor.fetchall()  # unprocessed SQL output
    tables = [ table[ 0 ] for table in tables ]
    
    # we have to delete the FK tables first
    for table in tables:
        if table != 'wine_info' and table != 'note_categories':
            cursor.execute( 'DROP TABLE ' + table )
            tables.remove( table )
    
    # now we can delete the PK tables - loop has max 2 elements, so it's technically inefficient but whatever
    for table in tables:
        cursor.execute( 'DROP TABLE ' + table )


def make_wine_tables( db_info ):
    """
    :param db_info: -h host -u user -p password -w wine_database name, all optional
    :return: nothing, created and populated tables in your MySQL server
    """
    
    # initialize default database connection values
    host, user, password, database = db_info
    
    # create mysql connector
    wine_db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    
    # create mysql cursor
    wine_db.start_transaction( isolation_level = 'READ COMMITTED' )
    cursor = wine_db.cursor( buffered = True )
    
    # drop necessary tables (if there are any)
    drop_tables( cursor )
    # cursor.execute( 'drop table wine_info, note_categories, wine_traits, grapes, suggested_food_pairings, notes' )
    
    # read wines from json
    wines = read_wine_json()
    
    # create tables
    print( 'Creating wine tables...' )
    create_tables( wine_db )
    
    # populate tables with wine info
    count = 1
    for wine in wines:
        if count % 20 == 0 or count == 1 or count == len( wines ):
            print( 'Now processing wine ' + str( count ) + ' / ' + str( len( wines ) ) )
        populate_tables( wine_db, wine, cursor )
        count += 1
