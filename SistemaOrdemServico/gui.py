import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END, Toplevel
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from user import UserManager
from manipulacaoOrdemServico import ManipularOrdemServicos
from relatoriosPDF import ManipularCriacaodeRelatorios
from window_financeiro import ManipularWindowFinanceiro



class LoginGUI:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_manager = UserManager(db_manager)
        self.manipular_ordens = ManipularOrdemServicos(db_manager)
        self.manipular_relatorios = ManipularCriacaodeRelatorios(db_manager)
        self.manipular_telaFinanceiro = ManipularWindowFinanceiro(db_manager)

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

        # CRIANDO BOTÕES TELA PRINCIPAL #
        
        #### BOTÃO MODIFICAR ORDEM DE SERVIÇO ####
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

        #### BOTÃO DELETAR ORDEM DE SERVIÇO ####
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

        #### BOTÃO INSERT ORDEM DE SERVIÇO####
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

        #### BOTÃO CADASTRAR CLIENTE ORDEM DE SERVIÇO ####
        img_tlPrincipal_btnCadCliente = PhotoImage(file="./img/img_tlPrincipal_btnCadCliente.png")
        btnCadCliente_tlPrincipal = Button(
            image = img_tlPrincipal_btnCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.abrirTelaCadCliente,
            relief = "flat")

        btnCadCliente_tlPrincipal.place(
            x = 809, y = 71,
            width = 138,
            height = 60)

        #### BOTÃO CADASTRAR SERVIÇO ORDEM DE SERVIÇO####
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
            command = self.gerarRelatorioOrdensNAOfaturadas,
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
    
    
    def abrir_janela_financeiro(self):
        self.manipular_telaFinanceiro.criarTelaFinanceiro()

            
    ############# CRIANDO TELA CADASTRO DE SERVIÇOS #############
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
        img_btnModify_tlCadServ = PhotoImage(file="./img/img_btnModify.png")
        btnModify_tlCadServ = Button(
            self.tlServicos,
            image = img_btnModify_tlCadServ,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.modificarItemSelecionadoDaTabServico,
            relief = "flat")

        btnModify_tlCadServ.place(
            x = 492, y = 115,
            width = 90,
            height = 30)
        
        #### BOTÃO INSERIR SERVIÇOS ####
        img_btnInsert_tlCadServ = PhotoImage(file = "./img/img_btnInsert.png")
        btnInsert_tlCadServ = Button(
            self.tlServicos,
            image = img_btnInsert_tlCadServ,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cadastrarServico_TelaCadServico,
            relief = "flat")

        btnInsert_tlCadServ.place(
            x = 390, y = 115,
            width = 90,
            height = 30)

        #### BOTÃO DELETAR SERVIÇOS ####
        self.img_btnDelete_tlCadServ = PhotoImage(file = "./img/img_btnDelete.png")
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
        img_btnPrint_tlCadServ = PhotoImage(file = "./img/img_btnPrint.png")
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
    
        ############# CRIANDO TELA CADASTRO DE CLIENTES #############
    def criar_TelaCadClientes(self):
        
        self.tlClientes = Toplevel(self.telaPrincipal)
        self.tlClientes.title('Lista Clientes Cadastrados')
        self.tlClientes.geometry("781x622")
        self.tlClientes.configure(bg="#ffffff")
                
        canvas = Canvas(
            self.tlClientes,
            bg = "#ffffff",
            height = 622,
            width = 781,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)
        
        background_img_tlCadCliente = PhotoImage(file="./img/img_tlCadCliente_backgroundCadCliente.png")
        background = canvas.create_image(
            389.5, 311.0,
            image=background_img_tlCadCliente)

        # !!!!!!!!!!!!!! ver se fica!!!!!!!!!!!!!!!!
        verificaInteger = self.tlClientes.register(self._verificarValor_Inteiro)
        verificaFloat = self.tlClientes.register(self._verificarValor_Float)
        verificaTexto = self.tlClientes.register(self._verificarValor_Texto)
        
        #### BOTÃO MODIFICAR CLIENTE ####
        img_btnModify_tlCadCliente = PhotoImage(file="./img/img_btnModify.png")
        btnModify_tlCadCliente = Button(
            self.tlClientes,
            image = img_btnModify_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.modificarItemSelecionadoDaTabCliente,
            relief = "flat")

        btnModify_tlCadCliente.place(
            x = 251, y = 106,
            width = 90,
            height = 30)
        
        #### BOTÃO INSERIR CLIENTE ####
        img_btnInsert_tlCadCliente = PhotoImage(file = "./img/img_btnInsert.png")
        btnInsert_tlCadCliente = Button(
            self.tlClientes,
            image = img_btnInsert_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cadastrarCliente_TelaCadCliente,
            relief = "flat")

        btnInsert_tlCadCliente.place(
            x = 370, y = 106,
            width = 90,
            height = 30)

        #### BOTÃO DELETAR CLIENTE ####
        self.img_btnDelete_tlCadCliente = PhotoImage(file = "./img/img_btnDelete.png")
        self.btnDelete_tlCadCliente = Button(
            self.tlClientes,
            image = self.img_btnDelete_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.deletarCliente_TelaCadCliente,
            relief = "flat")

        self.btnDelete_tlCadCliente.place(
            x = 488, y = 106,
            width = 90,
            height = 30)
        
        #### BOTÃO IMPRIMIR CLIENTE ####
        img_btnPrint_tlCadCliente = PhotoImage(file = "./img/img_btnPrint.png")
        btnPrint_tlCadCliente = Button(
            self.tlClientes,
            image = img_btnPrint_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.gerarRelatorioCadCliente,
            relief = "flat")

        btnPrint_tlCadCliente.place(
            x = 643, y = 106,
            width = 115,
            height = 30)
        
        #botões que serão ocultos ao chamar a função de modificação:
        self.botoesParaOcultar_TelaCadCliente = [self.btnDelete_tlCadCliente, btnInsert_tlCadCliente, btnModify_tlCadCliente, btnPrint_tlCadCliente]
        
        inputCodCliente_tlCadCliente_img = PhotoImage(file = f"./img/img_tlCadCliente_inputCodCliente.png")
        inputCodServ_tlCadCliente_bg = canvas.create_image(
            122.0, 80.0,
            image = inputCodCliente_tlCadCliente_img)

        self.inputCodCliente_tlCadCliente = Entry(
            self.tlClientes,
            bd=0,
            bg="#d9d9d9",
            highlightthickness=0,
            validate="key",
            validatecommand=(verificaInteger, "%P"))

        self.inputCodCliente_tlCadCliente.place(
            x = 80.0, y = 65,
            width = 84.0,
            height = 28)
        
        inputNomeCliente_tlCadCliente_img = PhotoImage(file = "./img/img_tlCadCliente_inputNomeCliente.png")
        inputNomeCliente_tlCadCliente_bg = canvas.create_image(
            414.5, 80.0,
            image = inputNomeCliente_tlCadCliente_img)

        self.inputNomeCliente_tlCadCliente = Entry(
            self.tlClientes,
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0,
            validate="key",
            validatecommand=(verificaTexto, "%P"))

        self.inputNomeCliente_tlCadCliente.place(
            x = 254.0, y = 65,
            width = 321.0,
            height = 28)

        inputNotasIsentas_tlCadCliente_img = PhotoImage(file = "./img/img_tlCadCliente_inputNotasIsentas.png")
        inputNotasIsentas_tlCadCliente_bg = canvas.create_image(
            710.5, 80.0,
            image = inputNotasIsentas_tlCadCliente_img)
        
        
        self.inputNotasIsentas_tlCadCliente = tk.Entry(
            self.tlClientes,
            bd=0,
            bg="#d9d9d9",
            highlightthickness=0,
            validate="key",
            validatecommand=(verificaFloat, "%P")
        )

        self.inputNotasIsentas_tlCadCliente.pack()
            
        self.inputNotasIsentas_tlCadCliente.place(
            x = 666.0, y = 65,
            width = 89.0,
            height = 28)        

        ############### TREEVIEW LISTA CLIENTES ###############
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
                            
        self.treeview_tlClientes = ttk.Treeview(self.tlClientes)

        self.treeview_tlClientes.pack(fill="both", expand=True)

        self.treeview_tlClientes["columns"] = ("ID","CodCliente", "Cliente", "NFIsenta")
                
        self.treeview_tlClientes.column("#0", width=0, stretch=tk.NO)
        self.treeview_tlClientes.column("ID", width=30, anchor="center")
        self.treeview_tlClientes.column("CodCliente", width=70, anchor="center")
        self.treeview_tlClientes.column("Cliente", width=250, anchor="w")
        self.treeview_tlClientes.column("NFIsenta", width=70, anchor="e")

        self.treeview_tlClientes.heading("#0", text="", anchor="w")
        self.treeview_tlClientes.heading("ID", text="ID", anchor="center")
        self.treeview_tlClientes.heading("CodCliente", text="Código Cliente", anchor="center")
        self.treeview_tlClientes.heading("Cliente", text="Razão Social", anchor="center")
        self.treeview_tlClientes.heading("NFIsenta", text="Notas Isentas", anchor="center")

        center_aligned_text(self.treeview_tlClientes)
        right_aligned_text(self.treeview_tlClientes)

        # Posicionar a TreeView
        self.treeview_tlClientes.place(x=13, y=166, height=427, width=737)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.tlClientes, orient="vertical", command=self.treeview_tlClientes.yview)
        self.treeview_tlClientes.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=750, y=165.5, height=426)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.tlClientes, orient="horizontal", command=self.treeview_tlClientes.xview)
        self.treeview_tlClientes.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=13, y=592, width=754)
        ########## FIM TABELA CLIENTES ##########
        self.mostrarTabelaClientes_TelaCadClientes()
        self.tlClientes.resizable(False, False)
        self.tlClientes.mainloop()
        
        
    #@@@@@@@@@@@@@@@@ FUNÇÕES TELA LOGIN @@@@@@@@@@@@@@@@@@@#
    
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
 
    
    #@@@@@@@@@@@@@@@@ FUNÇÕES TELA PRINCIPAL ORDEM DE SERVIÇOS @@@@@@@@@@@@@@@@@#
    
    def pegandoValoresTelaPrincipalOS(self):
        os_dtServico = self.input_DataOS.get()
        os_codCliente = int(self.input_CodCliente.get().strip())
        os_cliente = self.input_Cliente.get().strip().upper()
        os_codServico = int(self.input_CodServ.get().strip())
        os_descrServico = self.input_DescricaoServ.get().strip().upper()
        os_quantidade = int(self.input_Quantidade.get())
        os_vlrUnit = self.input_VlrUnitario.get()
        os_total = float(self.input_VlrTotal.get())
        os_faturado = self.input_Faturado.get()
        os_descComplementar = self.input_DescrCompl.get('1.0', 'end-1c')

        return os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_faturado, os_descComplementar

    def _preencherFaturado(self, faturado):
        self.input_Faturado.configure(state="normal")
        self.input_Faturado.delete(0, END)
        self.input_Faturado.insert(0, faturado)
        self.input_Faturado.configure(state="readonly")        
    
    def preencheCliente(self, event):
        if event.keysym == "Tab":

            list_tv_cliente = self.manipular_ordens.consultarCompletaTabelaClientes()
            
            input_codCliente = int(self.input_CodCliente.get())
            
            for index, cliente in enumerate(list_tv_cliente ):
                print(f'index e cliente{index}, {cliente}')
                codCliente = int(cliente[1])
                nomeCliente = str(cliente[2])
                print(f' código e nome{codCliente}, {nomeCliente}')
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

            l_codServDescrServVlrUnit = self.manipular_ordens.consultarCompletaTabelaServicosValores()
            
            input_codServ = int(self.input_CodServ.get())
            
            for index, servicos in enumerate(l_codServDescrServVlrUnit):
                
                codServ = int(servicos[1])
                descrServ = str(servicos[2])
                valorUnit = servicos[3]
                
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
            

    def cadastrarOrdemServicos(self):
        os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_faturado, os_descComplementar = self.pegandoValoresTelaPrincipalOS()
        
        self.manipular_ordens.inserirOrdemServicosDB(os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado)
       
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
        #self.resize_columns()

    def atualizar_VizualizacaoTelaPrincipal(self):
        self.cadastrarOrdemServicos()
        self.mostrarOrdensServico_TelaPrincipal()
        self.mostrar_alerta('Sucesso', 'Serviço inserido com sucesso!')
        self.resize_columns()

    
    #@@@@@@@@@@@@@@@@@@@ FUNÇÕES TELA CADASTRO SERVIÇOS @@@@@@@@@@@@@@@@@#
    def abrirTelaCadServ(self, event=None):
        """
        Abre a tela de cadastro de serviços.

        Este método é chamado para criar e exibir a tela de cadastro de serviços.

        Parâmetros:
        event (Tkinter event, opcional): Evento que disparou a abertura da tela.

        Retorna:
        Nenhum
        
        Observação: event=None É um parâmetro que permite que você passe um objeto de evento associado à função. Ele é opcional, o que significa que você não precisa fornecê-lo quando chama a função. Se não for fornecido, o valor padrão é None.
        """
        self.criar_TelaCadServ()   
    
    def fechar_TelaCadServ(self):
        """
        Fecha a tela de cadastro de serviços.

        Este método é chamado para destruir a janela da tela de cadastro de serviços.

        Parâmetros:
        Nenhum

        Retorna:
        Nenhum
        """
        self.tlServicos.destroy()
    
    def pegarValoresTelaCadServico(self):
        """
        Obtém os valores dos campos da tela de cadastro de serviços.

        Este método obtém os valores dos campos de entrada na tela de cadastro de serviços.

        Parâmetros:
        Nenhum

        Retorna:
        tuple: Uma tupla contendo o código de serviço, descrição do serviço e valor unitário.
        """
        codServico = self.inputCodServ_tlCadServ.get()
        descServico = self.inputDescServ_tlCadServ.get()
        vlrUnit = self.inputVlrUnit_tlCadServ.get()
        return codServico, descServico, vlrUnit
    
    def _limparTelaCadServ(self):
        """
        Limpa os campos de entrada na tela de cadastro de serviços.
        
        Este método é responsável por apagar o conteúdo dos campos de entrada na tela de cadastro de serviços.

        Parâmetros:
        Nenhum

        Retorna:
        Nenhum
        
        Observação: Se for fechando a aplicação antes de chamar está função _limparTelaCadServ, pode haver um problema relacionado ao ciclo de vida da aplicação.
        """
        self.inputCodServ_tlCadServ.delete(0, 'end')  # Limpar campo de código
        self.inputDescServ_tlCadServ.delete(0, 'end')  # Limpar campo de descrição
        self.inputVlrUnit_tlCadServ.delete(0, 'end')  # Limpar campo de valor unitário
        
    def _verificarSeCamposTelaServicosPreenchidos(self):
        """
        Verifica se os campos da tela de cadastro de serviços estão preenchidos.

        Esta função verifica se os campos de código de serviço, descrição de serviço e valor unitário da tela de cadastro de serviços estão preenchidos.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se todos os campos estão preenchidos, False se algum campo estiver vazio.
        """
        codServico, descServico, vlrUnit = self.pegarValoresTelaCadServico()
        
        # Retorna True se todos os campos estiverem preenchidos, caso contrário, retorna False
        return bool(codServico and descServico and vlrUnit)
    
    def _verificarSeCodigoServicoJaExiste(self):
        """
        Verifica se um código de serviço já existe no banco de dados.

        Esta função verifica se um código de serviço já está cadastrado no banco de dados da tabela 'tb_servicos_vlr'.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se o código de serviço já existe no banco de dados, False se não existe.
        """
        codServico = self.inputCodServ_tlCadServ.get()
        
        return self.manipular_ordens.verificarSeCodigoDoServicoCadastrado(codServico) is not None    
    
    def verificarSeCodigoServicoJaExiste(self, codServico):
        if self._verificarSeCodigoServicoJaExiste():
            self.mostrar_alerta("Valor Inválido", f"Código {codServico} já existe.")
            self._atualizarTelaCadServ()
            return False
    # FUNÇÃO BOTÃO INSERIR TELA CADASTRO DE SERVIÇOS    
    def cadastrarServico_TelaCadServico(self):
        """
        Insere um novo serviço na tela de cadastro de serviços.

        Esta função verifica os campos preenchidos na tela de cadastro de serviços, verifica se o código de serviço já existe no banco de dados, insere o novo serviço no banco e atualiza a tela.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se o serviço for inserido com sucesso, False em caso de erro.
        """
        try:
            # Verifica se os campos obrigatórios estão preenchidos
            if not self._verificarSeCamposTelaServicosPreenchidos():
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                self._atualizarTelaCadServ()
                return False
            
            codServico, descServico, vlrUnit = self.pegarValoresTelaCadServico()
            codServico = codServico.strip()
            descServico = descServico.strip().upper()
            vlrUnit = vlrUnit.replace(",", ".")
            
            # Verifica se o código de serviço já existe no banco de dados
            if self._verificarSeCodigoServicoJaExiste():
                self.mostrar_alerta("Valor Inválido", f"Código {codServico} já existe.")
                self._atualizarTelaCadServ()
                return False
            
            # Insere o novo serviço no banco de dados
            if self.manipular_ordens.inserirServicoDB(codServico, descServico, vlrUnit):
            # if self._inserirServicoNoBanco(codServico, descServico, vlrUnit):
                self.mostrar_alerta("Cadastro de Serviço", f"Serviço '{descServico}' cadastrado com sucesso!")
                self._atualizarTelaCadServ()
                return True
        except Exception as e:
            self.mostrar_alerta('Erro', f'Cadastro do Serviço não realizado!')
        return False
    
    # MOSTRAR A TABELA NA TELA CADASTRO DE SERVIÇOS        
    def mostrarTabelaServicos_TelaCadServ(self):
        """
        Preenche a tabela (Treeview) na tela de cadastro de serviços com dados da consulta.

        Este método preenche a tabela de serviços na tela de cadastro de serviços com os dados obtidos da consulta à tabela de serviços e valores.

        Parâmetros:
        Nenhum

        Retorna:
        Nenhum
        """
        # Limpa os dados existentes na tabela
        self.treeview_tlServicos.delete(*self.treeview_tlServicos.get_children())

        # Realiza a consulta à tabela de serviços e valores
        listandoServicos = self.manipular_ordens.consultarCompletaTabelaServicosValores()

        # Itera sobre os resultados da consulta e insere na tabela
        for resultado in listandoServicos:
            serv_id, serv_codServ, serv_descrServico, serv_vlrUnit = resultado

            # Insere uma nova linha na tabela com os valores obtidos
            self.treeview_tlServicos.insert("", "end", values=(serv_id, serv_codServ, serv_descrServico, serv_vlrUnit))

    #FUNÇÃO BOTÃO DELETAR NA TELA CADATRO DE SERVIÇOS
    def deletarServico_TelaCadServ(self):
        """
        Deleta um serviço da tabela na tela de cadastro de serviços.

        Este método permite a exclusão de um serviço selecionado da tabela na tela de cadastro de serviços.
        Ele confirma a exclusão com o usuário, realiza a exclusão no banco de dados e atualiza a tabela.

        Parâmetros:
        Nenhum

        Retorna:
        Nenhum
        """
        # Obtém o item selecionado na tabela
        selected_item = self.treeview_tlServicos.selection()
        
        # Verifica se algum item foi selecionado
        if not selected_item:
            self.mostrar_alerta("Nenhum item selecionado", "Por favor, selecione um item para deletar.")
            self._atualizarTelaCadServ()
            return
        
        # Obtém informações do item selecionado
        serv_id, serv_codServ, serv_descServico, serv_vlrUnit = self.pegarValoresLinhaSelecionadaDaTabelaServicos()
        
        # Confirmação de exclusão com o usuário
        if self.confirmar_exclusao(serv_descServico):
            # Deleta o serviço do banco de dados
            if self.manipular_ordens.deletarServicoDB(serv_id):
                # Remove o item da tabela
                self.treeview_tlServicos.delete(selected_item)
                self.mostrar_sucesso(serv_codServ, serv_descServico, serv_vlrUnit)
            else:
                self.mostrar_erro("Ocorreu um erro ao tentar deletar o serviço.")
        else:
            self.mostrar_alerta("Cancelado", "A exclusão foi cancelada pelo usuário.")
        
        # Atualiza a tela de cadastro de serviços
        self._atualizarTelaCadServ()

    ###FUNÇÕES PARA MODIFICAR
    def pegarValoresLinhaSelecionadaDaTabelaServicos(self):
        itemSelecionadoTbServicos = self.treeview_tlServicos.selection()
        item = self.treeview_tlServicos.item(itemSelecionadoTbServicos, 'values')
        serv_id, serv_codServ, serv_descServico, serv_vlrUnit = item
        return serv_id, serv_codServ, serv_descServico, serv_vlrUnit
    
    def _desabilitar_inputCodServ(self):
        # Desabilitar o campo
        self.inputCodServ_tlCadServ.config(state="disabled")
        # Alterar a cor de fundo para uma cor mais escura
        self.inputCodServ_tlCadServ.config(bg="#bfbfbf")
    
    # FUNÇÃO BOTÃO MODIFICAR TELA CADASTRO DE SERVIÇOS
    def modificarItemSelecionadoDaTabServico(self): 
        """
        Habilita a edição de um item selecionado na tabela da tela de cadastro de serviços.

        Este método permite que um item selecionado na tabela de serviços da tela de cadastro seja editado.
        Ele preenche os campos de entrada com os valores do item selecionado e desabilita o campo de código.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se a edição for habilitada com sucesso, False em caso de erro.
        """
        try:
            # Obtém os valores da linha selecionada na tabela de serviços
            serv_id, serv_codServ, serv_descServico, serv_vlrUnit = self.pegarValoresLinhaSelecionadaDaTabelaServicos()
            
            # Preenche o campo de código com o valor do item selecionado
            self.inputCodServ_tlCadServ.delete(0, 'end')
            self.inputCodServ_tlCadServ.insert(0, int(serv_codServ)) 
            
            # Desabilita o campo de código
            self._desabilitar_inputCodServ()
            
            # Preenche o campo de descrição com o valor do item selecionado
            self.inputDescServ_tlCadServ.delete(0, 'end')
            self.inputDescServ_tlCadServ.insert(0, str(serv_descServico))
            
            # Preenche o campo de valor unitário com o valor do item selecionado
            self.inputVlrUnit_tlCadServ.delete(0, 'end')
            self.inputVlrUnit_tlCadServ.insert(0, float(serv_vlrUnit))
            
            # Remove os botões anteriores e cria um botão "Salvar Modificações"
            self._apagarListaBotoes(self.botoesParaOcultar_TelaCadServ)
            self._criarBotaoSalvarModificacoes(self.tlServicos, self.validarModificacoesTelaCadServ, 349, 115)
            
            return True
        
        except Exception as e:
            # Exibe uma mensagem de alerta e recria a tela caso ocorra um erro
            self.mostrar_alerta('Atenção', f'Selecione uma linha da tabela abaixo:')
            self.fechar_TelaCadServ()
            self.criar_TelaCadServ() 
            return False
    
    # FUNÇÃO BOTÃO SALVAR MODIFICAÇÕES    
    def validarModificacoesTelaCadServ(self):
        """
        Salva as modificações feitas na tela de cadastro de serviços.

        Esta função captura os valores dos campos de entrada na tela de cadastro de serviços, valida se os campos obrigatórios estão preenchidos, modifica o serviço no banco de dados, atualiza a tela de cadastro e limpa os campos.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se as modificações forem salvas com sucesso, False em caso de erro.
        """
        try:
            codServico, descServico, vlrUnit = self.pegarValoresTelaCadServico()
            codServico = codServico.strip()
            descServico = descServico.strip().upper()
            vlrUnit = vlrUnit.replace(",", ".")           
            
            # Verificar se todos os campos obrigatórios estão preenchidos
            if not codServico or not descServico or not vlrUnit:
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                return False
            
            # Obter o serviço selecionado na tabela
            serv_id, serv_codServ, serv_descServico, serv_vlrUnit = self.pegarValoresLinhaSelecionadaDaTabelaServicos()
            
            # Modificar o serviço no banco de dados
            if self.manipular_ordens.editarServicoPeloIDServicosValoresDB(serv_id, codServico, descServico, vlrUnit):
                # Atualizar a tela de cadastro e limpar os campos
                self._limparTelaCadServ()
                self._atualizarTelaCadServ()
                return True
            else:
                return False
        except Exception as e:
            self.mostrar_alerta("Erro", f"Erro ao salvar: {e}")
            return False
            
    def _criarBotaoSalvarModificacoes(self, janela, comando, posicaoX, posicaoY):
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
            x=posicaoX, y=posicaoY,
            width=139,
            height=30
        )            
    
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
        self.manipular_relatorios.gerarRelatorioCadServ('Relatório dos Clientes Cadastrados.pdf')
    
    #@@@@@@@@@@@@@@@@@@@ FUNÇÕES TELA CADASTRO DE CLIENTES @@@@@@@@@@@@@@@@@@@#
    
    def abrirTelaCadCliente(self, event=None):
        self.criar_TelaCadClientes() 
    
    # MOSTRAR A TABELA NA TELA CADASTRO DE CLIENTES        
    def mostrarTabelaClientes_TelaCadClientes(self):
        
        # Limpa os dados existentes na tabela
        self.treeview_tlClientes.delete(*self.treeview_tlClientes.get_children())

        # Realiza a consulta à tabela de CLIENTES
        listandoClientes = self.manipular_ordens.consultarCompletaTabelaClientes()

        # Itera sobre os resultados da consulta e insere na tabela
        for resultado in listandoClientes:
            cli_id, codCliente, nomeCliente, qtdNFisenta = resultado

            # Insere uma nova linha na tabela com os valores obtidos
            self.treeview_tlClientes.insert("", "end", values=(cli_id, codCliente, nomeCliente, qtdNFisenta))
    
    def fechar_TelaCadCliente(self):
        self.tlClientes.destroy()
    
    def _limparTelaCadCliente(self):
        self.inputCodCliente_tlCadCliente.delete(0, 'end')  
        self.inputNomeCliente_tlCadCliente.delete(0, 'end')
        self.inputNotasIsentas_tlCadCliente.delete(0, 'end')
        
    def _atualizarTelaCadCliente(self):
        self.resize_columns()  # Redimensiona as colunas da tabela
        self.mostrarTabelaClientes_TelaCadClientes()  # Mostra a tabela de serviços
        self.fechar_TelaCadCliente()  # Fecha a tela de cadastro de serviços
        self.abrirTelaCadCliente()  # Recria a tela de cadastro de serviços 
    
    ### FUNÇÃO INSERIR ###
    # pegar dados dos campos
    def pegarValoresTelaCadClientes(self):
        codCliente = self.inputCodCliente_tlCadCliente.get()
        nomeCliente = self.inputNomeCliente_tlCadCliente.get()
        notasIsentas = self.inputNotasIsentas_tlCadCliente.get()
        if not notasIsentas:
            notasIsentas = 0 
        return codCliente, nomeCliente, notasIsentas
    
    # verificar se todos os campos estão preenchidos
    def _verificaSeCamposTelaClientesPreenchidos(self):
        codCliente, nomeCliente, notasIsentas = self.pegarValoresTelaCadClientes()
        return bool(codCliente and nomeCliente)
    
    # verificar se código do input já está cadastrado na tabela
    def _verificarSeCodigoClientteJaExiste(self):
        codCliente = self.inputCodCliente_tlCadCliente.get()
        return self.manipular_ordens.verificarSeCodigoDoClienteCadastrado(codCliente) is not None    
    
    def verificarSeCodigoClienteJaExiste(self, codCliente):
        if self._verificarSeCodigoClientteJaExiste():
            self.mostrar_alerta("Valor Inválido", f"Código {codCliente} já existe.")
            self._atualizarTelaCadCliente()
            return False
    
    # FUNÇÃO BOTÃO INSERIR TELA CADASTRO DE CLIENTES
    def cadastrarCliente_TelaCadCliente(self):
        try:
            # Verifica se os campos obrigatórios estão preenchidos
            if not self._verificaSeCamposTelaClientesPreenchidos():
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                self._atualizarTelaCadCliente()
                return False
            
            codCliente, nomeCliente, qtdNFisenta = self.pegarValoresTelaCadClientes()
            codCliente = codCliente.strip()
            nomeCliente = nomeCliente.strip().upper()
            #qtdNFisenta = qtdNFisenta.replace(",", ".")
            
            # Verifica se o código de serviço já existe no banco de dados
            if self._verificarSeCodigoClientteJaExiste():
                self.mostrar_alerta("Valor Inválido", f"Código {codCliente} já existe.")
                self._atualizarTelaCadCliente()
                return False
            
            # Insere o novo serviço no banco de dados
            if self.manipular_ordens.inserirClienteDB(codCliente, nomeCliente, qtdNFisenta):
            # if self._inserirServicoNoBanco(codServico, descServico, vlrUnit):
                self.mostrar_alerta("Cadastro de Serviço", f"Serviço '{nomeCliente}' cadastrado com sucesso!")
                self._atualizarTelaCadCliente()
                return True
        except Exception as e:
            self.mostrar_alerta('Erro', f'Cadastro do Cliente não realizado!\n(Erro:{e})')
        return False
    
    ### FUNÇÕES PARA MODIFICAR CADASTRO CLIENTE
    def pegarValoresLinhaSelecionadaDaTabelaCliente(self):
        itemSelecionadoTbCliente = self.treeview_tlClientes.selection()
        item = self.treeview_tlClientes.item(itemSelecionadoTbCliente, 'values')
        cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta = item
        return cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta
    
    def _desabilitar_inputCodCliente(self):
        # Desabilitar o campo
        self.inputCodCliente_tlCadCliente.config(state="disabled")
        # Alterar a cor de fundo para uma cor mais escura
        self.inputCodCliente_tlCadCliente.config(bg="#bfbfbf")
    
    # FUNÇÃO BOTÃO MODIFICAR TELA CADASTRO DE CLIENTE
    def modificarItemSelecionadoDaTabCliente(self): 
        try:
            # Obtém os valores da linha selecionada na tabela de serviços
            cli_id, codcliente, nomeCliente, qtdNFisenta = self.pegarValoresLinhaSelecionadaDaTabelaCliente()
            
            # Preenche o campo de código com o valor do item selecionado
            self.inputCodCliente_tlCadCliente.delete(0, 'end')
            self.inputCodCliente_tlCadCliente.insert(0, int(codcliente)) 
            
            # Desabilita o campo de código
            self._desabilitar_inputCodCliente()
            
            # Preenche o campo de descrição com o valor do item selecionado
            self.inputNomeCliente_tlCadCliente.delete(0, 'end')
            self.inputNomeCliente_tlCadCliente.insert(0, str(nomeCliente))
            
            # Preenche o campo de valor unitário com o valor do item selecionado
            self.inputNotasIsentas_tlCadCliente.delete(0, 'end')
            self.inputNotasIsentas_tlCadCliente.insert(0, float(qtdNFisenta))
            
            # Remove os botões anteriores e cria um botão "Salvar Modificações"
            self._apagarListaBotoes(self.botoesParaOcultar_TelaCadCliente)
            self._criarBotaoSalvarModificacoes(self.tlClientes, self.validarModificacoesTelaCadCliente, 320, 106)
            
            return True
        
        except Exception as e:
            # Exibe uma mensagem de alerta e recria a tela caso ocorra um erro
            self.mostrar_alerta('Atenção', f'Selecione uma linha da tabela abaixo:')
            self.fechar_TelaCadCliente()
            self.criar_TelaCadClientes() 
            return False
    
    # FUNÇÃO BOTÃO SALVAR MODIFICAÇÕES    
    def validarModificacoesTelaCadCliente(self):
        try:
            codCliente, nomeCliente, qtdNFisenta = self.pegarValoresTelaCadClientes()
            codCliente = codCliente.strip()
            nomeCliente = nomeCliente.strip().upper()
            qtdNFisenta = qtdNFisenta.replace(",", ".")           
            
            # Verificar se todos os campos obrigatórios estão preenchidos
            if not codCliente or not nomeCliente:
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                return False
            
            # Obter o serviço selecionado na tabela
            cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta = self.pegarValoresLinhaSelecionadaDaTabelaCliente()
            
            # Modificar o serviço no banco de dados
            if self.manipular_ordens.editarClientePeloIDClienteDB(cli_id, codCliente, nomeCliente, qtdNFisenta):
                # Atualizar a tela de cadastro e limpar os campos
                self._limparTelaCadCliente()
                self._atualizarTelaCadCliente()
                return True
            else:
                return False
        except Exception as e:
            self.mostrar_alerta("Erro", f"Erro ao salvar modificação do Cliente {nomeCliente}:\nErro:{e}")
            return False
            
    ### FUNÇÃO DELETAR CLIENTE ###    
    def deletarCliente_TelaCadCliente(self):
        # Obtém o item selecionado na tabela
        selected_itemTabCliente = self.treeview_tlClientes.selection()
        
        # Verifica se algum item foi selecionado
        if not selected_itemTabCliente:
            self.mostrar_alerta("Nenhum item selecionado", "Por favor, selecione um item para deletar.")
            self._atualizarTelaCadCliente()
            return
        
        # Obtém informações do item selecionado
        cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta = self.pegarValoresLinhaSelecionadaDaTabelaCliente()
        
        # Confirmação de exclusão com o usuário
        if self.confirmar_exclusao(cli_nomeCliente):
            # Deleta o serviço do banco de dados
            if self.manipular_ordens.deletarClienteDB(cli_id):
                # Remove o item da tabela
                self.treeview_tlClientes.delete(selected_itemTabCliente)
                self.mostrar_sucesso(cli_codcliente, cli_nomeCliente)
            else:
                self.mostrar_erro(f"Ocorreu um erro ao tentar deletar o cliente {cli_nomeCliente}.")
        else:
            self.mostrar_alerta("Cancelado", "A exclusão foi cancelada pelo usuário.")
        
        # Atualiza a tela de cadastro de Cliente
        self._atualizarTelaCadCliente()
    
    
    ### FUNÇÃO DE IMPRIMIR LISTA CLIENTES ###
    def gerarRelatorioCadCliente(self):
        """
        Gera um relatório em PDF dos clientes cadastrados.

        Esta função utiliza um nome de arquivo predefinido para gerar um relatório em PDF dos serviços cadastrados, utilizando o método 'gerarRelatorio' da classe.

        Parâmetros:
        Nenhum

        Retorna:
        None
        """
        self.manipular_relatorios.gerarRelatorioCadCliente('Relatório dos Clientes Cadastrados.pdf')
        
    ############### FINANCEIRO ###################
    def gerarRelatorioOrdensNAOfaturadas(self):
        self.manipular_relatorios.gerarRelatorioOdensServicoNAOfaturadas('Relatório Ordens há faturar.pdf')
            
    ############### FUNÇÕES GERAIS ###############
    
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

    def mostrar_sucesso(self, *variavelMSG):
        """
        Mostra uma mensagem de sucesso após a exclusão bem-sucedida.

        Parâmetros:
        variavelMSG (str): A mensagem utiliza o valor da(s) variável/variáveis para mostrar o sucesso na exclusão.

        Retorna:
        None
        """
        self.mostrar_alerta("Sucesso", f"O item selecionado {variavelMSG} foi deletado com sucesso.")

    def mostrar_erro(self, mensagem):
        """
        Mostra uma mensagem de erro em uma caixa de diálogo.

        Parâmetros:
        mensagem (str): A mensagem de erro a ser exibida.

        Retorna:
        None
        """
        self.mostrar_alerta("Erro", mensagem)

     
        
        
        
        
