import sqlite3
from tkinter import Entry, END
import hashlib
import subprocess
import viewLogin

# Conectar ao banco de dados
def conectarBD():
    return sqlite3.connect("db_OrdemServicos.db")


def getValuesEntry():
    nomeUsuario = viewLogin.inputLoginUsuario.get().strip().upper()
    senhaUsuario = viewLogin.inputLoginSenha.get().strip().upper()
        
    return nomeUsuario, senhaUsuario



# Verificar se usuário já está cadastrado (True ou False)
def verificarUsuarioExistente():
    conexao = conectarBD()
    cursor = conexao.cursor()
    
    nomeUsuario, senhaUsuario = getValuesEntry()

    # Executar a consulta para verificar se os valores já existem
    cursor.execute("SELECT * FROM tb_usuarios WHERE nomeUsuario=? AND senhaUsuario=?", (nomeUsuario, senhaUsuario))
    result = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    conexao.close()

    # Verificar o resultado da consulta
    if result is not None:
        print("Usuário já existe no banco de dados.")
        return True  # Retorna True se o usuário já existir
    else:
        print("Usuário não existe no banco de dados.")
        return False  # Retorna False se o usuário não existir


# Cadastrar o usuário no banco de dados
def cadastrarUsuarioDb(nomeUsuario, senhaUsuario):
    conexao = conectarBD()
    cursor = conexao.cursor()

    nomeUsuario, senhaUsuario = getValuesEntry()
    
    # Gerar o hash da senha
    senhaUsuario = hashlib.sha256(senhaUsuario.encode()).hexdigest()

    # Inserir os valores no banco de dados
    cursor.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)", (nomeUsuario, senhaUsuario))
    conexao.commit()

    # Limpar os campos
    viewLogin.inputLoginUsuario.delete(0, END)
    viewLogin.inputLoginSenha.delete(0, END)

    print(f'Usuário {nomeUsuario} cadastrado com sucesso!')
    

    
        

