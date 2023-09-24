from database import DatabaseManager
from datetime import datetime

class ManipularOrdemServicos():
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    #@@@@@@@@@@@@@@ FUNÇÕES TABELA CLIENTES @@@@@@@@@@@@@@#    
    def consultarCompletaTabelaClientes(self):
        """
        Consulta e retorna a lista completa de clientes cadastrados.

        Returns:
            list: Uma lista contendo as informações de clientes cadastrados na tabela.
                Cada entrada é uma tupla com os seguintes campos:
                - cli_id (int): ID do cliente.
                - cli_codCliente (int): Código do cliente.
                - cli_nomeCliente (str): Nome do cliente.
                - cli_qtdNFisenta (int): Quantidade de notas fiscais isentas do cliente.

        """
        cursor = self.db_manager.get_cursor()
        clientesCadastrados = cursor.execute('SELECT cli_id, cli_codCliente, cli_nomeCliente, cli_qtdNFisenta FROM tb_cliente')
        clientesCadastrados = cursor.fetchall()
        return clientesCadastrados 
    
    def verificarSeCodigoDoClienteCadastrado(self, codCliente):
        """
        Verifica se um código de cliente específico já está cadastrado na tabela de clientes.

        Args:
            codCliente (int): O código do cliente a ser verificado.

        Returns:
            int or None: O código do cliente se ele estiver cadastrado, caso contrário, retorna None.

        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT cli_codCliente FROM tb_cliente WHERE cli_codCliente=?", (codCliente,))
        resultado = cursor.fetchone()
        if resultado is not None:
            return resultado[0]
        else:
            return None
        
    def inserirClienteDB(self, codCliente, nomeCliente, NFIsenta):
        """
        Insere um novo cliente na tabela de clientes do banco de dados.

        Args:
            codCliente (int): O código do cliente a ser inserido.
            nomeCliente (str): O nome do cliente.
            NFIsenta (int): A quantidade de notas fiscais isentas do cliente.

        Returns:
            bool: True se o cliente for inserido com sucesso, False em caso de erro.

        """
        try:
            # Executa o comando SQL para inserir um novo cliente na tabela
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
        """
        Edita as informações de um cliente existente na tabela de clientes do banco de dados.

        Args:
            cli_id (int): O ID do cliente a ser editado.
            cli_codCliente (int): O novo código do cliente.
            cli_nomeCliente (str): O novo nome do cliente.
            cli_qtdNFisenta (int): A nova quantidade de notas fiscais isentas do cliente.

        Returns:
            bool: True se o cliente for editado com sucesso, False em caso de erro.

        """
        try:
            self.db_manager.cursor.execute(
                "UPDATE tb_cliente SET cli_nomeCliente = ?, cli_qtdNFisenta = ? WHERE cli_id = ?",
                (cli_nomeCliente, cli_qtdNFisenta, cli_id)
            )
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao modificar cliente:", e)
            return False
        
    def deletarClienteDB(self, cli_id):
        """
        Deleta um cliente da tabela de clientes do banco de dados.

        Args:
            cli_id (int): O ID do cliente a ser deletado.

        Returns:
            bool: True se o cliente for deletado com sucesso, False em caso de erro.

        """
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_cliente WHERE cli_id = ?", (cli_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro no banco ao deletar cliente:", e)
            return False
   
    #-------------fim tb clientes-------------#
    
    #@@@@@@@@@@@@@@ FUNÇÕES TABELA ORDENS DE SERVIÇO @@@@@@@@@@@@@@#
    
    def ordenarTBOrdensServico(self):
        """
        Ordena a tabela de Ordens de Serviço do banco de dados pelo ID em ordem decrescente.

        Esta função executa uma consulta SQL que ordena os registros da tabela de Ordens de Serviço pelo ID
        em ordem decrescente (do maior ID para o menor ID).

        Args:
            None

        Returns:
            None

        """
        cursor = self.db_manager.get_cursor()
        
        # Consulta SQL ordenando os dados pela coluna os_id em ordem decrescente
        cursor.execute("SELECT os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado FROM tb_ordens_servicos ORDER BY os_id DESC;")
        
    def inserirOrdemServicosDB(self, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_usuario):
        """
        Insere uma nova ordem de serviço no banco de dados.

        Esta função insere uma nova ordem de serviço no banco de dados com os detalhes fornecidos.

        Args:
            os_dtServico (str): A data do serviço.
            os_codCliente (int): O código do cliente associado à ordem de serviço.
            os_cliente (str): O nome do cliente associado à ordem de serviço.
            os_codServico (int): O código do serviço.
            os_descServico (str): A descrição do serviço.
            os_qtd (int): A quantidade do serviço.
            os_vlrUnit (float): O valor unitário do serviço.
            os_total (float): O valor total da ordem de serviço.
            os_descrComplementar (str): A descrição complementar do serviço.
            os_faturado (str): Indicação se o serviço está faturado ("SIM" ou "NÃO").
            os_usuario (str): O nome do usuário responsável pela ordem de serviço.

        Returns:
            bool: True se a inserção for bem-sucedida, False em caso de erro.

        """
        try:
            # Executa o comando SQL para inserir uma nova ordem de serviço na tabela
            self.db_manager.cursor.execute(
                "INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)",
                (os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado, os_usuario)
            )
            # Confirma a transação no banco de dados
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao inserir ordem de serviços:", e)
            return False
        
    def deletarOrdemServicoDB(self, os_id):
        """
        Deleta uma ordem de serviço do banco de dados.

        Esta função exclui uma ordem de serviço com base no seu ID.

        Args:
            os_id (int): O ID da ordem de serviço a ser excluída.

        Returns:
            bool: True se a exclusão for bem-sucedida, False em caso de erro.

        """
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_ordens_servicos WHERE os_id = ?", (os_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro no banco ao deletar Ordem de Serviço:", e)
            return False
        
    def consultarOrdensServicoNAOFaturadas(self):
        """
        Consulta as ordens de serviço não faturadas no banco de dados e as retorna em ordem.

        Esta função consulta as ordens de serviço que ainda não foram faturadas (com 'os_faturado' igual a 'NÃO')
        no banco de dados e as retorna em ordem, primeiro por nome de cliente e, em seguida, por código de serviço.

        Returns:
            list: Uma lista de tuplas representando as ordens de serviço não faturadas.
                Cada tupla contém informações da ordem de serviço, incluindo:
                - ID da ordem de serviço
                - Data do serviço
                - Código do cliente
                - Nome do cliente
                - Código do serviço
                - Descrição do serviço
                - Quantidade
                - Valor unitário
                - Valor total
                - Descrição complementar
                - Status de faturamento ('NÃO')

        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT * FROM tb_ordens_servicos WHERE os_faturado = 'NÃO' ORDER BY os_cliente, os_codServico;")
        
        ordensNAOfaturadas = cursor.fetchall()
        return ordensNAOfaturadas
    
    def editarOrdemServicoPeloIDOrdensServicosDB(self, os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado):
        """
        Edita uma ordem de serviço no banco de dados com base no ID da ordem.

        Esta função atualiza os detalhes de uma ordem de serviço no banco de dados com base no ID da ordem fornecido.

        Args:
            os_id (int): O ID da ordem de serviço a ser editada.
            os_dtServico (str): Data do serviço.
            os_codCliente (int): Código do cliente.
            os_cliente (str): Nome do cliente.
            os_codServico (int): Código do serviço.
            os_descServico (str): Descrição do serviço.
            os_qtd (float): Quantidade do serviço.
            os_vlrUnit (float): Valor unitário do serviço.
            os_total (float): Valor total do serviço.
            os_descrComplementar (str): Descrição complementar do serviço.
            os_faturado (str): Indicação se o serviço está faturado ("SIM" ou "NÃO").

        Returns:
            bool: True se a ordem de serviço foi editada com sucesso, False em caso de erro.

        """
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
        """
        Modifica a situação de faturamento de "NÃO" para "SIM" em todas as ordens de serviço não faturadas.

        Esta função atualiza o estado de faturamento para "SIM" e registra a data de faturamento atual para todas as ordens de serviço que ainda não foram faturadas.

        Returns:
            bool: True se a operação for bem-sucedida, False em caso de erro.

        """
        try:
            # Comando SQL para atualizar os registros
            update_sql = """
            UPDATE tb_ordens_servicos
            SET os_faturado = 'SIM',
                os_dtFaturamento = ?
            WHERE os_faturado = 'NÃO';
            """
            # Obtenha a data atual no formato "DD-MM-YYYY"
            data_atual = datetime.now().strftime('%d-%m-%Y')
            # Execute o comando SQL
            self.db_manager.cursor.execute(update_sql, (data_atual,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print("Erro ao Fechar faturamento:", e)
            return False

    #-------------fim tb ordens de serviços-------------#
    
    #@@@@@@@@@@@@@@ FUNÇÕES TABELA SERVIÇOS @@@@@@@@@@@@@@#
    
    def consultarCompletaTabelaServicosValores(self):
        """
        Consulta e retorna todos os registros da tabela de Serviços e Valores.

        Returns:
            list: Uma lista de tuplas, onde cada tupla contém os seguintes valores:
                - serv_id (int): ID do serviço.
                - serv_codServ (int): Código do serviço.
                - serv_descrServico (str): Descrição do serviço.
                - serv_vlrUnit (float): Valor unitário do serviço.

        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT serv_id, serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr")
        listandoServiços = cursor.fetchall()
        return listandoServiços  

    def verificarSeCodigoDoServicoCadastrado(self, codServico):
        """
        Verifica se um código de serviço já está cadastrado na tabela de Serviços e Valores.

        Args:
            codServico (int): O código de serviço a ser verificado.

        Returns:
            int or None: O código de serviço cadastrado, se encontrado, ou None se não estiver cadastrado.

        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("SELECT serv_codServ FROM tb_servicos_vlr WHERE serv_codServ=?", (codServico,))
        resultado = cursor.fetchone()
        if resultado is not None:
            print(f'Resultado encontrado: {resultado[0]}')
            return resultado[0]
        else:
            return None
    
    def inserirServicoDB(self, codServico, descServico, vlrUnit):
        """
        Insere um novo serviço na tabela de Serviços e Valores.

        Args:
            codServico (int): O código do serviço a ser inserido.
            descServico (str): A descrição do serviço.
            vlrUnit (float): O valor unitário do serviço.

        Returns:
            bool: True se a inserção for bem-sucedida, False em caso de erro.

        """
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
        """
        Deleta um serviço da tabela de Serviços e Valores pelo seu ID.

        Args:
            serv_id (int): O ID do serviço a ser excluído.

        Returns:
            bool: True se a exclusão for bem-sucedida, False em caso de erro.

        """
        try:
            self.db_manager.cursor.execute("DELETE FROM tb_servicos_vlr WHERE serv_id = ?", (serv_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao deletar serviço:", e)
            return False

    def editarServicoPeloIDServicosValoresDB(self, serv_id, serv_codServ, serv_descrServico, serv_vlrUnit):
        """
        Edita um serviço da tabela de Serviços e Valores pelo seu ID.

        Args:
            serv_id (int): O ID do serviço a ser editado.
            serv_codServ (int): O novo código do serviço.
            serv_descrServico (str): A nova descrição do serviço.
            serv_vlrUnit (float): O novo valor unitário do serviço.

        Returns:
            bool: True se a edição for bem-sucedida, False em caso de erro.

        """
        try:
            self.db_manager.cursor.execute(
                "UPDATE tb_servicos_vlr SET serv_codServ = ?, serv_descrServico = ?, serv_vlrUnit = ? WHERE serv_id = ?",
                (serv_codServ, serv_descrServico, serv_vlrUnit, serv_id)
            )
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            # Em caso de erro, imprime a mensagem de erro e retorna False
            print("Erro ao modificar serviço:", e)
            return False

    #-------------fim tb ordens de serviços-------------#
        
  
    
    