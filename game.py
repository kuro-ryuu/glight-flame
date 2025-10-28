import connect_to_db
import random
import time
import mysql.connector

db_connection = connect_to_db.connect()
def map_choosing(): 
    pass
def get_airports(conti):
    sql = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
FROM airport
WHERE continent = '{conti}' 
AND type='large_airport'
ORDER by RAND()
LIMIT 30;"""
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
choose_continent = input("Enter your continent (EU or AS): ")
print(get_airports(choose_continent))
def obstacle_gen(number):
    pass
def disaster_gen(delay,magnitude):
    pass
while (True):
    map=input()
    difficulty=0 # TODO smth to read continent data
    if difficulty==1:
        delay=1 #difficulty changes disaster delay...
        magnitude=1
    else: 
        pass #TODO later
    while (True): #TODO change condition later
        obstacle_gen(random.randint(3,7))
        disaster_gen(delay,magnitude)
        #if score... stop game #TODO
        time.sleep(0.5)