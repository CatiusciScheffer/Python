import os
import pandas as pd
from PyPDF2 import PdfReader

# Caminho para a pasta dos PDFs e o arquivo CSV
pasta_pdf = r'.\pdf'
caminho_csv = 'CNPJ-PONTOS.csv'

# Carregue o arquivo CSV com a codificação correta (ISO-8859-1)
df = pd.read_csv(caminho_csv, delimiter=';', encoding='ISO-8859-1')

# Liste todos os arquivos na pasta dos PDFs
arquivos_pdf = os.listdir(pasta_pdf)

# Loop pelos arquivos PDF
for arquivo_pdf in arquivos_pdf:
    caminho_arquivo_pdf = os.path.join(pasta_pdf, arquivo_pdf)
    
    # Verifique se o arquivo já foi renomeado
    if not arquivo_pdf.startswith('ID - EMPRESA - '):
    
        try:
            # Abra o arquivo PDF usando PdfReader
            pdf_reader = PdfReader(caminho_arquivo_pdf)
        except Exception as e:
            print(f"Não foi possível abrir '{arquivo_pdf}': {e}")
            continue
        
        # Use len(pdf_reader.pages) para obter o número de páginas
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto_pdf = page.extract_text()
                
            # Loop pelos registros no CSV
            for index, row in df.iterrows():
                cnpj_csv = row['CNPJ']
                    
                # Verifique se o CNPJ do CSV está no texto do PDF
                if cnpj_csv in texto_pdf:
                    # Crie o novo nome do arquivo PDF
                    novo_nome = f"{row['ID']} - {row['EMPRESA']} - {arquivo_pdf}"
                    novo_caminho_arquivo_pdf = os.path.join(pasta_pdf, novo_nome)
                        
                    try:
                        # Renomeie o arquivo PDF
                        os.rename(caminho_arquivo_pdf, novo_caminho_arquivo_pdf)
                    except PermissionError as e:
                        print(f"Não foi possível renomear '{arquivo_pdf}': {e}")
                        
                    # Saia do loop interno, pois encontrou uma correspondência
                    break
        
        # Feche o arquivo PDF antes de renomeá-lo
        pdf_reader.stream.close()

