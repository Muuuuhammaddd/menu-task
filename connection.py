from menu import connection
import asyncpg
from passlib.context import CryptContext

secret = CryptContext(schemes=["argon2"], deprecated="auto")

async def hash_password(password):
    return secret.hash(password)


async def verify_password(password, hashed_password):
    return secret.verify(password, hashed_password)



async def registions(username, password):
    conn = await connection()
    try:
        password_hash = await hash_password(password)
        await conn.execute(
            "INSERT INTO users(username, password_hash) VALUES($1, $2)",
            username, password_hash
        )
        print("Registered")
        return True
    except Exception as error:
        print(f"Error registering: {error}")
        return False
    finally:
        await conn.close()


async def get_first_user():
    conn = await connection()
    try:
        row = await conn.fetchrow(
            "SELECT username FROM users ORDER BY user_id LIMIT 1"
        )
        return row["username"] if row else None
    except Exception as error:
        print(f"Error checking account: {error}")
        return None
    finally:
        await conn.close()


async def login_user(username, password):
    conn = await connection()
    try:
        row = await conn.fetchrow(
            "SELECT password_hash FROM users WHERE username = $1", username
        )
        if row is None:
            print("Error: user not found")
            return False
        if await verify_password(password, row["password_hash"]):
            print("==Login successful==")
            return True
        else:
            print("Error: wrong password")
            return False
    except Exception as error:
        print(f"Error logging in: {error}")
        return False
    finally:
        await conn.close()


async def create_category(name):
    conn = await connection()
    try:
        await conn.execute(
            "INSERT INTO category(name) VALUES($1)", name
        )
    except Exception as error:
        print(f"Error creating: {error}")
    finally:
        await conn.close()
        

async def get_category():
    conn = await connection()
    try:
        data = await conn.fetch(
            "SELECT * FROM category"
        )
        for i in data:
            print(f"ID: {i[0]}, Name: {i[1]}")
    except Exception as error:
        print(f"Error Geting: {error}")
    finally:
        await conn.close()
        
        
async def update_category(category_id, name):
    conn = await connection()
    try:
        await conn.execute(
            "UPDATE category SET name = $1 WHERE category_id = $2", name, category_id
        )
        print("==Updated==")
    except Exception as error:
        print(f"Error updating: {error}")
    finally:
        await conn.close()
        
        
async def delete_category(category_id):
    conn = await connection()
    try:
        await conn.execute(
            "DELETE FROM category WHERE category_id = $1", category_id
        )
        print("==Deleted==")
    except Exception as error:
        print(f"Error deleting: {error}")
    finally:
        await conn.close()
        




async def create_dish(name, price, category_id):
    conn = await connection()
    try:
        await conn.execute(
            "INSERT INTO dishes(name, price, category_id) VALUES($1, $2, $3)", name, price, category_id
        )
    except Exception as error:
        print(f"Error creating: {error}")
    finally:
        await conn.close()
        

async def get_dish():
    conn = await connection()
    try:
        data = await conn.fetch(
            "SELECT * FROM dishes"
        )
        for i in data:
            print(f"ID:{i[0]}, Name:{i[1]}, Price:{i[2]}, Category ID:{i[3]}")
    except Exception as error:
        print(f"Error Geting: {error}")
    finally:
        await conn.close()
        

async def update_dish(dish_id, name, price, category_id):
    conn = await connection()
    try:
        await conn.execute(
            "UPDATE dishes SET name = $1, price = $2, category_id = $3 WHERE dish_id = $4", name, price, category_id, dish_id
        )
        print("==Updated==")
    except Exception as error:
        print(f"Error updating: {error}")
    finally:
        await conn.close()
        
        
async def delete_dish(dish_id):
    conn = await connection()
    try:
        await conn.execute(
            "DELETE FROM dishes WHERE dish_id = $1", dish_id
        )
        print("==Deleted==")
    except Exception as error:
        print(f"Error deleting: {error}")
    finally:
        await conn.close()
        




async def create_order(dish_id, quantity):
    conn = await connection()
    try:
        await conn.execute(
            "INSERT INTO orders(dish_id, quantity) VALUES($1, $2)", dish_id, quantity
        )
    except Exception as error:
        print(f"Error creating: {error}")
    finally:
        await conn.close()
        
        
async def get_order():
    conn = await connection()
    try:
        data = await conn.fetch("""
            SELECT orders.order_id,
                dishes.name,
                orders.quantity,
                dishes.price*orders.quantity AS total
            FROM orders
            JOIN dishes ON dishes.dish_id=orders.dish_id
        """)
        for i in data:
            print(f"Order:{i[0]} | Dish:{i[1]} | Qty:{i[2]} | Total:{i[3]}")
    except Exception as error:
        print(f"Error Geting {error}")
    finally:
        await conn.close()
        
        
async def update_order(order_id, quantity):
    conn = await connection()
    try:
        await conn.execute(
            "UPDATE orders SET quantity = $1 WHERE order_id = $2", quantity, order_id
        )    
        print("==Updated==")
    except Exception as error:
        print(f"Error Updating: {error}")
    finally:
        await conn.close()
        
        
async def delete_order(order_id):
    conn = await connection()
    try:
        await conn.execute(
            "DELETE FROM orders WHERE order_id=$1", order_id
        )
        print("==Deleted==")
    except Exception as error:
        print(f"Error Deleting: {error}")
    finally:
        await conn.close()