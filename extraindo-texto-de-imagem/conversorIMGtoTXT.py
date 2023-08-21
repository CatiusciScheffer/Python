import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage, Button

# Configuração do caminho do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Função para selecionar o arquivo de imagem
def selecionar_arquivo():
    """
    Abre uma janela de diálogo para permitir que o usuário selecione um arquivo de imagem.
    
    Returns:
        str: O caminho completo do arquivo de imagem selecionado pelo usuário.
    """
    # Abre a janela de diálogo para seleção de arquivo de imagem
    file_path = filedialog.askopenfilename(title="Selecione o arquivo de imagem", filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
    
    # Verifica se o usuário cancelou a seleção
    if not file_path:
        status_label.config(text="Nenhum arquivo selecionado.")
        return
    
    # Atualiza o rótulo de status com o caminho do arquivo selecionado
    status_label.config(text=f"Arquivo selecionado: {file_path}")
    
    return file_path

# Função para converter e baixar o arquivo de texto
def converter_e_baixar(file_path):
    """
    Converte uma imagem em texto usando o Tesseract e salva o resultado em um arquivo de texto.

    Args:
        file_path (str): O caminho completo para o arquivo de imagem a ser convertido.

    """
    # Verifica se o caminho do arquivo de imagem foi fornecido
    if not file_path:
        status_label.config(text="Nenhum arquivo selecionado.")
        return

    # Lê a imagem do arquivo usando o OpenCV
    img = cv2.imread(file_path)
    config = r'--oem 3 --psm 6 --psm 10'

    # Executa a extração de texto da imagem usando o Tesseract
    resultado = pytesseract.image_to_string(img, lang='por+por_3')

    # Solicita ao usuário para escolher o local e nome do arquivo de saída
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

    # Verifica se um local de salvamento foi selecionado
    if not save_path:
        status_label.config(text="Nenhum local de salvamento selecionado.")
        return

    # Salva o resultado em um arquivo de texto
    with open(save_path, 'w', encoding='utf-8') as arquivo:
        arquivo.write(resultado)

    # Atualiza o rótulo de status para mostrar onde o texto foi salvo
    status_label.config(text=f"Texto extraído foi salvo em: {save_path}")

# Configuração da janela principal
window = tk.Tk()
window.geometry("496x315")
window.configure(bg="#ffffff")
window.title('Converter imagem (JPG, JPEG, PNG) em texto')

# Funções para manipulação dos botões
def selecionar_arquivo_click():
    """
    Função para manipular o clique no botão de seleção de arquivo.

    Abre a janela de diálogo para selecionar um arquivo de imagem. 
    Se um arquivo for selecionado, atualiza o rótulo de status para mostrar o arquivo selecionado.

    """
    # Chama a função para selecionar um arquivo de imagem
    arquivo_selecionado = selecionar_arquivo()
    
    # Verifica se um arquivo foi selecionado e atualiza o rótulo de status
    if arquivo_selecionado:
        status_label.config(text=f"Arquivo selecionado: {arquivo_selecionado}")


def converter_e_baixar_click():
    """
    Função para manipular o clique no botão de conversão e download.

    Obtém o caminho do arquivo selecionado a partir do rótulo de status,
    em seguida, chama a função para converter a imagem em texto e salvar o resultado.

    """
    # Obtém o caminho do arquivo selecionado a partir do rótulo de status
    arquivo_selecionado = status_label.cget("text")
    
    # Extrai o caminho do arquivo da string e chama a função de conversão e download
    converter_e_baixar(arquivo_selecionado.split(": ")[1])


# Criando a janela do programa
canvas = tk.Canvas(
    window,
    bg="#ffffff",
    height=315,
    width=496,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

# Criação dos botões e elementos da interface

# cria o background
background_img = PhotoImage(file="./img/background.png")
background = canvas.create_image(
    248.0, 157.5,
    image=background_img)

# cria o botão de selecionar o arquivo
img_btn_selecionar = PhotoImage(file="./img/img_btn_selecionar.png")
btn_selecionar = Button(
    image=img_btn_selecionar,
    borderwidth=0,
    highlightthickness=0,
    command=selecionar_arquivo_click,
    relief="flat")
btn_selecionar.place(
    x=97, y=100,
    width=298,
    height=45)

# cria o botão de converter e salvar o arquivo
img_btn_download = PhotoImage(file="./img/img_btn_download.png")
btn_download = Button(
    image=img_btn_download,
    borderwidth=0,
    highlightthickness=0,
    command=converter_e_baixar_click,
    relief="flat")
btn_download.place(
    x=97, y=156,
    width=298,
    height=45)

# local onde aparece o status da conversão
status_label = tk.Label(
    window,
    text="Nenhum arquivo selecionado.",
    font=("Arial", 8),
    fg='gray',
    bg="#DCDCDC")
status_label.place(x=13, y=282)

window.resizable(False, False)
window.mainloop()
