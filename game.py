import connect_to_db
import random
import time
import keyboard
db_connection = connect_to_db().connect()
def map_choosing(): 
    pass
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
    last_command_time = 0
    command_interval = 0.5  # seconds
    playerpos=0
    while (True): #TODO change condition later
        now = time.time()
        if now - last_command_time > command_interval:
            #GAME LOGIC HERE
            obstacle_gen(random.randint(3,7))
            disaster_gen(delay,magnitude)
            last_command_time = now

        #KEYBOARD HANDING
        if keyboard.is_pressed('a'): playerpos-=1
        if keyboard.is_pressed('d'): playerpos+=1
        
        #if score... stop game #TODO
        time.sleep(0.01)