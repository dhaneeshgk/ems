""" module containing context managers for 
    - DB connection, close
    - DB cursor, commit
""" 

import sqlite3

class SqliteDB:
    def __init__(self, DB_PATH):
        self.DB_PATH = DB_PATH
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.DB_PATH)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, traceback):
        self.connection.close()


class DBCursor:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None
    
    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, traceback):
        self.connection.commit()