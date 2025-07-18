import mysql.connector
import csv

def connect_db():
    return mysql.connector.connect(
        host="localhost", user="your_user", password="your_pass"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost", user="your_user", password="your_pass", database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    )""")
    connection.commit()
    cursor.close()

def insert_data(connection, data_file):
    cursor = connection.cursor()
    with open(data_file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute("SELECT user_id FROM user_data WHERE user_id=%s", (row[0],))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (row[0], row[1], row[2], row[3])
                )
    connection.commit()
    cursor.close()
