import sqlite3
import random
import time
import os
import render

# Simple SQLite-backed version of obstacle storage for the game.
# This script runs a short, non-interactive test: it creates a small DB,
# inserts a few obstacles, advances them several ticks, and renders frames.

DB_PATH = os.path.join(os.path.dirname(__file__), 'game_sqlite.db')

def db_connect(path=DB_PATH):
    return sqlite3.connect(path)

def db_init(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS obstacles(x INTEGER, y INTEGER)')
    conn.commit()

def clear_obstacles(conn):
    c = conn.cursor()
    c.execute('DELETE FROM obstacles')
    conn.commit()

def add_obstacle(conn, x, y):
    c = conn.cursor()
    c.execute('INSERT INTO obstacles(x,y) VALUES(?,?)', (x, y))
    conn.commit()

def move_obstacles(conn):
    c = conn.cursor()
    # increment y by 1 for all obstacles
    c.execute('UPDATE obstacles SET y = y + 1')
    conn.commit()

def remove_out_of_bounds(conn, map_height):
    c = conn.cursor()
    c.execute('DELETE FROM obstacles WHERE y >= ?', (map_height,))
    conn.commit()

def get_obstacles(conn):
    c = conn.cursor()
    c.execute('SELECT x,y FROM obstacles')
    return [[row[0], row[1]] for row in c.fetchall()]

def run_test():
    # game constants (small map for demo)
    map_width = 10
    map_height = 8
    playerpos = 4
    fuel = 100

    # prepare DB
    conn = db_connect()
    db_init(conn)
    clear_obstacles(conn)

    # initial obstacles
    for i in range(3):
        x = random.randint(0, map_width - 1)
        add_obstacle(conn, x, -1 - i)  # start above the top so they fall in

    # run a few ticks, rendering each time
    ticks = 6
    for t in range(ticks):
        # pull obstacles to list and render
        coords = get_obstacles(conn)
        render.set_state(coords, map_width, map_height, playerpos)
        header = f"[sqlite] Tick {t+1}/{ticks}  Fuel: {fuel}  Obstacles: {len(coords)}"
        render.render_and_draw(header)

        # advance
        time.sleep(0.4)
        move_obstacles(conn)
        remove_out_of_bounds(conn, map_height)

    # final state print
    coords = get_obstacles(conn)
    print("Final obstacles (x,y):", coords)
    conn.close()

if __name__ == '__main__':
    run_test()
