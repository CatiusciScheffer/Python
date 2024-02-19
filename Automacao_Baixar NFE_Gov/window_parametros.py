from tkinter import Tk, Label, Entry, Button, Frame, filedialog, messagebox
from datetime import datetime

data_inicio_pesquisa = None
data_fim_pesquisa = None
caminho_pasta = None
cnpj = None
senha = None

def obter_datas():
    def obter_entrada():
        # Obtém os valores dos campos de entrada
        data_inicio = entry_data_inicio.get()
        data_fim = entry_data_fim.get()
        cnpj_pesquisar = entry_CNPJ.get()
        senha_login = entry_senha_login.get()

        # Verifica se os valores têm o formato correto (dd/mm/yyyy)
        if not validar_formato(data_inicio) or not validar_formato(data_fim):
            messagebox.showerror("Formato Inválido", "Por favor, digite as datas no formato dd/mm/yyyy.")
            return

        # Se os formatos estiverem corretos, atribui às variáveis globais
        global data_inicio_pesquisa, data_fim_pesquisa, cnpj, senha
        data_inicio_pesquisa = data_inicio
        data_fim_pesquisa = data_fim
        cnpj = cnpj_pesquisar
        senha = senha_login

        # Fecha a janela
        root.destroy()

    def validar_formato(data):
        try:
            # Tenta converter a string para o formato de data especificado
            datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            # Se houver um erro, a string não está no formato correto
            return False

    def escolher_pasta():
        pasta_selecionada = filedialog.askdirectory()
        if pasta_selecionada:
            global caminho_pasta
            caminho_pasta = pasta_selecionada
            

    root = Tk()
    root.title("Digite o período para fazer o download das Notas")
    root.geometry('500x400')

    # Frame central para centralizar os elementos
    frame_central = Frame(root)
    frame_central.place(relx=0.5, rely=0.5, anchor='center')

    # CNPJ A LOGAR
    label_CNPJ = Label(frame_central, pady=5, text="CNPJ: ")
    label_CNPJ.pack()
    entry_CNPJ = Entry(frame_central)
    entry_CNPJ.pack()

    # SENHA PARA LOGIN
    label_senha_login = Label(frame_central, pady=5, text="SENHA: ")
    label_senha_login.pack()
    entry_senha_login = Entry(frame_central)
    entry_senha_login.pack()

    # DATA DE INÍCIO DA BUSCA
    label_data_inicio = Label(frame_central, pady=5, text="DATA DE INÍCIO(dd/mm/yyyy): ")
    label_data_inicio.pack()
    entry_data_inicio = Entry(frame_central)
    entry_data_inicio.pack()

    # Adicionando um espaço com um frame vazio
    frame_espaco = Frame(frame_central, height=10)
    frame_espaco.pack()

    label_data_fim = Label(frame_central, pady=5, text="DATA FIM(dd/mm/yyyy): ")
    label_data_fim.pack()

    entry_data_fim = Entry(frame_central)
    entry_data_fim.pack()

    # Campo vazio para dar espaço
    espaco_vazio = Label(frame_central, pady=5, text="")
    espaco_vazio.pack()

    # Adicionando um botão para escolher a pasta
    button_escolher_pasta = Button(frame_central, text="SALVAR EM: ", command=escolher_pasta, padx=20)
    button_escolher_pasta.pack()

    # Campo vazio para dar espaço
    espaco_vazio = Label(frame_central, pady=5, text="")
    espaco_vazio.pack()
    

    button_ok = Button(frame_central, text="COMEÇAR DOWNLOAD", command=obter_entrada, padx=20)  
    button_ok.pack()

    # Ajustando a posição verticalmente
    altura_frame = frame_central.winfo_reqheight()
    frame_central.place_configure(rely=0.5 - altura_frame / (2 * root.winfo_reqheight()))

    root.mainloop()
    
    # Retorna os valores apenas se a janela foi fechada corretamente
    return data_inicio_pesquisa, data_fim_pesquisa, caminho_pasta, cnpj, senha

# # Obter entradas do usuário para as datas de pesquisa e a pasta
# inicio, fim, pasta, cnpj, senha = obter_datas()
# print("Data de Início:", inicio)
# print("Data Fim:", fim)
# print("Caminho da Pasta:", pasta)
# print("CNPJ:", cnpj)
# print("senha:", senha)
