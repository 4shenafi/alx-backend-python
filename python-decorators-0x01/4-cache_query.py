# 4-cache_query.py
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("[CACHE HIT] Returning cached result")
            return query_cache[query]
        else:
            print("[CACHE MISS] Querying DB")
            result = func(conn, query)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users)
