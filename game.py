import random, time, keyboard
import sys
import render
#some basic variables
def var_setup():
    global coords_list, map_height, map_width, fuel, delay, magnitude
    global last_command_time, obs_interval, last_key_time, paused, key_delay
    global playerpos, score
    coords_list = []  # list of [x, y]
    map_height=10
    map_width=10
    score=0

    fuel=1000
    delay=0
    magnitude=0

    last_command_time = 0
    obs_interval = 0.6
    last_key_time=0  # seconds
    paused = 0
    key_delay=0.2
    playerpos=0
# import mysql.connector, connect_to_db #   TODO WHY ERROR????
# db_connection = connect_to_db().connect()
# rendering moved to render.py
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
    # #map picking
    # map=input()
    # difficulty=0 # TODO smth to read continent data
    # if difficulty==1:
    #     delay=1 #difficulty changes disaster delay...
    #     magnitude=1
    # else: 
    #     pass #TODO later
    var_setup()
    while (True): #TODO change condition later
        # render and draw (simple full redraw)
        #header = f"{coords_list} Fuel: {fuel} PlayerPos: {playerpos},{map_height - 1}"
        header = f"Score: {score}\nFuel: {fuel}\nPlayerPos: {playerpos},{map_height - 1}"
        render.set_state(coords_list, map_width, map_height, playerpos)
        render.render_and_draw(header)
        now = time.time()
        if now - last_command_time > obs_interval:
            #GAME LOGIC HERE
            obstacle_gen(random.randint(0, map_width - 1))
            disaster_gen(delay,magnitude)
            last_command_time = now
            
        #KEYBOARD HANDING (throttle by last_key_time)
        if (now - last_key_time > key_delay):
            moved = False
            if keyboard.is_pressed('a'):
                playerpos -= 1
                moved = True
            if keyboard.is_pressed('d'):
                playerpos += 1
                moved = True
            while True:
                # toggle pause
                if keyboard.is_pressed('space'):
                    paused = 1
                    print("Game paused. Press space to resume.")
                    time.sleep(0.3)
                    while True:
                        if keyboard.is_pressed('space'):
                            print("Game resuming in:")
                            for i in range(3, 0, -1):
                                print(i)
                                time.sleep(1)
                            print("Go!")
                            time.sleep(0.5)
                            paused = 0
                            time.sleep(0.3)
                            break
                        time.sleep(0.1)
                break                
            if keyboard.is_pressed('q'):
                exit("Game quit. Thank you for playing!")
            if moved:
                # clamp to map bounds
                if playerpos < 0:
                    playerpos = 0
                    moved = False
                if playerpos > map_width - 1:
                    playerpos = map_width -1
                    moved = False
                if moved:
                    fuel -= 10
                last_key_time = now
                render.set_state(coords_list, map_width, map_height, playerpos)
                render.render_and_draw(header)
        if fuel == 0:
            exit("Game Over! You ran out of fuel.")

        #if score... stop game #TODO
        time.sleep(0.5)