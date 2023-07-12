from tkinter import *
import sqlite3
from tkinter import messagebox, END
import hashlib

    
def conectarBD():
    return sqlite3.connect("db_OrdemServicos.db")


def getValuesEntry():
    nomeUsuario = inputLoginUsuario.get().strip().upper()
    senhaUsuario = inputLoginSenha.get().strip().upper()
    return nomeUsuario, senhaUsuario


def converterSenhaHash(senhaUsuarioHash):
  senhaUsuarioHash = hashlib.sha256(senhaUsuarioHash.encode()).hexdigest()
  return senhaUsuarioHash
  
def limparCamposTlLogin():
  inputLoginUsuario.delete(0, END)
  inputLoginSenha.delete(0, END)
  

def fecharTlLogin():
   telaLogin.destroy()

  
def abrirTlPrincipal():
    telaPrincipal = Tk()
    telaPrincipal.title('Sistema Ordens de Serviços')
    telaPrincipal.geometry("900x600")
    telaPrincipal.resizable(False, False)
    telaPrincipal.mainloop()

def entrarNoSistema():
    fecharTlLogin()
    abrirTlPrincipal()

def cadastrarUsuarioDb():
    conexao = conectarBD()
    cursor = conexao.cursor()

    nomeUsuario, senhaUsuario = getValuesEntry()
        
    senhaUsuario = converterSenhaHash(senhaUsuario)

    # Inserir os valores no banco de dados
    cursor.execute("INSERT INTO tb_usuarios(nomeUsuario, senhaUsuario) VALUES (?, ?)", (nomeUsuario, senhaUsuario))
    conexao.commit()

    
    limparCamposTlLogin()
    messagebox.showinfo('Cadastro de Usuário',f'Usuário(a) {nomeUsuario} cadastrado com sucesso!')
    fecharTlLogin()
    abrirTlPrincipal()
    
    
def verificarUsuarioExistente():
    conexao = conectarBD()
    cursor = conexao.cursor()
    
    nomeUsuario, senhaUsuario = getValuesEntry()
        
    # Executar a consulta para verificar se os valores já existem
    cursor.execute("SELECT nomeUsuario FROM tb_usuarios WHERE nomeUsuario=?", (nomeUsuario,))
    result = cursor.fetchone()
    print(result)

    # Fechar a conexão com o banco de dados
    cursor.close()
    conexao.close()

    # Verificar o resultado da consulta
    if result is not None:
        fecharTlLogin()
        abrirTlPrincipal()
        return True  # Retorna True se o usuário já existir
    else:
        cadastrarUsuarioDb()
        return False  # Retorna False se o usuário não existir   


telaLogin = Tk()
telaLogin.title('Sistema Ordens de Serviços')
telaLogin.geometry("700x400")
telaLogin.configure(bg="#ffffff")


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


background_img = PhotoImage(file="./img/imgBgLogin.png")
background = canvas.create_image(
    350.0, 200.0,
    image=background_img)

imgBtnCadastrar = PhotoImage(file="./img/imgBtnCadastrar.png")
BtnCadastrar = Button(
    image = imgBtnCadastrar,
    borderwidth = 0,
    highlightthickness = 0,
    command = verificarUsuarioExistente,
    relief = "flat")

BtnCadastrar.place(
    x = 472, y = 305,
    width = 103,
    height = 32)

imgBtnEntrar = PhotoImage(file="./img/imgBtnEntrar.png")
BtnEntrar = Button(
    image = imgBtnEntrar,
    borderwidth = 0,
    highlightthickness = 0,
    command = entrarNoSistema,
    relief = "flat")

BtnEntrar.place(
    x = 472, y = 261,
    width = 103,
    height = 32)

inputLoginUsuario_img = PhotoImage(file="./img/img_textBox0.png")
inputLoginUsuario_bg = canvas.create_image(
    523.5, 164.0,
    image = inputLoginUsuario_img)

inputLoginUsuario = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

inputLoginUsuario.place(
    x = 414.0, y = 148,
    width = 219.0,
    height = 30)

inputLoginSenha_img = PhotoImage(file="./img/img_textBox1.png")
inputLoginSenha_bg = canvas.create_image(
    523.5, 226.0,
    image = inputLoginSenha_img)

inputLoginSenha = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

inputLoginSenha.place(
    x = 414.0, y = 210,
    width = 219.0,
    height = 30)

telaLogin.resizable(False, False)
telaLogin.mainloop()





