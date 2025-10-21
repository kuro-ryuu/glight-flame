import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='some_database_name',
    user='some_user_name',
    password='some_password',
    autocommit=True
)