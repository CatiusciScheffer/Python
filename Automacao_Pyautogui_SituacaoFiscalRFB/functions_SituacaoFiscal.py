import time
import pyautogui
import sys
import numpy as np
import pyperclip
import cv2
from PIL import ImageGrab
import csv
import logging

# Configuração do logging com nível DEBUG
logging.basicConfig(filename='situacao_fiscal_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class LerSituacaoFiscal:
    def __init__(self):
        
        pyautogui.PAUSE = 5
        pyautogui.FAILSAFE = True
        self.tempo_esperar_carregar = 3
      
    def esperarImagemCarregar(self, imagem, id_empresa=None, empresa=None, cnpj=None, max_attempts=50):
        
        for _ in range(max_attempts):
            time.sleep(self.tempo_esperar_carregar)
            imagem_procurada = pyautogui.locateOnScreen(imagem, grayscale=True, confidence=0.3)
            if imagem_procurada:
                return imagem_procurada
            else:
                logging.exception('Erro na função "esperarImagemCarregar"!')
                continue


    def pesquisar_texto(texto_colar):
        try:
            pyautogui.hotkey('ctrl', 'f')  # Abre a caixa de pesquisa
            texto_procurar = str(texto_colar)
            pyperclip.copy(texto_procurar)  # Copia o texto para a área de transferência
            pyautogui.hotkey('ctrl', 'v')  # Cola o texto na caixa de pesquisa
        except Exception as e:
            logging.exception(f'Erro na função "pesquisar_texto" {e}')

    def voltarHome(self):
        # Localiza o centro da imagem 'home.png' na tela
        try:
            volta_home = pyautogui.locateOnScreen(r'.\img\home.png')

            if volta_home:
                centro_volta_home = pyautogui.locateCenterOnScreen (r'.\img\home.png')
                # Clica no centro da imagem para voltar à página inicial
                pyautogui.click(centro_volta_home)
            
        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=742, y=893)
            logging.exception('Erro na função "voltarHome"!')

    def procurarCor(self):
        # tive que criar esta função porque os outros métodos de clicar onde precisava na tela da caixa de entrada da receita federal não funcionaram, não podia ser por coordenadas e salvando as imagens também não funcionou, então quando com ctrl+f para localizar um texo, o mesmo era marcado com a cor aranja o que me permitiu procurar esta cor, pegar o primeiro ponto dela na lista e clicar.
        
        try:    
            # Captura uma região da tela (no exemplo, toda a tela: 1920x1080 pixels)
            screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
            # Define a cor laranja que você deseja procurar (no formato BGR)
            color_to_find_laranja = (255, 150, 50)
            color_to_find_amarelo = (255, 255, 0)
            # Encontra os pixels correspondentes à cor laranja na imagem
            mask = cv2.inRange(screen, color_to_find_laranja, color_to_find_laranja)
            mask1 = cv2.inRange(screen, color_to_find_amarelo, color_to_find_amarelo)
            # Obtém as coordenadas dos pixels de cor laranja
            if np.any(mask > 0):
                coordinates = np.column_stack(np.where(mask > 0))
            elif np.any(mask1 > 0):
                coordinates = np.column_stack(np.where(mask1 > 0))

            return coordinates
        except Exception as e:
            time.sleep(self.tempo_esperar_carregar)
            logging.exception(f'Erro na função "procuraCor": {e}!')
            return coordinates
        

    def clicarSeCorLaranja(self):
        
        try:
            # Verifica se há coordenadas de pixels de cor laranja
            if len(listaCoordenadas := self.procurarCor()) > 0:
                for coord in listaCoordenadas:
                    pyautogui.click(coord[1], coord[0])
                    break
                return True
            return False
        except Exception as e:
            logging.exception(f'Erro na função "clicarSeCorLaranja": {e}')
            return False

    def abrirNavegador(self, enderecoHTTP):
        try:
            # Abre o diálogo "Executar" pressionando 'Win + R'
            pyautogui.hotkey('win', 'r')
            # Aguarda até que a imagem 'tl_win_exec.png' seja carregada
            self.esperarImagemCarregar(r'.\img\tl_win_exec.png')
            # Escreve o endereço HTTP no campo de texto do diálogo
            pyautogui.write(enderecoHTTP)
            # Pressiona Enter para abrir o navegador com o URL especificado
            pyautogui.press('enter')
        except Exception as e:
            logging.exception(f'Erro na função "abrirNavegador": {e}')
        
    def fecharNavegador(self):
        # Pressiona 'Alt + F4' para fechar a janela do navegador ativa
        pyautogui.hotkey('ctrl', 'w')

    def ler_csv(self, arquivo_csv):
        try:
            dados_csv = []
            with open(arquivo_csv, mode='r', encoding='ISO-8859-1') as file:
                csv_reader = csv.DictReader(file, delimiter=';')
                for row in csv_reader:
                    dados_csv.append(row)
            return dados_csv
        except Exception as e:
            logging.exception(f'Erro na função "ler_csv: "{e}')
        
    def alterarPerfildeAcesso(self):
        try:
            alterar_perfil = pyautogui.locateCenterOnScreen(r'.\img\btn_alt_perfil.png')

            if alterar_perfil:
                # Clica no centro da imagem para voltar à página inicial
                pyautogui.click(alterar_perfil)

        except pyautogui.ImageNotFoundException:
            time.sleep(self.tempo_esperar_carregar)
            pyautogui.click(x=1167, y= 223)
            logging.exception('Except "alterarPerfildeAcesso"!')
        
    def digitarCNPJ_AlterarPerfil(self, cnpj):
        try:
            self.esperarImagemCarregar(r'.\img\cp_digitar_cnpj.png')
            campo_digitar_cnpj = pyautogui.locateCenterOnScreen(r'.\img\cp_digitar_cnpj.png')
            
            if campo_digitar_cnpj:
                pyautogui.click(campo_digitar_cnpj)
                time.sleep(self.tempo_esperar_carregar)
                pyautogui.write(cnpj)
        
        except pyautogui.ImageNotFoundException:
            time.sleep(self.tempo_esperar_carregar)
            pyautogui.click(x=582, y= 450)
            logging.exception('Except "digitarCNPJ_AlterarPerfildeAcesso"!')

    def clicar_AlterarPerfil(self):
        try:
            # clica no botão alterar cnpj                
            self.esperarImagemCarregar(r'.\img\btn_conf_alt_cnpj1.png')
            btn_alt_cnpj = pyautogui.locateCenterOnScreen(r'.\img\btn_conf_alt_cnpj1.png')
            
            if btn_alt_cnpj:
                pyautogui.click(btn_alt_cnpj)

        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=816, y= 473)
            logging.exception('Except "clicar_AlterarPerfil"!')

    def clicar_CertidaoSituacaoFiscal(self):
        try:
            self.esperarImagemCarregar(r'.\img\btn_click_situacaoFiscalx.png')            
            btn_sitFiscal = pyautogui.locateCenterOnScreen(r'.\img\btn_click_situacaoFiscalx.png')
            
            if btn_sitFiscal:
                pyautogui.click(btn_sitFiscal)
        
        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=505, y= 270)
            logging.exception('Except "clicar_CertidaoSituacaoFiscal"!')
            
    def clicar_CertidaoSituacaoFiscalList(self):
        try:
            self.esperarImagemCarregar(r'.\img\espera_btn_lista_sitFiscal.png')
            btn_sitFiscal_lista = pyautogui.locateOnScreen(r'.\img\btn_escolhe_situacaoFiscal.png')
            
            if btn_sitFiscal_lista:
                pyautogui.click(btn_sitFiscal_lista)

        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=362, y= 445)
            logging.exception('Except "clicar_CertidaoSituacaoFiscalList"!')

    def clicar_GerarRelatorio(self):
        try:
            self.esperarImagemCarregar(r'.\img\tela_gerar_relatorio.png')
            teste = pyautogui.locateOnScreen((r'.\img\tela_gerar_relatorio.png'))
            #print(f'ACHEI IMAGEM TELA RELATÓRIO SITUAÇÃO {teste}')
            
            btn_GerarRelatorio = pyautogui.locateOnScreen(r'.\img\#btn_gerarRelatorio.png')
            #print(f'ahei botão {btn_GerarRelatorio}')
            btn_GerarRelatorio_amarelo = pyautogui.locateOnScreen(r'.\img\#btn_GerarRelatorio_amarelo.png')
            #print(f'achei botão amarelo {btn_GerarRelatorio_amarelo}')

            if btn_GerarRelatorio:
                pyautogui.click(btn_GerarRelatorio)
                #print('Cliquei no botão de "Gerar Relatório"')
            
            elif btn_GerarRelatorio_amarelo:
                pyautogui.click(btn_GerarRelatorio_amarelo)
                #print('Cliquei no botão de "Gerar Relatório AMARELO"')

        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=934, y= 392)
            logging.exception('Except "clicar_GerarRelatorio"!')

                
    def escrever_dados_no_csv(self, arquivo_csv, dados_relatorio):
        try:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as arquivo:
                campo_nomes = ['ID', 'EMPRESA', 'CNPJ', 'VERIFICADO']
                escritor_csv = csv.DictWriter(arquivo, fieldnames=campo_nomes)
                if arquivo.tell() == 0:
                    escritor_csv.writeheader()
                escritor_csv.writerow(dados_relatorio)
        except FileNotFoundError:
            ???
            

    
    def chegar_download(self):
        time.sleep(self.tempo_esperar_carregar)
        self.abrirNavegador('chrome https://cav.receita.fazenda.gov.br')
        time.sleep(self.tempo_esperar_carregar)
        self.clicar_CertidaoSituacaoFiscal()
        time.sleep(self.tempo_esperar_carregar)
        self.clicar_CertidaoSituacaoFiscalList()                  
        time.sleep(self.tempo_esperar_carregar)

    def msg_logar_certificado(self):
        pyautogui.alert('SIGA AS INSTRUÇÕES:\n1) Feche todas as janelas do Chrome;\n2) Logue novamente com Chrome o site da RFB com certificado do escritório;\n3) Agora clique em ok e não mexa mais no PC;')

    def verificarSituacaoFiscalCNPJ(self, arquivo_csv):
        
        # Lê os dados do arquivo CSV
        dados = self.ler_csv(arquivo_csv)        

        self.chegar_download()

        # Itera sobre os CNPJs na lista e consulta no ecac cada item(cnpj) dela
        for i, linha in enumerate(dados):
                
            cnpj = linha['CNPJ']
            id_empresa = linha['ID']
            empresa = linha['EMPRESA']
            status = linha['VERIFICADO']                
                
            # Verifica o status e atribui 'Sim' ou 'Não' a 'verificado'
            if status == 'NAO':
                verificado = 'SIM'
            else:
                verificado = '?'
                
            # Adicione as informações à lista de dados
            dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': verificado}                
            
            contagem_downloads = 0
            
            time.sleep(self.tempo_esperar_carregar)

            # clica para alterar perfil
            self.alterarPerfildeAcesso()

            # Insere o CNPJ
            self.digitarCNPJ_AlterarPerfil(cnpj)
                           
            # clica no botão alterar cnpj
            self.clicar_AlterarPerfil()
                        
            time.sleep(self.tempo_esperar_carregar) 

            ################EXCEPT NAS MENSAGENS POR ERRO AO ALTERAR PERFIL################
            
            #NÃO ALTEROU O PERFIL_MENSAGEN NA CAIXA DE ENTRADA
            try:
                msg_nova_cx_postal = pyautogui.locateOnScreen(r'.\img\cx_ir_caixa_entrada.png')

                if msg_nova_cx_postal is not None:
                    #escrever no relatório
                    texto_msg_cx_entrada = '---> Mensagem na Caixa de Entrada!!!'
                    dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_msg_cx_entrada}
                    self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                    time.sleep(self.tempo_esperar_carregar)
                    # se entrar na caixa postal poderá ter várias mensagens que precisam ser lidas
                    # então não quero fazer isso, tenho que voltar para o início do for mas no póximo índice
                    contagem_downloads += 1
                    # vou ter que fechar todas as abas do navegador
                    pyautogui.hotkey('ctrl', 'shift', 'w')
                    # logar novamento com certificado
                    self.msg_logar_certificado()
                    #vou ter que começar o código do início 
                    self.chegar_download()
                    continue

            except pyautogui.ImageNotFoundException:
                    print('Imagem "cx_ir_caixa_entrada" não encontrada. Executando as próximas linhas mesmo assim.')
                
            #NÃO ALTEROU O PERFIL_FALTA PROCURAÇÃO
            try:
                procuracao_problema = pyautogui.locateOnScreen(r'.\img\proc_inexistente.png')
                if procuracao_problema is not None:
                    texto_msg_erro_procuracao = '---> Ausência de procuração!!!'
                    
                    dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_msg_erro_procuracao}
                    self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                    
                    #se não tem procuração, vou er que sair completamente de todas as páginas do chrome, começar novamente deste indice em diante
                    contagem_downloads += 1
                    # vou ter que fechar todas as abas do navegador
                    pyautogui.hotkey('ctrl', 'shift', 'w')
                    # logar novamento com certificado
                    self.msg_logar_certificado()
                    #vou ter que começar o código do início 
                    self.chegar_download()
                    continue
                
            except pyautogui.ImageNotFoundException:
                print('Imagem "proc_inexistente.png" não encontrada. Executando as próximas linhas mesmo assim.')

            #NÃO ALTEROU O PERFIL_PROCURAÇÃO EXPIRADA
            try:
                procuracao_problema = pyautogui.locateOnScreen(r'.\img\proc_expirada.png')
                if procuracao_problema is not None:
                    texto_msg_erro_procuracao = '---> Procuração Vencida!!!'
                    
                    dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_msg_erro_procuracao}
                    self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                    
                    #se não tem procuração, vou er que sair completamente de todas as páginas do chrome, começar novamente deste indice em diante
                    contagem_downloads += 1
                    # vou ter que fechar todas as abas do navegador
                    pyautogui.hotkey('ctrl', 'shift', 'w')
                    # logar novamento com certificado
                    self.msg_logar_certificado()
                    #vou ter que começar o código do início 
                    self.chegar_download()
                    continue
                
            except pyautogui.ImageNotFoundException:
                print('Imagem "proc_expirada.png" não encontrada. Executando as próximas linhas mesmo assim.')
            

            #NÃO ALTEROU O PERFIL_PÁGINA EXPIRADA 
            try:
                pagina_expirada = pyautogui.locateOnScreen(r'.\img\pagina_expirou.png')
                #print(pagina_expirada)
                if pagina_expirada is not None:
                    texto_msg_erro_pg = '******** Página expirou, operação cancelada *********'
                    dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_msg_erro_pg}
                    self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                    time.sleep(self.tempo_esperar_carregar)
                    self.voltarHome()
                    #print('página expirada')
                    sys.exit()

            except pyautogui.ImageNotFoundException:
                print('Imagem "pagina_expirou.png" não encontrada. Executando as próximas linhas mesmo assim.')
                    
            ##NÃO ALTEROU O PERFIL_MENSAGEM DE QUE ESTE ACESSO É ROBOTIZADO
            try:
                msg_robotizado = pyautogui.locateOnScreen(r'.\img\msg_automacao.png')
                if msg_robotizado is not None:
                    self.digitarCNPJ_AlterarPerfil(cnpj)
                    pyautogui.press('backspace', presses=14)
                    pyautogui.write(cnpj)
                    self.clicar_AlterarPerfil()
                
            except pyautogui.ImageNotFoundException:
                print('Imagem "msg_automacao.png" não encontrada. Executando as próximas linhas mesmo assim.')

            ###############AQUI AS MENSAGENS NÃO ACONTECERAM OU FORAM RESOLVIDAS E COMEÇAMOS O DOWNLOAD DOS RELTÓRIOS DE SITUAÇÃO FISCAL.###############

            try:   
                time.sleep(self.tempo_esperar_carregar) 
                self.esperarImagemCarregar(r'.\img\espera_relatorios_aparecer.png')
                
                time.sleep(self.tempo_esperar_carregar)

                img_tela_download_relatorio = pyautogui.locateOnScreen(r'.\img\espera_relatorios_aparecer.png')

                time.sleep(self.tempo_esperar_carregar)

                if img_tela_download_relatorio:
                    #print('achei a tela de relatório')
                    #print(img_tela_download_relatorio)
                    #clicar na gerar relatório da esquerda
                    self.procurarTexto('Gerar Relatório')
                    time.sleep(self.tempo_esperar_carregar)
                    process = self.clicarSeCorLaranja()
                    time.sleep(self.tempo_esperar_carregar)                
                                    
                    if process == True:
                        # gerar_relatorio = pyautogui.position(x=915, y=393)#gerar relatório da direita
                        # time.sleep(0.5)
                        # pyautogui.click(gerar_relatorio)
                        # time.sleep(self.tempo_esperar_carregar)
                        # time.sleep(0.5)
                        # pyautogui.press('esc')
                        # time.sleep(0.1)
                        # pyautogui.press('esc')
                        time.sleep(0.2)
                        self.clicar_GerarRelatorio()
                        time.sleep(0.3) 
                        pyautogui.press('esc')    

                        # Escreva as informações no CSV
                        dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': 'Download OK!!!'}
                            
                        contagem_downloads += 1

                        self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                        continue                    
                            
            except pyautogui.ImageNotFoundException:
                texto_msg_erro_download = '******** Erro no download!********'
                                
                dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_msg_erro_download}
                                
                # Escreva as informações no CSV
                self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                #print('não achei a tela de download')
                contagem_downloads -= 1
                #print('não achei a tela de download')                
            
            time.sleep(self.tempo_esperar_carregar)            
                
            #print(f'LINHA VERIFICADO:{i}')
            i = i + 1
            # Verifica se todos os CNPJs foram processados
            if i <= len(dados):
                print(len(dados))
                continue
            if i >= len(dados):
                self.escrever_dados_no_csv('relatorio.csv', contagem_downloads)   
                        
                    
        # Aguarda por um período antes de recomeçar o processo
        time.sleep(self.tempo_esperar_carregar)

        


        
