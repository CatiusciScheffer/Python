import os
import pandas as pd
from unidecode import unidecode

"""
Script para renomear arquivos PDF com base em um arquivo CSV.

Este script lê um arquivo CSV contendo informações sobre empresas, incluindo
os campos 'ID', 'EMPRESA' e 'CNPJ'. Os arquivos PDF no diretório especificado
são renomeados de acordo com as informações no CSV.

O nome do arquivo PDF é construído no formato: "{ID}-{EMPRESA}-20231219.pdf". 
O CNPJ é formatado para ter 14 dígitos, preenchendo com zeros à esquerda, 
e caracteres especiais em 'EMPRESA' são convertidos para suas formas equivalentes ASCII.

Parâmetros:
- diretorio_pdf: Caminho para o diretório dos arquivos PDF originais.
- diretorio_pdf_novo: Caminho para o diretório dos arquivos PDF renomeados.
- caminho_csv: Caminho para o arquivo CSV contendo informações sobre as empresas.

Dependências:
- pandas: Biblioteca para manipulação de dados em formato de tabela (DataFrame).
- unidecode: Biblioteca para converter caracteres especiais em equivalentes ASCII.
- os: Módulo para operações no sistema operacional.
"""

# Caminho para o diretório dos arquivos PDF
diretorio_pdf = r'C:/Users/cpcsc/Downloads/SITUACAO_FISCAL'
diretorio_pdf_novo = r'C:/Users/cpcsc/Downloads/SITUACAO_FISCAL_C'
# Caminho para o arquivo CSV
caminho_csv = r'C:/Users/cpcsc/Downloads/LISTA_EMPRESAS/LISTA_EMPRESA_CNPJ_COMPL.csv'

# Carregar o arquivo CSV
df = pd.read_csv(caminho_csv, delimiter=';', encoding='utf-8')

for indice, linha in df.iterrows():
    try:
        # ---> VERIFICAR A DATA DO NOME DOARQUIVO --->
        novo_nome = f"{linha['ID']}-{unidecode(linha['EMPRESA'])}-20240108.pdf"
        cnpj_formatado = str(linha['CNPJ']).zfill(14)
        # ---> VERIFICAR A DATA DO NOME DOARQUIVO --->
        caminho_antigo = os.path.join(diretorio_pdf, f"RelatorioSituacaoFiscal-{cnpj_formatado}-20240108.pdf")
        caminho_novo = os.path.join(diretorio_pdf, novo_nome)
        
        if os.path.exists(caminho_antigo):
            os.rename(caminho_antigo, caminho_novo)
            
        else:
            print(f"Arquivo não encontrado: {caminho_antigo}")

    except Exception as e:
        print(f'NÃO FOI POSSÍVEL RENOMEAR: {str(e)}')
        
    if os.path.exists(caminho_antigo):
        os.rename(caminho_antigo, caminho_novo)
    else:
        print(f"Arquivo não encontrado: {caminho_antigo}")