import sqlite3 as lite



def conectarBD():
  conectandoBD = lite.connect('cadastro.db')
  return conectandoBD


#CRIANDO TABELAS
def criarTabelaCadastro():
  
    conectarBD = lite.connect('cadastro.db')
    cur = conectarBD.cursor()

    # Verifica se a tabela já existe
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cadastroNumeros'")
    result = cur.fetchone()

    if result is None:
        # A tabela não existe, então podemos criá-la
        cur.execute("CREATE TABLE cadastroNumeros(id INTEGER PRIMARY KEY AUTOINCREMENT, Telefone TEXT, Mensagem TEXT)")
        conectarBD.commit()
    else:
        # A tabela já existe
        pass

    cur.close()




