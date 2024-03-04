import time
import pyautogui
import sys
import numpy as np
import pyperclip
import cv2
from PIL import ImageGrab
import csv

class LerSituacaoFiscal:
    def __init__(self):
        """
        Classe para configurar a automação de tarefas com o PyAutoGUI.

        Esta classe define configurações importantes para automação de tarefas
        utilizando a biblioteca PyAutoGUI.

        Atributos:
            PAUSE (float): Tempo de pausa entre a execução de cada ação (em segundos).
            FAILSAFE (bool): Habilita a verificação de segurança que permite a interrupção
                da automação movendo o cursor para o canto superior esquerdo da tela.

        Exemplo de uso:
            automation = AutomationUtils()
            # Configura uma pausa de 4 segundos entre as ações
            # e ativa a função FAILSAFE.
        """
        pyautogui.PAUSE = 4.5
        pyautogui.FAILSAFE = True
        self.tempo_esperar_carregar = 1.5
      
    def esperarImagemCarregar(self, imagem, id_empresa=None, empresa=None, cnpj=None, max_attempts=50):
        """
        Espera até que uma imagem seja localizada na tela.

        Esta função utiliza a biblioteca PyAutoGUI para procurar repetidamente uma imagem
        na tela. Ela realiza várias tentativas até encontrar a imagem ou atingir o número
        máximo de tentativas definido por `max_attempts`.

        Args:
            imagem (str): O caminho para a imagem que você deseja localizar na tela.
            id_empresa (str): O ID da empresa.
            empresa (str): O nome da empresa.
            cnpj (str): O CNPJ da empresa.
            max_attempts (int, opcional): O número máximo de tentativas antes de desistir
                de encontrar a imagem. 

        Returns:
            tuple or None: Retorna uma tupla contendo as coordenadas (x, y) da posição da
                imagem encontrada na tela, ou None se a imagem não for encontrada após
                todas as tentativas.
        """
        for _ in range(max_attempts):
            time.sleep(self.tempo_esperar_carregar)
            imagem_procurada = pyautogui.locateOnScreen(imagem, grayscale=True, confidence=0.3)
            if imagem_procurada:
                return imagem_procurada
            else:
                texto_pag_carreg = 'Erro ao carregar página, situação fiscal não baixada!'
                dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_pag_carreg}
                self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                continue

    def procurarTexto(self, texto_colar):
        """
        Realiza uma pesquisa de texto em um documento ou aplicativo.

        Esta função utiliza as bibliotecas PyAutoGUI e Pyperclip para automatizar
        uma pesquisa de texto em um documento ou aplicativo. Ela pressiona as teclas
        de atalho 'Ctrl + F' para abrir a caixa de pesquisa, cola o texto a ser
        procurado da área de transferência (clipboard) e inicia a pesquisa.

        Args:
            texto_colar (str): O texto que será colado na caixa de pesquisa.

        Exemplo de uso:
            automation = AutomationUtils()
            texto_a_procurar = "Exemplo de texto a ser procurado"
            automation.procurarTexto(texto_a_procurar)

        Observações:
            Certifique-se de que o documento ou aplicativo suporta a funcionalidade de
            pesquisa e que a janela relevante esteja em foco antes de chamar esta função.
        """
        # Pressiona 'Ctrl + F' para abrir a caixa de pesquisa
        pyautogui.hotkey('ctrl', 'f')
        # Converte o texto a ser procurado em uma string (caso não seja)
        texto_procurar = str(texto_colar)
        # Copia o texto para a área de transferência (clipboard)
        pyperclip.copy(texto_procurar)
        # Cole o texto na caixa de pesquisa usando 'Ctrl + V'
        pyautogui.hotkey('ctrl', 'v')

    def voltarHome(self):
        """
        Clica no botão 'HOME' para retornar à página inicial.

        Esta função utiliza a biblioteca PyAutoGUI para localizar o centro da imagem
        representando o botão 'HOME' na tela e, em seguida, clica nesse ponto para
        retornar à página inicial.

        Exemplo de uso:
            automation = AutomationUtils()
            automation.voltarHome()

        Observações:
            Certifique-se de que a imagem 'home.png' corresponda ao botão 'HOME' desejado
            e que a janela relevante esteja em foco antes de chamar esta função.
        """
        # Localiza o centro da imagem 'home.png' na tela
        try:
            volta_home = pyautogui.locateOnScreen(r'.\img\home.png')

            if volta_home:
                centro_volta_home = pyautogui.locateCenterOnScreen (r'.\img\home.png')
                # Clica no centro da imagem para voltar à página inicial
                pyautogui.click(centro_volta_home)
            else:
                print("Imagem 'home.png' não encontrada. Certifique-se de que a imagem corresponde ao botão 'HOME'.")
        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=742, y=893)
            print('imagem para volar pra home não localizada, cliquei nas coordenadas')

    def procurarCor(self):
        # tive que criar esta função porque os outros métodos de clicar onde precisava na tela da caixa de entrada da receita federal não funcionaram, não podia ser por coordenadas e salvando as imagens também não funcionou, então quando com ctrl+f para localizar um texo, o mesmo era marcado com a cor aranja o que me permitiu procurar esta cor, pegar o primeiro ponto dela na lista e clicar.
        """
        Procura por pixels de cor laranja em uma captura de tela.

        Esta função captura uma região da tela, define a cor laranja que deseja procurar
        (no formato BGR), e encontra os pixels correspondentes a essa cor na imagem.

        Returns:
            list of tuples: Uma lista de tuplas contendo as coordenadas (x, y) dos pixels
                que correspondem à cor laranja na imagem.

        Exemplo de uso:
            automation = AutomationUtils()
            coordenadas_laranja = automation.procurarCor()
            if coordenadas_laranja:
                print("Coordenadas dos pixels de cor laranja:", coordenadas_laranja)
            else:
                print("Nenhum pixel de cor laranja encontrado na captura de tela.")
        """
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
        except:
            time.sleep(self.tempo_esperar_carregar)
            print('erro na função procura cor')
            return coordinates
        

    def clicarSeCorLaranja(self):
        """
        Clica na primeira ocorrência de cor laranja na tela, se existir.

        Esta função verifica se há pixels de cor laranja na captura de tela e,
        se encontrar, clica na primeira ocorrência.

        Returns:
            bool: True se um pixel de cor laranja foi encontrado e clicado, False caso contrário.

        Exemplo de uso:
            automation = AutomationUtils()
            if automation.clicarSeCorLaranja():
                print("Clicou na primeira ocorrência de cor laranja.")
            else:
                print("Nenhuma cor laranja encontrada na tela.")
        """
        # Verifica se há coordenadas de pixels de cor laranja
        if len(listaCoordenadas := self.procurarCor()) > 0:
            for coord in listaCoordenadas:
                pyautogui.click(coord[1], coord[0])
                break
            return True
        return False

    def abrirNavegador(self, enderecoHTTP):
        """
        Abre um navegador da web e navega até um endereço HTTP especificado.

        Esta função utiliza a biblioteca PyAutoGUI para abrir o diálogo "Executar",
        aguarda até que uma imagem representando o ícone do executável seja carregada,
        escreve o endereço HTTP no campo de texto do diálogo e pressiona Enter para
        abrir um navegador da web com o URL especificado.

        Args:
            enderecoHTTP (str): O endereço HTTP (URL) que deseja abrir no navegador.

        Exemplo de uso:
            automation = AutomationUtils()
            endereco = "https://www.example.com"
            automation.abrirNavegador(endereco)

        Observações:
            Certifique-se de que a imagem 'tl_win_exec.png' corresponda ao ícone do
            executável associado ao seu navegador da web e que a janela relevante esteja
            em foco antes de chamar esta função.
        """
        # Abre o diálogo "Executar" pressionando 'Win + R'
        pyautogui.hotkey('win', 'r')
        # Aguarda até que a imagem 'tl_win_exec.png' seja carregada
        self.esperarImagemCarregar(r'.\img\tl_win_exec.png')
        # Escreve o endereço HTTP no campo de texto do diálogo
        pyautogui.write(enderecoHTTP)
        # Pressiona Enter para abrir o navegador com o URL especificado
        pyautogui.press('enter')
        
    def fecharNavegador(self):
        """
        Fecha apenas a janela do navegador ativa, para permitir que o login com certificado permaneça.

        Esta função utiliza a biblioteca PyAutoGUI para pressionar as teclas de atalho
        'ctrl + w', o que fecha a janela do navegador que está ativa.

        Exemplo de uso:
            automation = AutomationUtils()
            automation.fecharNavegador()

        Observações:
            Certifique-se de que a janela do navegador que deseja fechar esteja em foco
            antes de chamar esta função.
        """
        # Pressiona 'Alt + F4' para fechar a janela do navegador ativa
        pyautogui.hotkey('ctrl', 'w')

    def ler_csv(self, arquivo_csv):
        """
        Lê os dados de um arquivo CSV e retorna uma lista de dicionários.

        Esta função lê um arquivo CSV especificado, onde cada linha representa um registro
        de dados e as colunas são separadas por ponto e vírgula (;). Ela retorna os dados
        em forma de uma lista de dicionários, onde cada dicionário representa um registro
        e as chaves são os nomes das colunas.

        Args:
            arquivo_csv (str): O caminho para o arquivo CSV que deseja ler.

        Returns:
            list of dict: Uma lista de dicionários representando os registros do CSV.

        Exemplo de uso:
            automation = AutomationUtils()
            dados = automation.ler_csv('dados.csv')
            for registro in dados:
                print(registro['Nome'], registro['Idade'])

        Observações:
            Certifique-se de que o arquivo CSV esteja no formato correto (colunas separadas por
            ponto e vírgula) e que o caminho para o arquivo seja especificado corretamente.
        """
        dados_csv = []
        with open(arquivo_csv, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                dados_csv.append(row)
        return dados_csv
        
    def alterarPerfildeAcesso(self):
        """
        Realiza a ação de alterar o perfil de acesso.

        Esta função automatiza a ação de clicar no botão "Alterar Perfil de Acesso"
        em um aplicativo ou sistema. Ela aguarda até que a imagem 'espera_troca_perfil.png'
        seja carregada na tela, espera um breve período de tempo (1.5 segundos) e então
        localiza e clica no botão 'btn_alt_perfil.png'.

        Exemplo de uso:
            automation = AutomationUtils()
            automation.alterarPerfil()

        Observações:
            Certifique-se de que as imagens 'espera_troca_perfil.png' e 'btn_alt_perfil.png'
            correspondam aos elementos desejados e que a janela relevante esteja em foco antes
            de chamar esta função.
        """
        try:
            alterar_perfil = pyautogui.locateCenterOnScreen(r'.\img\btn_alt_perfil.png')

            if alterar_perfil:
                # Clica no centro da imagem para voltar à página inicial
                pyautogui.click(alterar_perfil)

        except pyautogui.ImageNotFoundException:
            time.sleep(self.tempo_esperar_carregar)
            pyautogui.click(x=1167, y= 223)
            print('imagem para alterar perfil não localizada, cliquei nas coordenadas')
        
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
            

    def clicar_AlterarPerfil(self):
        try:
            # clica no botão alterar cnpj                
            self.esperarImagemCarregar(r'.\img\btn_conf_alt_cnpj1.png')
            btn_alt_cnpj = pyautogui.locateCenterOnScreen(r'.\img\btn_conf_alt_cnpj1.png')
            
            if btn_alt_cnpj:
                pyautogui.click(btn_alt_cnpj)

        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=816, y= 473)
            

    def clicar_CertidaoSituacaoFiscal(self):
        try:
            self.esperarImagemCarregar(r'.\img\btn_click_situacaoFiscalx.png')            
            btn_sitFiscal = pyautogui.locateCenterOnScreen(r'.\img\btn_click_situacaoFiscalx.png')
            
            if btn_sitFiscal:
                pyautogui.click(btn_sitFiscal)
        
        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=505, y= 270)
            
    def clicar_CertidaoSituacaoFiscalList(self):
        try:
            self.esperarImagemCarregar(r'.\img\espera_btn_lista_sitFiscal.png')
            btn_sitFiscal_lista = pyautogui.locateOnScreen(r'.\img\btn_escolhe_situacaoFiscal.png')
            
            if btn_sitFiscal_lista:
                pyautogui.click(btn_sitFiscal_lista)

        except pyautogui.ImageNotFoundException:
            pyautogui.click(x=362, y= 445)
                
    def escrever_dados_no_csv(self, arquivo_csv, dados_relatorio):
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as arquivo_csv:
            campo_nomes = ['ID', 'EMPRESA', 'CNPJ', 'VERIFICADO']
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campo_nomes)                      
            # Escreve os dados no CSV
            escritor_csv.writerow(dados_relatorio)
    
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
                print(pagina_expirada)
                if pagina_expirada is not None:
                    texto_msg_erro_pg = '******** Página expirou, operação cancelada *********'
                    dados_relatorio = {'ID': id_empresa, 'EMPRESA': empresa, 'CNPJ': cnpj, 'VERIFICADO': texto_msg_erro_pg}
                    self.escrever_dados_no_csv('relatorio.csv', dados_relatorio)
                    time.sleep(self.tempo_esperar_carregar)
                    self.voltarHome()
                    print('página expirada')
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
                    print('achei a tela de relatório')
                    print(img_tela_download_relatorio)
                    #clicar na gerar relatório da esquerda
                    self.procurarTexto('Gerar Relatório')
                    time.sleep(self.tempo_esperar_carregar)
                    process = self.clicarSeCorLaranja()
                    time.sleep(self.tempo_esperar_carregar)                
                                    
                    if process == True:
                        gerar_relatorio = pyautogui.position(x=936, y=397)#gerar relatório da direita
                        time.sleep(0.5)
                        pyautogui.click(gerar_relatorio)
                        time.sleep(self.tempo_esperar_carregar)
                        time.sleep(0.5)
                        pyautogui.press('esc')
                        time.sleep(0.1)
                        pyautogui.press('esc')
                        time.sleep(0.1)
                                                                        
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
                print('não achei a tela de download')
                contagem_downloads -= 1
                print('não achei a tela de download')                
            
            time.sleep(self.tempo_esperar_carregar)            
                
            print(f'LINHA VERIFICADO:{i}')
            i = i + 1
            # Verifica se todos os CNPJs foram processados
            if i <= len(dados):
                print(len(dados))
                continue
            if i >= len(dados):
                self.escrever_dados_no_csv('relatorio.csv', contagem_downloads)   
                        
                    
        # Aguarda por um período antes de recomeçar o processo
        time.sleep(self.tempo_esperar_carregar)

        


        
