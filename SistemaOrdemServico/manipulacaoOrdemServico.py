import sqlite3
from database import DatabaseManager

class ManipularOrdemServicos():
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def selecionarCliente(self):
        cursor = self.db_manager.get_cursor()
        clientesCadastrados = cursor.execute('SELECT cli_codCliente, cli_nomeCliente FROM tb_cliente ORDER BY cli_codCliente ASC;')
        clientesCadastrados = cursor.fetchall()
        
        listandoClientesOS = []
        
        for cliente in clientesCadastrados:
            listandoClientesOS.append(cliente)
            
        return listandoClientesOS   
    
    def selecionarDescricaoServico(self):
        cursor = self.db_manager.get_cursor()
        servicosCadastrados = cursor.execute('SELECT serv_descrServico FROM tb_servicos_vlr;')
        servicosCadastrados = cursor.fetchall()
        
        listandoServicosOS = []
        
        for servico in servicosCadastrados:
            listandoServicosOS.append(servico)
            
        return listandoServicosOS
    
    def novoTeste(self):
        
        cursor = self.db_manager.get_cursor()
        servicosCadastrados = cursor.execute('SELECT serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr;')
        servicosCadastrados = cursor.fetchall()
        
        listandoServicosOS = []
        
        for servico in servicosCadastrados:
            listandoServicosOS.append(servico)
            
        return listandoServicosOS
    
    
    
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
        cursor.execute("SELECT serv_descrServico FROM tb_servicos_vlr WHERE serv_codServ=?", (codServico,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
        else:
            return None

    def criarOrdemServico(self, os_dtServico, os_codCliente, os_cliente, os_observacao, os_codServico, os_descServico, os_qtd, os_vlrUnit):
        
        # Verificar se o cliente existe na tabela tb_cliente
        os_cliente = self.verificaSeClienteCadastrado(os_codCliente)
        if os_cliente is None:
            print(f"Cliente com código {os_codCliente} não existe na tabela tb_cliente.")
            pass

        # Verificar se o serviço existe na tabela tb_servicos_vlr
        os_descServico = self.verificaSeServicoCadastrado(os_codServico)
        if os_descServico is None:
            print(f"Serviço com código {os_codServico} não existe na tabela tb_servicos_vlr.")
            pass

        # Verificar usuário logado e preencher os_usuario com o nome do usuário

        # Buscar valor unitário
        os_vlrUnit = self.pegandoValorUnitarioPeloCodServico(os_vlrUnit)

        # Executar a instrução INSERT
        self.db_manager.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_observacao, os_codServico, os_descServico, os_qtd, os_vlrUnit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (os_dtServico, os_codCliente, os_cliente, os_observacao, os_codServico, os_descServico, os_qtd, os_vlrUnit))

        # Salvar a transação
        self.db_manager.commit()
        print("Ordem de serviço inserida com sucesso.")



