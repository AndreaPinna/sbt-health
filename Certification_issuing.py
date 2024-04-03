# Copyright 2024 Andrea Pinna - Università di Cagliari
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import mysql.connector
import dApp
import time


# Health authority DBMS

db_connection = mysql.connector.connect(
    host="sql11.freesqldatabase.com",
    user="",
    password="",
    database=""
)

cursor = db_connection.cursor()

# Certification issuing

def record_vaccine(address, vaccine):
    select_citizen_query = "SELECT * FROM Citizens WHERE soul_address = '"+address+"'"
    cursor.execute(select_citizen_query)
    citizen = cursor.fetchone()
    print(citizen)
    select_vaccine_query = "SELECT * FROM Vaccines WHERE name = '"+vaccine+"'"
    cursor.execute(select_vaccine_query)
    vaccine_data = cursor.fetchone()
    print(vaccine_data)
    return dApp.create_certificate(address,vaccine)

def getCertificates(address):

    #print("Citizen Data.")
    select_citizen_query = "SELECT * FROM Citizens WHERE soul_address = '" + address + "'"
    cursor.execute(select_citizen_query)
    citizen = cursor.fetchone()
    print(citizen)
    #List of SBT certificates
    vaccine_records=[]
    vaccines_SBT_id=dApp.get_certificates(address)
    for v in vaccines_SBT_id:
        vaccine = dApp.get_titleOf(v)
        select_vaccine_query = "SELECT * FROM Vaccines WHERE name = '" + vaccine + "'"
        cursor.execute(select_vaccine_query)
        vaccine_data = cursor.fetchone()
        vaccine_records+=vaccine_data
        print(vaccine_data)
    return vaccine_records

def burn(vaccine_id):
    return dApp.burn(vaccine_id)

