from PyPDF2 import PdfReader
import os
import re

# Caminho para a pasta contendo os arquivos PDF
pasta_com_pdfs = r'C:\Users\cpcsc\Downloads\termos_exclusao-2209'

# Caminho para o arquivo de texto onde os prints serão salvos
arquivo_de_texto = r'C:\Users\cpcsc\Downloads\termos_exclusao-2209\RelacaoTermosExclusao_2023.txt'

# Abra o arquivo de texto para escrita
with open(arquivo_de_texto, 'w', encoding='utf-8') as arquivo_texto:

    # Lista todos os arquivos na pasta
    arquivos_pdf = [f for f in os.listdir(pasta_com_pdfs) if f.endswith('.pdf')]

    # Percorre todos os arquivos PDF na lista
    for arquivo_pdf in arquivos_pdf:
        # Caminho completo para o arquivo PDF
        caminho_pdf = os.path.join(pasta_com_pdfs, arquivo_pdf)

        # Inicialize uma variável para armazenar o nome empresarial
        nome_empresarial = None

        # Abra o arquivo PDF
        pdf_reader = PdfReader(caminho_pdf)

        # Percorra todas as páginas do PDF
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            
            # Use expressões regulares para encontrar o texto "Nome Empresarial:" e capturar o que está na mesma linha
            match = re.search(r'Dados da Matriz\s*([^\n]*)\n', page_text)
            if match:
                nome_empresarial = match.group(1).strip()  # Remove espaços em branco extras no início e no fim
                arquivo_texto.write("\nCliente:" + f'{nome_empresarial[:-17]}' + '\n')

                debitoPrevGFIP_RFB = 'Débitos Previdenciários - Divergências entre GFIP e GPS (valor original, sem os acréscimos legais)'
                debitoPrevDCTF_RFB = 'Débitos Previdenciários – Outros (valor original, sem os acréscimos legais)'
                debitoPrev_PGFN = 'Débitos Previdenciários'

                if debitoPrevGFIP_RFB in page_text:
                    arquivo_texto.write('Existem débitos previdenciários GFIP\n')

                if debitoPrevDCTF_RFB in page_text:
                    arquivo_texto.write('Existem débitos previdenciários DCTF\n')

                if debitoPrev_PGFN in page_text:
                    arquivo_texto.write('Existem débitos previdenciários PGFN\n')
                else:
                    arquivo_texto.write('Sem pendências previdenciárias\n')

        # Verifique se o nome empresarial foi encontrado
        if not nome_empresarial:
            arquivo_texto.write("Nome Empresarial não encontrado no PDF:" + arquivo_pdf + '\n')

print("Prints salvos em", arquivo_de_texto)
