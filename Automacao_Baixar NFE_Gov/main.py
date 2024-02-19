import tkinter as tk
import random
import time
import os
import shutil
import appdirs
from pathlib import Path
from datetime import datetime
from tkinter import messagebox
from window_parametros import obter_datas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException

# Pegando os valores da planilha de notas no site para gerar relação posterior
def extrair_valores(linha):
    chave = linha.get_attribute('data-chave')
    data = linha.find_element(By.CLASS_NAME, 'td-data').text.strip()
    emitida_para = linha.find_element(By.CLASS_NAME, 'td-texto-grande').text.strip()
    municipio = linha.find_element(By.CLASS_NAME, 'td-center').text.strip()
    valor = linha.find_element(By.CLASS_NAME, 'td-valor').text.strip()
    situacao = linha.find_element(By.CLASS_NAME, 'td-situacao').text.strip()

    return {
        'Chave': chave,
        'Data': data,
        'Emitida para': emitida_para,
        'Município': municipio,
        'Valor': valor,
        'Situação': situacao
    }

def iterar_linhas():
    # Iterar sobre cada linha
    for linha in linhas:
        try:
            # Extrair os valores específicos que você deseja (ajuste conforme necessário)
            valores = extrair_valores(linha)
                        
            # Converter as datas para objetos datetime
            data_formatada = datetime.strptime(valores['Data'], '%d/%m/%Y')
            data_inicio_formatada = datetime.strptime(data_inicio_pesquisa, '%d/%m/%Y')
            data_fim_formatada = datetime.strptime(data_fim_pesquisa, '%d/%m/%Y')
            
            # Se a data da linha iterada estiver entre a data inicial e final informada pelo usuário, será feito download
            if data_inicio_formatada <= data_formatada <= data_fim_formatada:
                escrever_no_arquivo(f'{valores["Data"]}   {valores["Valor"]}   {valores["Emitida para"][0:40]}   {valores["Município"]}   Download OK')

                # clicar nos 3 pontos para abrir opções
                time.sleep(tempo_variavel)
                clicar_opcoes_lista_nfe = linha.find_element(By.XPATH, './/td[7]/div/a')
                clicar_opcoes_lista_nfe.click()

                time.sleep(tempo_variavel)

                # Aguardar a opção "Download XML" estar disponível
                xpath_download = '//*[contains(@id, "popover")]/div[2]/a[contains(@href, "Download/NFSe/")]'
                time.sleep(tempo_variavel)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath_download)))
                time.sleep(tempo_variavel)

                # Clicar no link de download
                clicar_opcoes_lista_nfe_download = linha.find_element(By.XPATH, xpath_download)
                clicar_opcoes_lista_nfe_download.click()

                time.sleep(tempo_variavel)

            # Se da data não estiver entre as datas desejadas, ignorar o download
            elif data_formatada <= data_inicio_formatada:
                escrever_no_arquivo(f'{valores["Data"]}   {valores["Valor"]}   {valores["Emitida para"][0:40]}   {valores["Município"]}   *** SEM DOWNLOAD')
            # Demais casos em que as datas não estejam nos parâmetro, ignorar o download
            else:
                escrever_no_arquivo(f'{valores["Data"]}   {valores["Valor"]}   {valores["Emitida para"][0:40]}   {valores["Município"]}   *** SEM DOWNLOAD')
        except StaleElementReferenceException:
            # Se ocorrer uma exceção StaleElementReferenceException, continue para a próxima iteração
            continue

    return

# GERAR RELATÓRIO DAS NOTAS DO SITE
def escrever_no_arquivo(mensagem):
    # Obtém o caminho da pasta de downloads
    pasta_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Define o caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_downloads, f'RELATORIO_DE_DOWNLOAD.TXT')

    # Abre o arquivo em modo de adição (append) ou cria o arquivo se não existir
    with open(caminho_arquivo, 'a') as arquivo:
        # Escreve a mensagem no arquivo
        arquivo.write(mensagem + '\n')

