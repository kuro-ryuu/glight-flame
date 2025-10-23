import random, time, keyboard
import sys
import render
#some basic variables
coords_list = []  # list of [x, y]
map_height=20
map_width=10

fuel=1000
delay=0
magnitude=0

last_command_time = 0
obs_interval = 1
last_key_time=0  # seconds
key_delay=0.2
playerpos=0
# import mysql.connector, connect_to_db #   TODO WHY ERROR????
# db_connection = connect_to_db().connect()
# rendering moved to render.py
def map_choosing(): 
    pass
def obstacle_gen(number):
    # Add new obstacle at (number, -1) if not present
    if [number, -1] not in coords_list:
        coords_list.append([number, -1])

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
        header = f"Remaining fuel: {fuel}"
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
            if moved:
                # clamp to map bounds
                if playerpos < 0:
                    playerpos = 0
                if playerpos > map_width - 1:
                    playerpos = map_width - 1
                fuel -= 10
                last_key_time = now
                # immediate redraw so movement appears instantly
                render.set_state(coords_list, map_width, map_height, playerpos)
                render.render_and_draw(header)

        #if score... stop game #TODO
        time.sleep(0.01)