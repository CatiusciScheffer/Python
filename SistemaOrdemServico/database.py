import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connected_user = None  # Variável para armazenar o username do usuário conectado

    def connect(self, username):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.connected_user = username  # Armazena o username do usuário conectado

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        self.connection.commit()

    def fetch_one(self, query, params=None):
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchall()

    def get_cursor(self):
        if not self.connection:
            self.connect()

        return self.cursor

    def get_connected_user(self):
        return self.connected_user
    
    