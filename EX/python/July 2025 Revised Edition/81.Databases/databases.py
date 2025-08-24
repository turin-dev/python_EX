"""Examples using dbm for key‑value storage and sqlite3 for SQL databases."""

from __future__ import annotations

import dbm
import sqlite3


def demo_dbm() -> None:
    with dbm.open('demo.dbm', 'c') as db:
        db[b'user1'] = b'Alice'
        db[b'user2'] = b'Bob'
        print("Keys in dbm:", list(db.keys()))
        print("user1 ->", db[b'user1'])


def demo_sqlite() -> None:
    conn = sqlite3.connect('demo.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)')
    cur.execute('INSERT INTO items (name) VALUES (?)', ('Widget',))
    cur.execute('SELECT id, name FROM items')
    print("SQLite rows:", cur.fetchall())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    demo_dbm()
    demo_sqlite()