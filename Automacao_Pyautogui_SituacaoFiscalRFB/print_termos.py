from PyPDF2 import PdfReader
import os
import re

# Caminho para a pasta contendo os arquivos PDF
pasta_com_pdfs = r'C:\Users\cpcsc\Downloads\termos_exclusao-2209'

# Caminho para o arquivo de texto onde os prints serão salvos
arquivo_de_texto = r'C:\Users\cpcsc\Downloads\termos_exclusao-2209\TermosExclusao_2023.txt'

# Abra o arquivo de texto para escrita
with open(arquivo_de_texto, 'w', encoding='utf-8') as arquivo_texto:

    # Lista todos os arquivos na pasta
    arquivos_pdf = [f for f in os.listdir(pasta_com_pdfs) if f.endswith('.pdf')]

    # Percorre todos os arquivos PDF na lista
    for arquivo_pdf in arquivos_pdf:
        # Caminho completo para o arquivo PDF
        caminho_pdf = os.path.join(pasta_com_pdfs, arquivo_pdf)

        # Inicialize uma variável para armazenar o texto de todas as páginas
        texto_total = ""

        # Abra o arquivo PDF
        pdf_reader = PdfReader(caminho_pdf)
        
        # Percorra todas as páginas do PDF
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            texto_total += page_text

        # Use expressões regulares para encontrar o texto "Nome Empresarial:" e capturar o que está na mesma linha
        match = re.search(r'Dados da Matriz\s*([^\n]*)\n', texto_total)
        if match:
            nome_empresarial = match.group(1).strip()  # Remove espaços em branco extras no início e no fim
            linha = '-' * 60
            arquivo_texto.write(linha + '\n')
            arquivo_texto.write("\nCliente:" + f'{nome_empresarial[:-17]}' + '\n')
            arquivo_texto.write(texto_total + '\n')
            arquivo_texto.write(linha + '\n')
        else:
            arquivo_texto.write("Nome Empresarial não encontrado no PDF:" + arquivo_pdf + '\n')

print("Prints salvos em", arquivo_de_texto)


