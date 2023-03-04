"""
one-stop shop to run one command and create/populate both databases
"""
import getopt
import sys

import mysql.connector

from Database.Flavor.make_flavor_tables import make_flavor_tables
from Database.Wine.make_wine_tables import make_wine_tables


def handle_arguments( argv ):
    # initialize default database connection values
    h = 'localhost'
    u = 'root'
    p = ''
    w = 'wine_db'
    f = 'flavor_db'
    
    # handle arguments
    opts, args = getopt.getopt( argv, "h:u:p:w:f:",
                                [ 'host', 'user', 'password', 'wine_database', 'flavor_database' ] )
    for opt, arg in opts:
        if opt in ('-h', '--host'):
            h = arg
        elif opt in ('-u', '--user'):
            u = arg
        elif opt in ('-p', '--password'):
            p = arg
        elif opt in ('-w', '--wine_database'):
            w = arg
        elif opt in ('-f', '--flavor_database'):
            f = arg
    
    return h, u, p, w, f


# instantiate database connection information by reading arguments or using default values
host, user, password, wine_db, flavor_db = handle_arguments( sys.argv[ 1: ] )

# create mysql connection
db = mysql.connector.connect(
    host = host,
    user = user,
    password = password
)

# create cursor to send queries adn obtain results
cursor = db.cursor( buffered = True )

# create databases
cursor.execute( 'CREATE DATABASE ' + wine_db )
cursor.execute( 'CREATE DATABASE ' + flavor_db )

# create/populate tablse
make_wine_tables( [ host, user, password, wine_db ] )
make_flavor_tables( [ host, user, password, flavor_db ] )

print( 'All done :)' )
