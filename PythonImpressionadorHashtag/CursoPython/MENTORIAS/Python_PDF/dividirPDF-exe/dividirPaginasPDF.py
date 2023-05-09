import PyPDF2 as pyf
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# abrir a janela de diálogo para selecionar o arquivo
nome_arquivo = filedialog.askopenfilename()

# verificar se o usuário selecionou um arquivo
if not nome_arquivo:
    print("Nenhum arquivo selecionado.")
else:
    with open(nome_arquivo, 'rb') as file:
        arquivo_pdf = pyf.PdfReader(file)

        # abrir a janela de diálogo para selecionar o diretório de saída
        diretorio_saida = filedialog.askdirectory()
        if not diretorio_saida:
            print("Nenhum diretório de saída selecionado.")
        else:
            i = 1
            for pagina in arquivo_pdf.pages:
                arquivo_novo = pyf.PdfWriter()
                arquivo_novo.add_page(pagina)
                # salvar o arquivo
                nome_arquivo_final = f'Arquivo{i}.pdf'
                caminho_arquivo_final = Path(diretorio_saida) / nome_arquivo_final
                with caminho_arquivo_final.open(mode='wb') as arquivo_final:
                    arquivo_novo.write(arquivo_final)
                    i += 1
                    


