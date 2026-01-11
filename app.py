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

app = Flask(__name__)
CORS(app)

# --- Multiplayer: per-player state and threads ---
import uuid


class Player:
    def __init__(self, pid=None):
        self.id = pid or str(uuid.uuid4())
        self.coords_list = []  # list of [x, y]
        self.map_height = 10
        self.map_width = 10
        self.score = 0

        self.fuel = 1000
        self.delay = 0
        self.magnitude = 0

        self.last_command_time = time.time()
        self.obs_interval = 0.6
        self.last_key_time = time.time()
        self.paused = 0
        self.key_delay = 0.2
        self.playerpos = 0

        self.key_pressed = None
        self.key_lock = threading.Lock()
        self.state_lock = threading.Lock()
        self.last_frame = ""
        self.stop_event = threading.Event()
        self.running = False

        self.thread = None

    def restart_game(self):
        self.coords_list = []
        self.score = 0
        self.fuel = 1000
        self.delay = 0
        self.magnitude = 0
        self.last_command_time = time.time()
        self.last_key_time = time.time()
        self.paused = 0
        self.playerpos = 0
        render.set_state(self.coords_list, self.map_width, self.map_height, self.playerpos)

    def obstacle_gen(self, number):
        if [number, -1] not in self.coords_list:
            self.coords_list.append([number, -1])
            self.score += 10
        for i, p in enumerate(self.coords_list):
            self.coords_list[i][1] = p[1] + 1
        self.coords_list[:] = [p for p in self.coords_list if p[1] < self.map_height]

    def disaster_gen(self):
        return

    def game_loop(self):
        last_maintime = 0
        while not self.stop_event.is_set():
            if not self.running:
                # when not running, show a simple prompt and skip rendering/keys
                with self.state_lock:
                    self.last_frame = f"Player {self.id}: Press Start"
                time.sleep(0.1)
                continue
            maintime = time.time()
            if maintime - last_maintime > 0.01:
                last_maintime = maintime
                header = f"Current map: WebGame\nScore: {self.score}\nFuel: {self.fuel}\nPlayerPos: {self.playerpos},{self.map_height - 1}"
                # render state and prepare frame
                with self.state_lock:
                    render.set_state(self.coords_list, self.map_width, self.map_height, self.playerpos)
                    rows = render.render_rows()
                if rows == "GAME OVER":
                    rows = "Game Over! Press 'r' to restart."
                    # update frame and enter restart-wait loop without holding state lock
                    self.last_frame = header + "\n" + rows
                    self.paused = 1
                    # wait for restart key, or break if stopped/not running
                    while not self.stop_event.is_set() and self.running:
                        k = None
                        with self.key_lock:
                            k = self.key_pressed
                            if k is not None:
                                self.key_pressed = None
                        if k == 'r' or k == 'restart':
                            self.restart_game()
                            print(f"Player {self.id} restarted!")
                            self.paused = 0
                            time.sleep(0.3)
                            break
                        time.sleep(0.1)
                self.last_frame = header + "\n" + rows

                now = time.time()
                if now - self.last_command_time > self.obs_interval:
                    self.obstacle_gen(random.randint(0, self.map_width - 1))
                    self.disaster_gen()
                    self.last_command_time = now

                # Handle key_pressed input (throttled by key_delay)
                if (now - self.last_key_time) > self.key_delay:
                    with self.key_lock:
                        k = self.key_pressed
                        if k is not None:
                            self.key_pressed = None
                    moved = False
                    if k == 'a' or k == 'left':
                        self.playerpos -= 1
                        moved = True
                    elif k == 'd' or k == 'right':
                        self.playerpos += 1
                        moved = True
                    elif k == 'space':
                        # pause until space pressed again, or until stopped/not running
                        self.paused = 1
                        print("Game paused. Press space to resume.")
                        time.sleep(0.2)
                        while not self.stop_event.is_set() and self.running:
                            kk = None
                            with self.key_lock:
                                kk = self.key_pressed
                                if kk is not None:
                                    self.key_pressed = None
                            if kk == 'space':
                                print("Game resuming in:")
                                for i in range(3, 0, -1):
                                    print(i)
                                    time.sleep(1)
                                print("Go!")
                                self.paused = 0
                                time.sleep(0.1)
                                break
                            time.sleep(0.1)
                    elif k == 'r' or k == 'restart':
                        self.restart_game()
                        print(f"Player {self.id} restarted!")
                    elif k == 'q' or k == 'quit':
                        self.stop_event.set()

                    if moved:
                        if self.playerpos < 0:
                            self.playerpos = 0
                            moved = False
                        if self.playerpos > self.map_width - 1:
                            self.playerpos = self.map_width - 1
                            moved = False
                        if moved:
                            self.fuel -= 10
                    if moved or k is not None:
                        self.last_key_time = now
            time.sleep(0.001)


