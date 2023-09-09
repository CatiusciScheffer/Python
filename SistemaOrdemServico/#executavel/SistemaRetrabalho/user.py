import hashlib
from database import DatabaseManager
from tkinter import messagebox

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def registerNewUser(self, username, password):
        """
        Registra um novo usuário no sistema.

        Args:
            username (str): O nome de usuário do novo usuário.
            password (str): A senha do novo usuário.

        Returns:
            None
        """
        if not username or not password:
            messagebox.showinfo("Erro de Preenchimento", "Preencha todos os campos!")
            self.registerNewUser()  # Chama a função novamente se campos estiverem em branco
        else:
            hashed_password = self._hash_password(password)  # Hash da senha antes de armazená-la no banco de dados
            self.db_manager.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)",
                                    (username, hashed_password))
    
    def checkUsernameAndPasswordRegistered(self, username, password):
        """
        Verifica se um nome de usuário e senha estão registrados no sistema.

        Args:
            username (str): O nome de usuário a ser verificado.
            password (str): A senha a ser verificada.

        Returns:
            bool: True se as credenciais forem válidas, False caso contrário.
        """
        hashed_password = self._hash_password(password)  # Hash da senha antes de comparar
        result = self.db_manager.fetch_one("SELECT nomeUsuario, senhaUsuario FROM tb_usuarios WHERE nomeUsuario=?",
                                          (username,))

        if result is not None:
            stored_username, stored_password = result
            if hashed_password == stored_password:
                return True  # Credenciais válidas
            else:
                messagebox.showinfo("Erro de Autenticação", "Senha inválida.")
                self.checkUsernameAndPasswordRegistered()  # Chama a função novamente se a senha for inválida

        return False  # Credenciais inválidas

    def _hash_password(self, password):
        """
        Função interna para calcular o hash de uma senha.

        Args:
            password (str): A senha a ser hashada.

        Returns:
            str: O hash da senha no formato hexadecimal.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

