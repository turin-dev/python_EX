"""
Demonstration of using the sqlite3 module to create a simple database.

Run this script to create an `example.db` file in the current directory,
insert sample data and query users over a certain age.  The results will
be printed to standard output.
"""

import sqlite3
from typing import Iterable, Tuple


def init_db(db_path: str = "example.db") -> sqlite3.Connection:
    """Create a database and return a connection object."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, age INTEGER)")
    con.commit()
    return con


def insert_users(con: sqlite3.Connection, users: Iterable[Tuple[str, int]]) -> None:
    """Insert multiple user records into the database."""
    con.executemany("INSERT INTO users VALUES (?, ?)", users)
    con.commit()


def get_users_over(con: sqlite3.Connection, age: int) -> list[Tuple[str, int]]:
    """Retrieve all users whose age is greater than or equal to the given age."""
    cur = con.cursor()
    cur.execute("SELECT name, age FROM users WHERE age >= ?", (age,))
    return cur.fetchall()


def main() -> None:
    con = init_db()
    # Populate sample users
    sample = [("Alice", 30), ("Bob", 25), ("Carol", 27), ("Dave", 35)]
    insert_users(con, sample)
    # Query and print results
    for name, age in get_users_over(con, 30):
        print(f"{name} is {age} years old")
    con.close()


if __name__ == "__main__":
    main()