# Registry of players
players = {}
players_lock = threading.Lock()

def create_player(pid=None):
    p = Player(pid)
    with players_lock:
        players[p.id] = p
    p.thread = threading.Thread(target=p.game_loop, daemon=True)
    p.thread.start()
    return p


# create a default player for compatibility
default_player = create_player(pid='default')


@app.route('/start', methods=['POST'])
def start_player():
    data = request.get_json(silent=True) or request.form or request.values
    pid = data.get('player') or data.get('id') or request.args.get('player') or 'default'
    with players_lock:
        p = players.get(pid)
    if not p:
        # create and start
        p = create_player(pid)
    # restart and mark running
    p.restart_game()
    p.running = True
    return jsonify({'status': 'started', 'player': p.id})


@app.route('/stop', methods=['POST'])
def stop_player():
    data = request.get_json(silent=True) or request.form or request.values
    pid = data.get('player') or request.args.get('player') or 'default'
    with players_lock:
        p = players.get(pid)
    if not p:
        return jsonify({'error': 'player not found', 'player': pid}), 404
    p.running = False
    return jsonify({'status': 'stopped', 'player': pid})


@app.route('/key', methods=['POST'])
def post_key():
    """Accepts JSON/form with 'key' and optional 'player' id."""
    data = request.get_json(silent=True) or request.form or request.values
    key = data.get('key')
    pid = data.get('player') or request.args.get('player') or 'default'
    if not key:
        return jsonify({'error': 'no key provided'}), 400
    with players_lock:
        p = players.get(pid)
    if not p:
        return jsonify({'error': 'player not found', 'player': pid}), 404
    if not p.running:
        return jsonify({'error': 'player not running', 'player': pid}), 400
    with p.key_lock:
        p.key_pressed = key
    return jsonify({'status': 'ok', 'key': key, 'player': pid})


@app.route('/frame', methods=['GET'])
def get_frame():
    """Returns the latest rendered frame for a player as plain text.
    Use query `?player=<id>` or omit for default player.
    """
    pid = request.args.get('player') or 'default'
    with players_lock:
        p = players.get(pid)
    if not p:
        return jsonify({'error': 'player not found', 'player': pid}), 404
    with p.state_lock:
        frame = p.last_frame
    return Response(frame, mimetype='text/plain')


@app.route('/state', methods=['GET'])
def get_state():
    pid = request.args.get('player') or 'default'
    with players_lock:
        p = players.get(pid)
    if not p:
        return jsonify({'error': 'player not found', 'player': pid}), 404
    with p.state_lock:
        s = dict(playerpos=p.playerpos, fuel=p.fuel, score=p.score, paused=p.paused)
    return jsonify(s)


@app.route('/player', methods=['POST'])
def create_player_route():
    """Create a new player and start its game thread. Optional JSON/form field 'player' to set id."""
    data = request.get_json(silent=True) or request.form or request.values
    pid = data.get('player') or data.get('id')
    p = create_player(pid)
    return jsonify({'status': 'created', 'player': p.id})


@app.route('/players', methods=['GET'])
def list_players():
    with players_lock:
        ids = list(players.keys())
    return jsonify({'players': ids})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)