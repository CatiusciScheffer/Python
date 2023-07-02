from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.title('Entrar no Sistema')

window.geometry("700x400")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 400,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"./img/imgBgLogin.png")
background = canvas.create_image(
    350.0, 200.0,
    image=background_img)

img0 = PhotoImage(file = f"./img/imgBtnCadastrar.png")
btnLoginCadastrar = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnLoginCadastrar.place(
    x = 472, y = 305,
    width = 103,
    height = 32)

img1 = PhotoImage(file = f"./img/imgBtnEntrar.png")
btnLoginEntrar = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnLoginEntrar.place(
    x = 472, y = 261,
    width = 103,
    height = 32)

inputLoginUsuario_img = PhotoImage(file = f"./img/imgCxTextLogin.png")
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

inputLoginSenha_img = PhotoImage(file = f"./img/imgCxTextLogin.png")
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

window.resizable(False, False)
window.mainloop()
