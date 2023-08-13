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
    
    def consultaTabelaServicosValores(self):
        cursor = self.db_manager.get_cursor()

        cursor.execute("SELECT serv_id, serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr")

        listandoServicos = cursor.fetchall()
        
        
        # for servico in servicosCadastrados:
        #     listandoServicosOS.append(servico)
            
        return listandoServicos
    
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
            print(f'resultado{resultado}')
            return resultado[0]
        else:
            return None
    
    def inserirOrdemServico(self, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado):
        
        cursor = self.db_manager.get_cursor()
      
        cursor.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado) VALUES (?, ?, ?, ?, ?, ?, ?, ? ,?, ?)", (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado))

    def inserirServicoDB(self, codServico, descServico, vlrUnit):
        try:
            # Executa o comando SQL para inserir um novo serviço na tabela
            self.db_manager.cursor.execute(
                "INSERT INTO tb_servicos_vlr (serv_codServ, serv_descrServico, serv_vlrUnit) VALUES (?, ?, ?)",
                (codServico, descServico, vlrUnit)
            )
            # Confirma a transação no banco de dados
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao inserir serviço:", e)
            return False        

    def deletarServicoDB(self, serv_id):
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_servicos_vlr WHERE serv_id = ?", (serv_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao deletar serviço:", e)
            return False

    def editarServicoPeloIDServicosValoresDB(self, serv_id, serv_codServ, serv_descrServico, serv_vlrUnit):
        try:
            self.db_manager.cursor.execute(
                "UPDATE tb_servicos_vlr SET serv_descrServico = ?, serv_vlrUnit = ? WHERE serv_id = ?",
                (serv_descrServico, serv_vlrUnit, serv_id)
            )
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao modificar serviço:", e)
            return False