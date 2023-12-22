import pyautogui
import time

# Obtém as coordenadas atuais do cursor do mouse
x, y = pyautogui.position()
time.sleep(5)
# Imprime as coordenadas
print(f'Coordenadas do Mouse: x = {x}, y = {y}')
