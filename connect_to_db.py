import mysql.connector
def connect():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='root',
        password='password',
        autocommit=True
    )
    return conn