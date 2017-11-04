import sqlite3
from os import path

class ServerDatabase:
    
    def __init__(self, name):
        self.sqlite_db_file = name + "_db" + ".sqlite"

        if not path.exists(self.sqlite_db_file):
            self.build_schema()
        self.db_conn = sqlite3.connect(self.sqlite_db_file)

        print("Database for " + name + " initialised")
    
    def start_session(self, player):
        pass 

    def end_session(self, player):
        pass

    def end_game(self, game):
        pass

    def build_schema(self):
        print("Building schema...")

        conn = sqlite3.connect(self.sqlite_db_file)
        c = conn.cursor()

        conn.commit()
        conn.close()


