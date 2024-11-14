import sqlite3

connection = sqlite3.connect('datebase.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY, 
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')

# for i in range(1, 5):
#      cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (f"Продукт {i}", f"Описание {i}", f"{i * 100}"))


def get_all_products():
    cursor.execute("SELECT id, title, description, price FROM Products")
    products = cursor.fetchall()
    return products

pro = get_all_products()

connection.commit()
connection.close()