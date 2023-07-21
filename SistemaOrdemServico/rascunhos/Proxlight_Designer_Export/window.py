import tkinter as tk
from tkinter import ttk
from tkinter import *


def btn_clicked():
    print("Button Clicked")


telaPrincipal = Tk()
telaPrincipal.title("Cadasto de Serviços")

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

img_tlPrincipal_background = PhotoImage(file = f"img_tlPrincipal_background.png")
background_tlPrincipal = canvas.create_image(
    500.0, 360.0,
    image=img_tlPrincipal_background)

img_tlPrincipal_btnModificar = PhotoImage(file = f"img_tlPrincipal_btnModify.png")
btnModifyOS_tlPrincipal = Button(
    image = img_tlPrincipal_btnModificar,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnModifyOS_tlPrincipal.place(
    x = 656, y = 253,
    width = 103,
    height = 40)

img_tlPrincipal_btnDelete = PhotoImage(file = f"img_tlPrincipal_btnDelete.png")
btnDeleteOS_tlPrincipal = Button(
    image = img_tlPrincipal_btnDelete,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnDeleteOS_tlPrincipal.place(
    x = 656, y = 196,
    width = 103,
    height = 40)

img_tlPrincipal_btnInsert = PhotoImage(file = f"img_tlPrincipal_btnInsert.png")
btnInsertOS_tlPrincipal = Button(
    image = img_tlPrincipal_btnInsert,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnInsertOS_tlPrincipal.place(
    x = 566, y = 196,
    width = 81,
    height = 97)

img_tlPrincipal_btnCadCliente = PhotoImage(file = f"img_tlPrincipal_btnCadCliente.png")
btnCadCliente_tlPrincipal = Button(
    image = img_tlPrincipal_btnCadCliente,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnCadCliente_tlPrincipal.place(
    x = 809, y = 71,
    width = 138,
    height = 60)

img_tlPrincipal_btnCadServico = PhotoImage(file = f"img_tlPrincipal_btnCadServico.png")
btnCadServ_tlPrincipal = Button(
    image = img_tlPrincipal_btnCadServico,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnCadServ_tlPrincipal.place(
    x = 809, y = 145,
    width = 138,
    height = 60)

img_tlPrincipal_btnFinanceiro = PhotoImage(file = f"img_tlPrincipal_btnFinanceiro.png")
btnFinanceiro_tlPrincipal = Button(
    image = img_tlPrincipal_btnFinanceiro,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

btnFinanceiro_tlPrincipal.place(
    x = 809, y = 220,
    width = 138,
    height = 60)

input_DataOS_img = PhotoImage(file = f"img_tlPrincipal_inputData.png")
input_DataOS_bg = canvas.create_image(
    120.0, 84.0,
    image = input_DataOS_img)

input_DataOS = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

input_DataOS.place(
    x = 69.0, y = 71,
    width = 102.0,
    height = 24)

input_CodServ_img = PhotoImage(file = f"img_tlPrincipal_inputCodServ.png")
input_CodServ_bg = canvas.create_image(
    168.0, 119.0,
    image = input_CodServ_img)

input_CodServ = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

input_CodServ.place(
    x = 115.0, y = 106,
    width = 106.0,
    height = 24)

input_Quantidade_img = PhotoImage(file = f"img_tlPrincipal_inputQuantidade.png")
input_Quantidade_bg = canvas.create_image(
    151.0, 155.0,
    image = input_Quantidade_img)

input_Quantidade = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

input_Quantidade.place(
    x = 110.0, y = 142,
    width = 82.0,
    height = 24)

input_VlrUnitario_img = PhotoImage(file = f"img_tlPrincipal_inputVltUnitario.png")
input_VlrUnitario_bg = canvas.create_image(
    348.5, 155.0,
    image = input_VlrUnitario_img)

input_VlrUnitario = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

input_VlrUnitario.place(
    x = 304.0, y = 142,
    width = 89.0,
    height = 24)

input_VlrTotal_img = PhotoImage(file = f"img_tlPrincipal_inputVltTotal.png")
input_VlrTotal_bg = canvas.create_image(
    534.5, 155.0,
    image = input_VlrTotal_img)

input_VlrTotal = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

input_VlrTotal.place(
    x = 490.0, y = 142,
    width = 89.0,
    height = 24)

input_Faturado_img = PhotoImage(file = f"img_tlPrincipal_inputFaturado.png")
input_Faturado_bg = canvas.create_image(
    711.5, 155.0,
    image = input_Faturado_img)

input_Faturado = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

input_Faturado.place(
    x = 667.0, y = 142,
    width = 89.0,
    height = 24)

input_TipoServ_img = PhotoImage(file = f"img_tlPrincipal_inputTipoServ.png")
input_TipoServ_bg = canvas.create_image(
    550.0, 119.0,
    image = input_TipoServ_img)

input_TipoServ = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

input_TipoServ.place(
    x = 344.0, y = 106,
    width = 412.0,
    height = 24)

input_CodCliente_img = PhotoImage(file = f"img_tlPrincipal_inputCodCliente.png")
input_CodCliente_bg = canvas.create_image(
    319.0, 84.0,
    image = input_CodCliente_img)

input_CodCliente = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

input_CodCliente.place(
    x = 277.0, y = 71,
    width = 84.0,
    height = 24)

input_Cliente_img = PhotoImage(file = f"img_tlPrincipal_inputCliente.png")
input_Cliente_bg = canvas.create_image(
    595.5, 84.0,
    image = input_Cliente_img)

input_Cliente = Entry(
    bd = 0,
    bg = "#8a8a8a",
    highlightthickness = 0)

input_Cliente.place(
    x = 435.0, y = 71,
    width = 321.0,
    height = 24)

input_DescrServ_img = PhotoImage(file = f"img_tlPrincipal_textDescricaoServ.png")
input_DescrServ_bg = canvas.create_image(
    291.0, 244.5,
    image = input_DescrServ_img)

input_DescrServ = Text(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

input_DescrServ.place(
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
telaPrincipal.mainloop()
