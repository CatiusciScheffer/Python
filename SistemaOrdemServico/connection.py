import sqlite3 as lite


def conectarBD():
  conexao = lite.connect('db_OrdemServicos.db')
  return conexao


#CRIANDO TABELA CADASTRO LOGIN DOS USUÁRIOS
def criarTbCadastroUsuario():
  conexao = lite.connect('db_OrdemServicos.db')
  cursor = conexao.cursor()
  
  #Verfificar se a tb existe
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tb_usuarios'")
  result = cursor.fetchone()
  
  if result is None:
    #se a tabelanão existe, crie
    cursor.execute("CREATE TABLE tb_usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT,nomeUsuario TEXT, senhaUsuario TEXT)")
    conexao.commit()
  else:
    #como a tabela já existe pause
    pass
  


  

criarTbCadastroUsuario()