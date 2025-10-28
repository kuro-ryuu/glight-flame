import random, time, keyboard
import sys
import render
#some basic variables
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
def obstacle_gen(number):
    global score
    # Add new obstacle at (number, -1) if not present
    if [number, -1] not in coords_list:
        coords_list.append([number, -1])
        score += 10

    # Move all obstacles down (y += 1)
    for i, p in enumerate(coords_list):
        coords_list[i][1] = p[1] + 1

    # Remove obstacles that are out of bounds (y >= map_height)
    coords_list[:] = [p for p in coords_list if p[1] < map_height]
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
        time.sleep(0.01)