import sqlite3
from flet import (
    Page, 
    app, 
    Row, 
    Container, 
    colors, 
    TextField, 
    FloatingActionButton, 
    icons, 
    Tabs, 
    Tab,
    Column,
    Checkbox, 
    MainAxisAlignment,
    alignment,
    IconButton,
    CrossAxisAlignment,
    Text,
    OutlinedButton, 
    Divider,
    ScrollMode,
    TextThemeStyle)

class ToDo:
    def __init__(self, page:Page):
        self.page = page
        self.page.horizontal_alignment = CrossAxisAlignment.CENTER
        self.page.window_width=385
        self.page.window_min_width=385
        self.page.bgcolor = colors.WHITE        
        self.page.window_always_on_top = True
        self.page.title = 'Tarefas'
        self.manipularDB('CREATE TABLE IF NOT EXISTS tb_tarefas(tarefa, status)')
        self.mostrarListaTarefa = self.mostrarListaTarefa()
        self.mostarBtnDeletarTarefa = self.mostarBtnDeletarTarefa()
        self.mostarBtnEditarTarefa = self.mostarBtnEditarTarefa()
        #CAMPOS DO APP
        self.input_tarefa = ''
        self.query = self.manipularDB('SELECT * FROM tb_tarefas')
        self.view = 'TUDO'
        self.main_page()
        
        
    
    def pegarValorInput(self,e):
        self.tarefa = e.control.value
        return self.tarefa
        
    def pegarValorLabelTarefa(self, e):
        self.btn_checkbox = e.control.value
        print(self.btn_checkbox)
        return self.btn_checkbox
    
    #----------- FUNÇÕES BANCO DE DADOS -----------#  
    def manipularDB(self, query, parametros=[]):
        #abrir e fechar a conexão
        with sqlite3.connect('db_tarefas.db') as conexao:
            cursor = conexao.cursor()
            # executar a query com os parâmetro ou sem
            cursor.execute(query, parametros)
            # salvar o que a query executou no banco
            conexao.commit()
            #retornar todas as linhas se a query tiver um select
            return cursor.fetchall()
        
    def adicionarTarefaDB(self, e, tarefa):
                
        tarefa = self.tarefa.upper()
        status = 'ANDAMENTO'
        if tarefa:
            self.manipularDB(query='INSERT INTO tb_tarefas(tarefa, status) VALUES(?, ?)', parametros=[tarefa, status])        
        
            self.mostrarListaTarefa.controls.append(
                Checkbox(label= tarefa, value=False, width=260, height=39.9, expand=False))
            
            self.mostarBtnEditarTarefa.controls.append(
                IconButton(icon=icons.MODE_EDIT_OUTLINE,icon_color='#62de14',icon_size=16,tooltip="Editar Tarefa",key='btnEditar',on_click=''))
            
            self.mostarBtnDeletarTarefa.controls.append(
                IconButton(icon=icons.DELETE_FOREVER_ROUNDED,icon_color="pink600",icon_size=16,tooltip="Deletar Tarefa",key='btnDeletar',on_click=''))
            
        
        self.page.update()
                
    def deletarTarefaDB(self, e):
        lista_botoes_del = self.mostarBtnDeletarTarefa.controls
        lista_tarefasView = self.mostrarListaTarefa.controls
        lista_botoes_editar = self.mostarBtnEditarTarefa.controls

        # Encontre o índice do IconButton de deletar clicado
        indexBtnDel = lista_botoes_del.index(e.control)
        
        # Use o índice encontrado para deletar os ícones de deletar, editar e a tarefa associada
        del lista_botoes_del[indexBtnDel]
        del lista_botoes_editar[indexBtnDel]
        del lista_tarefasView[indexBtnDel]
        
        self.page.update()

        # Agora, obtenha o registro correspondente no banco de dados
        registro_a_deletar = self.manipularDB('SELECT tarefa, status FROM tb_tarefas')[indexBtnDel]

        # Extraia os valores do registro
        tarefa, status = registro_a_deletar

        # Execute uma operação de exclusão no banco de dados
        self.manipularDB('DELETE FROM tb_tarefas WHERE tarefa = ? AND status = ?', [tarefa, status])

    def editarTarefaDB(self, e):
        pass
                       
    def filtarListaTarefas(self, query):
        query
        self.page.update()
        return query
    
    
    
        
    #----------- FIM FUNÇÕES BANCO DE DADOS -----------#  
            
    def criar_lista_tarefas(self):
        pass       
        
    def atualizar_lista_tarefas(self):
        pass
        
    
    def mudar_abas(self, e):
        if e.control.selected_index == 0:
            self.query = self.manipularDB('SELECT * FROM tb_tarefas')
            self.view = 'TUDO'
        elif e.control.selected_index == 1:
            self.query = self.manipularDB('SELECT * FROM tb_tarefas WHERE status="ANDAMENTO"')
            self.view = 'ANDAMENTO'
        else:
            self.query = self.manipularDB('SELECT * FROM tb_tarefas WHERE status="CONCLUÍDA"')
            self.view = 'CONCLUÍDA'
        
        self.mostrarListaTarefa.controls = [
            Checkbox(
                label=res[0],
                value=True if res[1] == 'CONCLUÍDA' else False,
                width=260,
                height=39.9,
                expand=False,
                key='btnCheck',
                tooltip='Clique para concluir',
                on_change=lambda e: self.concluirTarefa(e),
            ) for res in self.query if res
        ]
        
        self.mostarBtnDeletarTarefa.controls = [
            IconButton(
                icon=icons.DELETE_FOREVER_ROUNDED,
                icon_color="pink600",
                icon_size=16,
                tooltip="Deletar Tarefa",
                key='btnDeletar',
                selected=True,
                on_click=lambda e: self.deletarTarefaDB(e),  # Configure o on_click corretamente
            )for res in self.query if res 
        ]
        
        self.mostarBtnEditarTarefa.controls = [
            IconButton(
                icon=icons.MODE_EDIT_OUTLINE,
                icon_color='#62de14',
                icon_size=16,
                tooltip="Editar Tarefa",
                key='btnEditar',
                selected = False,
                on_click=''
            )for res in self.query if res
        ]
        
        self.page.update()
 

    def concluirTarefa(self, e):
        lista_tarefasView = self.mostrarListaTarefa.controls

        # Encontre o índice do Checkbox clicado
        indexTarefa = lista_tarefasView.index(e.control)

        # Obtenha o nome da tarefa correspondente ao Checkbox clicado
        nome_tarefa = lista_tarefasView[indexTarefa].label
        status_tarefa = lista_tarefasView[indexTarefa].value
        print(status_tarefa, nome_tarefa)

        if status_tarefa == True:
            self.manipularDB('UPDATE tb_tarefas SET status = "CONCLUÍDA" WHERE tarefa = ?', [nome_tarefa])
            self.page.update()
        else:
            self.manipularDB('UPDATE tb_tarefas SET status = "ANDAMENTO" WHERE tarefa = ?', [nome_tarefa])
            self.page.update()
        self.page.update()
    
    def mostrarListaTarefa(self):
        self.query = self.manipularDB('SELECT * FROM tb_tarefas')
        lista_tarefas =  Column(
            controls=[
                Checkbox(
                    label= res[0],
                    value=True if res[1] == 'CONCLUÍDA' else False,
                    width=260,
                    height=39.9,
                    expand=False,
                    key='btnCheck',
                    tooltip='Clique para concluir',
                    on_change=lambda e: self.concluirTarefa(e),
                )for res in self.query if res                
            ],
        )
        
        self.page.update()
        return lista_tarefas
            
    def mostarBtnEditarTarefa(self):
            lista = self.filtarListaTarefas(query = self.manipularDB('SELECT * FROM tb_tarefas'))
            btn_Editar = Column(
                controls=[
                        IconButton(
                        icon=icons.MODE_EDIT_OUTLINE,
                        icon_color='#62de14',
                        icon_size=16,
                        tooltip="Editar Tarefa",
                        key='btnEditar',
                        selected = False,
                        on_click=''
                        )for res in lista if res                
                    ],
                )
            self.page.update()
            return btn_Editar
     
    def mostarBtnDeletarTarefa(self):
        lista = self.filtarListaTarefas(query = self.manipularDB('SELECT * FROM tb_tarefas'))
        btn_deletar =  Column(
            controls=[
                IconButton(
                    icon=icons.DELETE_FOREVER_ROUNDED,
                    icon_color="pink600",
                    icon_size=16,
                    tooltip="Deletar Tarefa",
                    key='btnDeletar',
                    selected=True,
                    on_click=lambda e: self.deletarTarefaDB(e),  # Configure o on_click corretamente
                ) for res in lista if res                
            ],
        ) 
        self.page.update()
        return btn_deletar

    def main_page(self):
        # CRIAR OBJETOS
        
        titulo = Text(value="Lista de Tarefas", 
                      style=TextThemeStyle.HEADLINE_MEDIUM)
        
        input_tarefa = TextField(
            label='Digite uma tarefa', 
            width=270, 
            autofocus=True,
            max_length=30,
            on_change=self.pegarValorInput,
            on_submit=lambda e: self.adicionarTarefaDB(e, input_tarefa))
        
        btn_add_tarefa = FloatingActionButton(
            icon=icons.ADD,
            tooltip='Adicionar Tarefa',
            on_click=lambda e: self.adicionarTarefaDB(e, input_tarefa))
        
        contador_tarefas = Text('? tarefas acima')
        
        btn_apagar_tudo = OutlinedButton(
            text= 'Apagar tudo',
            icon='DELETE_SWEEP',
            on_click=''
            )
        
         
        # EMPACOTANDO OBJETO NO CONTAINER
        container_inserir_tarefa = Column(
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[titulo
                    ],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment= CrossAxisAlignment.START,
                    controls=[
                        input_tarefa,
                        btn_add_tarefa,
                    ],
                ),
            ],
        )
        
        container_abas_tarefas = Container(
            alignment=alignment.center,
            content=(
                Tabs(
                    selected_index=0,
                    on_change=self.mudar_abas,
                    tabs=[
                        Tab(icon=icons.VIEW_LIST_ROUNDED, text='TUDO'),
                        Tab(icon=icons.PLAYLIST_PLAY_ROUNDED, text='FAZENDO'),
                        Tab(icon=icons.PLAYLIST_ADD_CHECK_ROUNDED, text='FEITO'),
                    ]
                )
            )
        )
                
        container_lista_tarefas = Column(
            scroll=ScrollMode.AUTO,
            width=335,
            spacing=0,
            expand=True,
            controls=[
                Row(
                    alignment= MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment= CrossAxisAlignment.CENTER,
                    controls=[
                        self.mostrarListaTarefa,
                        Row(
                            controls=[
                                self.mostarBtnDeletarTarefa,
                                self.mostarBtnEditarTarefa,
                            ],
                        ),
                    ],
                ),
            ],
        )
        
        linha_divisoria = Column(
            width=335,
            controls=[
                Divider(height=2,
                        opacity=0.5,
                    ),
                ],
            )
        
        container_rodape = Row(
            width=335,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                contador_tarefas,
                btn_apagar_tudo
            ]
        )
               
        # ADICIONAR NA PÁGINA
        
        self.page.add(container_inserir_tarefa, container_abas_tarefas, container_lista_tarefas, linha_divisoria, container_rodape)
        
    
app(target=ToDo)