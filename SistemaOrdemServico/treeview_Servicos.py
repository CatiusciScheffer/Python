import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END
from tkcalendar import DateEntry
from user import UserManager
from manipulacaoOrdemServico import ManipularOrdemServicos
from datetime import datetime


class ListaServicosGUI:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_manager = UserManager(db_manager)
        self.manipular_ordens = ManipularOrdemServicos(db_manager)

        self.tlServicos = Tk()
        self.tlServicos.title('Lista Serviços Cadastrados')
        self.tlServicos.geometry("800x720")
        self.tlServicos.configure(bg="#ffffff")
                
        canvas = Canvas(
            self.tlServicos,
            bg="#ffffff",
            height=720,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
                )
        canvas.place(x=0, y=0)


        ############### TREEVIEW LISTA SERVIÇOS ###############
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
                            
        # Criar a TreeView
        self.treeview = ttk.Treeview(self.tlServicos)

        self.treeview.pack(fill="both", expand=True)

        # Configurar as colunas com largura e alinhamento
        self.treeview["columns"] = ("ID","CodServ", "DescrServico", "ValorUnit", )
                
        self.treeview.column("#0", width=0, stretch=tk.NO)  # Coluna de ícones (não visível)
        self.treeview.column("ID", width=30, anchor="center")
        self.treeview.column("CodServ", width=70, anchor="center")
        self.treeview.column("DescrServico", width=250, anchor="w")
        self.treeview.column("ValorUnit", width=70, anchor="e")


        # Definir as colunas que serão exibidas
        self.treeview.heading("#0", text="", anchor="w")  # Coluna de ícones (não visível)
        self.treeview.heading("ID", text="ID", anchor="center")
        self.treeview.heading("CodServ", text="Cód.Serv.", anchor="center")
        self.treeview.heading("DescrServico", text="Descrição Serviço", anchor="center")
        self.treeview.heading("ValorUnit", text="Valor Unit.", anchor="center")


        # Aplicar formatação de alinhamento
        center_aligned_text(self.treeview)
        right_aligned_text(self.treeview)

        # Posicionar a TreeView na janela principal usando o place()
        self.treeview.place(x=13, y=13, height=690, width=770)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.tlServicos, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=969, y=323, height=690)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.tlServicos, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=14, y=690, width=770)

        self.mostrarOrdensServicoTelaPrincipal()
    
        self.tlServicos.resizable(False, False)
        self.tlServicos.mainloop()
    
        ######################################################
    def mostrarOrdensServicoTelaPrincipal(self):
            
        cursor = self.db_manager.get_cursor()

        # Adicione a cláusula ORDER BY para ordenar os registros pelo ID em ordem decrescente
        cursor.execute("SELECT * FROM tb_servicos_vlr")
       
        resultados = cursor.fetchall()

        # Iterar sobre os resultados e adicioná-los à Treeview no início (índice "0")
        for resultado in resultados:
            serv_id, serv_codServ, Serv_descServico, serv_vlrUnit = resultado
                
            self.treeview.insert("", "0", values=(serv_id, serv_codServ, Serv_descServico, serv_vlrUnit))
                
                



        