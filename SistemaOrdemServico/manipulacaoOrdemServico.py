#import sqlite3
from database import DatabaseManager

class ManipularOrdemServicos():
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def buscarValoresTBCliente(self):
        cursor = self.db_manager.get_cursor()
        clientesCadastrados = cursor.execute('SELECT cli_codCliente, cli_nomeCliente, cli_qtdNFisenta FROM tb_cliente;')
        clientesCadastrados = cursor.fetchall()
        
        listandoClientesOS = []
        
        for cliente in clientesCadastrados:
            listandoClientesOS.append(cliente)
            
        return listandoClientesOS   
    
    def buscarValoresTBServicosValore(self):
        
        cursor = self.db_manager.get_cursor()
        servicosCadastrados = cursor.execute('SELECT serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr;')
        servicosCadastrados = cursor.fetchall()
        
        listandoServicosOS = []
        
        for servico in servicosCadastrados:
            listandoServicosOS.append(servico)
            
        return listandoServicosOS
    
    def ordenarTBOrdensServico(self):
        cursor = self.db_manager.get_cursor()
        
        # Consulta SQL ordenando os dados pela coluna os_id em ordem decrescente
        cursor.execute("SELECT os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado FROM tb_ordens_servicos ORDER BY os_id DESC;")

    def verificaSeClienteCadastrado(self, codCliente):
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT cli_nomeCliente FROM tb_cliente WHERE cli_codCliente=?", (codCliente,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado
        else:
            print(f"Cliente com código {codCliente} não existe na tabela tb_cliente.")
            return None

    def verificaSeServicoCadastrado(self, codServico):
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT serv_codServ FROM tb_servicos_vlr WHERE serv_codServ=?", (codServico,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
        else:
            return None

    
    def inserirOrdemServico(self, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado):
        
        cursor = self.db_manager.get_cursor()
      
        cursor.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado) VALUES (?, ?, ?, ?, ?, ?, ?, ? ,?, ?)", (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado))

               



