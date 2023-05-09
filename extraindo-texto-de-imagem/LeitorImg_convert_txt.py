# Lê uma imagem, extrai o texto criando arquivo txt.

import cv2
import pytesseract

#caminho da instalação do pytesseract

pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')


# Lendo arquivo de imagem e extraindo o texto desta imagem

img = cv2.imread('teste.jpg')
config = r'--oem 3 --psm 6 --psm 10'

resultado = pytesseract.image_to_string(img, lang='por')
resultado = resultado.replace('.', '')
resultado = resultado.replace('/n','')

print(resultado)

# Criando arquivo transcricao.txt a partir a leitura da imagem

with open("transcricao.txt", 'w') as arquivo:
    arquivo.write(resultado)

