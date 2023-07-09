from tkinter import Tk, Label
from PIL import ImageTk, Image

# Criar a janela principal
janela = Tk()

# Carregar a imagem
imagem = Image.open("./img/background.png")

# Redimensionar a imagem para se adequar à janela
#imagem_redimensionada = imagem.resize((800, 600))

# Converter a imagem em um objeto PhotoImage
imagem_tk = ImageTk.PhotoImage(imagem)

# Criar um widget Label com a imagem como plano de fundo
label = Label(janela, image=imagem_tk)
label.pack()

# Executar o loop principal
janela.mainloop()
