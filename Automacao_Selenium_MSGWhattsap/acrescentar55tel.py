import pandas as pd

# Carregue o arquivo Excel
nome_arquivo_excel = "lista-telefones-inss.xlsx"  # Substitua pelo nome do seu arquivo Excel
df = pd.read_excel(nome_arquivo_excel)

# Função para adicionar "55" antes dos números na coluna 'telefone'
def adicionar_55(telefone):
    if pd.notna(telefone):
        return "55" + str(telefone)
    return telefone

# Aplicar a função à coluna 'telefone'
df['telefone'] = df['telefone'].apply(adicionar_55)

# Salvar o DataFrame de volta no arquivo Excel
df.to_excel(nome_arquivo_excel, index=False)
