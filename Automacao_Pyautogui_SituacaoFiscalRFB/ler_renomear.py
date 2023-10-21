import os
import pandas as pd
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog
import shutil

# Crie uma janela de diálogo para selecionar o arquivo CSV
root = tk.Tk()
root.withdraw()  # Esconda a janela principal

caminho_csv = filedialog.askopenfilename(
    title="Selecione o arquivo CSV",
    filetypes=[("Arquivos CSV", "*.csv")]
)

# Crie uma janela de diálogo para selecionar a pasta dos PDFs
pasta_pdf = filedialog.askdirectory(
    title="Selecione a pasta dos PDFs"
)

# Verifique se o caminho para a pasta dos PDFs é válido
if not os.path.exists(pasta_pdf):
    print(f"O caminho '{pasta_pdf}' não existe. Certifique-se de fornecer um caminho válido para a pasta dos PDFs.")
    exit(1)

# Carregue o arquivo CSV com a codificação correta (ISO-8859-1)
df = pd.read_csv(caminho_csv, delimiter=';', encoding='ISO-8859-1')

# Lista vazia para armazenar os caminhos dos arquivos renomeados
arquivos_renomeados = []

# Loop pelos arquivos PDF
for arquivo_pdf in os.listdir(pasta_pdf):
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
                cnpj_csv = str(row['CNPJ'])  # Converta o valor para uma string
                    
                # Verifique se o CNPJ do CSV está no texto do PDF
                if cnpj_csv in texto_pdf:
                    # Crie o novo nome do arquivo PDF
                    novo_nome = f"{row['ID']} - {row['EMPRESA'][:10]} - {arquivo_pdf}"
                    novo_caminho_arquivo_pdf = os.path.join(pasta_pdf, novo_nome)
                        
                    try:
                        # Renomeie o arquivo PDF no novo local
                        os.rename(caminho_arquivo_pdf, novo_caminho_arquivo_pdf)
                        
                        # Adicione o novo caminho à lista de arquivos renomeados
                        arquivos_renomeados.append(novo_caminho_arquivo_pdf)
                    except PermissionError as e:
                        print(f"Não foi possível renomear '{arquivo_pdf}': {e}")
                        
                    # Saia do loop interno, pois encontrou uma correspondência
                    break
        
        # Feche o arquivo PDF antes de renomeá-lo
        pdf_reader.stream.close()

# Imprima os arquivos renomeados
for arquivo_renomeado in arquivos_renomeados:
    print(f"Arquivo renomeado: {arquivo_renomeado}")

