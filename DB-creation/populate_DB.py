from faker import Faker
import mysql.connector

db_connection = mysql.connector.connect(
    host="sql11.freesqldatabase.com",
    user="",
    password="",
    database=""
)

cursor = db_connection.cursor()

vaccines_data = [
    ("P", "P Inc.", "123 P St."),
    ("M", "M Inc.", "456 M Ave."),
    ("AZ", "AZ PLC", "789 AstraZeneca Rd."),
    ("JJ", "J&J", "321 J&J Blvd."),
    ("S", "SB Ltd.", "654 S St.")
]



insert_vaccines_query = "INSERT INTO Vaccines (name, pharma_company, sc_address) VALUES (%s, %s, %s)"
cursor.executemany(insert_vaccines_query, vaccines_data)
db_connection.commit()



fake = Faker()
addresses = [
              "0x3c0DfacAF323bd34F1DfAA95f29bF540c5DF1473",
              "0xb58175AFa0f523a1929f6326d412a9DF1672f9B3",
              "0xdBe3E1eBCABeD2de836F9D835897e2Cd90247486",
              "0x9f2C5c26E613d59439Ef21a57bd49D79Ec59EDbf",
              "0x5eF70B827282CD6a523df3e9BDfa9ed0fAe4Cb38"
            ] 

for i in range(5):
    name = fake.first_name()
    surname = fake.last_name()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
    tax_code = fake.random_int(min=100000000, max=999999999)
    soul_address = addresses[i]
    insert_citizen_query = """
    INSERT INTO Citizens (name, surname, birth_date, tax_code, soul_address) 
    VALUES (%s, %s, %s, %s, %s)
    """
    print (name, soul_address)
    cursor.execute(insert_citizen_query, (name, surname, birth_date, tax_code, soul_address))

db_connection.commit()

cursor.close()
db_connection.close()
