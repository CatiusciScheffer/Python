import sqlite3

def buscarNomeCliente(codCliente):
    conexao = sqlite3.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT cli_nomeCliente FROM tb_cliente WHERE cli_codCliente=?", (codCliente,))
    resultado = cursor.fetchone()
    if resultado is not None:
        return resultado[0]
    else:
        return None

def buscarDescricaoServico(codServico):
    conexao = sqlite3.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT serv_descrServico FROM tb_servicos_vlr WHERE serv_codServ=?", (codServico,))
    resultado = cursor.fetchone()
    if resultado is not None:
        return resultado[0]
    else:
        return None

def buscarValorUnitario(codServico):
    conexao = sqlite3.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT serv_vlrUnit FROM tb_servicos_vlr WHERE serv_codServ=?", (codServico,))
    resultado = cursor.fetchone()
    if resultado is not None:
        return resultado[0]
    else:
        return 0.0

def inserirOrdemServico(os_dtServico, os_codCliente, os_observacao, os_codServico, os_qtd, os_vlrUnit, os_usuario):
    conexao = sqlite3.connect('db_OrdemServicos.db')
    cursor = conexao.cursor()

    # Verificar se o cliente existe na tabela tb_cliente
    cliente = buscarNomeCliente(os_codCliente)
    if cliente is None:
        print(f"Cliente com código {os_codCliente} não existe na tabela tb_cliente.")
        return

    # Verificar se o serviço existe na tabela tb_servicos_vlr
    descricaoServico = buscarDescricaoServico(os_codServico)
    if descricaoServico is None:
        print(f"Serviço com código {os_codServico} não existe na tabela tb_servicos_vlr.")
        return

    # Verificar usuário logado e preencher os_usuario com o nome do usuário
    os_usuario = 'useteste'

    # Buscar valor unitário
    vlrUnit = buscarValorUnitario(os_codServico)

    # Calcular o total
    os_total = os_qtd * os_vlrUnit

    # Executar a instrução INSERT
    cursor.execute("INSERT INTO tb_ordens_servicos (os_dtServico, os_codCliente, os_Cliente, os_observacao, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (os_dtServico, os_codCliente, cliente, os_observacao, os_codServico, descricaoServico, os_qtd, vlrUnit, os_total, os_usuario))

    # Salvar a transação
    conexao.commit()
    print("Ordem de serviço inserida com sucesso.")

# Exemplo de inserção de ordem de serviço
inserirOrdemServico("2023-05-17", 156, "Observação trigger", 8, 2, '', '')
