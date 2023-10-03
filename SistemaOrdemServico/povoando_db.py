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
    
# importarCadastroServico()

def importarRetrabalhoAgoSet2023():
    conexao = lite.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    with open(r'C:\Users\cpcsc\Downloads\retrabalho.csv', 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            os_dtServico = str(row['DATA'])
            os_codCliente = int(row['COD.CLIENTE'])
            os_cliente = str(row['CLIENTE'])
            os_codServico = int(row['COD.SERV'])
            os_descServico = str(row['DESCRSERV'])
            os_descrComplementar = str(row['OBS'])
            os_qtd = int(row['QTD'])
            os_vlrUnit = (row['VLRUNIT'])
            os_total = (row['TOTAL']) 
            #os_usuario = str(row['RESP'])           

            cursor.execute('''
                INSERT INTO tb_ordens_servicos(os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_descrComplementar, os_total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_descrComplementar, os_total))

    conexao.commit()
    conexao.close()
    
importarRetrabalhoAgoSet2023() 


        
        