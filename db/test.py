import sqlite3

with sqlite3.connect("./users.db") as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO Users (status, id_teleg) VALUES (1, 922347990);")
    conn.commit()
