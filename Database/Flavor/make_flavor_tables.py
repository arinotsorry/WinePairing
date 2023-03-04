import json

import mysql.connector

from Database.Flavor.create_tables import create_tables
from Database.Flavor.populate_tables import populate_tables


def drop_tables( cursor ):
    cursor.execute( 'SHOW TABLES' )
    tables = cursor.fetchall()  # unprocessed SQL output
    tables = [ table[ 0 ] for table in tables ]
    
    # we have to delete the FK tables first
    if 'cocktail' in tables:
        cursor.execute( 'DROP TABLE cocktail' )
    if 'savory' in tables:
        cursor.execute( 'DROP TABLE savory' )
    if 'sweet' in tables:
        cursor.execute( 'DROP TABLE sweet' )
    
    # next drop PK table
    if 'flavors' in tables:
        cursor.execute( 'DROP TABLE flavors' )


# Read in wine JSON information and convert it to a usable JSON
def read_json():
    """
    Reads the scraped wine information stored in the json file and converts it to a usable JSON object we can use later
    :return: a list of all the wines, each as a JSON object
    """
    path = 'Flavor/foods.json'
    file = open( path, 'r' )
    content = file.read()
    
    return json.loads( content )


def make_flavor_tables( db_info ):
    # assign arguments to database information
    host, user, password, database = db_info
    
    # create mysql connector
    flavor_db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    
    # create mysql cursor
    flavor_db.start_transaction( isolation_level = 'READ COMMITTED' )
    cursor = flavor_db.cursor( buffered = True )
    
    # drop necessary tables (if there are any)
    drop_tables( cursor )
    
    # create tables
    print( 'Creating flavor tables...' )
    create_tables( cursor )
    
    # read in json with food and flavor data
    foods_json = read_json()
    
    # populate the tables with that data
    populate_tables( foods_json, cursor )
    
    flavor_db.commit()
