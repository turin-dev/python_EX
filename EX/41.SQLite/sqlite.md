# 41. Working with SQLite databases

The `sqlite3` module wraps the SQLite embedded database engine.  SQLite is a
lightweight disk‑based database that does not require a separate server
process.  The documentation notes that it provides a “lightweight disk‑based
database” and the `sqlite3` module offers an SQL interface compliant with
DB‑API 2.0【232817957113109†L82-L92】.  SQLite is useful for prototyping and
applications that need an embedded database【232817957113109†L82-L88】.

## Connecting to a database

* **Create or open a database:** Call `sqlite3.connect('example.db')` to create
  a new database file or open an existing one.  Using `:memory:` creates an
  in‑memory database that is discarded when the connection is closed.
* **Connection and cursor:** A connection object represents the database.  Call
  `conn.cursor()` to obtain a cursor for executing SQL statements【232817957113109†L125-L146】.
* **Executing SQL:** Use `cursor.execute(sql, params)` to run queries and
  commands.  For multiple inserts use `executemany()` with a sequence of
  parameter tuples.
* **Commit and close:** Changes are persisted when `conn.commit()` is called.
  Always close the connection with `conn.close()` when finished.

## Example: Creating and querying a table

The following script creates a simple `users` table, inserts a few rows and
selects all records:

```python
import sqlite3

con = sqlite3.connect('example.db')
cur = con.cursor()

# Create table
cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, age INTEGER)")

# Insert a row of data
cur.execute("INSERT INTO users VALUES (?, ?)", ("Alice", 30))

# Insert many rows at once
users = [("Bob", 25), ("Carol", 27), ("Dave", 35)]
cur.executemany("INSERT INTO users VALUES (?, ?)", users)

# Commit the changes
con.commit()

# Query the database
cur.execute("SELECT name, age FROM users WHERE age >= ?", (30,))
for row in cur.fetchall():
    print(row)

con.close()
```

SQLite uses dynamic typing; columns accept any data type unless you enforce
constraints.  To register adapters and converters for custom types see the
advanced topics in the standard library documentation.

## Transactions and isolation levels

SQLite operates in autocommit mode unless you explicitly start a transaction
with `BEGIN`.  You can control isolation behaviour via the connection’s
`isolation_level` attribute.  The default isolation level is `''` (autocommit).

## Summary

The `sqlite3` module provides a self‑contained SQL database engine that is
useful for small to medium‑sized applications.  Because it follows the DB‑API
specification【232817957113109†L82-L92】, the same programming patterns used with
other SQL databases apply.
