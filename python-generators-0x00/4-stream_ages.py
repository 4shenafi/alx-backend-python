from seed import connect_to_prodev

def stream_user_ages():
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield float(row[0])

    cursor.close()
    conn.close()

def average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")
