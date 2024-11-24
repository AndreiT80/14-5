# Домашнее задание по теме "План написания админ панели"

import sqlite3
from distutils.command.check import check


connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
id INTEDGER PRIMARY KEY, 
title TEXT NOT NULL,
description TEXT,
price INTEDGER NOT NULL
)
""")

#cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON Products(title)")
#for i in range(1, 5):
#    cursor.execute("INSERT INTO Products (id, title, description, price) VALUES(?, ?, ?, ?)",
#                 (i, f"Продукт {i}", f"Описание {i}", f" {i * 100}"))
connection.commit()
connection.close()

connection = sqlite3.connect("new_users.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEDGER PRIMARY KEY, 
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEDGER NOT NULL,
balance INTEDGER NOT NULL
)
""")

#cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users(email)")
#for i in range(1, 6):
#    cursor.execute( "INSERT INTO Users(username, email, age, balance) VALUES (?,?,?,?)",
#                    (f"newuser{i}", f"example{i}@gmail.com", f"{10 * i}", "1000"))
#    connection.commit()


def is_included(username):
    connection = sqlite3.connect('new_users.db')
    cursor = connection.cursor()
    k = cursor.execute('SELECT username FROM users').fetchall()
    connection.commit()
    return (username,) in k

def add_user(username, email, age):
    connection = sqlite3.connect('new_users.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO users (username, email, age, balance)'
                   f' VALUES("{username}", "{email}", "{age}", 1000)')
    connection.commit()
    connection.close()



def get_all_products():
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    sid = cursor.fetchall()

    connection.commit()
    connection.close()
    return sid