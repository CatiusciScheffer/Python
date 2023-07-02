from tkinter import *
import main

window = Tk()
window.title('Cadastro')

window.geometry("700x400")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=400,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=f"./img/background.png")
background = canvas.create_image(
    386.0, 200.0,
    image=background_img)

inputTelefone_img = PhotoImage(file=f"./img/img_textBox0.png")
inputTelefone_bg = canvas.create_image(
    530.0, 139.5,
    image=inputTelefone_img)

inputTelefone = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

inputTelefone.place(
    x=447.0, y=121,
    width=166.0,
    height=35)

inputMensagem_img = PhotoImage(file=f"./img/img_textBox1.png")
inputMensagem_bg = canvas.create_image(
    530.0, 256.5,
    image=inputMensagem_img)

inputMensagem = Text(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

inputMensagem.place(
    x=447.0, y=205,
    width=166.0,
    height=101)

img0 = PhotoImage(file=f"./img/img0.png")
btnEnviar = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=main.btn_clicked,
    relief="flat")

btnEnviar.place(
    x=481, y=337,
    width=97,
    height=28)

window.resizable(False, False)
window.mainloop()