# O DOWNLOAD ACONTECE NA PASTA PADRÃO DE DOWNLOAD, COM ISSO BUSCO OS DOWNLOADS PELO CNPJ CONTIDO NO NOME E MAIS O RELATÓRIO
        # E MOVO PARA A PASTA QUE O USUÁRIO DEFINIU
def salvar_downloas_pasta_selecionada():
    try:
        # Obtém o caminho da pasta de downloads
        pasta_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Itera sobre os arquivos na pasta de downloads
        for arquivo in os.listdir(pasta_downloads):
            caminho_arquivo = os.path.join(pasta_downloads, arquivo)

            # Verifica se o arquivo contém o valor da variável 'cnpj' e é do tipo .xml
            if cnpj in arquivo and arquivo.lower().endswith('.xml'):
                # Move o arquivo para a pasta selecionada
                shutil.move(caminho_arquivo, local_download)

            # Verifica se o arquivo é o RELATORIO_DE_DOWNLOAD.TXT
            elif arquivo == f'RELATORIO_DE_DOWNLOAD.TXT':
                # Move o arquivo para a pasta selecionada
                shutil.move(caminho_arquivo, local_download)
    except:
        # caso já existam na pasta selecionada algum xml ou o relatório, a movimentação do arquivo não será possível, então o usuário é avisado e como os downloads já abacaram o programa é forçado a encerrar
        exibir_mensagem('Falha para salvar arquivos', 'Atenção arquivos estão na pasta de download pois já existiam na pasta que você selecionou.')
        # Fechar o navegador
        driver.quit()
        quit()

def exibir_mensagem(titulo, mensagem_a_exibir):
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    messagebox.showinfo(titulo, mensagem_a_exibir)

def data_hora_now():
   # Obter a data e hora atuais
    data_hora_atual = datetime.now()

    # Formatando a data e hora
    formato_personalizado = "%Y-%m-%d %H:%M:%S"
    data_hora_formatada = data_hora_atual.strftime(formato_personalizado)

    # Exibir a data e hora formatadas
    return data_hora_formatada


# ARMAZENANDO DADOS DE ENTRADA DO USUÁRIO NAS VARIÁVEI PARA USO AQUI
data_inicio_pesquisa, data_fim_pesquisa, local_download, cnpj, senha = obter_datas()

# Gere um valor aleatório entre os valores do parâmetro
tempo_variavel = random.uniform(1, 3)

# pegar a pasta de download
pasta_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')

#@@@   achar a pasta de perfil do chrome   @@@#
# Encontrar o diretório de dados do usuário do Chrome
user_data_dir = appdirs.user_data_dir(appname="Chrome", appauthor="Google", roaming=True)
# Construir o caminho completo para o diretório do perfil 'Profile Selenium' dentro do diretório de dados do usuário
profile_dir = os.path.join(user_data_dir, 'User Data', 'Profile Selenium')
escrever_no_arquivo(f'Caminho Chrome: {profile_dir}')
escrever_no_arquivo('')
#@@@@@@         @@@@@@#

#pegar nome do usuário do sistema
nome_usuario = os.getlogin()
escrever_no_arquivo(f'Usuário: {nome_usuario}')
escrever_no_arquivo('')

chrome_options = Options()
chrome_options.add_argument(rf'--user-data-dir={profile_dir}')
chrome_options.add_experimental_option('prefs', {
    'download.prompt_for_download': False, # libera o download sem verificação
    'download.default_directory': pasta_downloads, 
    #'download.directory_upgrade': False,
    #'safebrowsing.enabled': False,
})

# ---- ABRIR NAVEGADOR ---- #
servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument(rf'--user-data-dir={profile_dir}')

time.sleep(tempo_variavel)
driver = webdriver.Chrome(service=servico, options=options)

