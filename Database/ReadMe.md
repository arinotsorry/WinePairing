## Creating the databases:

You first need to set up the MySQL CLI on your machine.

After that, you should be able to just run `create_databases.py`, which will create the wine and flavor databases.

### Input arguments:

all of these are optional and have default values as listed below:

- -h, --hostname, default 'localhost'
- -u, --user, default 'root'
- -p, --password, default ''
- -w, --wine_database, default 'wine_db'
- -f, --flavor_database, default 'flavor_db'