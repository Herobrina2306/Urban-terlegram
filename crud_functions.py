import sqlite3

connection = sqlite3.connect('datebase.db')
cursor1 = connection.cursor()

cursor1.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY, 
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
);
''')

connection2 = sqlite3.connect('user_datebase.db')
user_cursor = connection2.cursor()

user_cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
);
''')


def get_all_products():
    cursor1.execute("SELECT id, title, description, price FROM Products")
    products = cursor1.fetchall()
    connection.commit()
    return products

def add_user(username, email, age):
    user_cursor.execute(f'''INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', 1000)''')
    connection2.commit()


def is_included(username):
    check_user = user_cursor.execute('SELECT * FROM Users WHERE username = ?', (username, ))
    if len(check_user.fetchall()) == 0:
        return True
    else:
        return False



pro = get_all_products()


connection2.commit()


connection.commit()


