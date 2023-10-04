import os
import fitz  # PyMuPDF

# Diretório onde os arquivos PDF estão localizados
diretorio = r'C:\Users\cpcsc\Downloads\situacaoFiscal'

# Caminho para o arquivo de saída
arquivo_saida = 'saida.txt'

# Função para encontrar e extrair informações
def extrair_informacoes(pdf_file):
    # Abre o arquivo PDF usando o PyMuPDF (PyMuPDF é usado para trabalhar com PDFs)
    with fitz.open(pdf_file) as pdf_document:
        texto = ""
        encontrou_omissao = False  # Variável de controle para rastrear se uma omissão foi encontrada
        cnpj_gravado = False  # Variável de controle para rastrear se o CNPJ foi escrito
        omissao_dctfWeb = 'Omissão de DCTFWeb*'
        omissao_dctf = 'Omissão de DCTF'
        omissao_pgdas_d = 'Omissão de PGDAS-D'
        omissao_gfip = 'Pendência - Omissão de GFIP'
        omissao_defis = 'Omissão de DEFIS'
        omissao_efd_contribuicoes = 'Omissão de EFD-CONTRIB'
        
        pendencia_debito_parcelamento = 'Pendência - Parcelamento (PARCSN/PARCMEI)'
        pendencia_debitos_SIEF = 'Pendência - Débito (SIEF)'
        pendencia_processo_SIEF = 'Pendência - Processo Fiscal (SIEF)'
        pendencia_debito_GFIP = 'Pendência - Divergência GFIP x GPS (AGUIA)'
        pendencia_parcelamento_SISPAR = 'Pendência - Parcelamento (SISPAR)'
        pendencia_inscricao_divida= 'Pendência - Inscrição (Sistema DIVIDA)'
        pendencia_divida_SIDA = 'Pendência - Inscrição (SIDA)'
        pendencia_debito_SICOB = 'Pendência - Débito (SICOB)'
        parcelamento_PARCSNPARCMEI_susp = 'Parcelamento com Exigibilidade Suspensa (PARCSN/PARCMEI)'
        processo_SIEF_susp = 'Processo Fiscal com Exigibilidade Suspensa (SIEF)'
        inscricao_SISPAR_susp = 'Inscrição com Exigibilidade Suspensa (Sistema DIVIDA)'
        inscricao_SIDA_susp = 'Inscrição com Exigibilidade Suspensa (SIDA)'
        
        
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
                    output_file.write('\n' + '-' * 30 + 'INÍCIO' + '-' * 30 + '\n')
                    output_file.write(cnpj + '\n')
                cnpj_gravado = True

            # Verifica se a linha contém 'Omissão de DCTFWeb*'
            if omissao_dctfWeb in linha:
                encontrou_omissao = True
                omit_found = True  # Define omit_found como True
                with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
                    output_file.write(linha[:31] + '\n')
                continue

            # Se encontrou uma omissão, processa as linhas até encontrar '_____'
            if encontrou_omissao:
                if '_____' in linha:
                    encontrou_omissao = False
                    with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
                        output_file.write('\n' + '-' * 30 + 'FIM' + '-' * 30 + '\n')
                else:
                    with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
                        output_file.write(linha + '\n')

        # Verifica se uma omissão foi encontrada e escreve "DCTFWeb - Sem Omissões" somente se omit_found for False
        if not omit_found:
            semPendenciaDCTFWeb = 'DCTFWeb - Sem Omissões'
            with open(arquivo_saida, 'a', encoding='utf-8') as output_file:
                output_file.write(semPendenciaDCTFWeb + '\n')
                output_file.write('\n' + '-' * 30 + 'FIM' + '-' * 30 + '\n')

# Itera pelos arquivos PDF no diretório
for root, dirs, files in os.walk(diretorio):
    for file in files:
        if file.endswith('.pdf'):
            pdf_file = os.path.join(root, file)
            extrair_informacoes(pdf_file)
