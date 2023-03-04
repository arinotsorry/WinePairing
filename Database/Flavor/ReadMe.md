## Creating the Flavor Database:

`foods.json` is populated with food information scraped off [flavorfox.app](flavorfox.app).
<br />
`make_flavor_tables.py` is what the outer `create_databases.py ` function runs to make the flavor tables. It uses:

- `create_tables.py` to create the flavor tables
- `populate_tables.py` to process the food json data and insert it into the tables
  <br />

`csv_to_json.py` is just me reading from the csv files I created and dumping that info into the `foods.json` file. It
was a one-time use file.

### Schema

![img.png](schema.png)

### run `make_flavor_tables.py <args>`.

This works by

- parsing `foods.json` and storing the information within the program for easy access
- creating tables in a MySQL
  database ([you have to set this up yourself beforehand, sorry :/](https://dev.mysql.com/doc/mysql-getting-started/en/))
- processing the json data so it is formatted correctly for calls to the database
- populating the flavor tables with data
