import pyautogui
import time

time.sleep(5)
# Obtém as coordenadas atuais do mouse
posicao = pyautogui.position()

# Exibe as coordenadas
print(posicao)