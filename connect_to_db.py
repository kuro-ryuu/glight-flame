import sqlite3
def connect():
    conn = sqlite3.connect(
        "./database/flight_simulator_database_script.sql"
    )
    return conn