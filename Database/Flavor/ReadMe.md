## Creating the Flavor Database:

`foods.json` is populated with food information scraped off [flavorfox.app](flavorfox.app).
<br />
`make_flavor_tables.py` is what you run to make the flavor tables. It uses:

- `create_tables.py` to create the flavor tables
- `populate_tables.py` to process the food json data and insert it into the tables
  <br />

`csv_to_json.py` is just me reading from the csv files I created and dumping that info into the `foods.json` file. It
was a one-time use file.

### But first...

Before you begin, you have to
[set up your own MySQL server](https://dev.mysql.com/doc/mysql-getting-started/en/) *__and name it flavor_db if you want
to use my default arguments__*.
<br />
<br />
Save the host/user/password/database name, because `make_flavor_tables.py` takes these as optional arguments (see below)

### run `make_flavor_tables.py <args>`.

This works by

- parsing `foods.json` and storing the information within the program for easy access
- creating tables in a MySQL
  database ([you have to set this up yourself beforehand, sorry :/](https://dev.mysql.com/doc/mysql-getting-started/en/))
- processing the json data so it is formatted correctly for calls to the database
- populating the flavor tables with data

#### Input arguments:

all of these are optional and have default values as listed below:

- -h, --hostname, default 'localhost'
- -u, --user, default 'root'
- -p, --password, default ''
- -d, --database, default 'wine_db'


