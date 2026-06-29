import sqlite3
from core.config import DATABASE

def connect():
    return sqlite3.connect(DATABASE)

def add_user(user_id, username, first_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users (user_id, username, first_name)
    VALUES (?, ?, ?)
    """, (user_id, username, first_name))

    conn.commit()
    conn.close()

def add_order(user_id, product, amount):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO orders (user_id, product, amount)
    VALUES (?, ?, ?)
    """, (user_id, product, amount))

    conn.commit()
    conn.close()
