# top fence removed
import random, time, keyboard
import os
# import mysql.connector, connect_to_db #   TODO WHY ERROR????
# db_connection = connect_to_db().connect()
def map_gen():
    # clear console (Windows: cls, others: clear)
    #os.system('cls' if os.name == 'nt' else 'clear')
    #TODO this feels laggy at terminal
    print(f"Remaining fuel: {fuel}")
    for y in range(map_height):
        for x in range(map_width):
            if (x, y) == (playerpos, map_height - 1):
                print(end="A")
            elif coords_list and ((x, y) in coords_set):
                print(end="O")
            else:
                print(end=" ")
        print()
def map_choosing(): 
    pass
def obstacle_gen(number):
    # use module-level containers for obstacles
    global coords_list, coords_set
    # Add new obstacle at (number, -1) if not present
    if (number, -1) not in coords_set:
        coords_list.append([number, -1])
        coords_set.add((number, -1))

    # Move all obstacles down (y += 1)
    for i, p in enumerate(coords_list):
        coords_list[i][1] = p[1] + 1

    # Remove obstacles that are out of bounds (y >= map_height)
    coords_list[:] = [p for p in coords_list if p[1] < map_height]

    # Rebuild the set to reflect current list
    coords_set.clear()
    coords_set.update((p[0], p[1]) for p in coords_list)
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
    #some basic variables
    # obstacles: keep a list for order and a set for fast membership
    coords_list = []  # list of [x, y]
    coords_set = set()  # set of (x, y) tuples for O(1) checks
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
    while (True): #TODO change condition later
        map_gen()
        now = time.time()
        if now - last_command_time > obs_interval:
            #GAME LOGIC HERE
            obstacle_gen(random.randint(0, map_width - 1))
            disaster_gen(delay,magnitude)
            last_command_time = now

        #KEYBOARD HANDING
        if (now - last_command_time > key_delay):
            if keyboard.is_pressed('a'): 
                playerpos-=1
                fuel-=10
                last_key_time = now
            if keyboard.is_pressed('d'): 
                playerpos+=1
                fuel-=10
                last_key_time = now
        
        #if score... stop game #TODO
        time.sleep(0.01)