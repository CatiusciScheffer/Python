import os
import fitz  # PyMuPDF

# Diretório dos arquivos PDF
diretorio = r'C:\Users\cpcsc\Downloads\situacaoFiscal'

# Caminho para o arquivo de saída
arquivo_saida = 'saida.txt'

# Função para encontrar e extrair informações
def extrair_informacoes(pdf_file):
    with fitz.open(pdf_file) as pdf_document:
        texto = ""
        encontrou_omissao = False  # Variável de controle
        cnpj_gravado = False  # Variável de controle
        dctfWeb = 'Omissão de DCTFWeb*'

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            page_text = page.get_text("text")
            texto += page_text

        linhas = texto.splitlines()

        for i in range(len(linhas)):
            linha = linhas[i]

            if 'CNPJ:' in linha and not cnpj_gravado:
                cnpj = linha.strip()
                with open(arquivo_saida, 'a') as output_file:
                    output_file.write('-' * 60 + '\n')
                    output_file.write(cnpj + '\n')
                cnpj_gravado = True

            if 'Omissão de DCTFWeb*' in linha:
                encontrou_omissao = True
                with open(arquivo_saida, 'a') as output_file:
                    output_file.write(linha[:31] + '\n')
                continue

            if encontrou_omissao:
                if '_____' in linha:
                    encontrou_omissao = False
                else:
                    with open(arquivo_saida, 'a') as output_file:
                        output_file.write(linha + '\n')

        if not encontrou_omissao:
            semPendenciaDCTFWeb = 'DCTFWeb - Sem Omissões'
            with open(arquivo_saida, 'a') as output_file:
                output_file.write(semPendenciaDCTFWeb + '\n')
        

# Iterar pelos arquivos PDF no diretório
for root, dirs, files in os.walk(diretorio):
    for file in files:
        if file.endswith('.pdf'):
            pdf_file = os.path.join(root, file)
            extrair_informacoes(pdf_file)

print("Extração de informações concluída.")
