import sqlite3


if __name__ == "__main__":
    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        id_teleg INTEGER NOT NULL UNIQUE,
        status INTEGER DEFAULT 1
        )
        """)
        conn.commit()
