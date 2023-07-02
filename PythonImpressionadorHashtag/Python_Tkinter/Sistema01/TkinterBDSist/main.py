from tkinter import END
import connection

conectarBD = connection.conectarBD()

criarTabela = connection.criarTabelaCadastro()

def btn_clicked():
    
    # Obter os valores do campo de entrada e do objeto Text
    telefone = view.inputTelefone.get()
    mensagem = view.inputMensagem.get("1.0", END)
    
    # Conecta-se ao banco de dados
    conectarBD
    
    # Cria um cursor para executar comandos SQL
    cursor = conectarBD.cursor()
    
    # Define a instrução SQL para inserir os dados
    sql = "INSERT INTO cadastroNumeros(Telefone, Mensagem) VALUES (?, ?)"
    
    # Executa o comando SQL passando os valores a serem inseridos
    cursor.execute(sql, (telefone, mensagem))
    
    # Salva as alterações no banco de dados
    conectarBD.commit()
    
    # Limpa os campos telefone e mensagem
    view.inputTelefone.delete(0, END)
    view.inputMensagem.delete("1.0", END)
    
    # Fecha a conexão com o banco de dados
    conectarBD.close()


import view
