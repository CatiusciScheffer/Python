import pyautogui
import time

time.sleep(2)
# Obtém as coordenadas atuais do mouse
posicao = pyautogui.position()

# Exibe as coordenadas
print(posicao)