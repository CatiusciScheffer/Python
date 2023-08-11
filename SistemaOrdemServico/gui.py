import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END, Toplevel
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from user import UserManager
from manipulacaoOrdemServico import ManipularOrdemServicos
from relatoriosPDF import ManipularCriacaodeRelatorios



class LoginGUI:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_manager = UserManager(db_manager)
        self.manipular_ordens = ManipularOrdemServicos(db_manager)
        self.manipular_relatorios = ManipularCriacaodeRelatorios(db_manager)

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

        background_img = PhotoImage(file="./img/img_tlLogin_backgroundLogin.png")
        background = canvas.create_image(
            350.0, 200.0,
            image=background_img)
        
        input_login_usuario_img = PhotoImage(file="./img/img_tlLogin_inputUsuario.png")
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

        input_login_senha_img = PhotoImage(file="./img/img_tlLogin_inputSenhaUsuario.png")
        input_login_senha_bg = canvas.create_image(
            523.5, 226.0,
            image = input_login_senha_img)

        self.input_login_senha = Entry(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0,
            show="☺")

        self.input_login_senha.place(
            x = 414.0, y = 210,
            width = 219.0,
            height = 30)
        
        imgBtnEntrar = PhotoImage(file="./img/img_tlLogin_BtnEntrar.png")
        BtnEntrar = Button(
            image = imgBtnEntrar,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.fechar_tl_login,
            relief = "flat")

        BtnEntrar.place(
            x = 472, y = 261,
            width = 103,
            height = 32)
        
        #Faz entrar sem clique no botão enter, apenas clicando
        BtnEntrar.bind("<Return>", self.fechar_tl_login)

        self.tela_login.resizable(False, False)
        self.tela_login.mainloop()
        
    def fechar_tl_login(self, event=None):
        self.verificar_usuario_existente()
        self.abrir_tl_principal()
        #self.tela_login.destroy()
        
        

    def abrir_tl_principal(self):
        
        self.telaPrincipal = Tk()        
        self.telaPrincipal.title(f"Cadasto de Serviços")

        self.telaPrincipal.geometry("1000x720")
        self.telaPrincipal.configure(bg = "#ffffff")
        
        canvas = Canvas(
            self.telaPrincipal,
            bg = "#ffffff",
            height = 720,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        img_tlPrincipal_background = PhotoImage(file="./img/img_tlPrincipal_background.png")
        background_tlPrincipal = canvas.create_image(
            500.0, 360.0,
            image=img_tlPrincipal_background)

        input_DataOS_img = PhotoImage(file="./img/img_tlPrincipal_inputData.png")
        input_DataOS_bg = canvas.create_image(
            120.0, 84.0,
            image = input_DataOS_img)
        
        # self.input_DataOS = tk.Label(telaPrincipal, text=f"{datetime.now()}")
        # self.input_DataOS.pack()
        
        self.input_DataOS = DateEntry(
            bd=0,
            bg="#d9d9d9",
            highlightthickness=0,
            date_pattern='dd/mm/yyyy')  # Defina o formato da data desejado

        self.input_DataOS.place(
            x=69.0, y=73,
            width=102.0,
            height=22)
        
        input_CodCliente_img = PhotoImage(file="./img/img_tlPrincipal_inputCodCliente.png")
        input_CodCliente_bg = canvas.create_image(
            319.0, 84.0,
            image = input_CodCliente_img)

        self.input_CodCliente = Entry(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_CodCliente.place(
            x = 277.0, y = 71,
            width = 84.0,
            height = 24)

        # Associa a função atualizarValore aos eventos <FocusOut> e <Tab> do campo input_CodServ
        self.input_CodCliente.bind("<FocusOut>", self.preencheCliente)
        self.input_CodCliente.bind("<Tab>", self.preencheCliente)
        
        input_Cliente_img = PhotoImage(file="./img/img_tlPrincipal_inputCliente.png")
        input_Cliente_bg = canvas.create_image(
            595.5, 84.0,
            image = input_Cliente_img)
        
        self.input_Cliente = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0,
            state="readonly")

        self.input_Cliente.place(
            x = 435.0, y = 73,
            width = 321.0,
            height = 22)
        
        input_CodServ_img = PhotoImage(file="./img/img_tlPrincipal_inputCodServ.png")
        input_CodServ_bg = canvas.create_image(
            168.0, 119.0,
            image = input_CodServ_img)

        self.input_CodServ = Entry(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_CodServ.place(
            x = 115.0, y = 106,
            width = 106.0,
            height = 24)
        
        # Associa a função atualizarValore aos eventos <FocusOut> e <Tab> do campo input_CodServ
        self.input_CodServ.bind("<FocusOut>", self.preencheDescrServicoEvalorUnitario)
        self.input_CodServ.bind("<Tab>", self.preencheDescrServicoEvalorUnitario)

        input_DescricaoServ_img = PhotoImage(file="./img/img_tlPrincipal_inputTipoServ.png")
        input_DescricaoServ_bg = canvas.create_image(
            550.0, 119.0,
            image = input_DescricaoServ_img)

        self.input_DescricaoServ = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0,
            state='readonly'
        )
        
        self.input_DescricaoServ.place(
            x = 344.0, y = 108,
            width = 412.0,
            height = 22)
        
        
        input_Quantidade_img = PhotoImage(file="./img/img_tlPrincipal_inputQuantidade.png")
        input_Quantidade_bg = canvas.create_image(
            151.0, 155.0,
            image = input_Quantidade_img)

        self.input_Quantidade = Entry(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_Quantidade.place(
            x = 110.0, y = 142,
            width = 82.0,
            height = 24)
        
        
        input_VlrUnitario_img = PhotoImage(file="./img/img_tlPrincipal_inputVltUnitario.png")
        input_VlrUnitario_bg = canvas.create_image(
            348.5, 155.0,
            image = input_VlrUnitario_img)

        self.input_VlrUnitario = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0)

        self.input_VlrUnitario.place(
            x = 304.0, y = 142,
            width = 89.0,
            height = 24)
        
        # Associa a função atualizarValore aos eventos <FocusOut> e <Tab> do campo input_VlrTotal
        self.input_VlrUnitario.bind("<FocusOut>", self.preencherValorTotal)
        self.input_VlrUnitario.bind("<Tab>", self.preencherValorTotal)
        
        input_VlrTotal_img = PhotoImage(file="./img/img_tlPrincipal_inputVltTotal.png")
        input_VlrTotal_bg = canvas.create_image(
            534.5, 155.0,
            image = input_VlrTotal_img)

        self.input_VlrTotal = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0,
            state='readonly')

        self.input_VlrTotal.place(
            x = 490.0, y = 144,
            width = 90.0,
            height = 22)

        input_Faturado_img = PhotoImage(file="./img/img_tlPrincipal_inputFaturado.png")
        input_Faturado_bg = canvas.create_image(711.5, 155.0, image=input_Faturado_img)

        self.input_Faturado = Entry(
            bd=0,
            bg="#8a8a8a",
            highlightthickness=0,
            state="readonly"
        )

        self.input_Faturado.place(
            x=667.0, y=144,
            width=90.0,
            height=22
        )
        
        input_DescrCompl_img = PhotoImage(file="./img/img_tlPrincipal_textDescricaoServ.png")
        input_DescrServ_bg = canvas.create_image(
            291.0, 244.5,
            image = input_DescrCompl_img)

        self.input_DescrCompl = tk.Text(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_DescrCompl.place(
            x = 30.0, y = 196,
            width = 522.0,
            height = 95)

        ########### CRIANDO BOTÕES TELA PRINCIPAL ###########
        
        #### BOTÃO MODIFICAR ####
        img_tlPrincipal_btnModificar = PhotoImage(file="./img/img_tlPrincipal_btnModify.png")
        btnModifyOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnModificar,
            borderwidth = 0,
            highlightthickness = 0,
            #command = btn_clicked,
            relief = "flat")

        btnModifyOS_tlPrincipal.place(
            x = 656, y = 253,
            width = 103,
            height = 40)

        #### BOTÃO DELETAR ####
        img_tlPrincipal_btnDelete = PhotoImage(file="./img/img_tlPrincipal_btnDelete.png")
        btnDeleteOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnDelete,
            borderwidth = 0,
            highlightthickness = 0,
            #command = btn_clicked,
            relief = "flat")

        btnDeleteOS_tlPrincipal.place(
            x = 656, y = 196,
            width = 103,
            height = 40)

        #### BOTÃO INSERT ####
        img_tlPrincipal_btnInsert = PhotoImage(file="./img/img_tlPrincipal_btnInsert.png")
        btnInsertOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnInsert,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.atualizar_VizualizacaoTelaPrincipal,
            relief = "flat")

        btnInsertOS_tlPrincipal.place(
            x = 566, y = 196,
            width = 81,
            height = 97)

        #### BOTÃO CADASTRAR CLIENTE ####
        img_tlPrincipal_btnCadCliente = PhotoImage(file="./img/img_tlPrincipal_btnCadCliente.png")
        btnCadCliente_tlPrincipal = Button(
            image = img_tlPrincipal_btnCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            #command = btn_clicked,
            relief = "flat")

        btnCadCliente_tlPrincipal.place(
            x = 809, y = 71,
            width = 138,
            height = 60)

        #### BOTÃO CADASTRAR SERVIÇO ####
        img_tlPrincipal_btnCadServico = PhotoImage(file="./img/img_tlPrincipal_btnCadServico.png")
        btnCadServ_tlPrincipal = Button(
            image = img_tlPrincipal_btnCadServico,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.abrirTelaCadServ,
            relief = "flat")

        btnCadServ_tlPrincipal.place(
            x = 809, y = 145,
            width = 138,
            height = 60)

        #### BOTÃO FINANCEIRO ####
        img_tlPrincipal_btnFinanceiro = PhotoImage(file="./img/img_tlPrincipal_btnFinanceiro.png")
        btnFinanceiro_tlPrincipal = Button(
            image = img_tlPrincipal_btnFinanceiro,
            borderwidth = 0,
            highlightthickness = 0,
            #command ='',
            relief = "flat")

        btnFinanceiro_tlPrincipal.place(
            x = 809, y = 220,
            width = 138,
            height = 60)
        
        ############# CRIANDO TREEVIEW ORDEM DE SERVIÇOS #############
              
        # Função para centralizar o texto nas células da TreeView
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
            
        # Criar a TreeView
        self.treeview = ttk.Treeview(self.telaPrincipal)

        self.treeview.pack(fill="both", expand=True)

        # Configurar as colunas com largura e alinhamento
        self.treeview["columns"] = ("ID","Data", "CodCliente", "Cliente", "CodServ", "DescrServico", "QTD", "ValorUnit", "ValorTotal", "DescComplementar", "Faturado")
        
        self.treeview.column("#0", width=0, stretch=tk.NO)  # Coluna de ícones (não visível)
        self.treeview.column("ID", width=50, anchor="center")
        self.treeview.column("Data", width=70, anchor="center")
        self.treeview.column("CodCliente", width=70, anchor="center")
        self.treeview.column("Cliente", width=200, anchor="w")
        self.treeview.column("CodServ", width=70, anchor="center")
        self.treeview.column("DescrServico", width=146, anchor="w")
        self.treeview.column("QTD", width=38, anchor="e")
        self.treeview.column("ValorUnit", width=65, anchor="e")
        self.treeview.column("ValorTotal", width=65, anchor="e")
        self.treeview.column("DescComplementar", width=200, anchor="w")
        self.treeview.column("Faturado", width=70, anchor="center")
        #self.treeview.column("Resp", width=100, anchor="center")

        # Definir as colunas que serão exibidas
        self.treeview.heading("#0", text="", anchor="w")  # Coluna de ícones (não visível)
        self.treeview.heading("ID", text="ID", anchor="center")
        self.treeview.heading("Data", text="Data", anchor="center")
        self.treeview.heading("CodCliente", text="Cód.Cliente", anchor="center")
        self.treeview.heading("Cliente", text="Cliente", anchor="center")
        self.treeview.heading("CodServ", text="Cód.Serv.", anchor="center")
        self.treeview.heading("DescrServico", text="Descrição Serviço", anchor="center")
        self.treeview.heading("QTD", text="QTD", anchor="center")
        self.treeview.heading("ValorUnit", text="Valor Unit.", anchor="center")
        self.treeview.heading("ValorTotal", text="Valor Total", anchor="center")
        self.treeview.heading("DescComplementar", text="Descrição Complementar", anchor="center")
        self.treeview.heading("Faturado", text="Faturado", anchor="center")
        #self.treeview.heading("Resp", text="Responsável", anchor="center")

        # Aplicar formatação de alinhamento
        center_aligned_text(self.treeview)
        right_aligned_text(self.treeview)

        # Posicionar a TreeView na janela principal usando o place()
        self.treeview.place(x=13, y=322, height=369, width=957)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.telaPrincipal, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=969, y=323, height=367)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.telaPrincipal, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=14, y=690, width=973)
        
        self.mostrarOrdensServico_TelaPrincipal()
        self.resize_columns()    
            
        # Iniciar o loop principal do Tkinter
        self.telaPrincipal.resizable(False, False)
        self.telaPrincipal.mainloop()
    
    def criar_TelaCadServ(self):
        
        self.tlServicos = Toplevel(self.telaPrincipal)
        self.tlServicos.title('Lista Serviços Cadastrados')
        self.tlServicos.geometry("837x577")
        self.tlServicos.configure(bg="#ffffff")
                
        canvas = Canvas(
            self.tlServicos,
            bg = "#ffffff",
            height = 577,
            width = 837,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)
        
        background_img_tlCadServ = PhotoImage(file="./img/img_tlCadServ_backgroundCadServ.png")
        background = canvas.create_image(
            417.5, 288.5,
            image=background_img_tlCadServ)

        
        verificaInteger = self.tlServicos.register(self._verificarValor_Inteiro)
        verificaFloat = self.tlServicos.register(self._verificarValor_Float)
        verificaTexto = self.tlServicos.register(self._verificarValor_Texto)
        
        #### BOTÃO MODIFICAR SERVIÇOS ####
        img_btnModify_tlCadServ = PhotoImage(file="./img/img_tlCadServ_btnModify.png")
        btnModify_tlCadServ = Button(
            self.tlServicos,
            image = img_btnModify_tlCadServ,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.habiltarEdicaoItemTreeviewTelaCadServ,
            relief = "flat")

        btnModify_tlCadServ.place(
            x = 492, y = 115,
            width = 90,
            height = 30)
        
        #### BOTÃO INSERIR SERVIÇOS ####
        img_btnInsert_tlCadServ = PhotoImage(file = "./img/img_tlCadServ_btnInsert.png")
        btnInsert_tlCadServ = Button(
            self.tlServicos,
            image = img_btnInsert_tlCadServ,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.inserirServico_CadServ,
            relief = "flat")

        btnInsert_tlCadServ.place(
            x = 390, y = 115,
            width = 90,
            height = 30)

        #### BOTÃO DELETAR SERVIÇOS ####
        self.img_btnDelete_tlCadServ = PhotoImage(file = "./img/img_tlCadServ_btnDelete.png")
        self.btnDelete_tlCadServ = Button(
            self.tlServicos,
            image = self.img_btnDelete_tlCadServ,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.deletarServico_TelaCadServ,
            relief = "flat")

        self.btnDelete_tlCadServ.place(
            x = 594, y = 115,
            width = 90,
            height = 30)
        
        #### BOTÃO IMPRIMIR SERVIÇOS ####
        img_btnPrint_tlCadServ = PhotoImage(file = "./img/img_tlCadServ_btnPrint.png")
        btnPrint_tlCadServ = Button(
            self.tlServicos,
            image = img_btnPrint_tlCadServ,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.gerarRelatorioCadServ,
            relief = "flat")

        btnPrint_tlCadServ.place(
            x = 696, y = 115,
            width = 115,
            height = 30)
        #botões que serão ocultos ao chamar a função de modificação:
        self.botoesParaOcultar_TelaCadServ = [self.btnDelete_tlCadServ, btnInsert_tlCadServ, btnModify_tlCadServ, btnPrint_tlCadServ]
        
        inputCodServ_tlCadServ_img = PhotoImage(file = f"./img/img_tlCadServ_inputCodServ.png")
        inputCodServ_tlCadServ_bg = canvas.create_image(
            113.0, 85.0,
            image = inputCodServ_tlCadServ_img)

        self.inputCodServ_tlCadServ = Entry(
            self.tlServicos,
            bd=0,
            bg="#d9d9d9",
            highlightthickness=0,
            validate="key",
            validatecommand=(verificaInteger, "%P"))

        self.inputCodServ_tlCadServ.place(
            x = 85.0, y = 70,
            width = 56.0,
            height = 28)
        
        inputDescServ_tlCadServ_img = PhotoImage(file = "./img/img_tlCadServ_inputTipoServ.png")
        inputDescServ_tlCadServ_bg = canvas.create_image(
            426.0, 85.0,
            image = inputDescServ_tlCadServ_img)

        self.inputDescServ_tlCadServ = Entry(
            self.tlServicos,
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0,
            validate="key",
            validatecommand=(verificaTexto, "%P"))

        self.inputDescServ_tlCadServ.place(
            x = 220.0, y = 70,
            width = 412.0,
            height = 28)

        inputVlrUnit_tlCadServ_img = PhotoImage(file = "./img/img_tlCadServ_inputVlrUnit.png")
        inputVlrUnit_tlCadServ_bg = canvas.create_image(
            763.5, 85.0,
            image = inputVlrUnit_tlCadServ_img)
        
        
        self.inputVlrUnit_tlCadServ = tk.Entry(
            self.tlServicos,
            bd=0,
            bg="#d9d9d9",
            highlightthickness=0,
            validate="key",
            validatecommand=(verificaFloat, "%P")
        )

        self.inputVlrUnit_tlCadServ.pack()
            
        self.inputVlrUnit_tlCadServ.place(
            x = 719.0, y = 70,
            width = 89.0,
            height = 28)        

        ############### TREEVIEW LISTA SERVIÇOS ###############
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
                            
        self.treeview_tlServicos = ttk.Treeview(self.tlServicos)

        self.treeview_tlServicos.pack(fill="both", expand=True)

        self.treeview_tlServicos["columns"] = ("ID","CodServ", "DescrServico", "ValorUnit", )
                
        self.treeview_tlServicos.column("#0", width=0, stretch=tk.NO)
        self.treeview_tlServicos.column("ID", width=30, anchor="center")
        self.treeview_tlServicos.column("CodServ", width=70, anchor="center")
        self.treeview_tlServicos.column("DescrServico", width=250, anchor="w")
        self.treeview_tlServicos.column("ValorUnit", width=70, anchor="e")

        self.treeview_tlServicos.heading("#0", text="", anchor="w")
        self.treeview_tlServicos.heading("ID", text="ID", anchor="center")
        self.treeview_tlServicos.heading("CodServ", text="Cód.Serv.", anchor="center")
        self.treeview_tlServicos.heading("DescrServico", text="Descrição Serviço", anchor="center")
        self.treeview_tlServicos.heading("ValorUnit", text="Valor Unit.", anchor="center")

        center_aligned_text(self.treeview_tlServicos)
        right_aligned_text(self.treeview_tlServicos)

        # Posicionar a TreeView
        self.treeview_tlServicos.place(x=15, y=180, height=364.5, width=788.5)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.tlServicos, orient="vertical", command=self.treeview_tlServicos.yview)
        self.treeview_tlServicos.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=804, y=181, height=364)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.tlServicos, orient="horizontal", command=self.treeview_tlServicos.xview)
        self.treeview_tlServicos.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=16, y=545, width=805)
        ########## FIM TABELA SERVICOS ##########
        
        self.mostrarTabelaServicos_TelaCadServ()
        self.tlServicos.resizable(False, False)
        self.tlServicos.mainloop()
    
    ############## FUNÇÕES TELA LOGIN ##############
    
    def verificar_usuario_existente(self):
        input_usuario = self.input_login_usuario.get().strip().upper()
        input_senha = self.input_login_senha.get().strip().upper()
        print(f'usuario{input_usuario}, senha{input_senha}')

        if self.user_manager.checkUsernameAndPasswordRegistered(input_usuario, input_senha):
            self.tela_login.destroy()
            #self.abrir_tl_principal()
            self.username = input_usuario
            return self.username  # Retorna o nome do usuário logado
        else:
            self.user_manager.registerNewUser(input_usuario, input_senha)
            self.mostrar_alerta("Cadastro de Usuário", f" ☻ Usuário(a) {input_usuario} cadastrado com sucesso!")
            self.tela_login.destroy()
            #self.abrir_tl_principal()
            self.username = input_usuario
            return self.username  # Retorna o nome do usuário logado
 
    
    ############## FUNÇÕES TELA PRINCIPAL ORDEM DE SERVIÇOS ##############
    def pegandoValoresTelaPrincipalOS(self):
        dtServico = self.input_DataOS.get()
        codCliente = int(self.input_CodCliente.get().strip())
        cliente = self.input_Cliente.get().strip().upper()
        codServico = int(self.input_CodServ.get().strip())
        descrServico = self.input_DescricaoServ.get().strip().upper()
        descComplementar = self.input_DescrCompl.get('1.0', 'end-1c')  # Usar '1.0' e 'end-1c' para er todo o conteúdo
        quantidade = int(self.input_Quantidade.get())
        vlrUnit = float(self.input_VlrUnitario.get())
        total = float(self.input_VlrTotal.get())
        faturado = self.input_Faturado.get()

        os_values = {
            'dtServico': dtServico,
            'codCliente': codCliente,
            'cliente': cliente,
            'codServico': codServico,
            'descServico': descrServico,
            'descComplementar': descComplementar,
            'quantidade': quantidade,
            'vlrUnit': vlrUnit,
            'total': total,
            'os_faturado': faturado
        }
        return os_values

    def _preencherFaturado(self, faturado):
        self.input_Faturado.configure(state="normal")
        self.input_Faturado.delete(0, END)
        self.input_Faturado.insert(0, faturado)
        self.input_Faturado.configure(state="readonly")        
    
    def preencheCliente(self, event):
        if event.keysym == "Tab":

            l_codCliente = self.manipular_ordens.buscarValoresTBCliente()
            
            input_codCliente = int(self.input_CodCliente.get())
            
            for index, cliente in enumerate(l_codCliente):
                
                codCliente = int(cliente[0])
                nomeCliente = str(cliente[1])
                
                if codCliente == input_codCliente:
                    self.input_Cliente.configure(state="normal")
                    self.input_Cliente.delete(0, END)
                    self.input_Cliente.insert(0, nomeCliente)
                    self.input_Cliente.configure(state="readonly")
                    self._preencherFaturado('NÃO')
                    break
                else:
                    pass
    
    def _preencherDescricaoServicos(self, descricao):
        self.input_DescricaoServ.configure(state="normal")
        self.input_DescricaoServ.delete(0, END)
        self.input_DescricaoServ.insert(0, descricao)
        self.input_DescricaoServ.configure(state="readonly")
    
    def _preencherValorUnitario(self, valor_unitario):
        self.input_VlrUnitario.delete(0, END)
        self.input_VlrUnitario.insert(0, valor_unitario)  
        
                    
    def preencheDescrServicoEvalorUnitario(self, event):
        if event.keysym == "Tab":

            l_codServDescrServVlrUnit = self.manipular_ordens.buscarValoresTBServicosValore()
            
            input_codServ = int(self.input_CodServ.get())
            
            for index, servicos in enumerate(l_codServDescrServVlrUnit):
                
                codServ = int(servicos[0])
                descrServ = str(servicos[1])
                valorUnit = float(servicos[2])
                
                if codServ == input_codServ:
                    self._preencherDescricaoServicos(descrServ)
                    self._preencherValorUnitario(valorUnit)
                    break
                else:
                    pass
                
    def preencherValorTotal(self, event):
        
        if event.keysym == "Tab":
            
            quantidade = int(self.input_Quantidade.get())
            vlrUnitario = float(self.input_VlrUnitario.get())
            
            calcularVlrTotal = quantidade * vlrUnitario
            
            self.input_VlrTotal.configure(state="normal")
            self.input_VlrTotal.delete(0, END)
            self.input_VlrTotal.insert(0, calcularVlrTotal)
            self.input_VlrTotal.configure(state="readonly")
            

    def inserir_OrdemServico(self):
        dictInputValoresTelaPrincipal = self.pegandoValoresTelaPrincipalOS()

        dtServico = dictInputValoresTelaPrincipal['dtServico']
        codCliente = dictInputValoresTelaPrincipal['codCliente']
        cliente = dictInputValoresTelaPrincipal['cliente']
        codServico = dictInputValoresTelaPrincipal['codServico']
        descServico = dictInputValoresTelaPrincipal['descServico']
        qtd = dictInputValoresTelaPrincipal['quantidade']
        vlrUnit = dictInputValoresTelaPrincipal['vlrUnit']
        total = dictInputValoresTelaPrincipal['total']
        descrComplementar = dictInputValoresTelaPrincipal['descComplementar']
        faturado = dictInputValoresTelaPrincipal['os_faturado']

        cursor = self.db_manager.get_cursor()

        cursor.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado) VALUES (?, ?, ?, ?, ?, ?, ?, ? ,?, ?)", (dtServico, codCliente, cliente, codServico, descServico, qtd, vlrUnit, total, descrComplementar, faturado))
       
        # Confirmar a transação
        self.db_manager.connection.commit()
        self.resize_columns()
    
        
    def mostrarOrdensServico_TelaPrincipal(self):
        cursor = self.db_manager.get_cursor()

        # Adicione a cláusula ORDER BY para ordenar os registros pelo ID em ordem decrescente
        cursor.execute("SELECT * FROM tb_ordens_servicos ORDER BY os_id ASC")

        resultados = cursor.fetchall()

        # Limpar a Treeview antes de adicionar os novos registros
        self.treeview.delete(*self.treeview.get_children())

        # Iterar sobre os resultados e adicioná-los à Treeview no início (índice "0")
        for resultado in resultados:
            os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_observacao, os_faturado = resultado
            self.treeview.insert("", "0", values=(os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_observacao, os_faturado))

        # Redimensionar as colunas para ajustar o conteúdo
        self.resize_columns()

    def atualizar_VizualizacaoTelaPrincipal(self):
        self.inserir_OrdemServico()
        self.mostrarOrdensServico_TelaPrincipal()
        self.mostrar_alerta('Sucesso', 'Serviço inserido com sucesso!')

    
    ############### FUNÇÕES TELA CADASTRO SERVIÇOS ###############
    def abrirTelaCadServ(self, event=None):
        self.criar_TelaCadServ()   
    
    def _limparTelaCadServ(self):     
        self.inputCodServ_tlCadServ.delete(0, 'end')
        self.inputDescServ_tlCadServ.delete(0, 'end')
        self.inputVlrUnit_tlCadServ.delete(0, 'end')
    
    def fechar_TelaCadServ(self):
        self.tlServicos.destroy()
    
    def inserirServico_CadServ(self):
        
        try:
            codServico = self.inputCodServ_tlCadServ.get().strip()
            descServico = self.inputDescServ_tlCadServ.get().strip().upper()
            vlrUnit = self.inputVlrUnit_tlCadServ.get()
            vlrUnit = vlrUnit.replace(",", ".")
            
            valoresDigitados = [codServico, descServico, vlrUnit]
            
            if not valoresDigitados[0] or not valoresDigitados[1] or not valoresDigitados[2]  :
                    self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                    self._atualizarTelaCadServ()
                    return
            
            self._inserirServicoNoBanco(codServico, descServico, vlrUnit)
            self.mostrar_alerta("Cadastro de Serviço", f"Serviço '{descServico}' cadastrado com sucesso!")
            self._atualizarTelaCadServ()
            return True
        
        except Exception as e:
            self.mostrar_alerta('Erro', f'Cadastro do Serviço não realizado!')
            self._limparTelaCadServ()          
            return False
            
    
    def _inserirServicoNoBanco(self, codServico, descServico, vlrUnit):
        try:
            verificacodServico = self.inputCodServ_tlCadServ.get().strip()
            if verificacodServico is None:
                print(verificacodServico)
                self.db_manager.cursor.execute("INSERT INTO tb_servicos_vlr (serv_codServ, serv_descrServico, serv_vlrUnit) VALUES (?, ?, ?)", (codServico, descServico, vlrUnit))
                self.db_manager.connection.commit()
                return
            
        except Exception as e:
            print("Erro ao inserir serviço:", e)
            return False
    
    
              
    def mostrarTabelaServicos_TelaCadServ(self):
        cursor = self.db_manager.get_cursor()

        cursor.execute("SELECT serv_id, serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr")

        listandoServicos = cursor.fetchall()
        # Limpar a Treeview antes de adicionar os novos registros
        self.treeview_tlServicos.delete(*self.treeview_tlServicos.get_children())

        # Iterar sobre os listandoServicos e adicioná-los à Treeview no início (índice "0")
        for resultado in listandoServicos:
            serv_id, serv_codServ, serv_descrServico, serv_vlrUnit = resultado   
            
            self.treeview_tlServicos.insert("", "end", values=(serv_id, serv_codServ, serv_descrServico, serv_vlrUnit))
    
    def deletarServico_TelaCadServ(self):
        selected_item = self.treeview_tlServicos.selection()
        
        if not selected_item:
            self.mostrar_alerta("Nenhum item selecionado", "Por favor, selecione um item para deletar.")
            return
            
        service_info = self.obter_informacoes_item_selecionado(selected_item)
        
        if self.confirmar_exclusao(service_info['serv_descrServico']):
            if self._deletarServicoDoBanco(service_info['serv_id']):
                self.treeview_tlServicos.delete(selected_item)
                self.mostrar_sucesso(service_info['serv_descrServico'])
            else:
                self.mostrar_erro("Ocorreu um erro ao tentar deletar o serviço.")
        else:
            self.mostrar_alerta("Cancelado", "A exclusão foi cancelada pelo usuário.")
            
        self._atualizarTelaCadServ()

    def obter_informacoes_item_selecionado(self, item):
        values = self.treeview_tlServicos.item(item, 'values')
        serv_id = values[0]
        serv_descrServico = values[2]
        return {'serv_id': serv_id, 'serv_descrServico': serv_descrServico}
        
    def _deletarServicoDoBanco(self, serv_id):
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_servicos_vlr WHERE serv_id = ?", (serv_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao deletar serviço:", e)
            return False

    
    def habiltarEdicaoItemTreeviewTelaCadServ(self): 
        try:   
            itemSelecionado = self.treeview_tlServicos.selection()
            item = self.treeview_tlServicos.item(itemSelecionado, 'values')
            serv_id = item[0]
            serv_codServ = item[1]
            serv_descServico = item[2]
            serv_vlrUnit = item[3]
                      
            
            self.inputCodServ_tlCadServ.delete(0, 'end')
            self.inputCodServ_tlCadServ.insert(0, int(serv_codServ)) 
            
            self.inputDescServ_tlCadServ.delete(0, 'end')
            self.inputDescServ_tlCadServ.insert(0, str(serv_descServico))
            
            self.inputVlrUnit_tlCadServ.delete(0, 'end')
            self.inputVlrUnit_tlCadServ.insert(0, float(serv_vlrUnit))
            
            self._apagarListaBotoes(self.botoesParaOcultar_TelaCadServ)
            self._criarBotaoSalvarModificacoes(self.tlServicos, self.salvarModificacoesTelaCadServ)
            return True
        
        except Exception as e:
            self.mostrar_alerta('Atenção', f'Selecione uma linha da tabela abaixo:')
            self.fechar_TelaCadServ()
            self.criar_TelaCadServ() 
            return False
        
    def salvarModificacoesTelaCadServ(self):
        """
        Salva as modificações feitas na tela de cadastro de serviços.

        Esta função captura os valores dos campos de entrada na tela de cadastro de serviços, valida se os campos
        obrigatórios estão preenchidos, modifica o serviço no banco de dados, atualiza a tela de cadastro e limpa os campos.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se as modificações forem salvas com sucesso, False em caso de erro.
        """
        try:
            codServico = self.inputCodServ_tlCadServ.get().strip()
            descServico = self.inputDescServ_tlCadServ.get().strip().upper()
            vlrUnit = self.inputVlrUnit_tlCadServ.get()
            vlrUnit = vlrUnit.replace(",", ".")

            # Verificar se todos os campos obrigatórios estão preenchidos
            if not codServico or not descServico or not vlrUnit:
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                return False

            # Obter o serviço selecionado na tabela
            itemSelecionado = self.treeview_tlServicos.selection()
            item = self.treeview_tlServicos.item(itemSelecionado, 'values')
            serv_id = item[0]

            # Modificar o serviço no banco de dados
            if self._modificarServicoDoBanco(serv_id, codServico, descServico, vlrUnit):
                # Atualizar a tela de cadastro e limpar os campos
                self._atualizarTelaCadServ()
                self._limparTelaCadServ()
                return True
            else:
                return False
        except Exception as e:
            self.mostrar_alerta("Erro", f"Erro ao salvar: {e}")
            return False
            
                
    def _modificarServicoDoBanco(self, serv_id, serv_codServ, serv_descrServico, serv_vlrUnit):
        """
        Modifica um serviço cadastrado no banco de dados.

        Esta função atualiza as informações de um serviço no banco de dados, com base nos parâmetros fornecidos.

        Parâmetros:
        serv_id (int): O ID do serviço a ser modificado.
        serv_codServ (str): O novo código do serviço.
        serv_descrServico (str): A nova descrição do serviço.
        serv_vlrUnit (float): O novo valor unitário do serviço.

        Retorna:
        bool: True se a modificação for bem-sucedida, False em caso de erro.
        """
        try:
            self.db_manager.cursor.execute(
                "UPDATE tb_servicos_vlr SET serv_codServ = ?, serv_descrServico = ?, serv_vlrUnit = ? WHERE serv_id = ?",
                (serv_codServ, serv_descrServico, serv_vlrUnit, serv_id)
            )
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao modificar serviço:", e)
            return False
        
    def _atualizarTelaCadServ(self):
        """
        Atualiza a tela de cadastro de serviços.

        Esta função executa uma sequência de ações para atualizar a interface gráfica da tela de cadastro de serviços.
        Isso inclui redimensionar as colunas da tabela, mostrar a tabela de serviços, fechar e recriar a tela de cadastro.

        Parâmetros:
        Nenhum

        Retorna:
        None
        """
        self.resize_columns()  # Redimensiona as colunas da tabela
        self.mostrarTabelaServicos_TelaCadServ()  # Mostra a tabela de serviços
        self.fechar_TelaCadServ()  # Fecha a tela de cadastro de serviços
        self.criar_TelaCadServ()  # Recria a tela de cadastro de serviços 
    
    def gerarRelatorioCadServ(self):
        """
        Gera um relatório em PDF dos serviços cadastrados.

        Esta função utiliza um nome de arquivo predefinido para gerar um relatório em PDF dos serviços cadastrados,
        utilizando o método 'gerarRelatorio' da classe.

        Parâmetros:
        Nenhum

        Retorna:
        None
        """
        nome_arquivo = 'Relatório dos Serviços Cadastrados.pdf'
        self.gerarRelatorio(nome_arquivo)
            
    ############### FUNÇÕES GERAIS ###############
    
    def gerarRelatorio(self, nome_arquivo):
        """
        Gera um relatório em um arquivo PDF que abre diretamente no navegador padrão.

        Essa função utiliza o nome do arquivo fornecido para gerar um relatório em PDF.

        Parâmetros:
        nome_arquivo (str): O nome do arquivo de saída para o relatório em PDF.

        Retorna:
        None
        """
        self.manipular_relatorios.gerarRelatorioCadServ(nome_arquivo) 
    
    def _apagarListaBotoes(self, listaBotoesParaApagar):
        """
        Remove os botões presentes na lista da visualização.

        Essa função percorre a lista de botões fornecida e utiliza o método `place_forget()` para remover cada botão da visualização da interface gráfica.

        Parâmetros:
        listaBotoesParaApagar (list): Uma lista contendo os botões a serem removidos.

        Retorna:
        None
        """
        for botao in listaBotoesParaApagar:
            botao.place_forget()
            
    def mostrar_alerta(self, titulo, mensagem):
        """
        Mostra uma caixa de diálogo de alerta com um título e mensagem.

        Esta função exibe uma caixa de diálogo com o título e a mensagem fornecidos, informando o usuário sobre alguma informação ou evento.

        Parâmetros:
        titulo (str): O título da caixa de diálogo de alerta.
        mensagem (str): A mensagem a ser exibida na caixa de diálogo.

        Retorna:
        None
        """
        messagebox.showinfo(titulo, mensagem)

    def run(self):
        """
        Inicia a execução da interface gráfica.

        Essa função inicia o loop principal da interface gráfica, permitindo que a janela de login e seus elementos interajam com o usuário e respondam a eventos até que a janela seja fechada.

        Parâmetros:
        Nenhum

        Retorna:
        None
        """
        self.tela_login.mainloop()
        
    def resize_columns(self):
        """
        Redimensiona dinamicamente as colunas de um widget Treeview para acomodar o conteúdo.

        Para cada coluna do widget Treeview, esta função redefine o texto do cabeçalho para centralizar
        corretamente e calcula a largura ideal da coluna com base no maior comprimento do conteúdo da coluna.
        Uma largura mínima também é definida para garantir que a coluna seja sempre visível.

        Parâmetros:
        Nenhum

        Retorna:
        None
        """
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, anchor="center")  # Redefinir o texto do cabeçalho para alinhar corretamente

            # Calcular a largura ideal da coluna com base no maior comprimento do conteúdo da coluna
            col_width = max(len(self.treeview.set(row, col)) for row in self.treeview.get_children()) * 10
            
            # Definir uma largura mínima para a coluna
            col_width = max(col_width, 100)

            self.treeview.column(col, width=col_width)  # Redimensionar a coluna

        
    def _verificarValor_Inteiro(self, valorInteiro):
        """
        Verifica se um valor é uma representação válida de um número inteiro.

        Esta função verifica se o valor é uma string vazia ou se contém apenas dígitos, indicando um número inteiro.

        Parâmetros:
        valorInteiro (str): O valor a ser verificado.

        Retorna:
        bool: True se o valor for uma representação válida de um número inteiro, False caso contrário.
        """
        if valorInteiro == '' or valorInteiro.isdigit():
            return True
        return False

    def _verificarValor_Float(self, valor):
        """
        Verifica se um valor pode ser convertido para um número de ponto flutuante (float).

        Esta função substitui vírgulas por pontos na string do valor e tenta convertê-la em float.
        
        Parâmetros:
        valor (str): O valor a ser verificado.

        Retorna:
        bool: True se o valor puder ser convertido para float, False caso contrário.
        """
        valor = valor.replace(",", ".")  # Substitui vírgulas por pontos para lidar com formatação
        
        try:
            valorFloat = float(valor)  # Tenta converter o valor para float
            return True
        except ValueError:
            return False  # Retorna False se a conversão falhar (valor não é um número válido)
        
    def _verificarValor_Texto(self, valor):
        # Aceitar apenas texto (não vazio)
        return len(valor.strip()) > 0

    def _criarBotaoSalvarModificacoes(self, janela, comando):
        """
        Cria e posiciona um botão para salvar modificações na tela ativa no momento.

        Parâmetros:
        janela (Tk): A janela da interface gráfica onde o botão será colocado.
        comando (function): A função que será executada quando o botão for clicado.

        Retorna:
        None
        """
        # Carrega a imagem do botão "Salvar Modificações" a partir de um arquivo
        self.img_btnSalvarModificacoes = PhotoImage(file="./img/img_btnSalvarModificacoes.png")

        # Cria um botão usando a imagem carregada e configura seus atributos
        self.btnSalvarModificacoes = Button(
            janela,
            image=self.img_btnSalvarModificacoes,
            borderwidth=0,
            highlightthickness=0,
            command=comando,
            relief="flat"
        )

        # Posiciona o botão na janela usando coordenadas e define as dimensões
        self.btnSalvarModificacoes.place(
            x=239, y=115,
            width=139,
            height=30
        )
        
    def confirmar_exclusao(self, variavelMSGErro):
        """
        Exibe uma caixa de diálogo de confirmação para verificar se o usuário deseja excluir.

        Parâmetros:
        variavelMSGErro (str): A mensagem utiliza o valor da variável para confirmar as exclusão.

        Retorna:
        bool: True se o usuário confirmar a exclusão, False caso contrário.
        """
        
        resposta = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja excluir '{variavelMSGErro}'?")
        
        return resposta

    def mostrar_sucesso(self, variavelMSGErro):
        """
        Mostra uma mensagem de sucesso após a exclusão bem-sucedida.

        Parâmetros:
        variavelMSGErro (str): A mensagem utiliza o valor da variável para mostrar o sucesso na exclusão.

        Retorna:
        None
        """
        self.mostrar_alerta("Sucesso", f"O serviço '{variavelMSGErro}' foi deletado com sucesso.")

    def mostrar_erro(self, mensagem):
        """
        Mostra uma mensagem de erro em uma caixa de diálogo.

        Parâmetros:
        mensagem (str): A mensagem de erro a ser exibida.

        Retorna:
        None
        """
        self.mostrar_alerta("Erro", mensagem)

     
        
        
        
        
