import PyPDF2 as pyf 
from pathlib import Path


nome_arquivo = "MGLU_ER_4T20_POR.pdf"
arquivo = pyf.PdfReader(nome_arquivo)

textoProcurado = 'MENSAGEM DA DIRETORIA'

i = 1

for pagina in arquivo.pages:
  textoInPagina = pagina.extract_text()
  if textoProcurado in textoInPagina:
    print(f'Texto localixado na página {i}.')
  i += 1