from database import DatabaseManager
from gui import LoginGUI

def main():
    db_manager = DatabaseManager("db_OrdemServicos.db")
    db_manager.connect('')

    login_gui = LoginGUI(db_manager)
    login_gui.tela_login.mainloop()

    db_manager.close()

if __name__ == "__main__":
    main()
