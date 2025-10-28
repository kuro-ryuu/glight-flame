import connect_to_db
import random
import time
import mysql.connector

db_connection = connect_to_db.connect()
def map_choosing(): 
    pass
def get_airports(conti):
    sql = f"""SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
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
airports_in_continent = get_airports(choose_continent)
final_result = [list(i) for i in airports_in_continent]
airport_list = final_result[2]

for airport in airports_in_continent:
    print(airport["name"])

airport_pick = ""
for i in range(len(airports_in_continent)):
    airports_in_continent[i] = airports_in_continent[i]['name'].lower()
while airport_pick not in airports_in_continent:
    airport_pick = input("Select your airport: ").lower()
    if airport_pick in airports_in_continent:
        print("Airports selected")
    else:
        print("Airports not selected, please try again")
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