import getopt
import json
import sys

import mysql.connector

from create_tables import create_tables


def handle_arguments( argv ):
    # initialize default database connection values
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'flavor_db'
    
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
    
    return host, user, password, database


def drop_tables( cursor ):
    cursor.execute( 'SHOW TABLES' )
    tables = cursor.fetchall()  # unprocessed SQL output
    tables = [ table[ 0 ] for table in tables ]
    
    """
    # we have to delete the FK tables first
    for table in tables:
        if table != 'wine_info' and table != 'note_categories':
            cursor.execute( 'DROP TABLE ' + table )
            tables.remove( table )
    """
    
    # now we can delete the PK tables - loop has max 2 elements, so it's technically inefficient but whatever
    for table in tables:
        cursor.execute( 'DROP TABLE ' + table )


# Read in wine JSON information and convert it to a usable JSON
def read_json():
    """
    Reads the scraped wine information stored in the json file and converts it to a usable JSON object we can use later
    :return: a list of all the wines, each as a JSON object
    """
    path = 'foods.json'
    file = open( path, 'r' )
    content = file.read()
    
    return json.loads( content )


def main( argv ):
    # assign arguments to database information
    host, user, password, database = handle_arguments( argv )
    
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
    create_tables( cursor )
    
    # read in json with food and flavor data
    food_json = read_json()


main( sys.argv )
