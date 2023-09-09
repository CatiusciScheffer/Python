from database import DatabaseManager
from gui import LoginGUI
import connection  # Importe o módulo de criação de tabelas

def main():
    """
    Função principal do programa.

    Esta função realiza as seguintes etapas:
    1. Cria uma instância do DatabaseManager para gerenciar o banco de dados "db_OrdemServicos.db".
    2. Conecta ao banco de dados (atualmente sem um nome de usuário).
    3. Cria as tabelas se elas ainda não existirem.
    4. Cria uma instância da interface gráfica de login (LoginGUI) passando o DatabaseManager.
    5. Inicia o loop principal da interface gráfica (mainloop) para interagir com o usuário.
    6. Após o término da interface gráfica (quando o usuário fecha a janela de login), fecha a conexão com o banco de dados.

    Returns:
        None

    """
    # Cria uma instância do DatabaseManager para gerenciar o banco de dados
    db_manager = DatabaseManager("db_OrdemServicos.db")
    
    # Conecta ao banco de dados (atualmente sem um nome de usuário)
    db_manager.connect('')

    # Cria as tabelas se elas ainda não existirem
    connection.criarTabela("tb_usuarios", connection.tb_usuarios_sql)
    connection.criarTabela("tb_ordens_servicos", connection.tb_ordens_servicos_sql)
    connection.criarTabela("tb_servicos_vlr", connection.tb_servicos_vlr_sql)
    connection.criarTabela("tb_cliente", connection.tb_cliente_sql)

    # Cria uma instância da interface gráfica de login (LoginGUI) passando o DatabaseManager
    login_gui = LoginGUI(db_manager)

    # Inicia o loop principal da interface gráfica (mainloop) para interagir com o usuário
    login_gui.tela_login.mainloop()

    # Após o término da interface gráfica (quando o usuário fecha a janela de login), fecha a conexão com o banco de dados
    db_manager.close()

if __name__ == "__main__":
    main()
