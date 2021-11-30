# Libraries
import mysql.connector as mariadb
import json

# Config JSON
with open('config.json', 'r') as file:
    config = json.load(file)

# DataBase connection config
mariadb = mariadb.connect(host=config['DB2']['DB_HOST'],
                          port=config['DB2']['DB_PORT'],
                          user=config['DB2']['DB_USER'],
                          password=config['DB2']['DB_PASS'])

# Work cursor
cursor = mariadb.cursor(buffered=True)

# DataBase creation
db_verification = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'dictionary'"
db_create = "CREATE DATABASE dictionary"
db_drop = "DROP DATABASE dictionary"

# Execute query
cursor.execute(db_verification)
resp = cursor.fetchone()

if resp is None:
    cursor.execute(db_create)
    cursor.execute(db_verification)
    resp = cursor.fetchone()
    print("THE DATABASE {} WAS CREATED SUCCESSFULLY".format(resp[0]))
else:
    print("THE DATABASE {} EXISTS".format(resp[0]))
    cursor.execute(db_drop)
    cursor.execute(db_create)

# Creation of tables for the inventory DataBase
db_select = "USE dictionary"

# Table words
db_words_exists = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'dictionary' AND table_name = 'words'"
db_words_drop = "DROP TABLE words"
db_words = '''CREATE TABLE IF NOT EXISTS words 
              (Id_word int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
              word varchar(150) NOT NULL,
              definition varchar(255) NOT NULL)'''

# Execute query
cursor.execute(db_select)
resp = cursor.fetchone()

# Creating tables
if resp is None:
    # Creating table brand
    cursor.execute(db_words_exists)
    resp = cursor.fetchone()
    if resp is not None:
        print("THE brand table ALREADY EXISTS")
        #cursor.execute(db_brand_drop)
        print("RECREATING words TABLE")
        cursor.execute(db_words)
        print("THE TABLE brand WAS CREATED SUCCESSFULLY")
    else:
        cursor.execute(db_words)
        print("THE TABLE words WAS CREATED SUCCESSFULLY")
else:
    print("THE DATABASE NOT EXISTS")