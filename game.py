import mysql.connector
import connect_to_db
import random
import time
import tkinter
db_connection = connect_to_db().connect()
def map_gen(map):
    pass
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
    while (True): #TODO change condition later
# Map generation
            rows, cols = 5, 10
    board = [["⬚" for _ in range(cols)] for _ in range(rows)]

    for row in board:
        print(" ".join(row))
        obstacle_gen(random.randint(3,7))
        disaster_gen(delay,magnitude)
        #if score... stop game #TODO
        time.sleep(0.5)