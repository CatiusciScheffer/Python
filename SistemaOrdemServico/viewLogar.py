from tkinter import *
import sqlite3
from tkinter import messagebox, END
import hashlib
import viewPrincipal

    
def conectarBD():
    return sqlite3.connect("db_OrdemServicos.db")


def getValuesEntry():
    nomeUsuario = inputLoginUsuario.get().strip().upper()
    senhaUsuario = inputLoginSenha.get().strip().upper()
    return nomeUsuario, senhaUsuario


def converterSenhaHash(senhaUsuarioHash):
  senhaUsuarioHash = hashlib.sha256(senhaUsuarioHash.encode()).hexdigest()

  
def limparCamposTlLogin():
  inputLoginUsuario.delete(0, END)
  inputLoginSenha.delete(0, END)
  

"""def fecharTlLogin():
  telaLogin.destroy()"""

  
def abrirTlPrincipal():
    viewPrincipal.telaPrincipal.mainloop()


def cadastrarUsuarioDb(nomeUsuario, senhaUsuario):
    conexao = conectarBD()
    cursor = conexao.cursor()

    nomeUsuario, senhaUsuario = getValuesEntry()
    
    senhaUsuario = converterSenhaHash(senhaUsuario)

    # Inserir os valores no banco de dados
    cursor.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)", (nomeUsuario, senhaUsuario))
    conexao.commit()

    
    limparCamposTlLogin()
    messagebox.showinfo('Usuário cadastrado cpm sucesso!')
    #fecharTlLogin()
    abrirTlPrincipal()
    
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
        #fecharTlLogin()
        abrirTlPrincipal()
        return True  # Retorna True se o usuário já existir
    else:
        cadastrarUsuarioDb()
        return False  # Retorna False se o usuário não existir   

background = None
background_img = None
img0 = None
img1 = None
inputLoginSenha_img = None
inputLoginUsuario_img = None

def carregarImagens():
    global background_img
    background_img = PhotoImage(file="./background.png")

def criarImagemFundo():
    global background
    background = canvas.create_image(350.0, 200.0, image=background_img)

def criarCanvas():
    global canvas
    canvas = Canvas(
        telaLogin,
        bg="#ffffff",
        height=400,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Aguardar o carregamento da imagem antes de criar a imagem de fundo
    canvas.after(10, criarImagemFundo)

# Restante do código...

telaLogin = Tk()
carregarImagens()
criarCanvas()



background_img = PhotoImage(file="./background.png")
background = canvas.create_image(
    350.0, 200.0,
    image=background_img)

img0 = PhotoImage(file="./img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = verificarUsuarioExistente,
    relief = "flat")

b0.place(
    x = 472, y = 305,
    width = 103,
    height = 32)

img1 = PhotoImage(file="./img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = verificarUsuarioExistente,
    relief = "flat")

b1.place(
    x = 472, y = 261,
    width = 103,
    height = 32)

inputLoginSenha_img = PhotoImage(file="./img_textBox0.png")
inputLoginSenha_bg = canvas.create_image(
    523.5, 164.0,
    image = inputLoginSenha_img)

inputLoginSenha = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

inputLoginSenha.place(
    x = 414.0, y = 148,
    width = 219.0,
    height = 30)

inputLoginUsuario_img = PhotoImage(file="./img_textBox1.png")
inputLoginUsuario_bg = canvas.create_image(
    523.5, 226.0,
    image = inputLoginUsuario_img)

inputLoginUsuario = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

inputLoginUsuario.place(
    x = 414.0, y = 210,
    width = 219.0,
    height = 30)

telaLogin.resizable(False, False)
telaLogin.mainloop()





