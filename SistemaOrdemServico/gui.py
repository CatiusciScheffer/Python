import tkinter as tk
from tkinter import Tk, Button, Entry, PhotoImage, Canvas, ttk, messagebox, END
from datetime import datetime, timedelta
from user import UserManager
from manipulacaoOrdemServico import ManipularOrdemServicos



class LoginGUI:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_manager = UserManager(db_manager)
        self.manipular_ordens = ManipularOrdemServicos(db_manager)

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

        imgBtnEntrar = PhotoImage(file="./img/img_tlLogin_BtnEntrar.png")
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

        if self.user_manager.checkUsernameAndPasswordRegistered(username, password):
            self.fechar_tl_login()
            self.abrir_tl_principal()
            return username  # Retorna o nome do usuário logado
        else:
            self.user_manager.registerNewUser(username, password)
            self.mostrar_alerta("Cadastro de Usuário", f"Usuário(a) {username} cadastrado com sucesso!")
            self.fechar_tl_login()
            self.abrir_tl_principal()
            return username  # Retorna o nome do usuário logado

    def fechar_tl_login(self):
        self.tela_login.destroy()

    def abrir_tl_principal(self):
        
        telaPrincipal = Tk()        
        telaPrincipal.title(f"Cadasto de Serviços")

        telaPrincipal.geometry("1000x720")
        telaPrincipal.configure(bg = "#ffffff")
        
        canvas = Canvas(
            telaPrincipal,
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
        
        self.input_DataOS = tk.Label(telaPrincipal, text=f"{datetime.now()}")
        self.input_DataOS.pack()
        
        # self.input_DataOS = Entry(
        #     bd = 0,
        #     bg = "#d9d9d9",
        #     highlightthickness = 0)

        self.input_DataOS.place(
            x = 69.0, y = 71,
            width = 102.0,
            height = 24)

        
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

        input_Cliente_img = PhotoImage(file="./img/img_tlPrincipal_inputCliente.png")
        input_Cliente_bg = canvas.create_image(
            595.5, 84.0,
            image = input_Cliente_img)
        
        self.input_Cliente = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0)

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

        input_TipoServ_img = PhotoImage(file="./img/img_tlPrincipal_inputTipoServ.png")
        input_TipoServ_bg = canvas.create_image(
            550.0, 119.0,
            image = input_TipoServ_img)

        self.input_TipoServ = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0
        )
        
        self.input_TipoServ.place(
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
        
    


        input_VlrTotal_img = PhotoImage(file="./img/img_tlPrincipal_inputVltTotal.png")
        input_VlrTotal_bg = canvas.create_image(
            534.5, 155.0,
            image = input_VlrTotal_img)

        self.input_VlrTotal = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0)

        self.input_VlrTotal.place(
            x = 490.0, y = 142,
            width = 89.0,
            height = 24)

        input_Faturado_img = PhotoImage(file="./img/img_tlPrincipal_inputFaturado.png")
        input_Faturado_bg = canvas.create_image(
            711.5, 155.0,
            image = input_Faturado_img)

        self.input_Faturado = Entry(
            bd = 0,
            bg = "#8a8a8a",
            highlightthickness = 0)

        self.input_Faturado.place(
            x = 667.0, y = 142,
            width = 89.0,
            height = 24)


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

        img_tlPrincipal_btnInsert = PhotoImage(file="./img/img_tlPrincipal_btnInsert.png")
        btnInsertOS_tlPrincipal = Button(
            image = img_tlPrincipal_btnInsert,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.inserirOrdemServico,
            relief = "flat")

        btnInsertOS_tlPrincipal.place(
            x = 566, y = 196,
            width = 81,
            height = 97)

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

        img_tlPrincipal_btnCadServico = PhotoImage(file="./img/img_tlPrincipal_btnCadServico.png")
        btnCadServ_tlPrincipal = Button(
            image = img_tlPrincipal_btnCadServico,
            borderwidth = 0,
            highlightthickness = 0,
            #command = btn_clicked,
            relief = "flat")

        btnCadServ_tlPrincipal.place(
            x = 809, y = 145,
            width = 138,
            height = 60)

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
        
        input_DescrServ_img = PhotoImage(file="./img/img_tlPrincipal_textDescricaoServ.png")
        input_DescrServ_bg = canvas.create_image(
            291.0, 244.5,
            image = input_DescrServ_img)

        self.input_DescrServ = tk.Text(
            bd = 0,
            bg = "#d9d9d9",
            highlightthickness = 0)

        self.input_DescrServ.place(
            x = 30.0, y = 196,
            width = 522.0,
            height = 95)
        
        
       
        #criando Treeview
        # Função para centralizar o texto nas células da TreeView
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
            
        # Criar a TreeView
        treeview = ttk.Treeview(telaPrincipal)

        treeview.pack(fill="both", expand=True)

        # Configurar as colunas com largura e alinhamento
        treeview["columns"] = ("ID","Data", "CodCliente", "Cliente", "CodServ", "TipoServico", "QTD", "ValorUnit", "ValorTotal", "DescServicos", "Resp","Faturado")
        treeview.column("#0", width=0, stretch=tk.NO)  # Coluna de ícones (não visível)
        treeview.column("ID", width=50, anchor="center")
        treeview.column("Data", width=70, anchor="center")
        treeview.column("CodCliente", width=70, anchor="center")
        treeview.column("Cliente", width=200, anchor="center")
        treeview.column("CodServ", width=70, anchor="center")
        treeview.column("TipoServico", width=146, anchor="w")
        treeview.column("QTD", width=38, anchor="e")
        treeview.column("ValorUnit", width=65, anchor="e")
        treeview.column("ValorTotal", width=65, anchor="e")
        treeview.column("DescServicos", width=200, anchor="w")
        treeview.column("Resp", width=100, anchor="center")
        treeview.column("Faturado", width=70, anchor="center")

        # Definir as colunas que serão exibidas
        treeview.heading("#0", text="", anchor="w")  # Coluna de ícones (não visível)
        treeview.heading("ID", text="ID", anchor="center")
        treeview.heading("Data", text="Data", anchor="center")
        treeview.heading("CodCliente", text="Cód.Cliente", anchor="center")
        treeview.heading("Cliente", text="Cliente", anchor="center")
        treeview.heading("CodServ", text="Cód.Serv.", anchor="center")
        treeview.heading("TipoServico", text="Tipo Serviço", anchor="center")
        treeview.heading("QTD", text="QTD", anchor="center")
        treeview.heading("ValorUnit", text="Valor Unit.", anchor="center")
        treeview.heading("ValorTotal", text="Valor Total", anchor="center")
        treeview.heading("DescServicos", text="Descrição dos Serviços", anchor="center")
        treeview.heading("Resp", text="Responsável", anchor="center")
        treeview.heading("Faturado", text="Faturado", anchor="center")

        # Aplicar formatação de alinhamento
        center_aligned_text(treeview)
        right_aligned_text(treeview)

        # Inserir alguns dados de exemplo na TreeView
        treeview.insert("", "end", values=(1, "2023-07-21", "001", "Cliente A", "101", "Manutenção", "2", "50.00", "100.00", "Manutenção do equipamento", "Amanda","Sim"))
        treeview.insert("", "end", values=(2, "2023-07-22", "002", "Cliente B", "102", "Instalação", "1", "150.00", "150.00", "Instalação do sistema", "Elisete","Não"))
        treeview.insert("", "end", values=(3, "2023-07-23", "003", "Cliente C", "103", "Consultoria", "3", "80.00", "240.00", "Consultoria em TI", "Catiusci Pagnonceli Chaves Scheffer","Sim"))

        # Posicionar a TreeView na janela principal usando o place()
        treeview.place(x=13, y=322, height=369, width=957)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(telaPrincipal, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=969, y=323, height=367)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(telaPrincipal, orient="horizontal", command=treeview.xview)
        treeview.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=14, y=690, width=973)
            
            
        # Iniciar o loop principal do Tkinter
        telaPrincipal.resizable(False, False)
        telaPrincipal.mainloop()
     
     
    def preencheDescrServicoEvalorUnitario(self, event):
        if event.keysym == "Tab":

            l_codServDescrServVlrUnit = self.manipular_ordens.novoTeste()
            
            input_codServ = int(self.input_CodServ.get())
            
            for index, servicos in enumerate(l_codServDescrServVlrUnit):
                
                codServ = int(servicos[0])
                descrServ = str(servicos[1])
                valorUnit = float(servicos[2])
                print(f'codigo {codServ}, descrição{descrServ}, vlr unitario{valorUnit}')

                if codServ == input_codServ:
                    self.input_TipoServ.delete(0, "end")
                    self.input_TipoServ.insert(0, descrServ)
                    self.input_VlrUnitario.delete(0, "end")
                    self.input_VlrUnitario.insert(0, valorUnit)
                    break
                else:
                    pass


    
            
    
    def getValuesInputsOS(self):
        os_dtServico = self.input_DataOS.get()
        os_codCliente = int(self.input_CodCliente.get().strip())
        os_cliente = self.input_Cliente.get().strip().upper()
        os_observacao = self.input_TipoServ.get().strip().upper()
        os_codServico = int(self.input_CodServ.get().strip())
        os_descServico = self.input_DescrServ.get("1.0", "end")
        os_qtd = int(self.input_Quantidade.get())
        os_vlrUnit = float(self.input_VlrUnitario.get())
        os_total = float(self.input_VlrTotal.get())
        os_faturado = self.input_VlrUnitario.get()
        #os_usuario = self.tela_login.input_login_usuario.get()
        
        os_values = {
            'dtServico': os_dtServico,
            'codCliente': os_codCliente,
            'cliente': os_cliente,
            'observacao': os_observacao,
            'codServico': os_codServico,
            'descServico': os_descServico,
            'quantidade': os_qtd,
            'vlrUnit': os_vlrUnit,
            'total': os_total,
            'os_faturado': os_faturado            
        }
        return os_values
    
    
    
        
    def inserirOrdemServico(self):
        valoresOS = self.getValuesInputsOS()
        os_cliente = valoresOS['cliente']
        
        # Verificar se o cliente existe na tabela tb_cliente
        os_cliente_result = self.manipular_ordens.verificaSeClienteCadastrado(valoresOS['codCliente'])

        # Verificar se o cliente foi encontrado
        if os_cliente_result is not None:
            os_cliente = os_cliente_result[0]  # Extrair o valor único do cliente da tupla
            self.atualizar_valor_cliente(os_cliente)  # Atualiza o valor do cliente no Label
        else:
            print(f"Cliente com código {valoresOS['codCliente']} não existe na tabela tb_cliente.")
            return

        # Buscar valor unitário
        os_vlrUnit = self.manipular_ordens.pegandoValorUnitarioPeloCodServico(valoresOS['vlrUnit'])
        

        # Executar a instrução INSERT
        self.db_manager.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_observacao, os_codServico, os_descServico, os_qtd, os_vlrUnit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (valoresOS['dtServico'], valoresOS['codCliente'], os_cliente, valoresOS['observacao'], valoresOS['codServico'], valoresOS['descServico'], valoresOS['quantidade'], os_vlrUnit))


        # Salvar a transação
        self.db_manager.connection.commit()
        print("Ordem de serviço inserida com sucesso.")
            

    def mostrar_alerta(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def run(self):
        self.tela_login.mainloop()
        
    
        
        
        
        
        
        
        
        
