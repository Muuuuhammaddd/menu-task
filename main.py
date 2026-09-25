from menu import *
from connection import *
import asyncio
from getpass import getpass


async def register_screen():
    print("Аккаунт не найден. Нужно зарегистрироваться.\n")
    while True:
        username = input("Username: ")
        password = getpass("Password: ")
        if await register_user(username, password):
            return username


async def login_screen():
    while True:
        print("\n========== LOGIN ==========")
        username = input("Username: ")
        password = getpass("Password: ")
        if await login_user(username, password):
            return username


async def main():
    await create_tables()

    existing_user = await get_first_user()
    if existing_user is None:
        current_user = await register_screen()
    else:
        current_user = await login_screen()

    print(f"\nWelcome, {current_user}!")

    while True:
        n = int(input(f"""
========== MENU ({current_user}) ==========
1) Create Category
2) Get Categories
3) Update Category
4) Delete Category

5) Create Dish
6) Get Dishes
7) Update Dish
8) Delete Dish

9) Make Order
10) Get Orders
11) Update Order
12) Delete Order

0) Exit

Choose one: """))
        match n:
            case 1:
                await create_category(input("Category name: "))
            case 2:
                await get_category()
            case 3:
                id = int(input("Category ID: "))
                name = input("New name: ")
                await update_category(id, name)
            case 4:
                await delete_category(int(input("Category ID: ")))
                
            case 5:
                name = input("Dish name: ")
                price = int(input("Price: "))
                cat = int(input("Category ID: "))
                await create_dish(name, price, cat)
            case 6:
                await get_dish()
            case 7:
                id = int(input("Dish ID: "))
                price = int(input("New price: "))
                await update_dish(id, price)
            case 8:
                await delete_dish(int(input("Dish ID: ")))

            case 9:
                dish = int(input("Dish ID: "))
                qty = int(input("Quantity: "))
                await create_order(dish, qty)
            case 10:
                await get_order()
            case 11:
                order = int(input("Order ID: "))
                qty = int(input("New quantity: "))
                await update_order(order, qty)
            case 12:
                await delete_order(int(input("Order ID: ")))

            case 0:
                print("I believe in you")
                break
            case _:
                print("Try Again")

if __name__ == "__main__":
    asyncio.run(main())