import sqlite3

class DB:
    """
    DB class which was create to save url to db and work with it
    """
    def __init__(self, url: str):
        self.url = url

    def exec(self, req: str):
        with sqlite3.connect(self.url) as conn:
            cur = conn.cursor()
            cur.execute(req)
            conn.commit()

    def get_status(self, id: int):
        res = ""
        with sqlite3.connect(self.url) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT status FROM Users WHERE id_teleg = {id}")
            res = cur.fetchone()

        return res[0]
    def change_prev_step(self, id: int):
        self.exec(f"UPDATE Users SET status = {self.get_status(id) - 1} WHERE id_teleg = {id}")

    def change_next_step(self, id: int):
        self.exec(f"UPDATE Users SET status = {self.get_status(id) + 1} WHERE id_teleg = {id}")

    def create_new_user(self, id: int):
        self.exec("INSERT INTO Users (status, id_teleg) VALUES (1, 922347990);")

    def delete_user(self, id: int):
        self.exec(f"DELETE FROM Users WHERE id_teleg = {id}")


if __name__ == "__main__":
    """check if everything is working"""
    db = DB("./users.db")
    #res = db.get_status(922347990)
    #print(res)
    db.exec("DELETE FROM Users")
    #db.delete_user(922347990)
    #db.create_new_user(922347990)
    #res = db.get_status(922347990) 
    #print(res)
    #db.change_next_step(922347990)
    #res = db.get_status(922347990)
    #print(res)
    #db.delete_user(922347990)