# Esperar até que a tabela esteja carregada (pode ser necessário ajustar o seletor)
wait = WebDriverWait(driver, 10)

# maximizar a janela
driver.maximize_window()

# site a logar
time.sleep(tempo_variavel)
driver.get("https://www.nfse.gov.br/EmissorNacional/Login")
time.sleep(tempo_variavel)

# @@@---- FAZER LOGIN ----@@@ #
# preencher o cpf ou cnpj
cpf_cnpj = driver.find_element(By.ID, 'Inscricao')
cpf_cnpj.send_keys(cnpj)

time.sleep(tempo_variavel)

# preencher a senha
senha_login = driver.find_element(By.ID, 'Senha')
senha_login.send_keys(f'{senha}')

time.sleep(tempo_variavel)

# clicar em ENTRAR
btn_entrar = driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div[2]/div[1]/div/form/div[3]/button')
btn_entrar.click()

time.sleep(tempo_variavel)

# @@@---- ENTRAR NA LISTA DE NOTAS EMITIDAS ----@@@ #
lista_nfe_emitidas = driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[3]')
lista_nfe_emitidas.click()

time.sleep(tempo_variavel)

# CABEÇALHO DO RELATÓRIO
escrever_no_arquivo(data_hora_now())
escrever_no_arquivo('')
escrever_no_arquivo(f'DATA ÍNICIO: {data_inicio_pesquisa}')
escrever_no_arquivo('')
escrever_no_arquivo(f'DATA FIM: {data_fim_pesquisa}')
escrever_no_arquivo('')
escrever_no_arquivo(f'XML SALVOS EM: {local_download}')
escrever_no_arquivo('')
escrever_no_arquivo(f'CNPJ: {cnpj}')
escrever_no_arquivo('')
escrever_no_arquivo(f'SENHA: {senha}')
escrever_no_arquivo('')
# Contar e imprimir o número de elementos <li> para saber quantas páginas tenho que percorrer
# fiz fora do loop pois qdo deixei no loop diminuia o total a cada 5 pginas
numero_paginas = len(driver.find_elements(By.CSS_SELECTOR, 'ul.pagination li'))
escrever_no_arquivo(f'Total de páginas: {numero_paginas}')


# @@@---- PERCORRER A LISTA DE NOTAS MITIDAS ----@@@ #
while True:
    # Esperar até que a tabela esteja carregada
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-striped tbody tr')))

    # Localizar todas as linhas da tabela
    linhas = driver.find_elements(By.CSS_SELECTOR, 'table.table-striped tbody tr')

    # Obter a página atual
    pagina_atual = int(driver.find_element(By.CSS_SELECTOR, 'ul.pagination li.active a').text)
    escrever_no_arquivo('')
    escrever_no_arquivo(f'----------------------- Página atual: {pagina_atual} -----------------------')

    # Se a página atual for menor que o número total de páginas, clicar no botão "Próxima"
    if pagina_atual < numero_paginas:
                        
        iterar_linhas()
        
        time.sleep(tempo_variavel)
        
        #clica na próxima página
        next_page_button = driver.find_element(By.XPATH, '//ul[@class="pagination"]/li/a[@data-original-title="Próxima"]')
        next_page_button.click()
        escrever_no_arquivo('----------------------- FIM PÁGINA -----------------------')
        time.sleep(tempo_variavel)

    # iterar as linhas quando o número de páginas for igual ao total de página e com break para quebrar o loop
    elif pagina_atual == numero_paginas:
        
        iterar_linhas()
        
        time.sleep(tempo_variavel)
        escrever_no_arquivo('----------------------- FIM PÁGINA -----------------------')
        break              

# Movendo os arquivos baixados para a pasta definida pelo usuário
salvar_downloas_pasta_selecionada()

# Fechar o navegador
driver.quit()

exibir_mensagem('Sucesso', 'Download concluído, arquivos salvos na pasta selecionada!')
