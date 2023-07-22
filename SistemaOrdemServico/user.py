import hashlib
from database import DatabaseManager
from tkinter import messagebox

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # def register_user(self, username, password):
    #     hashed_password = self._hash_password(password)
    #     self.db_manager.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)",
    #                             (username, hashed_password))
    
    def register_user(self, username, password):
        if not username or not password:
            messagebox.showinfo("Erro de Preenchimento", "Preencha todos os campos!")
            self.register_user()
        else:
            hashed_password = self._hash_password(password)
            self.db_manager.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)",
                                    (username, hashed_password))
    
    def authenticate_user(self, username, password):
        hashed_password = self._hash_password(password)
        result = self.db_manager.fetch_one("SELECT nomeUsuario, senhaUsuario FROM tb_usuarios WHERE nomeUsuario=?",
                                        (username,))

        if result is not None:
            stored_username, stored_password = result
            if hashed_password == stored_password:
                return True
            else:
                messagebox.showinfo("Erro de Autenticação", "Senha inválida.")
                self.authenticate_user()

        return False

    def _hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
