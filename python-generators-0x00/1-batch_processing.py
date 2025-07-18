import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    conn.close()

def batch_processing():
    for batch in stream_users_in_batches(5):  # You can change batch size here
        filtered = [user for user in batch if user['age'] > 25]
        for user in filtered:
            print(user)
