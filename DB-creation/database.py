import mysql.connector

# DB connection
db_connection = mysql.connector.connect(
    host="sql11.freesqldatabase.com",
    user="",
    password="",
    database=""
)

cursor = db_connection.cursor()

cursor.execute(' CREATE DATABASE IF NOT EXISTS healthAuthority')
cursor.execute(" use healthAuthority")


create_vaccines_table_query = """
CREATE TABLE Vaccines (
    id_vaccine INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    pharma_company VARCHAR(255),
    sc_address VARCHAR(255) DEFAULT "0x544662DEC37dD3dd855D4ef0E1A4919aCb404227"
)
"""
cursor.execute(create_vaccines_table_query)


create_citizens_table_query = """
CREATE TABLE Citizens (
    id_citizen INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    birth_date DATE,
    tax_code VARCHAR(16) UNIQUE,
    soul_address VARCHAR(255) UNIQUE
)
"""
cursor.execute(create_citizens_table_query)

cursor.close()
db_connection.close()