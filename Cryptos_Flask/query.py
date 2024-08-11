@app.route('/add_crypto', methods=['GET','POST'])  # Define uma rota '/add_crypto' que aceita métodos GET e POST
def add_crypto():  # Define a função 'add_crypto' para lidar com requisições à rota '/add_crypto'
    session = create_session()  # Cria uma nova sessão do banco de dados para executar operações
    try:  # Inicia um bloco try para capturar exceções que possam ocorrer durante a execução do código
        formAddMoedas = AddCryptoForm()  # Cria uma instância do formulário 'AddCryptoForm' para capturar dados de entrada
        if formAddMoedas.validate_on_submit():  # Verifica se o formulário foi submetido e se todos os campos são válidos
            cripto_name = formAddMoedas.nomeMoeda.data  # Obtém o valor do campo 'nomeMoeda' do formulário
            cripto_symbol = formAddMoedas.symbolMoeda.data  # Obtém o valor do campo 'symbolMoeda' do formulário
            with app.app_context():  # Cria um contexto de aplicação para executar o código em um ambiente seguro
                moeda = cryptocurrencies(name=cripto_name, symbol=cripto_symbol)  # Cria uma nova instância de 'Cryptocurrency' com os valores fornecidos
                session.add(moeda)  # Adiciona a nova instância 'moeda' à sessão, marcando-a para inserção no banco de dados
                session.commit()  # Confirma (commit) as mudanças, inserindo o novo registro no banco de dados
        else:  # Caso a validação do formulário falhe
            print("Form validation failed")  # Imprime uma mensagem indicando que a validação do formulário falhou
    except Exception as e:  # Captura qualquer exceção que ocorra dentro do bloco try
        print(f"Erro ao adicionar moeda: {e}")  # Imprime uma mensagem de erro com detalhes da exceção capturada
        session.rollback()  # Faz rollback das mudanças na sessão, desfazendo qualquer operação não confirmada
    finally:  # Bloco que é executado sempre, independentemente de uma exceção ter ocorrido ou não
        session.close()  # Fecha a sessão do banco de dados para liberar recursos
    return redirect(url_for('moedas'))  # Redireciona o usuário para a rota 'moedas' após a operação ser concluída
