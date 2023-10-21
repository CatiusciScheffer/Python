import os
import fitz  # PyMuPDF

# Diretório onde os arquivos PDF estão localizados
diretorio = r'C:\Users\cpcsc\Downloads\situacaoFiscal'

# Caminho para o arquivo de saída
arquivo_saida = 'saida.txt'

def verificarTipoPendencias(ocorrencia, linha):
    if ocorrencia in linha:
        encontrou_omissao = True
        omit_found = True  # Define omit_found como True
        with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
            output_file.write(f'    ----> {linha.replace("_", "")}\n')
    

# Função para encontrar e extrair informações
def extrair_informacoes(pdf_file):
    # Abre o arquivo PDF usando o PyMuPDF (PyMuPDF é usado para trabalhar com PDFs)
    with fitz.open(pdf_file) as pdf_document:
        texto = ""
        encontrou_omissao = False  # Variável de controle para rastrear se uma omissão foi encontrada
        cnpj_gravado = False  # Variável de controle para rastrear se o CNPJ foi escrito
        
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
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            page_text = page.get_text("text")
            texto += page_text

        # Divide o texto em linhas
        linhas = texto.splitlines()
        # Itera por cada linha de texto
        for i in range(len(linhas)):
            linha = linhas[i]
            
            # Verifica se a linha contém 'CNPJ:' e ainda não foi escrita
            if 'CNPJ:' in linha and not cnpj_gravado:
                cnpj = linha.strip()
                with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
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
            with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
                output_file.write('    !!!! SEM PENDÊNCIAS !!!!' + '\n')

# Itera pelos arquivos PDF no diretório
for root, dirs, files in os.walk(diretorio):
    for file in files:
        if file.endswith('.pdf'):
            pdf_file = os.path.join(root, file)
            extrair_informacoes(pdf_file)
