# Lê uma imagem, extrai o texto criando arquivo txt.

import cv2
import pytesseract

#caminho da instalação do pytesseract

pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')


# Lendo arquivo de imagem e extraindo o texto desta imagem

img = cv2.imread('5.jpg')
config = r'--oem 3 --psm 6 --psm 10'

resultado = pytesseract.image_to_string(img, lang='por+por_3')
resultado = resultado.replace('.', '')
resultado = resultado.replace('cheque','\n')

print(resultado)

# Criando arquivo transcricao.txt a partir a leitura da imagem

with open("print.txt", 'w', encoding='utf-8') as arquivo:
    arquivo.write(resultado)

