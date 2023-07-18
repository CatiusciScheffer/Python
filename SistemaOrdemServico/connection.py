import sqlite3 as lite


def conectarBD():
  conexao = lite.connect('db_OrdemServicos.db')
  return conexao


#CRIANDO TABELA CADASTRO LOGIN DOS USUÁRIOS
# def criarTbCadastroUsuario():
#   conexao = lite.connect('db_OrdemServicos.db')
#   cursor = conexao.cursor()
  
#   #Verfificar se a tb existe
#   cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tb_usuarios'")
#   result = cursor.fetchone()
  
#   if result is None:
#     #se a tabelanão existe, crie
#     cursor.execute("CREATE TABLE tb_usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT,nomeUsuario TEXT, senhaUsuario TEXT)")
#     conexao.commit()
#   else:
#     #como a tabela já existe pause
#     pass
#criarTbCadastroUsuario()

import sqlite3

def criarTabela(tb_nome, tb_sql):
    conexao = sqlite3.connect('db_OrdemServicos.db')
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
    os_dtServico DATE NOT NULL DEFAULT (DATE('now', 'localtime', '-30 day')),
    os_codCliente INTEGER NOT NULL,
    os_cliente TEXT NOT NULL,
    os_observacao TEXT NOT NULL,
    os_codServico INTEGER NOT NULL,
    os_descServico TEXT,
    os_qtd REAL NOT NULL DEFAULT 0,
    os_vlrUnit REAL,
    os_total REAL,
    os_usuario TEXT,
    FOREIGN KEY (os_codCliente) REFERENCES tb_cliente(cli_codCliente),
    FOREIGN KEY (os_codServico) REFERENCES tb_servicos_vlr(serv_codServ)
);
"""

criarTabela("tb_ordens_servicos", tb_ordens_servicos_sql)

# Criar tabela tb_servicos_vlr
tb_servicos_vlr_sql = """
CREATE TABLE IF NOT EXISTS tb_ordens_servicos (
    serv_id INTEGER PRIMARY KEY AUTOINCREMENT,
    serv_codServ INTEGER NOT NULL,
    serv_descrServico TEXT NOT NULL,
    serv_vlrUnit REAL NOT NULL
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

