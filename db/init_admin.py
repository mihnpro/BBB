import os
import json

from table_exec import create_db

from dotenv import load_dotenv 


load_dotenv()
    

if __name__ == "__main__":
    create_db(os.path.abspath("./db/users.db"))
    passwd_env = os.getenv("PASSWORD")
    with open(os.path.abspath("./db/admin.json"), 'w') as file:
        json_object = {
            "max_chapter": 2,
            "password": passwd_env
        }
        file.write(json.dumps(json_object, indent=4))

