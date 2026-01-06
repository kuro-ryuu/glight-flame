import random
import time
import threading
import sqlite3
import db_init
import render
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS


# Database (kept for compatibility)
db_connection = db_init.open_db()
db_connection.row_factory = sqlite3.Row


# --- Game state and setup ---
key_pressed = None
key_lock = threading.Lock() # to protect key_pressed
state_lock = threading.Lock()
last_frame = ""
stop_event = threading.Event()

def var_setup():
    global coords_list, map_height, map_width, fuel, delay, magnitude
    global last_command_time, obs_interval, last_key_time, paused, key_delay
    global playerpos, score
    coords_list = []  # list of [x, y]
    map_height = 10
    map_width = 10
    score = 0

    fuel = 1000
    delay = 0
    magnitude = 0

    last_command_time = 0
    obs_interval = 0.6
    last_key_time = 0  # seconds
    paused = False
    key_delay = 0.2
    playerpos = 0


def obstacle_gen(number):
    global score
    if [number, -1] not in coords_list:
        coords_list.append([number, -1])
        score += 10
    for i, p in enumerate(coords_list):
        coords_list[i][1] = p[1] + 1
    coords_list[:] = [p for p in coords_list if p[1] < map_height]


def disaster_gen(delay, magnitude):
    return


def game_loop():
    global last_frame, last_command_time, last_key_time, playerpos, fuel, paused
    last_maintime = 0
    while not stop_event.is_set():
        maintime = time.time()
        if maintime - last_maintime > 0.01:
            last_maintime = maintime
            # Update header and frame
            header = f"Current map: WebGame\nScore: {score}\nFuel: {fuel}\nPlayerPos: {playerpos},{map_height - 1}"
            with state_lock:
                render.set_state(coords_list, map_width, map_height, playerpos)
                rows = render.render_rows()
                if rows == "GAME OVER":
                    last_frame = header + "\n" + rows
                    stop_event.set()
                    continue
                last_frame = header + "\n" + rows

            now = time.time()
            if now - last_command_time > obs_interval:
                obstacle_gen(random.randint(0, map_width - 1))
                disaster_gen(delay, magnitude)
                last_command_time = now

            # Handle key_pressed input (throttled by key_delay)
            if (now - last_key_time) > key_delay:
                with key_lock:
                    k = key_pressed
                    # consume
                    # note: do not clear if None
                    if k is not None:
                        # reset key
                        globals()['key_pressed'] = None
                moved = False
                if k == 'a' or k == 'left':
                    playerpos -= 1
                    moved = True
                elif k == 'd' or k == 'right':
                    playerpos += 1
                    moved = True
                elif k == 'space':
                    paused = not paused
                elif k == 'q' or k == 'quit':
                    stop_event.set()

                if moved:
                    if playerpos < 0:
                        playerpos = 0
                        moved = False
                    if playerpos > map_width - 1:
                        playerpos = map_width - 1
                        moved = False
                    if moved:
                        fuel -= 10
                    last_key_time = now
        time.sleep(0.001)


# initialize
var_setup()

# start game thread
game_thread = threading.Thread(target=game_loop, daemon=True)
game_thread.start()

app = Flask(__name__)
CORS(app)

@app.route('/key', methods=['POST'])
def post_key():
    """Accepts JSON or form data with 'key' field (e.g. 'left','right','space','q' or 'a','d')."""
    data = request.get_json(silent=True) or request.form or request.values
    key = data.get('key')
    if not key:
        return jsonify({'error': 'no key provided'}), 400
    with key_lock:
        globals()['key_pressed'] = key
    return jsonify({'status': 'ok', 'key': key})


@app.route('/frame', methods=['GET'])
def get_frame():
    """Returns the latest rendered frame as plain text."""
    with state_lock:
        frame = last_frame
    return Response(frame, mimetype='text/plain')


@app.route('/state', methods=['GET'])
def get_state():
    with state_lock:
        s = dict(playerpos=playerpos, fuel=fuel, score=score, paused=paused)
    return jsonify(s)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)