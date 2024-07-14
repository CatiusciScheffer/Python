import os
import PyPDF2

# Diretório onde deseja que o arquivo seja criado
diretorio_saida = R"C:/Users/cpcsc/Downloads/SITUACAO_FISCAL"
diretorio = R"C:/Users/cpcsc/Downloads/SITUACAO_FISCAL"
# Nome do arquivo de saída
arquivo_saida = os.path.join(diretorio_saida, 'SituaçãoFiscal_PendenciasGeral.txt')


def verificarTipoPendencias(ocorrencia, linha):
    if ocorrencia in linha:
        encontrou_omissao = True
        omit_found = True  # Define omit_found como True
        with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
            output_file.write(f'    ----> {linha.replace("_", "")}\n')
    

# Verifica se o diretório de saída existe, se não existir, cria-o
if not os.path.exists(diretorio_saida):
    os.makedirs(diretorio_saida)

# Verifica se o arquivo de saída existe, se não existir, cria-o
if not os.path.exists(arquivo_saida):
    open(arquivo_saida, 'w', encoding='utf-8').close()

# Função para encontrar e extrair informações
def extrair_informacoes(pdf_file):
    with open(pdf_file, 'rb') as file:
        # Usa PdfReader en lugar de PdfFileReader
        pdf_reader = PyPDF2.PdfReader(file)

        texto = ""
        encontrou_omissao = False
        cnpj_gravado = False
        
        tipos_omissoes_pendencias = [
            'Omissão de DCTFWeb*',
            'Omissão de DCTF',
            'Omissão de PGDAS-D',
            'Omissão de DEFIS',
            'Omissão de EFD-CONTRIB',
            'Omissão de GFIP',
            'Pendência - Parcelamento (PARCSN/PARCMEI)',
            'Pendência – Parcelamento (SIEFPAR)',
            'Pendência - Débito (SIEF)',
            'Pendência - Processo Fiscal (SIEF)',
            'Pendência - Divergência GFIP x GPS (AGUIA)',
            'Pendência - Parcelamento (SISPAR)',
            'Pendência - Inscrição (Sistema DIVIDA)',
            'Pendência - Inscrição (SIDA)',
            'Pendência - Débito (SICOB)',
            'Parcelamento com Exigibilidade Suspensa (PARCSN/PARCMEI)',
            'Processo Fiscal com Exigibilidade Suspensa (SIEF)',
            'Inscrição com Exigibilidade Suspensa (Sistema DIVIDA)',
            'Inscrição com Exigibilidade Suspensa (SIDA)'
        ]
        
        omit_found = False  # Variável para rastrear se uma omissão foi encontrada

        # Itera por cada página do PDF
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            texto += page.extract_text()

        # Divide o texto em linhas
        linhas = texto.splitlines()
        # Itera por cada linha de texto
        for i in range(len(linhas)):
            linha = linhas[i]
            
            # Verifica se a linha contém 'CNPJ:' e ainda não foi escrita
            if 'CNPJ:' in linha and not cnpj_gravado:
                cnpj = linha.strip()
                with open(arquivo_saida, 'a') as output_file:#, encoding='latin1'
                    output_file.write('\n')
                    output_file.write('\n' + '-' * 80 + '\n')
                    output_file.write(cnpj)
                    output_file.write('\n' + '-' * 80 + '\n')
                cnpj_gravado = True
            
            for tipoOcorrencia in tipos_omissoes_pendencias:
                verificarTipoPendencias(tipoOcorrencia, linha) 
                
        # Verifica se nenhum tipo de ocorrência foi encontrado em nenhuma linha
        tipo_nao_encontrado = True
        for tipoOcorrencia in tipos_omissoes_pendencias:
            if any(tipoOcorrencia in linha for linha in linhas):
                tipo_nao_encontrado = False
                break

        # Escreve a mensagem 'sem pendeeeeeeeencias' se nenhum tipo de ocorrência foi encontrado
        if tipo_nao_encontrado:
            with open(arquivo_saida, 'a') as output_file:#, encoding='latin1'
                output_file.write('    !!!! SEM PENDÊNCIAS !!!!' + '\n')

# Itera pelos arquivos PDF no diretório
for root, dirs, files in os.walk(diretorio):
    for file in files:
        if file.endswith('.pdf'):
            pdf_file = os.path.join(root, file)
            extrair_informacoes(pdf_file)
