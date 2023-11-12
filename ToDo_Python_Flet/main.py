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
    TextThemeStyle,
    AlertDialog,
    TextButton,
    ElevatedButton,
    Theme)

class ToDo:
    def __init__(self, page:Page):
        self.page = page
        self.page.horizontal_alignment = CrossAxisAlignment.CENTER
        self.page.window_width=385
        self.page.window_min_width=385
        self.page.window_always_on_top = True
        self.page.title = 'Tarefas'
        self.manipularDB('CREATE TABLE IF NOT EXISTS tb_tarefas(tarefa, status)')
        self.mostrarListaTarefa = self.mostrarListaTarefa()
        self.mostarBtnDeletarTarefa = self.mostarBtnDeletarTarefa()
        self.input_tarefa = ''
        self.modalExcluirTodasTarefas = self.modal_excluir_Tarefas
        self.contador_tarefas = Text(value = self.contarTarefasAbaSelecionada())
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
    
    ############ MANIPULAR BANCO DE DADOS ############
    def manipularDB(self, query, parametros=[]):
        
        with sqlite3.connect('db_tarefas.db') as conexao:
            cursor = conexao.cursor()
            
            cursor.execute(query, parametros)
            
            conexao.commit()
            
            return cursor.fetchall()
        
    def adicionarTarefa(self, e, tarefa):
        tarefa = self.tarefa.upper()
        status = 'ANDAMENTO'
        
        if tarefa:
            self.manipularDB(query='INSERT INTO tb_tarefas(tarefa, status) VALUES(?, ?)', parametros=[tarefa, status])        
            
            self.mostrarListaTarefa.controls.append(
                Checkbox(label=tarefa, value=False, width=250, height=39.9, expand=False))
            
            self.mostarBtnDeletarTarefa.controls.append(
                IconButton(icon=icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=16, tooltip="Deletar Tarefa", key='btnDeletar', on_click=''))
            
            e.control.value = ""
            self.page.update()
            self.contador_tarefas.value = self.contarTarefasAbaSelecionada()
            self.page.update()

    def deletarTarefa(self, e):
        lista_botoes_del = self.mostarBtnDeletarTarefa.controls
        lista_tarefasView = self.mostrarListaTarefa.controls

        indexBtnDel = lista_botoes_del.index(e.control)
        
        del lista_botoes_del[indexBtnDel]
        del lista_tarefasView[indexBtnDel]
        
        registro_a_deletar = self.manipularDB('SELECT tarefa, status FROM tb_tarefas')[indexBtnDel]

        tarefa, status = registro_a_deletar

        self.manipularDB('DELETE FROM tb_tarefas WHERE tarefa = ? AND status = ?', [tarefa, status])
        self.page.update()
        self.contador_tarefas.value = self.contarTarefasAbaSelecionada()
        self.fecharModalExcluirTodas()
        self.page.update()
    
    
        
    def modal_confirmarExclusao(self, e):
        modal = self.modal_excluir_Tarefas()  # Chame o método para obter o objeto AlertDialog
        self.abrirModalExclusao(e, modal)  # Passe o objeto como argumento

    def abrirModalExclusao(self, e, modal):
        self.page.dialog = modal
        modal.open = True
        self.page.update()

    def deletarTodasTarefas(self, e=None):
        self.manipularDB('DELETE FROM tb_tarefas;')
        self.mostarBtnDeletarTarefa.controls = []
        self.mostrarListaTarefa.controls = []
        self.contador_tarefas.value = self.contarTarefasAbaSelecionada()
        self.fecharModalExcluirTodas()
        self.page.update()


    def fecharModalExcluirTodas(self):
        modal = self.modal_excluir_Tarefas()
        modal.open = False
        self.page.update()
        
        
    def modal_excluir_Tarefas(self):
        modal = AlertDialog(
            modal=False,
            title=Text("Por favor, confirme"),
            content=Text("Você realmente deseja excluir todas essas tarefas?"),
            actions=[
                TextButton("Sim", on_click=self.deletarTodasTarefas),
                TextButton("Não", on_click=self.fecharModalExcluirTodas),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: self.fecharModalExcluirTodas,
        )
        return modal
    
    def filtarListaTarefas(self, query):
        query
        self.page.update()
        return query 
            
    def mudar_abas(self, e):
        self.page.update()
        
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
                width=250,
                height=39.9,
                expand=False,
                key='btnCheck',
                tooltip='Clique para concluir',
                on_change=lambda e: self.concluirTarefa(e, self.view),
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
                on_click=lambda e: self.deletarTarefa(e),
            )for res in self.query if res 
        ]

        self.page.update()
        self.contador_tarefas.value = self.contarTarefasAbaSelecionada()
        self.page.update()

    def contarTarefasAbaSelecionada(self):
        total_tarefas_listadas_acima = len(self.mostrarListaTarefa.controls)
        return total_tarefas_listadas_acima

    def concluirTarefa(self, e, aba=None):
        lista_tarefasView = self.mostrarListaTarefa.controls

        indexTarefa = lista_tarefasView.index(e.control)

        nome_tarefa = lista_tarefasView[indexTarefa].label
        status_tarefa = lista_tarefasView[indexTarefa].value

        if status_tarefa == True:
            self.manipularDB('UPDATE tb_tarefas SET status = "CONCLUÍDA" WHERE tarefa = ?', [nome_tarefa])
        else:
            self.manipularDB('UPDATE tb_tarefas SET status = "ANDAMENTO" WHERE tarefa = ?', [nome_tarefa])

        if aba == 'TUDO':
            self.query = self.manipularDB('SELECT * FROM tb_tarefas')
        elif aba == 'ANDAMENTO':
            self.query = self.manipularDB('SELECT * FROM tb_tarefas WHERE status="ANDAMENTO"')
        else:
            self.query = self.manipularDB('SELECT * FROM tb_tarefas WHERE status="CONCLUÍDA"')

        self.mostrarListaTarefa.controls = [
            Checkbox(
                label=res[0],
                value=True if res[1] == 'CONCLUÍDA' else False,
                width=250,
                height=39.9,
                expand=False,
                key='btnCheck',
                tooltip='Clique para concluir',
                on_change=lambda e: self.concluirTarefa(e, aba),
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
                on_click=lambda e: self.deletarTarefa(e, aba),
            ) for res in self.query if res
        ]

        self.page.update()
        self.contador_tarefas.value = self.contarTarefasAbaSelecionada()
        self.page.update()

    def mostrarListaTarefa(self):
        self.query = self.manipularDB('SELECT * FROM tb_tarefas')
        lista_tarefas =  Column(
            controls=[
                Checkbox(
                    label= res[0],
                    value=True if res[1] == 'CONCLUÍDA' else False,
                    width=250,
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
                    on_click=lambda e: self.deletarTarefa(e),
                ) for res in lista if res                
            ],
        ) 
        self.page.update()
        return btn_deletar


    def main_page(self):
        ############ CRIAR OBJETOS ############
        titulo = Text(value="Lista de Tarefas", 
                      style=TextThemeStyle.HEADLINE_MEDIUM)
        
        input_tarefa = TextField(
            label='Digite uma tarefa', 
            width=270, 
            autofocus=True,
            max_length=30,
            on_change=self.pegarValorInput,
            on_submit=lambda e: self.adicionarTarefa(e, input_tarefa))
        
        btn_add_tarefa = FloatingActionButton(
            icon=icons.ADD,
            tooltip='Adicionar Tarefa',
            on_click=lambda e: self.adicionarTarefa(e, input_tarefa))
        
        text_inform_tarefas_acima = Text('Total de Tarefas:')
        
        btn_apagar_tudo = OutlinedButton(
            text= 'Apagar tudo',
            icon='DELETE_SWEEP',
            on_click=lambda e: self.modal_confirmarExclusao(e),
            )
         
        ############ EMPACOTANDO OBJETO NOS CONTAINER ############
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
            width=340,
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
                                #tirei daqui o botão de editar por considerar desnecessário e que ocupa muito espaço, recriar na versão desktop agenda
                            ],
                        ),
                        
                    ],
                ),
            ],
        )
        
        ############ LINHA APÓS LISTA DE TAREFAS ############
        linha_divisoria = Column(
            width=335,
            controls=[
                Divider(height=2,
                        opacity=0.5,
                    ),
                ],
            )
        ############ CONTAINER DOS OBJETOS DO RODAPÉ ############
        container_rodape = Row(
            width=335,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                text_inform_tarefas_acima,
                self.contador_tarefas,
                btn_apagar_tudo
            ]
        )
               
        ############ ADICIONANDO TODOS OS ELEMENTOS À PÁGINA ############
        self.page.add(container_inserir_tarefa, container_abas_tarefas, container_lista_tarefas, linha_divisoria, container_rodape)
        
    
app(target=ToDo)