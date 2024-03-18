import sqlite3

with sqlite3.connect("./users.db") as conn:
    cur = conn.cursor()
    cur.execute("")
    conn.commit()
