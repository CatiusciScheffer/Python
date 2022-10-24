# Lê uma imagem, extrai o texto criando arquivo txt.

import cv2
import pytesseract

# Lendo arquivo de imagem e extraindo o texto desta imagem
img = cv2.imread('img.png')
config = r'--oem 3 --psm 6 --psm 10'
resultado = pytesseract.image_to_string(img, lang='por')
print(resultado)

# Criando arquivo transcricao.txt a partir a leitura da imagem

with open("transcricao.txt", 'w') as arquivo:
    arquivo.write(resultado)
