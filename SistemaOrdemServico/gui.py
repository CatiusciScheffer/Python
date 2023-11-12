import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END, Toplevel, simpledialog
from tkcalendar import DateEntry
from user import UserManager
from manipulacaoOrdemServico import ManipularOrdemServicos
from relatoriosPDF import ManipularCriacaodeRelatorios
import traceback


class LoginGUI:
    def __init__(self, db_manager):
        self.usuarioLogado = None
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
            show="*")

        self.input_login_senha.place(
            x = 414.0, y = 210,
            width = 219.0,
            height = 30)
        
        imgBtnEntrar = PhotoImage(file="./img/img_tlLogin_BtnEntrar.png")
        BtnEntrar = Button(
            image = imgBtnEntrar,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.fechar_TelaLogin,
            relief = "flat")

        BtnEntrar.place(
            x = 472, y = 261,
            width = 103,
            height = 32)
        
        #Faz entrar sem clique no botão enter, apenas clicando
        BtnEntrar.bind("<Return>", self.fechar_TelaLogin)

        self.tela_login.resizable(False, False)
        self.tela_login.mainloop()
        
    def fechar_TelaLogin(self, event=None):
        self.verificar_usuario_existente()
        #self.tela_login.destroy()
        self.criar_TelaPrincipal()
    
    def criar_TelaPrincipal(self):
        
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
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_VlrUnitario.place(
            x = 304.0, y = 144,
            width = 90.0,
            height = 22)
        
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
            327.5, 244.5,
            image = input_DescrCompl_img)

        self.input_DescrCompl = tk.Text(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_DescrCompl.place(
            x = 30.0, y = 195,
            width = 595.0,
            height = 97)
        # Insira o valor preenchido no campo de texto
        descricaoComplementarPadrao = "Aqui para detalhar o serviço..."
        self.input_DescrCompl.insert("1.0", descricaoComplementarPadrao)
        

        # CRIANDO BOTÕES TELA PRINCIPAL #
        
        #### BOTÃO MODIFICAR ORDEM DE SERVIÇO ####
        img_tlPrincipal_btnModificar = PhotoImage(file="./img/img_tlPrincipal_btnModify.png")
        btnModifyOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnModificar,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.modificarItemSelecionadoDaTabOrdemServico,
            relief = "flat")

        btnModifyOS_tlPrincipal.place(
            x = 782, y = 186,
            width = 173,
            height = 30)

        #### BOTÃO DELETAR ORDEM DE SERVIÇO ####
        img_tlPrincipal_btnDelete = PhotoImage(file="./img/img_tlPrincipal_btnDelete.png")
        btnDeleteOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnDelete,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.deletarOrdemServico_TelaPrincipal,
            relief = "flat")

        btnDeleteOS_tlPrincipal.place(
            x = 782, y = 225,
            width = 173,
            height = 30)

        #### BOTÃO INSERT ORDEM DE SERVIÇO####
        img_tlPrincipal_btnInsert = PhotoImage(file="./img/img_tlPrincipal_btnInsert.png")
        btnInsertOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnInsert,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.cadastrarOrdemServicos,
            relief = "flat")

        btnInsertOS_tlPrincipal.place(
            x = 654, y = 187,
            width = 105,
            height = 50)

        #### BOTÃO CADASTRAR CLIENTE ORDEM DE SERVIÇO ####
        img_tlPrincipal_btnCadCliente = PhotoImage(file="./img/img_tlPrincipal_btnCadCliente.png")
        btnCadCliente_tlPrincipal = Button(
            image = img_tlPrincipal_btnCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.abrirTelaCadCliente,
            relief = "flat")

        btnCadCliente_tlPrincipal.place(
            x = 782, y = 71,
            width = 173,
            height = 30)

        #### BOTÃO CADASTRAR SERVIÇO ORDEM DE SERVIÇO####
        img_tlPrincipal_btnCadServico = PhotoImage(file="./img/img_tlPrincipal_btnCadServico.png")
        btnCadServ_tlPrincipal = Button(
            image = img_tlPrincipal_btnCadServico,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.abrirTelaCadServ,
            relief = "flat")

        btnCadServ_tlPrincipal.place(
            x = 782, y = 109,
            width = 173,
            height = 30)
        
            
        #### BOTÃO REL À FATURAR ####
        img_tlPrincipal_btnFinanceiro = PhotoImage(file="./img/img_tlPrincipal_btnFinanceiro.png")
        btnFinanceiro_tlPrincipal = Button(
            image = img_tlPrincipal_btnFinanceiro,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.gerarRelatorioOrdensNAOfaturadas,
            relief = "flat")

        btnFinanceiro_tlPrincipal.place(
            x = 782, y = 148,
            width = 173,
            height = 30)
        
        #### BOTÃO FECHAMENTO ####
        img_tlPrincipal_btnFechamento = PhotoImage(file="./img/img_tlPrincipal_btnFechamento.png")
        btnFechamento_tlPrincipal = Button(
            image = img_tlPrincipal_btnFechamento,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.fazerFechamentoFaturamento,
            relief = "flat")

        btnFechamento_tlPrincipal.place(
            x = 654, y = 244,
            width = 105,
            height = 50)
        
        #### BOTÃO IMPRIMIR ####
        img_tlPrincipal_btnImprimir = PhotoImage(file="./img/img_tlPrincipal_btnImprimir.png")
        btnImprimir_tlPrincipal = Button(
            image = img_tlPrincipal_btnImprimir,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.gerarRelatorioOrdensGeral,
            relief = "flat")

        btnImprimir_tlPrincipal.place(
            x = 782, y = 263,
            width = 173,
            height = 30)
        
        # botões que serão ocultos ao chamar a função de modificação:
        self.botoesParaOcultar_TelaPrincipal = [btnFinanceiro_tlPrincipal, btnCadServ_tlPrincipal, btnCadCliente_tlPrincipal, btnInsertOS_tlPrincipal, btnDeleteOS_tlPrincipal, btnModifyOS_tlPrincipal, btnFechamento_tlPrincipal, btnImprimir_tlPrincipal]
        
        ############# CRIANDO TREEVIEW ORDEM DE SERVIÇOS #############
              
        # Função para centralizar o texto nas células da TreeView
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
            
        # Criar a TreeView
        self.treeviewTelaPrincipal = ttk.Treeview(self.telaPrincipal)

        self.treeviewTelaPrincipal.pack(fill="both", expand=True)

        # Configurar as colunas com largura e alinhamento
        self.treeviewTelaPrincipal["columns"] = ("ID","Data", "CodCliente", "Cliente", "CodServ", "DescrServico", "QTD", "ValorUnit", "ValorTotal", "DescComplementar", "Faturado", "Dt.Faturamento", "Responsavel")
        
        self.treeviewTelaPrincipal.column("#0", width=0, stretch=tk.NO)  # Coluna de ícones (não visível)
        self.treeviewTelaPrincipal.column("ID", width=50, anchor="center")
        self.treeviewTelaPrincipal.column("Data", width=70, anchor="center")
        self.treeviewTelaPrincipal.column("CodCliente", width=70, anchor="center")
        self.treeviewTelaPrincipal.column("Cliente", width=200, anchor="w")
        self.treeviewTelaPrincipal.column("CodServ", width=70, anchor="center")
        self.treeviewTelaPrincipal.column("DescrServico", width=146, anchor="w")
        self.treeviewTelaPrincipal.column("QTD", width=38, anchor="e")
        self.treeviewTelaPrincipal.column("ValorUnit", width=65, anchor="e")
        self.treeviewTelaPrincipal.column("ValorTotal", width=65, anchor="e")
        self.treeviewTelaPrincipal.column("DescComplementar", width=200, anchor="w")
        self.treeviewTelaPrincipal.column("Faturado", width=70, anchor="center")
        self.treeviewTelaPrincipal.column("Dt.Faturamento", width=70, anchor="center")
        self.treeviewTelaPrincipal.column("Responsavel", width=100, anchor="center")

        # Definir as colunas que serão exibidas
        self.treeviewTelaPrincipal.heading("#0", text="", anchor="w")  # Coluna de ícones (não visível)
        self.treeviewTelaPrincipal.heading("ID", text="ID", anchor="center")
        self.treeviewTelaPrincipal.heading("Data", text="Data", anchor="center")
        self.treeviewTelaPrincipal.heading("CodCliente", text="Cód.Cliente", anchor="center")
        self.treeviewTelaPrincipal.heading("Cliente", text="Cliente", anchor="center")
        self.treeviewTelaPrincipal.heading("CodServ", text="Cód.Serv.", anchor="center")
        self.treeviewTelaPrincipal.heading("DescrServico", text="Descrição Serviço", anchor="center")
        self.treeviewTelaPrincipal.heading("QTD", text="QTD", anchor="center")
        self.treeviewTelaPrincipal.heading("ValorUnit", text="Valor Unit.", anchor="center")
        self.treeviewTelaPrincipal.heading("ValorTotal", text="Valor Total", anchor="center")
        self.treeviewTelaPrincipal.heading("DescComplementar", text="Descrição Complementar", anchor="center")
        self.treeviewTelaPrincipal.heading("Faturado", text="Faturado", anchor="center")
        self.treeviewTelaPrincipal.heading("Dt.Faturamento", text="Dt.Faturamento", anchor="center")
        self.treeviewTelaPrincipal.heading("Responsavel", text="Responsável", anchor="center")

        # Aplicar formatação de alinhamento
        center_aligned_text(self.treeviewTelaPrincipal)
        right_aligned_text(self.treeviewTelaPrincipal)

        # Posicionar a TreeView na janela principal usando o place()
        self.treeviewTelaPrincipal.place(x=13, y=322, height=369, width=957)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.telaPrincipal, orient="vertical", command=self.treeviewTelaPrincipal.yview)
        self.treeviewTelaPrincipal.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=969, y=323, height=367)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.telaPrincipal, orient="horizontal", command=self.treeviewTelaPrincipal.xview)
        self.treeviewTelaPrincipal.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=14, y=690, width=973)
        
        self.mostrarOrdensServico_TelaPrincipal()
        
        self.ajustarLarguraColunaTreeview(self.treeviewTelaPrincipal) 
        # --------------- ORDENAR A TREEVIEW (CLIQUE CABEÇALHO) ----------------#   
        # Chamando a função para ordenar pelo clique nos cabeçalhos
        self.treeviewTelaPrincipal.heading("ID", text="ID", anchor="center")
        self.treeviewTelaPrincipal.heading("ID", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 0))
        
        self.treeviewTelaPrincipal.heading("Data", text="Data", anchor="center")
        self.treeviewTelaPrincipal.heading("Data", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 1))
        
        self.treeviewTelaPrincipal.heading("CodCliente", text="CodCliente", anchor="center")
        self.treeviewTelaPrincipal.heading("CodCliente", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 2))
        
        self.treeviewTelaPrincipal.heading("Cliente", text="Cliente", anchor="center")
        self.treeviewTelaPrincipal.heading("Cliente", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 3))
        
        self.treeviewTelaPrincipal.heading("CodServ", text="CodServ", anchor="center")
        self.treeviewTelaPrincipal.heading("CodServ", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 4))
        
        self.treeviewTelaPrincipal.heading("DescrServico", text="DescrServico", anchor="center")
        self.treeviewTelaPrincipal.heading("DescrServico", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 5))
        
        self.treeviewTelaPrincipal.heading("Faturado", text="Faturado", anchor="center")
        self.treeviewTelaPrincipal.heading("Faturado", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 10))
        
        self.treeviewTelaPrincipal.heading("Dt.Faturamento", text="Dt.Faturamento", anchor="center")
        self.treeviewTelaPrincipal.heading("Dt.Faturamento", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 11))
        
        self.treeviewTelaPrincipal.heading("Responsavel", text="Responsavel", anchor="center")
        self.treeviewTelaPrincipal.heading("Responsavel", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 12))       
        # --------------- ************************************* ----------------#
            
        # Iniciar o loop principal do Tkinter
        self.telaPrincipal.resizable(False, True)
        self.telaPrincipal.mainloop()
      
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
        
        #@@@@ botões que serão ocultos ao chamar a função de modificação @@@@#
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
        
        #----------------------- ORDENANDO POR CLIQUE NO CABEÇALHO TB SERVIÇOS-----------------------#
        self.treeview_tlServicos .heading("ID", text="ID", anchor="center")
        self.treeview_tlServicos .heading("ID", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlServicos , 0))
        
        self.treeview_tlServicos .heading("CodServ", text="CodServ", anchor="center")
        self.treeview_tlServicos .heading("CodServ", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlServicos , 1))
        
        self.treeview_tlServicos .heading("DescrServico", text="DescrServico", anchor="center")
        self.treeview_tlServicos .heading("DescrServico", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlServicos , 2))
        
        self.treeview_tlServicos .heading("ValorUnit", text="ValorUnit", anchor="center")
        self.treeview_tlServicos .heading("ValorUnit", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlServicos , 3))
        #----------------------- *********************************************-----------------------#
        
        
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
            validatecommand=(verificaInteger, "%P")
        )

        #self.inputNotasIsentas_tlCadCliente.pack()
            
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
        
        self.mostrarTabelaClientes_TelaCadClientes()
        
        #----------------------- ORDENANDO POR CLIQUE NO CABEÇALHO TB CLIENTES-----------------------#
        self.treeview_tlClientes.heading("ID", text="ID", anchor="center")
        self.treeview_tlClientes.heading("ID", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlClientes, 0))
        
        self.treeview_tlClientes.heading("CodCliente", text="CodCliente", anchor="center")
        self.treeview_tlClientes.heading("CodCliente", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlClientes, 1))
        
        self.treeview_tlClientes.heading("Cliente", text="Cliente", anchor="center")
        self.treeview_tlClientes.heading("Cliente", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlClientes, 2))
        
        self.treeview_tlClientes.heading("NFIsenta", text="NFIsenta", anchor="center")
        self.treeview_tlClientes.heading("NFIsenta", command=lambda: self.ordenarPeloCabecalhoTreview(self.treeview_tlClientes, 3))
        #----------------------- *********************************************-----------------------#
        
        self.tlClientes.resizable(False, False)
        self.tlClientes.mainloop()
        ########## FIM TABELA CLIENTES ##########
        
        
    #@@@@@@@@@@@@@@@@ FUNÇÕES TELA LOGIN @@@@@@@@@@@@@@@@@@@#
    
    def verificar_usuario_existente(self):
        """
        Verifica se o usuário e senha fornecidos existem no sistema e realiza o login, ou cria um novo usuário se não existir.

        Returns:
            str: O nome do usuário logado após a autenticação.

        Note:
            Este método verifica se o usuário e senha fornecidos existem no sistema.
            Se existirem, realiza o login e retorna o nome do usuário logado.
            Se não existirem, cria um novo usuário, realiza o login e retorna o nome do usuário logado.
        """
        # Obtém o nome de usuário e senha dos campos de entrada
        input_usuario = self.input_login_usuario.get().strip().upper()
        input_senha = self.input_login_senha.get().strip().upper()

        # Verifica se o usuário e senha existem no sistema
        if self.user_manager.checkUsernameAndPasswordRegistered(input_usuario, input_senha):
            self.tela_login.destroy()
            self.usuarioLogado = input_usuario
            return self.usuarioLogado  # Retorna o nome do usuário logado
        else:
            # Se o usuário não existir, registra um novo usuário
            self.user_manager.registerNewUser(input_usuario, input_senha)
            self.mostrar_alerta("Cadastro de Usuário", f" ☻ Usuário(a) {input_usuario} cadastrado com sucesso!")
            self.tela_login.destroy()
            self.usuarioLogado = input_usuario
            return self.usuarioLogado  # Retorna o nome do usuário logado
 
    #@@@@@@@@@@@@@@@@ FUNÇÕES TELA PRINCIPAL ORDEM DE SERVIÇOS @@@@@@@@@@@@@@@@@#
    
    def pegandoValoresTelaPrincipalOS(self):
        """
        Obtém os valores inseridos na tela principal de Ordens de Serviço.

        Returns:
            tuple: Uma tupla contendo os valores inseridos na tela, incluindo:
                - os_dtServico (str): Data do serviço.
                - os_codCliente (int): Código do cliente.
                - os_cliente (str): Nome do cliente.
                - os_codServico (int): Código do serviço.
                - os_descrServico (str): Descrição do serviço.
                - os_quantidade (int): Quantidade do serviço.
                - os_vlrUnit (str): Valor unitário do serviço.
                - os_total (float): Valor total do serviço.
                - os_descComplementar (str): Descrição complementar do serviço.
                - os_faturado (str): Indicação se o serviço está faturado ("SIM" ou "NÃO").

        Note:
            Os valores são obtidos a partir dos campos preenchidos na tela principal de Ordens de Serviço.

        Example:
            Os valores podem ser obtidos da seguinte forma:
            os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_faturado, os_descComplementar = pegandoValoresTelaPrincipalOS()
        """
        os_dtServico = self.input_DataOS.get()  # Obtém a data do serviço
        os_codCliente = int(self.input_CodCliente.get().strip())  # Obtém o código do cliente
        os_cliente = self.input_Cliente.get().strip().upper()  # Obtém o nome do cliente
        os_codServico = int(self.input_CodServ.get().strip())  # Obtém o código do serviço
        os_descrServico = self.input_DescricaoServ.get().strip().upper()  # Obtém a descrição do serviço
        os_quantidade = int(self.input_Quantidade.get())  # Obtém a quantidade do serviço
        os_vlrUnit = self.input_VlrUnitario.get()  # Obtém o valor unitário do serviço
        os_total = float(self.input_VlrTotal.get())  # Obtém o valor total do serviço
        os_descComplementar = self.input_DescrCompl.get('1.0', 'end-1c').upper()  # Obtém a descrição complementar do serviço
        os_faturado = self.input_Faturado.get()  # Obtém a indicação de faturamento do serviço

        return os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_faturado, os_descComplementar

    def pegarValoresLinhaSelecionadaDaTabelaOrdemServico(self):
        """
        Obtém os valores da linha selecionada na tabela de Ordens de Serviço da tela principal.

        Returns:
            tuple: Uma tupla contendo os valores da linha selecionada, incluindo:
                - os_id (int): ID da Ordem de Serviço.
                - os_dtServico (str): Data do serviço.
                - os_codCliente (int): Código do cliente.
                - os_cliente (str): Nome do cliente.
                - os_codServico (int): Código do serviço.
                - os_descrServico (str): Descrição do serviço.
                - os_quantidade (float): Quantidade do serviço.
                - os_vlrUnit (float): Valor unitário do serviço.
                - os_total (float): Valor total do serviço.
                - os_descComplementar (str): Descrição complementar do serviço.
                - os_faturado (str): Indicação se o serviço está faturado ("SIM" ou "NÃO").
                - os_dtFaturamento (str): Data de faturamento.
                - os_usuario (str): Nome do usuário responsável.

        Note:
            Os valores são obtidos da linha selecionada na tabela de Ordens de Serviço.
        """
        itemSelecionadoTbOrdemServicos = self.treeviewTelaPrincipal.selection()
        item = self.treeviewTelaPrincipal.item(itemSelecionadoTbOrdemServicos, 'values')
        os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado, os_dtFaturamento, os_usuario = item
        return os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado, os_dtFaturamento, os_usuario
    
    def _verificarSeCamposTelaOrdemServicosPreenchidos(self):
        """
        Função responsável por verificar se todos os campos na tela de cadastro de Ordens de Serviço estão preenchidos.

        Returns:
            bool: True se todos os campos estiverem preenchidos, False caso contrário.
        """
        # Obtém os valores dos campos da tela
        os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado = self.pegandoValoresTelaPrincipalOS()
        
        # Lista de verificações de campos individuais
        campos_preenchidos = [
            bool(os_dtServico),
            bool(os_codCliente),
            bool(os_cliente),
            bool(os_codServico),
            bool(os_descrServico),
            bool(os_quantidade),
            bool(os_vlrUnit),
            bool(os_total),
            bool(os_faturado),
            bool(os_descComplementar)
        ]

        # Verifica se todos os campos estão preenchidos
        return all(campos_preenchidos)
    
    def _limparTelaPrincipal(self):
        """
        Função responsável por limpar os campos de entrada e seleção da tela principal de cadastro de Ordens de Serviço.

        Returns:
            None
        """
        # Limpa os campos de entrada
        self.input_CodCliente.delete(0,'end')
        self.input_Cliente.delete(0, 'end')
        self.input_CodServ.delete(0, 'end')
        self.input_DescricaoServ.delete(0,'end')
        self.input_Quantidade.delete(0, 'end')
        self.input_VlrUnitario.delete(0, 'end')
        self.input_VlrTotal.delete(0, 'end')
        self.input_Faturado.delete(0, 'end')
 
    # FUNÇÃO BOTÃO MODIFICAR TELA PRINCIPAL
    def modificarItemSelecionadoDaTabOrdemServico(self): 
        """
        Função responsável por preencher os campos de edição com os valores da Ordem de Serviço selecionada na tabela
        e criar um botão "Salvar Modificações" para permitir a edição dos dados da Ordem de Serviço.

        Returns:
            bool: True se os campos foram preenchidos com sucesso, False caso contrário.
        """
        try:
            # Passo 1: Obtém os valores da linha selecionada na tabela de Ordem de Serviço
            os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado, os_dtFaturamento, os_usuario = self.pegarValoresLinhaSelecionadaDaTabelaOrdemServico()
            
            # Passo 2: Verificar se a Ordem de Serviço já foi faturada, se sim, impedir a modificação
            if os_faturado == 'SIM':
                self.mostrar_alerta("Atenção", "Este serviço já foi faturado, NÃO é possível modificar")
                return False
            
            # Passo 3: Preenche os campos de edição com os valores do item selecionado na lista
            self.input_DataOS.delete(0, 'end')
            self.input_DataOS.insert(0, os_dtServico)
            
            self.input_CodCliente.delete(0, 'end')  
            self.input_CodCliente.insert(0, os_codCliente)
            
            self.input_CodServ.delete(0, 'end')
            self.input_CodServ.insert(0, os_codServico)
            
            self.input_Quantidade.delete(0, 'end')
            self.input_Quantidade.insert(0, os_quantidade)
            
            self.input_VlrUnitario.delete(0, 'end')
            self.input_VlrUnitario.insert(0, os_vlrUnit)
            
            self.input_VlrTotal.delete(0, 'end')
            self.input_VlrTotal.insert(0, os_total)
            
            # Passo 4: Remove os botões anteriores e cria um botão "Salvar Modificações"
            self._apagarListaBotoes(self.botoesParaOcultar_TelaPrincipal)
            self._criarBotaoSalvarModificacoes(self.telaPrincipal, self.validarModificacoesTelaPrincipal, 654, 187, 105, 50, "./img/img_tlPrincipal_btnSalvarModificacao.png")
            
            # Passo 5: Retorna True para indicar que os campos foram preenchidos com sucesso
            return True
            
        except Exception as e:
            # Passo 6: Obter a traceback do erro
            traceback_str = traceback.format_exc()

            # Passo 7: Exibir a mensagem de erro e a traceback em caso de falha
            self.mostrar_alerta('Erro', f'O seguinte erro ocorreu:\n{e}\n\nTraceback:\n{traceback_str}')
            return False
        
    # FUNÇÃO BOTÃO SALVAR MODIFICAÇÕES TELA PRINCIPAL   
    def validarModificacoesTelaPrincipal(self):
        """
        Função responsável por validar e salvar as modificações feitas em uma Ordem de Serviço na tela principal.

        Returns:
            bool: True se as modificações foram salvas com sucesso, False caso contrário.
        """
        try:
            # Passo 1: Obter os valores da tela principal
            dtServico, codCliente, cliente, codServico, descrServico, quantidade, vlrUnit, total, descComplementar, faturado = self.pegandoValoresTelaPrincipalOS()
            
            # Passo 2: Formatar o valor unitário substituindo "," por "."
            vlrUnit = vlrUnit.replace(",", ".")           
            
            # Passo 3: Verificar se todos os campos obrigatórios estão preenchidos
            if not self._verificarSeCamposTelaOrdemServicosPreenchidos:
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                return False
            
            # Passo 4: Obter a Ordem de Serviço selecionada na tabela
            os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado, os_dtFaturamento, os_usuario = self.pegarValoresLinhaSelecionadaDaTabelaOrdemServico()
            
            # Passo 5: Modificar a Ordem de Serviço no banco de dados
            self.manipular_ordens.editarOrdemServicoPeloIDOrdensServicosDB(
                os_id, dtServico, codCliente, cliente, codServico, descrServico, quantidade, vlrUnit, total, faturado, descComplementar)
            
            # Passo 6: Atualizar a tela de cadastro e limpar os campos
            self._limparTelaPrincipal()
            self._atualizarTelaPrincipal()
            
            # Passo 7: Retornar True para indicar que as modificações foram salvas com sucesso
            return True
        except Exception as e:
            traceback_str = traceback.format_exc()
            # Passo 8: Exibir a mensagem de erro e a traceback em caso de falha
            self.mostrar_alerta('Erro', f'Erro ao salvar alteração na Ordem de Serviços:\n{e}\n\nTraceback:\n{traceback_str}')
            return False
            
    def _preencherFaturado(self, faturado):
        """
        Função interna responsável por preencher o campo de faturado com um valor especificado.

        Args:
            faturado (str): O valor de faturado a ser preenchido no campo.

        Returns:
            None
        """
        # Torna o campo de faturado editável
        self.input_Faturado.configure(state="normal")
        
        # Limpa o campo de faturado
        self.input_Faturado.delete(0, END)
        
        # Insere o valor de faturado especificado no campo de faturado
        self.input_Faturado.insert(0, faturado)
        
        # Torna o campo de faturado somente leitura novamente
        self.input_Faturado.configure(state="readonly")      
    
    def preencheCliente(self, event):
        """
        Função responsável por preencher o campo de cliente com o nome do cliente correspondente ao código inserido.

        Args:
            event (Event): O evento que acionou a função, geralmente associado à tecla "Tab".

        Returns:
            None
        """
        # Passo 1: Verifica se o evento foi acionado pela tecla "Tab".
        if event.keysym == "Tab":
            # Passo 2: Consulta a tabela de clientes para obter a lista de códigos de cliente e nomes de cliente.
            list_tb_cliente = self.manipular_ordens.consultarCompletaTabelaClientes()
            
            # Passo 3: Obtém o código de cliente inserido pelo usuário.
            input_codCliente = int(self.input_CodCliente.get())
            
            # Passo 4: Itera sobre a lista de clientes para encontrar o cliente com o código correspondente.
            for index, cliente in enumerate(list_tb_cliente):
                codCliente = int(cliente[1])
                nomeCliente = str(cliente[2])
                
                if codCliente == input_codCliente:
                    # Passo 5: Se encontrar o cliente, preenche o campo de cliente com o nome correspondente.
                    self.input_Cliente.configure(state="normal")
                    self.input_Cliente.delete(0, END)
                    self.input_Cliente.insert(0, nomeCliente)
                    self.input_Cliente.configure(state="readonly")
                    self._preencherFaturado('NÃO')
                    break
            else:
                # Passo 6: Se o código de cliente não existir na lista, exibe um alerta informando que o cliente não está cadastrado.
                self.mostrar_alerta('Aviso', f'Cliente não cadastrado!')
       
    def _preencherDescricaoServicos(self, descricao):
        """
        Função interna responsável por preencher o campo de descrição de serviços com uma descrição especificada.

        Args:
            descricao (str): A descrição do serviço a ser preenchida no campo.

        Returns:
            None
        """
        # Torna o campo de descrição de serviços editável
        self.input_DescricaoServ.configure(state="normal")
        
        # Limpa o campo de descrição de serviços
        self.input_DescricaoServ.delete(0, END)
        
        # Insere a descrição especificada no campo de descrição de serviços
        self.input_DescricaoServ.insert(0, descricao)
        
        # Torna o campo de descrição de serviços somente leitura novamente
        self.input_DescricaoServ.configure(state="readonly")
    
    def _preencherValorUnitario(self, valor_unitario):
        """
        Função interna responsável por preencher o campo de valor unitário com um valor especificado.

        Args:
            valor_unitario (float): O valor unitário a ser preenchido no campo.

        Returns:
            None
        """
        # Limpa o campo de valor unitário
        self.input_VlrUnitario.delete(0, END)
        
        # Insere o valor unitário especificado no campo
        self.input_VlrUnitario.insert(0, valor_unitario) 
        
    def preencheDescrServicoEvalorUnitario(self, event):
        """
        Função responsável por preencher a descrição do serviço e o valor unitário com base no código do serviço.

        Esta função é acionada quando a tecla "Tab" é pressionada em um campo específico (evento "Tab").
        Ela realiza as seguintes etapas:
        1. Verifica se o evento foi acionado pela tecla "Tab".
        2. Consulta a tabela de serviços e valores para obter a lista de códigos de serviço, descrições e valores unitários.
        3. Obtém o código de serviço inserido pelo usuário.
        4. Itera sobre a lista de serviços para encontrar o serviço com o código correspondente.
        5. Se encontrar o serviço, preenche a descrição do serviço e o valor unitário nos campos apropriados.
        6. Se o código de serviço não existir na lista, exibe um alerta informando que o serviço não está cadastrado.

        Args:
            event (Event): O evento que acionou a função, geralmente associado à tecla "Tab".

        Returns:
            None
        """
        # Passo 1: Verifica se o evento foi acionado pela tecla "Tab".
        if event.keysym == "Tab":
            # Passo 2: Consulta a tabela de serviços e valores para obter a lista de códigos de serviço, descrições e valores unitários.
            l_codServDescrServVlrUnit = self.manipular_ordens.consultarCompletaTabelaServicosValores()
            
            # Passo 3: Obtém o código de serviço inserido pelo usuário.
            input_codServ = int(self.input_CodServ.get())
            
            # Passo 4: Itera sobre a lista de serviços para encontrar o serviço com o código correspondente.
            for index, servicos in enumerate(l_codServDescrServVlrUnit):
                codServ = int(servicos[1])
                descrServ = str(servicos[2])
                valorUnit = servicos[3]
                
                if codServ == input_codServ:
                    # Passo 5: Se encontrar o serviço, preenche a descrição do serviço e o valor unitário nos campos apropriados.
                    self._preencherDescricaoServicos(descrServ)
                    self._preencherValorUnitario(valorUnit)
                    break
            else:
                # Passo 6: Se o código de serviço não existir na lista, exibe um alerta informando que o serviço não está cadastrado.
                self.mostrar_alerta('Aviso', f'Serviço não cadastrado!')

    def preencherValorTotal(self, event):
        """
        Função responsável por calcular e preencher o valor total com base na quantidade e no valor unitário.

        Esta função é acionada quando a tecla "Tab" é pressionada em um campo específico (evento "Tab").
        Ela realiza as seguintes etapas:
        1. Verifica se o evento foi acionado pela tecla "Tab".
        2. Obtém a quantidade e o valor unitário dos campos correspondentes.
        3. Calcula o valor total multiplicando a quantidade pelo valor unitário.
        4. Arredonda o valor total para duas casas decimais.
        5. Atualiza o campo de valor total com o valor calculado e o torna somente leitura.

        Args:
            event (Event): O evento que acionou a função, geralmente associado à tecla "Tab".

        Returns:
            None
        """
        # Passo 1: Verifica se o evento foi acionado pela tecla "Tab".
        if event.keysym == "Tab":
            # Passo 2: Obtém a quantidade e o valor unitário dos campos correspondentes.
            quantidade = int(self.input_Quantidade.get())
            vlrUnitario = float(self.input_VlrUnitario.get())
            
            # Passo 3: Calcula o valor total multiplicando a quantidade pelo valor unitário.
            calcularVlrTotal = quantidade * vlrUnitario
            vlrTotalArredondado = round(calcularVlrTotal, 2)
            
            # Passo 4: Atualiza o campo de valor total com o valor calculado e o torna somente leitura.
            self.input_VlrTotal.configure(state="normal")
            self.input_VlrTotal.delete(0, END)
            self.input_VlrTotal.insert(0, vlrTotalArredondado)
            self.input_VlrTotal.configure(state="readonly")
            
    def cadastrarOrdemServicos(self):
        """
        Função responsável por cadastrar uma ordem de serviço na tela principal do aplicativo.

        Esta função realiza as seguintes etapas:
        1. Obtém os valores dos campos da tela de ordem de serviço usando a função interna `pegandoValoresTelaPrincipalOS`.
        2. Obtém o nome de usuário logado.
        3. Verifica se todos os campos obrigatórios estão preenchidos chamando a função interna `_verificarSeCamposTelaOrdemServicosPreenchidos`.
        4. Insere a ordem de serviço no banco de dados chamando a função `inserirOrdemServicosDB` do objeto `self.manipular_ordens`.
        5. Exibe um alerta de sucesso se o cadastro for bem-sucedido.
        6. Atualiza a tela principal chamando a função interna `_atualizarTelaPrincipal`.

        Returns:
            None
        """
        try:
            # Passo 1: Obtém os valores dos campos da tela de ordem de serviço usando a função interna `pegandoValoresTelaPrincipalOS`.
            os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado  = self.pegandoValoresTelaPrincipalOS()
            
            # Obtém o nome de usuário logado.
            nomeUsuario = self.usuarioLogado 
            
            # Passo 3: Verifica se todos os campos obrigatórios estão preenchidos chamando a função interna `_verificarSeCamposTelaOrdemServicosPreenchidos`.
            if self._verificarSeCamposTelaOrdemServicosPreenchidos():
                # Passo 4: Insere a ordem de serviço no banco de dados chamando a função `inserirOrdemServicosDB` do objeto `self.manipular_ordens`.
                self.manipular_ordens.inserirOrdemServicosDB(os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_faturado, os_descComplementar, nomeUsuario)

                # Passo 5: Exibe um alerta de sucesso se o cadastro for bem-sucedido.
                self.mostrar_alerta('Sucesso', 'Serviço inserido com sucesso!')
                
                # Passo 6: Atualiza a tela principal chamando a função interna `_atualizarTelaPrincipal`.
                self._atualizarTelaPrincipal()
                
        except Exception as e:
            self.mostrar_alerta('Erro de Preenchimento', f'Preencha todos os campos! {e}')
  
    def fechar_TelaPrincipal(self):
        """
        Função responsável por fechar a tela principal do aplicativo.

        Esta função realiza as seguintes etapas:
        1. Destroi a janela da tela principal, encerrando a aplicação.

        Returns:
            None
        """
        # Passo 1: Destroi a janela da tela principal, encerrando a aplicação.
        self.telaPrincipal.destroy()
    
    def mostrarOrdensServico_TelaPrincipal(self):
        """
        Função responsável por exibir as ordens de serviço na Treeview da tela principal.

        Esta função realiza as seguintes etapas:
        1. Obtém um cursor para interagir com o banco de dados.
        2. Executa uma consulta SQL para selecionar todas as ordens de serviço ordenadas pelo ID em ordem crescente.
        3. Recupera os resultados da consulta.
        4. Limpa a Treeview para remover todos os registros existentes.
        5. Itera sobre os resultados da consulta e adiciona cada ordem de serviço à Treeview.
        6. Redimensiona as colunas da Treeview para ajustar o conteúdo exibido.

        Returns:
            None
        """
        # Passo 1: Obtém um cursor para interagir com o banco de dados.
        cursor = self.db_manager.get_cursor()

        # Passo 2: Executa uma consulta SQL para selecionar todas as ordens de serviço ordenadas pelo ID em ordem crescente.
        cursor.execute("SELECT * FROM tb_ordens_servicos ORDER BY os_id ASC")

        # Passo 3: Recupera os resultados da consulta.
        resultados = cursor.fetchall()

        # Passo 4: Limpa a Treeview para remover todos os registros existentes.
        self.treeviewTelaPrincipal.delete(*self.treeviewTelaPrincipal.get_children())

        # Passo 5: Itera sobre os resultados da consulta e adiciona cada ordem de serviço à Treeview.
        for resultado in resultados:
            os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_observacao, os_faturado, os_dtFaturamento, os_usuario = resultado
            
            self.treeviewTelaPrincipal.insert("", "0", values=(os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_observacao, os_faturado, os_dtFaturamento, os_usuario))
        
        # Passo 6: Redimensiona as colunas da Treeview para ajustar o conteúdo exibido.
        self.ajustarLarguraColunaTreeview(self.treeviewTelaPrincipal)

        
    def gerarRelatorioOrdensGeral(self):
        """
        Função responsável por gerar um relatório geral de todas as ordens de serviço.

        Esta função realiza as seguintes etapas:
        1. Chama a função `gerarRelatorioOdensServicoTodas` do objeto `self.manipular_relatorios`.
        2. Especifica o nome do arquivo de saída como 'Relatorio geral de retrabalho.pdf'.

        Returns:
            None
        """
        # Passo 1: Chama a função `gerarRelatorioOdensServicoTodas` do objeto `self.manipular_relatorios`.
        self.manipular_relatorios.gerarRelatorioOdensServicoTodas('Relatorio geral de retrabalho.pdf')

    #FUNÇÃO BOTÃO DELETAR NA TELA PRINCIPAL ORDEM DE SERVIÇOS
    def deletarOrdemServico_TelaPrincipal(self):
        """
        Deleta uma ordem de serviço da tabela na principal.

        Este método permite a exclusão de uma ordem de serviço selecionado da tabela de ordem de serviço.
        Ele confirma a exclusão com o usuário, realiza a exclusão no banco de dados e atualiza a tabela.

        Parâmetros:
        Nenhum

        Retorna:
        Nenhum
        """
        # Obtém o item selecionado na tabela
        selected_item = self.treeviewTelaPrincipal.selection()
        
        # Verifica se algum item foi selecionado
        if not selected_item:
            self.mostrar_alerta("Nenhum item selecionado", "Por favor, selecione um item para deletar.")
            self._atualizarTelaPrincipal()
            return
                
        # Obtém informações do item selecionado
        os_id,os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total, os_descComplementar, os_faturado, os_dtFaturamento, os_usuario = self.pegarValoresLinhaSelecionadaDaTabelaOrdemServico()
        
        if os_faturado == 'SIM':
            self.mostrar_alerta("Atenção", "Este serviço já foi faturado, NÃO é possível deletá-lo")
            return
        
        # Confirmação de exclusão com o usuário
        if self.confirmar_solicitacao("Confirmar Exclusão", {'Tem certeza que deseja excluir o cliente: '}, {os_dtServico, os_codCliente, os_cliente, os_codServico, os_descrServico, os_quantidade, os_vlrUnit, os_total}):
            
            # Deleta o serviço do banco de dados
            if self.manipular_ordens.deletarOrdemServicoDB(os_id):
                # Remove o item da tabela
                self.treeviewTelaPrincipal.delete(selected_item)
                self.mostrar_sucesso(f'Exclusão bem sucedida do seguinte serviço: -> Cliente: {os_cliente}, -> Serviço: {os_descrServico}, -> Valor Total: {os_total}')
            else:
                self.mostrar_erro("Ocorreu um erro ao tentar deletar Ordem de Serviços.")
        else:
            self.mostrar_alerta("Cancelado", "A exclusão foi cancelada pelo usuário.")
        
        # Atualiza a tela de cadastro de serviços
        self._atualizarTelaPrincipal()
    
    def _atualizarTelaPrincipal(self):
        """
        Função interna responsável por atualizar a tela principal do aplicativo.

        Esta função realiza as seguintes etapas:
        1. Fecha a tela principal atual chamando a função interna `fechar_TelaPrincipal`.
        2. Cria uma nova tela principal chamando a função interna `criar_TelaPrincipal`.

        Returns:
            None
        """
        # Passo 1: Fecha a tela principal atual chamando a função interna `fechar_TelaPrincipal`.
        self.fechar_TelaPrincipal()
        
        # Passo 2: Cria uma nova tela principal chamando a função interna `criar_TelaPrincipal`.
        self.criar_TelaPrincipal()

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
        """
        Função responsável por verificar se um código de serviço já existe na tela de cadastro de serviços.

        Esta função realiza as seguintes etapas:
        1. Chama a função interna `_verificarSeCodigoServicoJaExiste` para realizar a verificação.
        2. Se o código de serviço já existir, exibe um alerta, atualiza a tela de cadastro de serviços e retorna False.

        Args:
            codServico (str): O código de serviço a ser verificado.

        Returns:
            bool: True se o código de serviço não existir, False caso contrário.
        """
        # Passo 1: Chama a função interna `_verificarSeCodigoServicoJaExiste` para realizar a verificação.
        if self._verificarSeCodigoServicoJaExiste():
            # Passo 2: Se o código de serviço já existir, exibe um alerta, atualiza a tela de cadastro de serviços e retorna False.
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
        Função responsável por deletar um serviço da tela de cadastro de serviços.

        Esta função realiza as seguintes etapas:
        1. Obtém o item selecionado na tabela de serviços.
        2. Verifica se algum item foi selecionado; caso contrário, exibe um alerta.
        3. Obtém informações do item selecionado (ID, código de serviço, descrição do serviço e valor unitário).
        4. Solicita confirmação ao usuário para a exclusão do serviço.
        5. Se confirmado, deleta o serviço do banco de dados.
        6. Se a exclusão no banco de dados for bem-sucedida, remove o item da tabela.
        7. Exibe uma mensagem de sucesso.
        8. Se ocorrer um erro na exclusão, exibe uma mensagem de erro.
        9. Se o usuário cancelar a exclusão, exibe uma mensagem de alerta.
        10. Atualiza a tela de cadastro de serviços.

        Returns:
            None
        """
        # Passo 1: Obtém o item selecionado na tabela de serviços.
        selected_item = self.treeview_tlServicos.selection()
        
        # Passo 2: Verifica se algum item foi selecionado; caso contrário, exibe um alerta.
        if not selected_item:
            self.mostrar_alerta("Nenhum item selecionado", "Por favor, selecione um item para deletar.")
            self._atualizarTelaCadServ()
            return
        
        # Passo 3: Obtém informações do item selecionado (ID, código de serviço, descrição do serviço e valor unitário).
        serv_id, serv_codServ, serv_descServico, serv_vlrUnit = self.pegarValoresLinhaSelecionadaDaTabelaServicos()
        
        # Passo 4: Solicita confirmação ao usuário para a exclusão do serviço.
        if self.confirmar_solicitacao(f"Confirmar Exclusão", 'Tem certeza que deseja excluir o serviço:', {serv_codServ, serv_descServico}):
            # Passo 5: Deleta o serviço do banco de dados.
            if self.manipular_ordens.deletarServicoDB(serv_id):
                # Passo 6: Se a exclusão no banco de dados for bem-sucedida, remove o item da tabela.
                self.treeview_tlServicos.delete(selected_item)
                # Passo 7: Exibe uma mensagem de sucesso.
                self.mostrar_sucesso(serv_codServ, serv_descServico, serv_vlrUnit)
            else:
                # Passo 8: Se ocorrer um erro na exclusão, exibe uma mensagem de erro.
                self.mostrar_erro("Ocorreu um erro ao tentar deletar o serviço.")
        else:
            # Passo 9: Se o usuário cancelar a exclusão, exibe uma mensagem de alerta.
            self.mostrar_alerta("Cancelado", "A exclusão foi cancelada pelo usuário.")
        
        # Passo 10: Atualiza a tela de cadastro de serviços.
        self._atualizarTelaCadServ()

    ###FUNÇÕES PARA MODIFICAR
    def pegarValoresLinhaSelecionadaDaTabelaServicos(self):
        """
        Função responsável por obter os valores da linha selecionada na tabela de serviços na tela de cadastro de serviços.

        Esta função realiza as seguintes etapas:
        1. Obtém o item (valores da linha) da tabela de serviços selecionado.
        2. Extrai os valores do item, que representam as informações do serviço (ID, código de serviço, descrição do serviço e valor unitário).
        3. Retorna os valores obtidos em uma tupla.

        Returns:
            Tuple[int, str, str, float]: Uma tupla contendo os valores da linha selecionada na seguinte ordem:
            (ID do serviço, código de serviço, descrição do serviço, valor unitário).
        """
        # Passo 1: Obtém o item (valores da linha) da tabela de serviços selecionado.
        itemSelecionadoTbServicos = self.treeview_tlServicos.selection()
        item = self.treeview_tlServicos.item(itemSelecionadoTbServicos, 'values')
        
        # Passo 2: Extrai os valores do item, que representam as informações do serviço.
        serv_id, serv_codServ, serv_descServico, serv_vlrUnit = item
        
        # Passo 3: Retorna os valores obtidos em uma tupla.
        return serv_id, serv_codServ, serv_descServico, float(serv_vlrUnit)
    
    def _desabilitar_inputCodServ(self):
        """
        Função interna responsável por desabilitar o campo de código de serviço na tela de cadastro de serviços.

        Esta função realiza as seguintes etapas:
        1. Desabilita o campo de código de serviço.
        2. Altera a cor de fundo do campo para uma cor mais escura.

        Returns:
            None
        """
        # Passo 1: Desabilita o campo de código de serviço.
        self.inputCodServ_tlCadServ.config(state="disabled")
        
        # Passo 2: Altera a cor de fundo do campo para uma cor mais escura.
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
            self._criarBotaoSalvarModificacoes(self.tlServicos, self.validarModificacoesTelaCadServ, 349, 115, 139, 30, "./img/img_btnSalvarModificacoes.png")
            
            return True
        
        except Exception as e:
            # Exibe uma mensagem de alerta e recria a tela caso ocorra um erro
            self.mostrar_alerta('Atenção', f'Selecione uma linha da tabela abaixo:/n{e}')
            self.fechar_TelaCadServ()
            self.criar_TelaCadServ() 
            return False
    
    # FUNÇÃO BOTÃO SALVAR MODIFICAÇÕES    
    def validarModificacoesTelaCadServ(self):
        """
        Função responsável por validar e salvar as modificações na tela de cadastro de serviços.

        Esta função realiza as seguintes etapas:
        1. Obtém os valores dos campos da tela de cadastro de serviços (código de serviço, descrição do serviço e valor unitário).
        2. Realiza validações para verificar se todos os campos obrigatórios estão preenchidos.
        3. Obtém os valores do serviço selecionado na tabela.
        4. Modifica o serviço no banco de dados com os novos valores.
        5. Se a modificação for bem-sucedida, limpa os campos e atualiza a tela de cadastro de serviços.
        6. Retorna True se a modificação for bem-sucedida, False caso contrário.

        Returns:
            bool: True se a modificação for bem-sucedida, False caso contrário.
        """
        try:
            # Passo 1: Obtém os valores dos campos da tela de cadastro de serviços.
            codServico, descServico, vlrUnit = self.pegarValoresTelaCadServico()
            codServico = codServico.strip()
            descServico = descServico.strip().upper()
            vlrUnit = vlrUnit.replace(",", ".")           
            
            # Passo 2: Realiza validações para verificar se todos os campos obrigatórios estão preenchidos.
            if not codServico or not descServico or not vlrUnit:
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                return False
            
            # Passo 3: Obtém os valores do serviço selecionado na tabela.
            serv_id, serv_codServ, serv_descServico, serv_vlrUnit = self.pegarValoresLinhaSelecionadaDaTabelaServicos()
            
            # Passo 4: Modifica o serviço no banco de dados com os novos valores.
            if self.manipular_ordens.editarServicoPeloIDServicosValoresDB(serv_id, codServico, descServico, vlrUnit):
                # Passo 5: Se a modificação for bem-sucedida, limpa os campos e atualiza a tela de cadastro de serviços.
                self._limparTelaCadServ()
                self._atualizarTelaCadServ()
                return True
            else:
                return False
        except Exception as e:
            # Passo 6: Em caso de erro, exibe uma mensagem de alerta e retorna False.
            self.mostrar_alerta("Erro", f"Erro ao salvar: {e}")
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
        self.ajustarLarguraColunaTreeview(self.treeview_tlServicos)  # Redimensiona as colunas da tabela
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
        """
        Função responsável por abrir a tela de cadastro de clientes.

        Esta função realiza o seguinte passo:
        1. Chama a função interna `criar_TelaCadClientes` para criar a tela de cadastro de clientes.

        Args:
            event (Tkinter Event, optional): Um evento (geralmente associado a um botão) que aciona a abertura da tela. O padrão é None.

        Returns:
            None
        """
        # Passo 1: Chama a função interna `criar_TelaCadClientes` para criar a tela de cadastro de clientes.
        self.criar_TelaCadClientes()

    # MOSTRAR A TABELA NA TELA CADASTRO DE CLIENTES        
    def mostrarTabelaClientes_TelaCadClientes(self):
        """
        Função responsável por atualizar e mostrar a tabela(treeview) de clientes na tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Limpa os dados existentes na tabela de clientes.
        2. Realiza uma consulta à tabela de CLIENTES para obter os registros.
        3. Itera sobre os resultados da consulta e insere cada registro na tabela de clientes.

        Returns:
            None
        """
        # Passo 1: Limpa os dados existentes na tabela de clientes.
        self.treeview_tlClientes.delete(*self.treeview_tlClientes.get_children())

        # Passo 2: Realiza a consulta à tabela de CLIENTES para obter os registros.
        listandoClientes = self.manipular_ordens.consultarCompletaTabelaClientes()

        # Passo 3: Itera sobre os resultados da consulta e insere cada registro na tabela de clientes.
        for resultado in listandoClientes:
            cli_id, codCliente, nomeCliente, qtdNFisenta = resultado

            # Insere uma nova linha na tabela com os valores obtidos.
            self.treeview_tlClientes.insert("", "end", values=(cli_id, codCliente, nomeCliente, qtdNFisenta))

    def fechar_TelaCadCliente(self):
        """
        Função responsável por fechar a janela da tela de cadastro de clientes.

        Esta função realiza o seguinte passo:
        1. Destroi a janela da tela de cadastro de clientes.

        Returns:
            None
        """
        # Passo 1: Destroi a janela da tela de cadastro de clientes.
        self.tlClientes.destroy()
    
    def _limparTelaCadCliente(self):
        """
        Função interna responsável por limpar os campos da tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Remove o conteúdo do campo "Código de Cliente".
        2. Remove o conteúdo do campo "Nome do Cliente".
        3. Remove o conteúdo do campo "Quantidade de Notas Fiscais Isentas".

        Returns:
            None
        """
        # Passo 1: Remove o conteúdo do campo "Código de Cliente".
        self.inputCodCliente_tlCadCliente.delete(0, 'end')  
        
        # Passo 2: Remove o conteúdo do campo "Nome do Cliente".
        self.inputNomeCliente_tlCadCliente.delete(0, 'end')
        
        # Passo 3: Remove o conteúdo do campo "Quantidade de Notas Fiscais Isentas".
        self.inputNotasIsentas_tlCadCliente.delete(0, 'end')
        
    def _atualizarTelaCadCliente(self):
        """
        Função interna responsável por atualizar a tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Redimensiona as colunas da tabela de clientes na tela.
        2. Mostra a tabela de clientes na tela de cadastro de clientes.
        3. Fecha a tela de cadastro de clientes.
        4. Recria a tela de cadastro de clientes.

        Returns:
            None
        """
        # Passo 1: Redimensiona as colunas da tabela de clientes na tela.
        self.ajustarLarguraColunaTreeview(self.treeview_tlClientes)
        
        # Passo 2: Mostra a tabela de clientes na tela de cadastro de clientes.
        self.mostrarTabelaClientes_TelaCadClientes()
        
        # Passo 3: Fecha a tela de cadastro de clientes.
        self.fechar_TelaCadCliente()
        
        # Passo 4: Recria a tela de cadastro de clientes.
        self.abrirTelaCadCliente()

    def pegarValoresTelaCadClientes(self):
        """
        Função responsável por obter os valores dos campos na tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Obtém o valor do campo "Código de Cliente".
        2. Obtém o valor do campo "Nome do Cliente".
        3. Obtém o valor do campo "Quantidade de Notas Fiscais Isentas".
        4. Se o campo "Quantidade de Notas Fiscais Isentas" estiver vazio, define o valor como 0.
        5. Retorna os valores obtidos em uma tupla (código de cliente, nome do cliente, quantidade de notas fiscais isentas).

        Returns:
            Tuple[str, str, float]: Uma tupla contendo os valores dos campos na tela de cadastro de clientes na seguinte ordem:
            (código de cliente, nome do cliente, quantidade de notas fiscais isentas).
        """
        # Passo 1: Obtém o valor do campo "Código de Cliente".
        codCliente = self.inputCodCliente_tlCadCliente.get()
        
        # Passo 2: Obtém o valor do campo "Nome do Cliente".
        nomeCliente = self.inputNomeCliente_tlCadCliente.get()
        
        # Passo 3: Obtém o valor do campo "Quantidade de Notas Fiscais Isentas".
        notasIsentas = self.inputNotasIsentas_tlCadCliente.get()
        
        # Passo 4: Se o campo "Quantidade de Notas Fiscais Isentas" estiver vazio, define o valor como 0.
        if not notasIsentas:
            notasIsentas = 0
        
        # Passo 5: Retorna os valores obtidos em uma tupla (código de cliente, nome do cliente, quantidade de notas fiscais isentas).
        return codCliente, nomeCliente, notasIsentas
    
    def _verificaSeCamposTelaClientesPreenchidos(self):
        """
        Função interna responsável por verificar se os campos obrigatórios na tela de cadastro de clientes estão preenchidos.

        Esta função realiza as seguintes etapas:
        1. Obtém os valores dos campos da tela de cadastro de clientes (código de cliente, nome do cliente e quantidade de notas fiscais isentas).
        2. Retorna True se os campos obrigatórios (código e nome do cliente) estão preenchidos, caso contrário retorna False.

        Returns:
            bool: True se os campos obrigatórios estão preenchidos, False caso contrário.
        """
        # Passo 1: Obtém os valores dos campos da tela de cadastro de clientes.
        codCliente, nomeCliente, notasIsentas = self.pegarValoresTelaCadClientes()
        
        # Passo 2: Retorna True se os campos obrigatórios (código e nome do cliente) estão preenchidos, caso contrário retorna False.
        return bool(codCliente and nomeCliente)
    
    def _verificarSeCodigoClientteJaExiste(self):
        """
        Função interna responsável por verificar se um código de cliente já existe no banco de dados.

        Esta função realiza as seguintes etapas:
        1. Obtém o código de cliente da entrada de texto na tela de cadastro de clientes.
        2. Chama a função `verificarSeCodigoDoClienteCadastrado` do objeto `manipular_ordens` para verificar se o código existe.
        3. Retorna True se o código já existe no banco de dados, False caso contrário.

        Returns:
            bool: True se o código de cliente já existe, False caso contrário.
        """
        # Passo 1: Obtém o código de cliente da entrada de texto na tela de cadastro de clientes.
        codCliente = self.inputCodCliente_tlCadCliente.get()
        
        # Passo 2: Chama a função `verificarSeCodigoDoClienteCadastrado` do objeto `manipular_ordens` para verificar se o código existe.
        return self.manipular_ordens.verificarSeCodigoDoClienteCadastrado(codCliente) is not None
  
    def verificarSeCodigoClienteJaExiste(self, codCliente):
        """
        Função responsável por verificar se um código de cliente já existe no banco de dados.

        Esta função realiza as seguintes etapas:
        1. Chama a função interna `_verificarSeCodigoClientteJaExiste` para verificar se o código já existe.
        2. Se o código já existe, exibe um alerta indicando que o valor é inválido.
        3. Atualiza a tela de cadastro de clientes.
        4. Retorna False se o código já existe, True caso contrário.

        Args:
            codCliente (str): O código do cliente a ser verificado.

        Returns:
            bool: False se o código já existe, True caso contrário.
        """
        # Passo 1: Chama a função interna `_verificarSeCodigoClientteJaExiste` para verificar se o código já existe.
        if self._verificarSeCodigoClientteJaExiste():
            # Passo 2: Se o código já existe, exibe um alerta indicando que o valor é inválido.
            self.mostrar_alerta("Valor Inválido", f"Código {codCliente} já existe.")
            # Passo 3: Atualiza a tela de cadastro de clientes.
            self._atualizarTelaCadCliente()
            # Passo 4: Retorna False para indicar que o código já existe.
            return False
        # Se o código não existe, retorna True.
        return True

    # FUNÇÃO BOTÃO INSERIR TELA CADASTRO DE CLIENTES
    def cadastrarCliente_TelaCadCliente(self):
        """
        Função responsável por cadastrar um novo cliente na tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Verifica se os campos obrigatórios (código, nome do cliente e quantidade de notas fiscais isentas) estão preenchidos.
        2. Remove espaços em branco extras do código do cliente e converte o nome do cliente para letras maiúsculas.
        3. Verifica se o código de cliente já existe no banco de dados.
        4. Insere o novo cliente no banco de dados se o código for único.
        5. Exibe uma mensagem de sucesso se o cadastro for bem-sucedido.
        6. Retorna True se o cadastro for bem-sucedido, False caso contrário.

        Returns:
            bool: True se o cadastro for bem-sucedido, False caso contrário.
        """
        try:
            # Passo 1: Verifica se os campos obrigatórios estão preenchidos.
            if not self._verificaSeCamposTelaClientesPreenchidos():
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                self._atualizarTelaCadCliente()
                return False
            
            # Passo 2: Remove espaços em branco extras do código do cliente e converte o nome do cliente para letras maiúsculas.
            codCliente, nomeCliente, qtdNFisenta = self.pegarValoresTelaCadClientes()
            codCliente = codCliente.strip()
            nomeCliente = nomeCliente.strip().upper()
            
            # Passo 3: Verifica se o código de cliente já existe no banco de dados.
            if self._verificarSeCodigoClientteJaExiste():
                self.mostrar_alerta("Valor Inválido", f"Código {codCliente} já existe.")
                self._atualizarTelaCadCliente()
                return False
            
            # Passo 4: Insere o novo cliente no banco de dados se o código for único.
            if self.manipular_ordens.inserirClienteDB(codCliente, nomeCliente, qtdNFisenta):
                # Passo 5: Exibe uma mensagem de sucesso se o cadastro for bem-sucedido.
                self.mostrar_alerta("Cadastro de Cliente", f"O cliente '{codCliente, nomeCliente}' foi cadastrado com sucesso!")
                self._atualizarTelaCadCliente()
                return True
        except Exception as e:
            # Passo 6: Exibe uma mensagem de erro se ocorrer uma exceção.
            self.mostrar_alerta('Erro', f'Cadastro do Cliente não realizado!\n(Erro:{e})')
        return False
    
    ### FUNÇÕES PARA MODIFICAR CADASTRO CLIENTE
    def pegarValoresLinhaSelecionadaDaTabelaCliente(self):
        """
        Função responsável por obter os valores da linha selecionada na treeview da tabela de clientes.

        Esta função realiza as seguintes etapas:
        1. Obtém o item (valores) da linha selecionada na tabela de clientes.
        2. Extrai os valores individuais (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
        3. Retorna os valores obtidos.

        Returns:
            Tuple[int, str, str, str]: Uma tupla contendo os valores da linha selecionada na seguinte ordem:
            (ID do cliente, código do cliente, nome do cliente, quantidade de notas fiscais isentas).
        """
        # Passo 1: Obtém o item (valores) da linha selecionada na tabela de clientes.
        itemSelecionadoTbCliente = self.treeview_tlClientes.selection()
        item = self.treeview_tlClientes.item(itemSelecionadoTbCliente, 'values')

        # Passo 2: Extrai os valores individuais (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
        cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta = item

        # Passo 3: Retorna os valores obtidos em uma tupla.
        return cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta

    def _desabilitar_inputCodCliente(self):
        """
        Função responsável por desabilitar o campo de código do cliente na tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Desabilita o campo para impedir que o usuário faça edições.
        2. Altera a cor de fundo do campo para uma cor mais escura para indicar que está desabilitado.

        Returns:
            None
        """
        # Passo 1: Desabilita o campo para impedir que o usuário faça edições.
        self.inputCodCliente_tlCadCliente.config(state="disabled")

        # Passo 2: Altera a cor de fundo do campo para uma cor mais escura para indicar que está desabilitado.
        self.inputCodCliente_tlCadCliente.config(bg="#bfbfbf")
    
    # FUNÇÃO BOTÃO MODIFICAR TELA CADASTRO DE CLIENTE
    def modificarItemSelecionadoDaTabCliente(self):
        """
        Função responsável por preencher os campos de edição na tela de cadastro de clientes com os valores do item selecionado na tabela de clientes.

        Esta função realiza as seguintes etapas:
        1. Obtém os valores da linha selecionada na tabela de clientes (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
        2. Preenche o campo de código com o valor do item selecionado.
        3. Desabilita o campo de código para evitar modificações.
        4. Preenche o campo de nome do cliente com o valor do item selecionado.
        5. Preenche o campo de quantidade de notas fiscais isentas com o valor do item selecionado.
        6. Remove os botões anteriores e cria um botão "Salvar Modificações" na tela.
        7. Retorna True se a operação for bem-sucedida, False caso contrário.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            # Passo 1: Obtém os valores da linha selecionada na tabela de clientes.
            cli_id, codcliente, nomeCliente, qtdNFisenta = self.pegarValoresLinhaSelecionadaDaTabelaCliente()
            
            # Passo 2: Preenche o campo de código com o valor do item selecionado.
            self.inputCodCliente_tlCadCliente.delete(0, 'end')
            self.inputCodCliente_tlCadCliente.insert(0, int(codcliente))
            
            # Passo 3: Desabilita o campo de código para evitar modificações.
            self._desabilitar_inputCodCliente()
            
            # Passo 4: Preenche o campo de nome do cliente com o valor do item selecionado.
            self.inputNomeCliente_tlCadCliente.delete(0, 'end')
            self.inputNomeCliente_tlCadCliente.insert(0, str(nomeCliente))
            
            # Passo 5: Preenche o campo de quantidade de notas fiscais isentas com o valor do item selecionado.
            self.inputNotasIsentas_tlCadCliente.delete(0, 'end')
            self.inputNotasIsentas_tlCadCliente.insert(0, int(qtdNFisenta))
            
            # Passo 6: Remove os botões anteriores e cria um botão "Salvar Modificações" na tela.
            self._apagarListaBotoes(self.botoesParaOcultar_TelaCadCliente)
            self._criarBotaoSalvarModificacoes(self.tlClientes, self.validarModificacoesTelaCadCliente, 320, 106, 139, 30, "./img/img_btnSalvarModificacoes.png")
            
            # Passo 7: Retorna True para indicar que a operação foi bem-sucedida.
            return True
        
        except Exception as e:
            # Exibe uma mensagem de alerta, recria a tela e retorna False em caso de erro.
            self.mostrar_alerta('Atenção', f'Selecione uma linha da tabela abaixo:')
            self.fechar_TelaCadCliente()
            self.criar_TelaCadClientes()
            return False
    
    # FUNÇÃO BOTÃO SALVAR MODIFICAÇÕES    
    def validarModificacoesTelaCadCliente(self):
        """
        Função responsável por validar e salvar as modificações feitas na tela de cadastro de clientes.

        Esta função realiza as seguintes etapas:
        1. Obtém os valores da tela de cadastro de clientes (código do cliente, nome do cliente e quantidade de notas fiscais isentas).
        2. Remove espaços em branco extras do código do cliente e converte o nome do cliente para letras maiúsculas.
        3. Substitui vírgulas por pontos na quantidade de notas fiscais isentas.
        4. Verifica se os campos obrigatórios (código e nome do cliente) estão preenchidos.
        5. Obtém os valores da linha selecionada da tabela de clientes (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
        6. Tenta editar o cliente no banco de dados com os novos valores.
        7. Se a edição for bem-sucedida, limpa a tela de cadastro de clientes e a atualiza.
        8. Se ocorrer um erro durante a edição, retorna False e exibe uma mensagem de erro.

        Returns:
            bool: True se a edição for bem-sucedida, False caso contrário.
        """
        try:
            # Passo 1: Obtém os valores da tela de cadastro de clientes.
            codCliente, nomeCliente, qtdNFisenta = self.pegarValoresTelaCadClientes()

            # Passo 2: Remove espaços em branco extras do código do cliente e converte o nome do cliente para letras maiúsculas.
            codCliente = codCliente.strip()
            nomeCliente = nomeCliente.strip().upper()

            # Passo 3: Substitui vírgulas por pontos na quantidade de notas fiscais isentas.
            ################qtdNFisenta = qtdNFisenta.replace(",", ".")

            # Passo 4: Verifica se os campos obrigatórios (código e nome do cliente) estão preenchidos.
            if not codCliente or not nomeCliente:
                self.mostrar_alerta("Campos Vazios", "Por favor, preencha todos os campos.")
                return False

            # Passo 5: Obtém os valores da linha selecionada da tabela de clientes (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
            cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta = self.pegarValoresLinhaSelecionadaDaTabelaCliente()

            # Passo 6: Tenta editar o cliente no banco de dados com os novos valores.
            if self.manipular_ordens.editarClientePeloIDClienteDB(cli_id, codCliente, nomeCliente, qtdNFisenta):
                # Passo 7: Se a edição for bem-sucedida, limpa a tela de cadastro de clientes e a atualiza.
                self._limparTelaCadCliente()
                self._atualizarTelaCadCliente()
                return True
            else:
                # Passo 8: Se ocorrer um erro durante a edição, retorna False e exibe uma mensagem de erro.
                return False
        except Exception as e:
            self.mostrar_alerta("Erro", f"Erro ao salvar modificação do Cliente!\nErro: {e}")
            return False
            
    ### FUNÇÃO BOTÃO DELETAR CLIENTE
    def deletarCliente_TelaCadCliente(self):
        """
            Função responsável por excluir um cliente da tela de cadastro de clientes.

            Esta função realiza as seguintes etapas:
            1. Verifica se algum item da tabela de clientes foi selecionado.
            2. Se nenhum item estiver selecionado, exibe um alerta e atualiza a tela.
            3. Obtém os valores da linha selecionada da tabela de clientes (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
            4. Pergunta ao usuário se deseja confirmar a exclusão do cliente.
            5. Se o usuário confirmar, tenta excluir o cliente do banco de dados.
            6. Se a exclusão for bem-sucedida, remove o item da tabela de clientes e exibe uma mensagem de sucesso.
            7. Se ocorrer um erro durante a exclusão, exibe uma mensagem de erro.
            8. Se o usuário cancelar a exclusão, exibe um alerta.
            9. Atualiza a tela de cadastro de clientes após a ação.

            Returns:
                None
        """
        # Passo 1: Verifica se algum item da tabela de clientes foi selecionado.
        selected_itemTabCliente = self.treeview_tlClientes.selection()

        if not selected_itemTabCliente:
            # Passo 2: Se nenhum item estiver selecionado, exibe um alerta e atualiza a tela.
            self.mostrar_alerta("Nenhum item selecionado", "Por favor, selecione um item para deletar.")
            self._atualizarTelaCadCliente()
            return

        # Passo 3: Obtém os valores da linha selecionada da tabela de clientes (ID, código do cliente, nome do cliente e quantidade de notas fiscais isentas).
        cli_id, cli_codcliente, cli_nomeCliente, cli_qtdNFisenta = self.pegarValoresLinhaSelecionadaDaTabelaCliente()

        # Passo 4: Pergunta ao usuário se deseja confirmar a exclusão do cliente.
        if self.confirmar_solicitacao("Confirmar Exclusão", f'Tem certeza que deseja excluir o cliente: {cli_codcliente}, {cli_nomeCliente}'):

            # Passo 5: Se o usuário confirmar, tenta excluir o cliente do banco de dados.
            if self.manipular_ordens.deletarClienteDB(cli_id):

                # Passo 6: Se a exclusão for bem-sucedida, remove o item da tabela de clientes e exibe uma mensagem de sucesso.
                self.treeview_tlClientes.delete(selected_itemTabCliente)
                self.mostrar_sucesso(f'Exclusão bem-sucedida do cliente: {cli_codcliente}, {cli_nomeCliente}')
            else:
                # Passo 7: Se ocorrer um erro durante a exclusão, exibe uma mensagem de erro.
                self.mostrar_erro(f"Ocorreu um erro ao tentar deletar o cliente {cli_nomeCliente}.")
        else:
            # Passo 8: Se o usuário cancelar a exclusão, exibe um alerta.
            self.mostrar_alerta("Cancelado", "A exclusão foi cancelada pelo usuário.")

        # Passo 9: Atualiza a tela de cadastro de clientes após a ação.
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
    
    #@@@@@ Função botão 'REL. À FATURAR' @@@@@#
    def gerarRelatorioOrdensNAOfaturadas(self):
        """
            Função responsável por gerar um relatório das ordens de serviço não faturadas.

            Esta função realiza as seguintes etapas:
            1. Chama a função 'gerarRelatorioOdensServicoNAOfaturadas' para gerar o relatório.
            2. Seleciona o local onde o relatório será salvo.

            Returns:
                str: O caminho do arquivo de saída do relatório gerado.
        """
        # Passo 1: Chama a função 'gerarRelatorioOdensServicoNAOfaturadas' para gerar o relatório.
        output_file = self.manipular_relatorios.gerarRelatorioOdensServicoNAOfaturadas()

        # Passo 2: Seleciona o local onde o relatório será salvo.
        self.manipular_relatorios.selecionalLocalSalvarRelatorio(output_file)

        # Retorna o caminho do arquivo de saída do relatório gerado.
        return output_file
        
    #@@@@@ Função botão 'FECHAMENTO' @@@@@#    
    def fazerFechamentoFaturamento(self):
        """
            Função responsável por realizar o fechamento do faturamento das ordens em aberto.

            Esta função realiza as seguintes etapas:
            1. Gera um relatório das ordens não faturadas.
            2. Solicita uma senha para confirmar o fechamento.
            3. Verifica se a senha fornecida está correta.
            4. Se a senha estiver correta, modifica a situação de faturamento para 'SIM' em todas as ordens que estiverem com 'NÃO' no faturamento.
            5. Confirma a solicitação de fechamento com o usuário.
            6. Atualiza a tela principal após o fechamento.

            Args:
                self: Uma referência à instância da classe que contém esse método.

            Returns:
                None
        """
        # Passo 1: Gera um relatório das ordens não faturadas.
        self.gerarRelatorioOrdensNAOfaturadas()

        # Passo 2: Solicita uma senha para confirmar o fechamento.
        senha = simpledialog.askstring("Confirmar Fechamento", "\nATENÇÃO\nApós o fechamento, todas as ordens terão 'SIM' em faturado\ne não irão mais aparecer no relatório À FATURAR!\nDigite a senha para confirmar o fechamento:")

        # Passo 3: Verifica se a senha fornecida está correta (substitua 'senha_correta' pela senha correta).
        senha_correta = "Fin123!"
        if senha == senha_correta:
            # Passo 4: Se a senha estiver correta, modifica a situação de faturamento para 'SIM' em todas as ordens.
            self.manipular_ordens.modificarsituacaoFaturamentoParaSIM()

            # Passo 5: Confirma a solicitação de fechamento com o usuário.
            self.confirmar_solicitacao("Confirmar Fechamento", 'Tem certeza que deseja FATURAR todas as ordens em aberta?')

            # Passo 6: Atualiza a tela principal após o fechamento.
            self._atualizarTelaPrincipal()
        else:
            # Senha incorreta.
            self.mostrar_alerta("Senha Incorreta", "Senha incorreta. Tente novamente.")
            
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
        
    def ajustarLarguraColunaTreeview(self, treeview):
        """
        Ajusta automaticamente a largura das colunas em um ttk.Treeview para acomodar o conteúdo das células.

        Args:
            treeview: Usado para definir em qual Treeview as colunas devem ser ajustadas.

        Returns:
            None

        Exemplo de uso: self.resize_columns(self.treeviewTelaPrincipal)  # Substitua 'self.treeviewTelaPrincipal' pelo seu objeto 'ttk.Treeview'
        """
        for col in treeview["columns"]:
            treeview.heading(col, text=col, anchor="center")  # Redefinir o texto do cabeçalho para alinhar corretamente

            children = treeview.get_children()
            if children:
                # Calcular a largura ideal da coluna com base no maior comprimento do conteúdo da coluna
                col_width = max(len(treeview.set(row, col)) for row in children) * 10
                # Definir uma largura mínima para a coluna no caso 60px
                col_width = max(col_width, 60)
                treeview.column(col, width=col_width)
        
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
        
    def confirmar_solicitacao(self, tituloMSG, textoMSG,*variavelMSGErro):
        """
            Exibe uma caixa de diálogo de confirmação com um título e uma mensagem,
            opcionalmente acompanhada de mensagens de erro adicionais.

            Args:
                tituloMSG (str): O título da caixa de diálogo.
                textoMSG (str): O texto da mensagem principal a ser exibida na caixa de diálogo.
                *variavelMSGErro (tuple): Uma tupla de strings contendo mensagens de erro
                    adicionais que podem ser exibidas na caixa de diálogo.

            Returns:
                bool: True se o usuário selecionar 'Sim' na caixa de diálogo, False caso contrário.
        """
                
        resposta = messagebox.askyesno(f"{tituloMSG}", f"{textoMSG} {variavelMSGErro}")
        
        return resposta

    def mostrar_sucesso(self, *variavelMSG):
        """
        Mostra uma mensagem de sucesso após a exclusão bem-sucedida.

        Parâmetros:
        variavelMSG (str): A mensagem utiliza o valor da(s) variável/variáveis para mostrar o sucesso na exclusão.

        Retorna:
        None
        """
        self.mostrar_alerta("Sucesso", f"{variavelMSG}")

    def mostrar_erro(self, mensagem):
        """
        Mostra uma mensagem de erro em uma caixa de diálogo.

        Parâmetros:
        mensagem (str): A mensagem de erro a ser exibida.

        Retorna:
        None
        """
        self.mostrar_alerta("Erro", mensagem)

    def _criarBotaoSalvarModificacoes(self, janela, comando, posicaoX, posicaoY, width, height,file_img):
        """
            Cria e configura um botão "Salvar Modificações" em uma janela.

            Args:
                janela (Tkinter.Tk): A janela na qual o botão será criado.
                comando (function): A função que será executada quando o botão for clicado.
                posicaoX (int): A coordenada X de posicionamento do botão na janela.
                posicaoY (int): A coordenada Y de posicionamento do botão na janela.
                width (int): A largura do botão.
                height (int): A altura do botão.
                file_img (str): O caminho do arquivo de imagem a ser usado como ícone do botão.

            Returns:
                None
        """
        
        # Carrega a imagem do botão "Salvar Modificações" a partir de um arquivo
        self.img_btnSalvarModificacoes = PhotoImage(file= file_img)

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
            width=width,
            height=height
        )             
    
    ############# FUNÇÕES ORDENAR TREEVIEW COM CLIQUE NO CABEÇALHO ##################
         
    def ordenarPeloCabecalhoTreview(self, treeview, coluna):
        """
        Ordena os itens na Treeview com base na coluna especificada.

        Args:
            treeview (ttk.Treeview): O widget Treeview que contém os itens a serem ordenados.
            coluna (int): O índice da coluna pela qual os itens serão ordenados.

        Note:
            Esta função classifica os itens na Treeview com base na coluna especificada. Os valores são classificados como números
            se forem conversíveis em float, caso contrário, são classificados como texto.

        Example:
            ordenarPeloCabecalhoTreview(self.treeviewTelaPrincipal, 0)
        """
        data = treeview.get_children()
        data = sorted(data, key=lambda item: (self._get_sort_key(treeview.item(item, "values")[coluna]), treeview.item(item, "values")[coluna]))
        for i, item in enumerate(data):
            treeview.move(item, "", i)

    def _get_sort_key(self, value):
        """
        Converte o valor em um número se possível, caso contrário, retorna o valor como texto.

        Args:
            value (str): O valor a ser convertido.

        Returns:
            float ou str: O valor convertido em float se possível, caso contrário, o valor original como texto.

        Example:
            _get_sort_key("123.45")  # Retorna 123.45 (float)
            _get_sort_key("abc")     # Retorna "abc" (str)
        """
        try:
            return float(value)
        except ValueError:
            return value
    
        
        
        