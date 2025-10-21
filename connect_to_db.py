import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='CDKR',
    password='1507',
    autocommit=True
)