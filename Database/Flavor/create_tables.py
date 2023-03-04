def create_tables( cursor ):
    # create flavors table
    statement = 'CREATE TABLE flavors ('
    statement += 'food VARCHAR(25) NOT NULL, '
    statement += 'category VARCHAR(10), '
    statement += 'cocktail BOOL, savory BOOL, sweet BOOL, '
    statement += 'PRIMARY KEY (food))'
    cursor.execute( statement )
    
    # create cocktail table
    statement = 'CREATE TABLE cocktail ('
    statement += 'food VARCHAR(25) NOT NULL, '
    statement += 'partner VARCHAR(25) NOT NULL, '
    statement += 'FOREIGN KEY (food) REFERENCES flavors(food), '
    statement += 'FOREIGN KEY (partner) REFERENCES flavors(food))'
    cursor.execute( statement )
    
    # create savory table
    statement = 'CREATE TABLE savory ('
    statement += 'food VARCHAR(25) NOT NULL, '
    statement += 'partner VARCHAR(25) NOT NULL, '
    statement += 'FOREIGN KEY (food) REFERENCES flavors(food), '
    statement += 'FOREIGN KEY (partner) REFERENCES flavors(food))'
    cursor.execute( statement )
    
    # create sweet table
    statement = 'CREATE TABLE sweet ('
    statement += 'food VARCHAR(25) NOT NULL, '
    statement += 'partner VARCHAR(25) NOT NULL, '
    statement += 'FOREIGN KEY (food) REFERENCES flavors(food), '
    statement += 'FOREIGN KEY (partner) REFERENCES flavors(food))'
    cursor.execute( statement )
