import sqlite3
import os


def open_db():

    if not (os.path.exists("./database/storage.db")):
        db = sqlite3.connect("./database/storage.db")
        cursor = db.cursor()
        with open("./database/dump.sql", "r",encoding="utf-8") as file:
            script = file.read()
            cursor.executescript(script)
            db.commit()
    else:
        db = sqlite3.connect("./database/storage.db")
    return db
