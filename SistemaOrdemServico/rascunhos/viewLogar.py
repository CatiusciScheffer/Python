############# CRIANDO TELA CADASTRO DE CLIENTES #############
    def criar_TelaCadServ(self):
        
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
            417.5, 288.5,
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
            #command = self.ModificarItemSelecionadoDaTabela,
            relief = "flat")

        btnModify_tlCadCliente.place(
            x = 492, y = 115,
            width = 90,
            height = 30)
        
        #### BOTÃO INSERIR CLIENTE ####
        img_btnInsert_tlCadCliente = PhotoImage(file = "./img/img_btnInsert.png")
        btnInsert_tlCadCliente = Button(
            self.tlClientes,
            image = img_btnInsert_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            #command = self.cadastrarServico_TelaCadServico,
            relief = "flat")

        btnInsert_tlCadCliente.place(
            x = 390, y = 115,
            width = 90,
            height = 30)

        #### BOTÃO DELETAR CLIENTE ####
        self.img_btnDelete_tlCadCliente = PhotoImage(file = "./img/img_btnDelete.png")
        self.btnDelete_tlCadCliente = Button(
            self.tlClientes,
            image = self.img_btnDelete_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            #command = self.deletarServico_TelaCadServ,
            relief = "flat")

        self.btnDelete_tlCadCliente.place(
            x = 594, y = 115,
            width = 90,
            height = 30)
        
        #### BOTÃO IMPRIMIR CLIENTE ####
        img_btnPrint_tlCadCliente = PhotoImage(file = "./img/img_btnPrint.png")
        btnPrint_tlCadCliente = Button(
            self.tlClientes,
            image = img_btnPrint_tlCadCliente,
            borderwidth = 0,
            highlightthickness = 0,
            #command = self.gerarRelatorioCadServ,
            relief = "flat")

        btnPrint_tlCadCliente.place(
            x = 696, y = 115,
            width = 115,
            height = 30)
        
        #botões que serão ocultos ao chamar a função de modificação:
        self.botoesParaOcultar_TelaCadServ = [self.btnDelete_tlCadCliente, btnInsert_tlCadCliente, btnModify_tlCadCliente, btnPrint_tlCadCliente]
        
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

        ############### TREEVIEW LISTA SERVIÇOS ###############
        def center_aligned_text(tree):
            tree.tag_configure('center', anchor='center')

        # Função para alinhar o texto à direita nas células da TreeView
        def right_aligned_text(tree):
            tree.tag_configure('right', anchor='e')
                            
        self.treeview_tlClientes = ttk.Treeview(self.tlClientes)

        self.treeview_tlClientes.pack(fill="both", expand=True)

        self.treeview_tlClientes["columns"] = ("ID","CodCliente", "Cliente", "NF Isenta")
                
        self.treeview_tlClientes.column("#0", width=0, stretch=tk.NO)
        self.treeview_tlClientes.column("ID", width=30, anchor="center")
        self.treeview_tlClientes.column("CodCliente", width=70, anchor="center")
        self.treeview_tlClientes.column("Cliente", width=250, anchor="w")
        self.treeview_tlClientes.column("NF Isenta", width=70, anchor="e")

        self.treeview_tlClientes.heading("#0", text="", anchor="w")
        self.treeview_tlClientes.heading("ID", text="ID", anchor="center")
        self.treeview_tlClientes.heading("CodCliente", text="Código Cliente", anchor="center")
        self.treeview_tlClientes.heading("Cliente", text="Razão Social", anchor="center")
        self.treeview_tlClientes.heading("NF_Isenta", text="Notas Isentas", anchor="center")

        center_aligned_text(self.treeview_tlClientes)
        right_aligned_text(self.treeview_tlClientes)

        # Posicionar a TreeView
        self.treeview_tlClientes.place(x=15, y=166, height=443, width=753)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.tlClientes, orient="vertical", command=self.treeview_tlClientes.yview)
        self.treeview_tlClientes.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=745, y=167, height=422)

        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.tlClientes, orient="horizontal", command=self.treeview_tlClientes.xview)
        self.treeview_tlClientes.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.place(x=16, y=589, width=751)
        ########## FIM TABELA CLIENTES ##########
        
        self.tlClientes.resizable(False, False)
        self.tlClientes.mainloop()