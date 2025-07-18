#!/usr/bin/python3

import mysql.connector


# ✅ Generator: Stream users in batches
def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing():
    for batch in stream_users_in_batches(batch_size=10):
        filtered = [user for user in batch if user[3] > 25]  # user[3] = age
        yield filtered