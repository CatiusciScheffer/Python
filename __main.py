import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox
import viewLogin
import viewPrincipal

# Conectar ao banco de dados
def conectarBD():
    return sqlite3.connect("db_OrdemServicos.db")

# Verificar se usuário já está cadastrado (True ou False)
def verificarUsuarioExistente(nomeUsuario, senhaUsuario):
    conexao = conectarBD()
    cursor = conexao.cursor()

    # Gerar o hash da senha
    senhaHash = hashlib.sha256(senhaUsuario.encode()).hexdigest()

    # Executar a consulta para verificar se os valores já existem
    cursor.execute("SELECT * FROM tb_usuarios WHERE nomeUsuario=? AND senhaUsuario=?", (nomeUsuario, senhaHash))
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

    # Gerar o hash da senha
    senhaHash = hashlib.sha256(senhaUsuario.encode()).hexdigest()

    # Inserir os valores no banco de dados
    cursor.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)", (nomeUsuario, senhaHash))
    conexao.commit()

    # Limpar os campos
    print(f'Usuário {nomeUsuario} cadastrado com sucesso!')

    # Chamar a função para exibir a tela principal
    viewPrincipal.exibirTelaPrincipal()

def realizarLogin(nomeUsuario, senhaUsuario):
    if verificarUsuarioExistente(nomeUsuario, senhaUsuario):
        # Fechar a tela de login
        viewLogin.fecharTelaLogin()
        
        # Chamar a função para exibir a tela principal
        viewPrincipal.exibirTelaPrincipal()
    else:
        messagebox.showerror("Erro", "Nome de usuário ou senha inválidos.")

def iniciarSistema():
    # Chamar a função para exibir a tela de login
    viewLogin.exibirTelaLogin(realizarLogin)

"""if __name__ == '__main__':
    iniciarSistema()"""
