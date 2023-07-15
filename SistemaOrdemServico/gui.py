from tkinter import Tk, Button, Entry, PhotoImage, Canvas
from tkinter import messagebox, END
from user import UserManager

class LoginGUI:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_manager = UserManager(db_manager)

        self.tela_login = Tk()
        self.tela_login.title('Sistema Ordens de Serviços')
        self.tela_login.geometry("700x400")
        self.tela_login.configure(bg="#ffffff")

        canvas = Canvas(
            self.tela_login,
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

        imgBtnEntrar = PhotoImage(file="./img/imgBtnEntrar.png")
        BtnEntrar = Button(
            image = imgBtnEntrar,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.verificar_usuario_existente,
            relief = "flat")

        BtnEntrar.place(
            x = 472, y = 261,
            width = 103,
            height = 32)

        input_login_usuario_img = PhotoImage(file="./img/img_textBox0.png")
        input_login_usuario_bg = canvas.create_image(
            523.5, 164.0,
            image = input_login_usuario_img)

        self.input_login_usuario = Entry(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_login_usuario.place(
            x = 414.0, y = 148,
            width = 219.0,
            height = 30)

        input_login_senha_img = PhotoImage(file="./img/img_textBox1.png")
        input_login_senha_bg = canvas.create_image(
            523.5, 226.0,
            image = input_login_senha_img)

        self.input_login_senha = Entry(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_login_senha.place(
            x = 414.0, y = 210,
            width = 219.0,
            height = 30)

        self.tela_login.resizable(False, False)
        self.tela_login.mainloop()


    def verificar_usuario_existente(self):
        username = self.input_login_usuario.get().strip().upper()
        password = self.input_login_senha.get().strip().upper()

        if self.user_manager.authenticate_user(username, password):
            self.fechar_tl_login()
            self.abrir_tl_principal()
            print(f'usuário já existe autenitic')
            pass
        else:
            self.user_manager.register_user(username, password)
            self.mostrar_alerta("Cadastro de Usuário", f"Usuário(a) {username} cadastrado com sucesso!")
            self.fechar_tl_login()

    def fechar_tl_login(self):
        self.tela_login.destroy()

    def abrir_tl_principal(self):
        telaPrincipal = Tk()
        telaPrincipal.title('Sistema Ordens de Serviços')
        telaPrincipal.geometry("900x600")
        telaPrincipal.resizable(False, False)
        telaPrincipal.mainloop()

    def mostrar_alerta(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def run(self):
        self.tela_login.mainloop()
