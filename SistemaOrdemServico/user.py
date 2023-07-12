import hashlib
from database import DatabaseManager

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def register_user(self, username, password):
        hashed_password = self._hash_password(password)
        self.db_manager.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)",
                                (username, hashed_password))

    def authenticate_user(self, username, password):
        hashed_password = self._hash_password(password)
        result = self.db_manager.fetch_one("SELECT nomeUsuario FROM tb_usuarios WHERE nomeUsuario=? AND senhaUsuario=?",
                                           (username, hashed_password))
        return result is not None

    def _hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
