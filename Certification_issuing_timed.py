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
    #s = input("continue? Y/N")
    #if s != "Y":
    #    return 0
    return dApp.create_certificate(address,vaccine)

def getCertificates(address):

    stats = {'bc':[], 'db':[]}
    #print("Citizen Data.")
    start = time.time()
    select_citizen_query = "SELECT * FROM Citizens WHERE soul_address = '" + address + "'"
    cursor.execute(select_citizen_query)
    citizen = cursor.fetchone()
    stats['db'].append(time.time() - start)

    #print(citizen)
    #print("List of SBT certificates")
    start = time.time()
    vaccines_SBT_id=dApp.get_certificates(address)
    stats['bc'].append(time.time() - start)
    for v in vaccines_SBT_id:

        start = time.time()
        vaccine = dApp.get_titleOf(v)
        stats['bc'].append(time.time() - start)

        start = time.time()
        select_vaccine_query = "SELECT * FROM Vaccines WHERE name = '" + vaccine + "'"
        cursor.execute(select_vaccine_query)
        vaccine_data = cursor.fetchone()
        stats['db'].append(time.time() - start)
        #print(vaccine_data)
    return stats['bc'],stats['db']

def burn(vaccine_id):
    return dApp.burn(vaccine_id)




if __name__ == '__main__':
    #Execution time

    address_to= "0xb58175AFa0f523a1929f6326d412a9DF1672f9B3"


    start = time.time()
    print(record_vaccine(address_to, "Moderna"))
    end = time.time()
    print(end - start)

    start = time.time()
    print(record_vaccine(address_to, "AstraZeneca"))
    end = time.time()
    print(end - start)

# timingBC=[]
# timingDB=[]
# timingTotal=[]
# for i in range(40):
#     print(i, end='\r')
#     start = time.time()
#     tBC,tDB = getCertificates(address_to)
#     timingBC+=tBC
#     timingDB+=tDB
#
#
# import statistics
# print("BC")
# print(len(timingBC))
# print("max;_ ", max(timingBC))
# print("average;_ ", statistics.mean(timingBC))
# print("ST dev: ", statistics.stdev(timingBC))
#
#
# print("DB")
# print(len(timingDB))
# print("max;_ ", max(timingDB))
# print("average;_ ", statistics.mean(timingDB))
# print("ST dev: ", statistics.stdev(timingDB))