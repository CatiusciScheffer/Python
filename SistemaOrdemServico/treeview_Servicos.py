import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END
from tkcalendar import DateEntry
from user import UserManager
from manipulacaoOrdemServico import ManipularOrdemServicos
from datetime import datetime


tlServicos = Tk()
tlServicos.title('Lista Serviços Cadastrados')
tlServicos.geometry("837x577")
tlServicos.configure(bg="#ffffff")
                
canvas = Canvas(
    tlServicos,
    bg = "#ffffff",
    height = 577,
    width = 837,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)
        
background_img_tlCadServ = PhotoImage(file =f"img_tlCadServ_backgroundCadServ.png")
background_tlCadServ = canvas.create_image(
    418.5, 288.5,
    image=background_img_tlCadServ)

img0 = PhotoImage(file ="./img/img_tlCadServ_btnModify.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    #command = btn_clicked,
    relief = "flat")
b0.place(
    x = 217, y = 115,
    width = 90,
    height = 30)

img1 = PhotoImage(file = "./img/img_tlCadServ_btnInsert.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    #command = btn_clicked,
     relief = "flat")

b1.place(
    x = 696, y = 115,
    width = 115,
    height = 30)

img2 = PhotoImage(file = "./img/img_tlCadServ_btnDelete.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    #command = btn_clicked,
    relief = "flat")

b2.place(
    x = 545, y = 115,
    width = 90,
    height = 30)

img3 = PhotoImage(file = "./img/img_tlCadServ_btnPrint.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    #command = btn_clicked,
    relief = "flat")

b3.place(
    x = 381, y = 115,
    width = 90,
    height = 30)

entry0_img = PhotoImage(file = "./img/img_tlCadServ_inputCodServ.png")
entry0_bg = canvas.create_image(
    113.0, 85.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#d9d9d9",
            highlightthickness = 0)

entry0.place(
        x = 85.0, y = 70,
    width = 56.0,
    height = 28)

    #     entry1_img = PhotoImage(file = "./img/img_tlCadServ_inputVlrUnit.png")
    #     entry1_bg = canvas.create_image(
    #         763.5, 85.0,
    #         image = entry1_img)

    #     self.entry1 = Entry(
    #         bd = 0,
    #         bg = "#d9d9d9",
    #         highlightthickness = 0)

    #     self.entry1.place(
    #         x = 719.0, y = 70,
    #         width = 89.0,
    #         height = 28)

    #     entry2_img = PhotoImage(file = "./img/img_tlCadServ_inputTipoServ.png")
    #     entry2_bg = canvas.create_image(
    #         426.0, 85.0,
    #         image = entry2_img)

    #     self.entry2 = Entry(
    #         bd = 0,
    #         bg = "#d9d9d9",
    #         highlightthickness = 0)

    #     self.entry2.place(
    #         x = 220.0, y = 70,
    #         width = 412.0,
    #         height = 28)

    #     ############### TREEVIEW LISTA SERVIÇOS ###############
    #     def center_aligned_text(tree):
    #         tree.tag_configure('center', anchor='center')

    #     # Função para alinhar o texto à direita nas células da TreeView
    #     def right_aligned_text(tree):
    #         tree.tag_configure('right', anchor='e')
                            
    #     self.treeview_tlServicos = ttk.Treeview(tlServicos)

    #     self.treeview_tlServicos.pack(fill="both", expand=True)

    #     self.treeview_tlServicos["columns"] = ("ID","CodServ", "DescrServico", "ValorUnit", )
                
    #     self.treeview_tlServicos.column("#0", width=0, stretch=tk.NO)
    #     self.treeview_tlServicos.column("ID", width=30, anchor="center")
    #     self.treeview_tlServicos.column("CodServ", width=70, anchor="center")
    #     self.treeview_tlServicos.column("DescrServico", width=250, anchor="w")
    #     self.treeview_tlServicos.column("ValorUnit", width=70, anchor="e")

    #     self.treeview_tlServicos.heading("#0", text="", anchor="w")
    #     self.treeview_tlServicos.heading("ID", text="ID", anchor="center")
    #     self.treeview_tlServicos.heading("CodServ", text="Cód.Serv.", anchor="center")
    #     self.treeview_tlServicos.heading("DescrServico", text="Descrição Serviço", anchor="center")
    #     self.treeview_tlServicos.heading("ValorUnit", text="Valor Unit.", anchor="center")

    #     center_aligned_text(self.treeview_tlServicos)
    #     right_aligned_text(self.treeview_tlServicos)

    #     # Posicionar a TreeView
    #     self.treeview_tlServicos.place(x=12, y=177, height=386, width=813)

    #     # Adicionar barra de rolagem vertical
    #     scrollbar_y = ttk.Scrollbar(tlServicos, orient="vertical", command=self.treeview_tlServicos.yview)
    #     self.treeview_tlServicos.configure(yscrollcommand=scrollbar_y.set)
    #     scrollbar_y.place(x=800, y=177, height=386)

    #     # Adicionar barra de rolagem horizontal
    #     scrollbar_x = ttk.Scrollbar(tlServicos, orient="horizontal", command=self.treeview_tlServicos.xview)
    #     self.treeview_tlServicos.configure(xscrollcommand=scrollbar_x.set)
    #     scrollbar_x.place(x=12, y=535, width=813)
    #     ########## FIM TABELA SERVICOS ##########
        
    #     self.mostrarTabelaCadastroServicos()
    #     tlServicos.resizable(False, False)
    
    # ############## FUNÇÕES TELA LOGIN ##############

        
tlServicos.mainloop()