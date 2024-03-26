import sqlite3

def create_db(url: str):
    with sqlite3.connect(url) as conn:
        cur = conn.cursor()
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        id_teleg INTEGER NOT NULL UNIQUE,
        status INTEGER DEFAULT 1
        )
        """)
        conn.commit()



if __name__ == "__main__":
    create_db("users.db")
