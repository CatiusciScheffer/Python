from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib
import time
import os
import time
import random
import pandas as pd

# Gere um valor aleatório entre 5 e 6 segundos
tempo_variavel = random.uniform(5, 8)

servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\cpcsc\AppData\Local\Google\Chrome\User Data\Profile Selenium')

time.sleep(tempo_variavel)
driver = webdriver.Chrome(service=servico, options=options)

time.sleep(tempo_variavel)
driver.get("https://web.whatsapp.com")

# esperar a tela que mostra os contatos carregar, so saí do looping qdo carregar
while len(driver.find_elements(By.ID, 'side')) < 1: 
    time.sleep(3)
time.sleep(tempo_variavel)

# lista onde será extraídos os contados, a mensagem e o arquivo para anexar
lista_contatos = pd.read_excel(r"AVISO_FGTS.xlsx")

for linha in lista_contatos.index:
    # enviar uma mensagem para a pessoa
    nome = lista_contatos.loc[linha, "nome"]
    mensagem = lista_contatos.loc[linha, "mensagem"]
    arquivo = lista_contatos.loc[linha, "arquivo"]
    telefone = lista_contatos.loc[linha, "telefone"]
    print(telefone)
    time.sleep(tempo_variavel)
    texto = mensagem.replace("fulano", nome)
    texto = urllib.parse.quote(texto)
    time.sleep(tempo_variavel)
    # enviar a mensagem
    link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"
    time.sleep(tempo_variavel)
    driver.get(link)
    time.sleep(tempo_variavel)
    # LISTA DA ESQUEDA COM AS CONVERSAS CARREGAR
    while len(driver.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
        time.sleep(1)
    time.sleep(tempo_variavel) # só uma garantia
    print('AQUI')
    # você tem que verificar se o número é inválido
    if len(driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
        time.sleep(tempo_variavel)
        print('CAÍ NO IF')
        time.sleep(tempo_variavel)
        # CLICA NO BOTÃO DE ENVIAR A MENSAGEM APÓS ESCREVER
        enviar_msg_sem_anexo = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
        time.sleep(tempo_variavel)
        enviar_msg_sem_anexo.click()
        # se tiver anexo e a coluna arquivo não for N
        if arquivo != "N":
            caminho_completo = os.path.abspath(rf"{arquivo}")
            #clicar no clips para anexar a img
            anexar_documento = driver.find_element(By.XPATH, 
                                   '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span')
            time.sleep(tempo_variavel)
            anexar_documento.click()
            time.sleep(tempo_variavel)
            #este é o clips que na verdade é um input com caminho do arquivo que só habilita na inspeção após clicar no clips acima (aparece logo abaixo da div do clips)
            input_caminho_anexo = driver.find_element(By.XPATH, 
                                   '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[1]/li/div/input')
            time.sleep(tempo_variavel)
            input_caminho_anexo.send_keys(caminho_completo)
            time.sleep(tempo_variavel)
            #após anexar o caminho da imagem aqui clica na seta de envio
            enviar_anexo = driver.find_element(By.XPATH, 
                                   '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
            time.sleep(tempo_variavel)
            enviar_anexo.click()
            time.sleep(tempo_variavel)
    else:
        print('não caí no if da imagem')
            
        time.sleep(tempo_variavel)
        
    time.sleep(10 + tempo_variavel)
driver.quit()