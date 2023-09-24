import sqlite3 as lite
import csv

# Defina a função importarCadastroClientes
def importarCadastroClientes():
    conexao = lite.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    with open(r'C:\Users\cpcsc\Downloads\clientes.csv', 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            cli_codCliente = int(row['CÓD.'])
            cli_nomeCliente = row['EMPRESA']
            cli_qtdNFisenta = int(row['ISENTO NF'])

            cursor.execute('''
                INSERT INTO tb_cliente (cli_codCliente, cli_nomeCliente, cli_qtdNFisenta)
                VALUES (?, ?, ?)
            ''', (cli_codCliente, cli_nomeCliente, cli_qtdNFisenta))

    conexao.commit()
    conexao.close()


# Agora você pode chamar a função diretamente
#importarCadastroClientes()

# Defina a função importarCadastroClientes
def importarCadastroServico():
    conexao = lite.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    with open(r'C:\Users\cpcsc\Downloads\servicos.csv', 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            serv_codServ = int(row['EVENTO'])
            serv_descrServico = row['DESCRIÇÕES PADROES']
            serv_vlrUnit = float(row['VALOR'])

            cursor.execute('''
                INSERT INTO tb_servicos_vlr (serv_codServ, serv_descrServico, serv_vlrUnit)
                VALUES (?, ?, ?)
            ''', (serv_codServ, serv_descrServico, serv_vlrUnit))

    conexao.commit()
    conexao.close()


# Agora você pode chamar a função diretamente
importarCadastroServico()

 
        
        