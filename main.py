import sqlite3
from tkinter import messagebox, END, Canvas
import hashlib
import viewLogin
import viewPrincipal


# Conectar ao banco de dados
def conectarBD():
    return sqlite3.connect("db_OrdemServicos.db")


def getValuesEntry():
    nomeUsuario = viewLogin.inputLoginUsuario.get().strip().upper()
    senhaUsuario = viewLogin.inputLoginSenha.get().strip().upper()
    return nomeUsuario, senhaUsuario


def converterSenhaHash(senhaUsuarioHash):
  senhaUsuarioHash = hashlib.sha256(senhaUsuarioHash.encode()).hexdigest()

  
def limparCamposTlLogin():
  viewLogin.inputLoginUsuario.delete(0, END)
  viewLogin.inputLoginSenha.delete(0, END)
  

def fecharTlLogin():
  viewLogin.telaLogin.destroy()
  
def abrirTlPrincipal():
    viewPrincipal.telaPrincipal.mainloop()


def cadastrarUsuarioDb(nomeUsuario, senhaUsuario):
    conexao = conectarBD()
    cursor = conexao.cursor()

    nomeUsuario, senhaUsuario = getValuesEntry()
    
    converterSenhaHash(senhaUsuario)

    # Inserir os valores no banco de dados
    cursor.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)", (nomeUsuario, senhaUsuario))
    conexao.commit()

    limparCamposTlLogin()
    messagebox.showinfo('Usuário cadastrado cpm sucesso!')
    fecharTlLogin()
    viewPrincipal.telaPrincipal.mainloop()
    
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
        fecharTlLogin()
        viewPrincipal.telaPrincipal.mainloop()
        return True  # Retorna True se o usuário já existir
    else:
        cadastrarUsuarioDb()
        return False  # Retorna False se o usuário não existir    