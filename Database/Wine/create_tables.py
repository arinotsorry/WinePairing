"""
Create wine_db tables from json
"""

"""
Generate the MySQL statements to create the wine tables
"""


# this one has to come first because it has a primary key
def create_wine_info_table():
    wine_info = 'CREATE TABLE wine_info ('
    wine_info += 'id INT UNSIGNED NOT NULL, '
    wine_info += 'id_without_vintage MEDIUMINT UNSIGNED, '
    wine_info += 'wine VARCHAR(69), '
    wine_info += 'winery VARCHAR(51), '
    
    wine_info += "type ENUM('Red wine', 'White wine', 'Sparkling wine', 'Dessert wine', 'Rosé wine', 'Fortified "
    wine_info += "Wine'), "
    
    wine_info += 'wine_description VARCHAR(1137), '
    wine_info += 'winery_description VARCHAR(3723), '
    wine_info += 'region VARCHAR(43), '
    wine_info += 'country VARCHAR(31), '
    wine_info += 'rating DECIMAL(2, 1), '
    wine_info += 'price DECIMAL(4, 2), '
    wine_info += 'image_link VARCHAR(59), '
    wine_info += 'PRIMARY KEY (id)'
    wine_info += ')'
    return wine_info


# the note_categories table also has a primary key, so we create it here, but we create the notes table last
def create_note_categories_table():
    note_categories = 'CREATE TABLE note_categories ('
    note_categories += 'note VARCHAR(28) NOT NULL, '
    note_categories += 'category VARCHAR(28), '
    note_categories += 'PRIMARY KEY (note))'
    return note_categories


def create_wine_traits_table():
    wine_traits = 'CREATE TABLE wine_traits ('
    wine_traits += 'id INT UNSIGNED NOT NULL, '
    wine_traits += 'style_description VARCHAR(1490), '
    wine_traits += 'style_blurb VARCHAR(1490), '
    wine_traits += 'alcohol_content DECIMAL(4, 2), '
    wine_traits += 'sweetness TINYINT, '
    wine_traits += 'body TINYINT, '
    wine_traits += "body_description ENUM('Full-bodied', 'Very full-bodied', 'Medium-bodied', 'Light-bodied', " \
                   "'Very light-bodied', 'None'), "
    wine_traits += 'acidity TINYINT, '
    wine_traits += "acidity_description ENUM('High', 'Medium', 'Low', 'None'), "
    wine_traits += 'oak TINYINT, '
    wine_traits += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    return wine_traits


def create_grapes_table():
    grapes_table = 'CREATE TABLE grapes ('
    grapes_table += 'id INT UNSIGNED NOT NULL, '
    grapes_table += 'grape VARCHAR(28), '
    grapes_table += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    return grapes_table


# this should preserve the order we put it into the table, but it doesn't reeeaaaally matter
def create_suggested_food_pairings_table():
    suggested_foods = 'CREATE TABLE suggested_food_pairings ('
    suggested_foods += 'id INT UNSIGNED NOT NULL, '
    suggested_foods += 'food VARCHAR(28), '
    suggested_foods += 'FOREIGN KEY (id) REFERENCES wine_info(id))'
    return suggested_foods


def create_notes_table():
    notes = 'CREATE TABLE notes ('
    notes += 'id INT UNSIGNED NOT NULL, '
    notes += 'note VARCHAR(28), '
    notes += 'FOREIGN KEY (id) REFERENCES wine_info(id), '
    notes += 'FOREIGN KEY (note) REFERENCES note_categories(note))'
    return notes


def create_tables( wine_db ):
    # create the two with primary keys - also populate these first
    wine_info = create_wine_info_table()
    note_categories = create_note_categories_table()
    
    # create tables with only 1 foreign key (id)
    wine_traits = create_wine_traits_table()
    grapes = create_grapes_table()
    suggested_food_pairings = create_suggested_food_pairings_table()
    
    # this table has two foreign keys! (id and note)
    notes_table = create_notes_table()
    
    # create a cursor to create tables in the wine database passed in
    cursor = wine_db.cursor( buffered = True )
    
    # execute the statements to create the tables
    cursor.execute( wine_info )
    cursor.execute( note_categories )
    cursor.execute( wine_traits )
    cursor.execute( grapes )
    cursor.execute( suggested_food_pairings )
    cursor.execute( notes_table )
    
    # commit changes to the database - don't forget this step or else you won't save!
    wine_db.commit()
