import sqlite3
import functools

def log_queries(func):
    """Decorator that logs the SQL query before executing it."""
    @functools.wraps(func)
    def wrapper(query):
        print(f"[LOG] Executing SQL Query: {query}")
        return func(query)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test the function
users = fetch_all_users(query="SELECT * FROM users")
print(users)
