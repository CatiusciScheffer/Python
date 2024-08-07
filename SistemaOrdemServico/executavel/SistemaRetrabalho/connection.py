import sqlite3 as lite

def conectarBD():
    """
    Cria uma conexão com o banco de dados 'db_OrdemServicos.db'.

    Returns:
        lite.Connection: Objeto de conexão com o banco de dados.
    """
    conexao = lite.connect('db_OrdemServicos.db')
    return conexao

def criarTabela(tb_nome, tb_sql):
    """
    Cria uma tabela no banco de dados se ela ainda não existir.

    Args:
        tb_nome (str): Nome da tabela a ser criada.
        tb_sql (str): Comando SQL para criar a tabela.

    Returns:
        None

    Example:
        criarTabela("tb_usuarios", tb_usuarios_sql)
    """
    conexao = lite.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()
    
    # Verificar se a tabela existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tb_nome,))
    result = cursor.fetchone()
    
    if result is None:
        # Se a tabela não existe, crie
        cursor.execute(tb_sql)
        conexao.commit()
        print(f"Tabela {tb_nome} criada com sucesso.")
    else:
        # Como a tabela já existe, não é necessário fazer nada
        print(f"Tabela {tb_nome} já existe.")

#@@@@@@@@@@@@@ Comandos SQL para criar as tabelas @@@@@@@@@@@@@#

# Criar tabela tb_usuario
tb_usuarios_sql = """
CREATE TABLE IF NOT EXISTS tb_usuarios(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nomeUsuario TEXT, 
  senhaUsuario TEXT
  );
  """
criarTabela("tb_usuarios", tb_usuarios_sql)

# Criar tabela tb_ordens_servicos
tb_ordens_servicos_sql = """
CREATE TABLE IF NOT EXISTS tb_ordens_servicos (
    os_id INTEGER PRIMARY KEY AUTOINCREMENT,
    os_dtServico DATE,
    os_codCliente INTEGER NOT NULL,
    os_cliente TEXT NOT NULL,
    os_codServico INTEGER NOT NULL,
    os_descServico TEXT NOT NULL,
    os_qtd INT NOT NULL,
    os_vlrUnit REAL NOT NULL,
    os_total REAL NOT NULL,
    os_descrComplementar TEXT,
    os_faturado TEXT DEFAULT 'NÃO',
    os_dtFaturamento DATE,
    os_usuario TEXT,
    FOREIGN KEY (os_codCliente) REFERENCES tb_cliente(cli_codCliente),
    FOREIGN KEY (os_codServico) REFERENCES tb_servicos_vlr(serv_codServ)
);
"""

criarTabela("tb_ordens_servicos", tb_ordens_servicos_sql)

# Criar tabela tb_servicos_vlr
tb_servicos_vlr_sql = """
CREATE TABLE IF NOT EXISTS tb_servicos_vlr (
    serv_id INTEGER PRIMARY KEY AUTOINCREMENT,
    serv_codServ INTEGER NOT NULL,
    serv_descrServico TEXT NOT NULL,
    serv_vlrUnit REAL NOT NULL DEFAULT 0.0
);
"""

criarTabela("tb_servicos_vlr", tb_servicos_vlr_sql)

# Criar tabela tb_cliente
tb_cliente_sql = """
CREATE TABLE IF NOT EXISTS tb_cliente (
    cli_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cli_codCliente INTEGER NOT NULL,
    cli_nomeCliente TEXT NOT NULL,
    cli_qtdNFisenta INTEGER NOT NULL DEFAULT 0
);
"""

criarTabela("tb_cliente", tb_cliente_sql)

