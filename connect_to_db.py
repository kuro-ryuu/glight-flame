import mysql.connector
def connect():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='Mrnoob',
        password='123456789',
        autocommit=True
    )
    return conn