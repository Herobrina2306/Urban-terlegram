import sqlite3

def con1():
    connection = sqlite3.connect('datebase.db')
    cursor1 = connection.cursor()
    return connection, cursor1




# cursor1.execute('''
# CREATE TABLE IF NOT EXISTS Products(
# id INTEGER PRIMARY KEY,
# title TEXT NOT NULL,
# description TEXT,
# price INTEGER NOT NULL
# );
# ''')

def con2():
    connection2 = sqlite3.connect('user_datebase.db')
    user_cursor = connection2.cursor()
    return connection2, user_cursor


def clos(con):
    con.commit()
    con.close()

# user_cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users(
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INTEGER NOT NULL,
# balance INTEGER NOT NULL
# );
# ''')


def get_all_products():
    connection, cursor1 = con1()
    cursor1.execute("SELECT id, title, description, price FROM Products")
    products = cursor1.fetchall()
    clos(connection)
    return products

def add_user(username, email, age):
    connection2, user_cursor = con2()
    user_cursor.execute(f'''INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', 1000)''')
    clos(connection2)


def is_included(username):
    connection2, user_cursor = con2()
    check_user = user_cursor.execute('SELECT * FROM Users WHERE username = ?', (username, ))
    if len(check_user.fetchall()) == 0:
        clos(connection2)
        return True
    else:
        clos(connection2)
        return False



pro = get_all_products()





