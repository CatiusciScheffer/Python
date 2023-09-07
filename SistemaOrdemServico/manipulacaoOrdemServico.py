#import sqlite3
from database import DatabaseManager
from datetime import datetime

class ManipularOrdemServicos():
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    #### FUNÇÕES TABELA CLIENTES ####    
    def consultarCompletaTabelaClientes(self):
        cursor = self.db_manager.get_cursor()
        clientesCadastrados = cursor.execute('SELECT cli_id, cli_codCliente, cli_nomeCliente, cli_qtdNFisenta FROM tb_cliente')
        clientesCadastrados = cursor.fetchall()
        return clientesCadastrados   
    
    def verificarSeCodigoDoClienteCadastrado(self, codCliente):
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT cli_codCliente FROM tb_cliente WHERE cli_codCliente=?", (codCliente,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
        else:
            return None
        
    def inserirClienteDB(self, codCliente, nomeCliente, NFIsenta):
        try:
            # Executa o comando SQL para inserir um novo serviço na tabela
            self.db_manager.cursor.execute(
                "INSERT INTO tb_cliente (cli_codCliente, cli_nomeCliente, cli_qtdNFisenta) VALUES (?, ?, ?)",
                (codCliente, nomeCliente, NFIsenta)
            )
            # Confirma a transação no banco de dados
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao cadastrar cliente:", e)
            return False
        
    def editarClientePeloIDClienteDB(self, cli_id, cli_codCliente, cli_nomeCliente, cli_qtdNFisenta):
        try:
            self.db_manager.cursor.execute(
                "UPDATE tb_cliente SET cli_nomeCliente = ?, cli_qtdNFisenta = ? WHERE cli_id = ?",
                (cli_nomeCliente, cli_qtdNFisenta, cli_id)
            )
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao modificar cliente:", e)
            return False
        
    def deletarClienteDB(self, cli_id):
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_cliente WHERE cli_id = ?", (cli_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro no banco ao deletar cliente:", e)
            return False
        
    #______________________________________________________#
    
    #### FUNÇÕES TABELA ORDENS DE SERVIÇO ####
    def ordenarTBOrdensServico(self):
        cursor = self.db_manager.get_cursor()
        
        # Consulta SQL ordenando os dados pela coluna os_id em ordem decrescente
        cursor.execute("SELECT os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado FROM tb_ordens_servicos ORDER BY os_id DESC;")
        
    def inserirOrdemServicosDB(self, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_usuario):
        try:
            # Executa o comando SQL para inserir um novo serviço na tabela
            self.db_manager.cursor.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)", (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_usuario))
       
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao inserir ordem de serviços:", e)
            return False 
        
    def deletarOrdemServicoDB(self, os_id):
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_ordens_servicos WHERE os_id = ?", (os_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro no banco ao deletar Ordem de Serviço:", e)
            return False
        
    def consultarOrdensServicoNAOFaturadas(self):
        cursor = self.db_manager.get_cursor()
        
        cursor.execute("SELECT * FROM tb_ordens_servicos WHERE os_faturado = 'NÃO' ORDER BY os_cliente, os_codServico;")
        
        ordensNAOfaturadas = cursor.fetchall()
        print(ordensNAOfaturadas)
        
        return ordensNAOfaturadas
    
    def editarOrdemServicoPeloIDOrdensServicosDB(self, os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado):
        try:
            self.db_manager.cursor.execute(
                "UPDATE tb_ordens_servicos SET os_dtServico = ?, os_codCliente = ?, os_cliente = ?, os_codServico = ?, os_descServico = ?, os_qtd = ?, os_vlrUnit = ?, os_total = ?, os_descrComplementar = ?, os_faturado = ? WHERE os_id = ?",
                (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_id)
            )
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao modificar Ordem de Serviço_DB:", e)
            return False
        
    def modificarsituacaoFaturamentoParaSIM(self):
        try:
            
            # Comando SQL para atualizar os registros
            update_sql = """
            UPDATE tb_ordens_servicos
            SET os_faturado = 'SIM',
                os_dtFaturamento = ?
            WHERE os_faturado = 'NÃO';
            """
            # Obtenha a data atual no formato "YYYY-MM-DD HH:MM:SS"
            data_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            # Execute o comando SQL
            self.db_manager.cursor.execute(update_sql, (data_atual,))
            self.db_manager.connection.commit()
            return True
        
        except Exception as e:
            print("Erro ao Fechar faturamento:", e)
            return False
    
    
    #______________________________________________________#
    
    #### FUNÇÕES TABELA SERVIÇOS ####
    def consultarCompletaTabelaServicosValores(self):
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT serv_id, serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr")
        listandoServicos = cursor.fetchall()    
        return listandoServicos    

    def verificarSeCodigoDoServicoCadastrado(self, codServico):
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT serv_codServ FROM tb_servicos_vlr WHERE serv_codServ=?", (codServico,))
        resultado = cursor.fetchone()
        if resultado is not None:
            print(f'resultado{resultado}')
            return resultado[0]
        else:
            return None
    
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
        
        