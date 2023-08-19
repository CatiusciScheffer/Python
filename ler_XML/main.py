import xmltodict
import json
import pandas as pd

with open('xml/NFSE_2853_144480_1_1.xml', 'rb') as arquivo:
    documento = xmltodict.parse(arquivo)

# Converter o documento XML para um JSON formatado
documento_json = json.dumps(documento, indent=2, ensure_ascii=False)

# Converter o JSON formatado em um dicionário
data = json.loads(documento_json)

# Converter o JSON para um DataFrame pandas
df = pd.json_normalize(data)

# Escolha o nome do arquivo Excel (substitua 'saida.xlsx' pelo nome que desejar)
output_filename = 'saida.xlsx'

# Exportar o DataFrame para um arquivo Excel
df.to_excel(output_filename, index=False)

print(f'Dados exportados para {output_filename}')

