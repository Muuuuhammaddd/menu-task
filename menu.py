import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
ps = os.getenv("PASSWORD_DB")

async def connection():
    try:
        conn = await asyncpg.connect(
            database="Menu2_db",
            host="localhost",
            user="postgres",
            port=5432,
            password=ps
        )
        print("Great Connection")
        return conn
    except Exception as error:
        print(f"Connection Error: {error}")


async def create_tables():
    conn = await connection()
    if conn is None:
        return
    try: 
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS category(
                category_id SERIAL PRIMARY KEY,
                name VARCHAR(30) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS dishes(
                dish_id SERIAL PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                price INT NOT NULL,
                category_id INT REFERENCES category(category_id)
            );

            CREATE TABLE IF NOT EXISTS orders(
                order_id SERIAL PRIMARY KEY,
                dish_id INT REFERENCES dishes(dish_id),
                quantity INT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
    except Exception as error:
        print(f"Create table error: {error}")
    finally:
        await conn.close()