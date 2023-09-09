import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        """
        Inicializa a classe DatabaseManager.

        Args:
            db_name (str): O nome do banco de dados.

        Attributes:
            db_name (str): O nome do banco de dados.
            connection (sqlite3.Connection): A conexão com o banco de dados.
            cursor (sqlite3.Cursor): O cursor para executar comandos SQL.
            connected_user (str): O nome do usuário conectado.

        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connected_user = None  # Variável para armazenar o username do usuário conectado

    def connect(self, username):
        """
        Estabelece uma conexão com o banco de dados.

        Args:
            username (str): O nome do usuário que está se conectando.

        Returns:
            None

        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.connected_user = username  # Armazena o username do usuário conectado

    def close(self):
        """
        Fecha a conexão com o banco de dados e o cursor.

        Returns:
            None

        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        """
        Executa uma consulta SQL no banco de dados.

        Args:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Os parâmetros a serem substituídos na consulta (opcional).

        Returns:
            None

        """
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        self.connection.commit()

    def fetch_one(self, query, params=None):
        """
        Executa uma consulta SQL no banco de dados e retorna uma única linha de resultado.

        Args:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Os parâmetros a serem substituídos na consulta (opcional).

        Returns:
            tuple: Uma tupla contendo os valores da linha de resultado.

        """
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        """
        Executa uma consulta SQL no banco de dados e retorna todas as linhas de resultado.

        Args:
            query (str): A consulta SQL a ser executada.
            params (tuple, optional): Os parâmetros a serem substituídos na consulta (opcional).

        Returns:
            list: Uma lista de tuplas, onde cada tupla contém os valores de uma linha de resultado.

        """
        if not self.connection:
            self.connect()

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchall()

    def get_cursor(self):
        """
        Retorna o cursor atual.

        Returns:
            sqlite3.Cursor: O cursor atual.

        """
        if not self.connection:
            self.connect()

        return self.cursor

    def get_connected_user(self):
        """
        Retorna o nome do usuário conectado.

        Returns:
            str: O nome do usuário conectado.

        """
        return self.connected_user
