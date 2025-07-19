# 3-concurrent.py
import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)

async def async_fetch_older_users():
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
