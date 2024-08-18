def realizar_compra(session, wallet_id, crypto_id, amount, fee_crypto_id, fee_amount, amount_paid):
    try:
        # Verificar a moeda e a carteira da transação
        wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=crypto_id).first()
        
        # Verificar a moeda e a carteira da taxa
        fee_wallet_balance = session.query(WalletBalance).filter_by(wallet_id=wallet_id, cryptocurrency_id=fee_crypto_id).first()

        # Adicionar dados na tabela de Transaction
        transaction = Transaction(
            wallet_id=wallet_id,
            crypto_Trans_id=crypto_id,
            crypto_price=amount_paid,  # Preço da moeda (considerar se você tem este dado)
            crypto_quantity=amount,
            transaction_total=amount_paid,
            type='Compra',
            fee_crypto_id=fee_crypto_id,
            fee_price=fee_amount,  # Preço da taxa (considerar se você tem este dado)
            fee_quantity=fee_amount,
            fee_total=fee_amount,
            receiving_wallet_id=None,  # Para compra, o receiving_wallet_id é None
            date=datetime.now()
        )
        session.add(transaction)

        if wallet_balance is None:
            # Caso não tenha registro na WalletBalance, inserir novos registros
            new_wallet_balance = WalletBalance(
                wallet_id=wallet_id,
                cryptocurrency_id=crypto_id,
                balance=amount  # Quantidade da moeda comprada
            )
            session.add(new_wallet_balance)
        else:
            # Atualizar saldo existente para a moeda da transação
            wallet_balance.balance += amount
            session.add(wallet_balance)
        
        if fee_wallet_balance is None:
            # Se não houver saldo para a moeda da taxa, inserir novo registro
            new_fee_wallet_balance = WalletBalance(
                wallet_id=wallet_id,
                cryptocurrency_id=fee_crypto_id,
                balance=fee_amount  # Quantidade da taxa
            )
            session.add(new_fee_wallet_balance)
        else:
            # Atualizar saldo existente para a moeda da taxa
            fee_wallet_balance.balance += fee_amount
            session.add(fee_wallet_balance)

        # Confirmar as alterações na base de dados
        session.commit()
    except Exception as e:
        # Em caso de erro, fazer rollback e imprimir o erro
        session.rollback()
        print(f"Erro ao realizar a compra: {e}")










        ******************

//Puxa oo preço da moeda selecionada na transação
document
  .getElementById("moedaTransacao")
  .addEventListener("change", function () {
    var cryptocurrency_id = this.value;
    var priceField = document.getElementById("precoTransacao");

    fetch("/get_price/" + cryptocurrency_id)
      .then((response) => response.json())
      .then((data) => {
        priceField.value = data.price;
      });
  });

//Puxa oo preço da moeda selecionada na taxa
document
  .getElementById("moedaTaxa")
  .addEventListener("change", function () {
    var cryptocurrency_id = this.value;
    var priceField = document.getElementById("precoTaxa");

    fetch("/get_price/" + cryptocurrency_id)
      .then((response) => response.json())
      .then((data) => {
        priceField.value = data.price;
      });
  });

// Função para calcular o total de uma transação
function calcularTotal(precoInput, quantidadeInput, totalInput) {
    const preco = parseFloat(precoInput.value) || 0;
    const quantidade = parseFloat(quantidadeInput.value) || 0;
    const total = preco * quantidade;
    totalInput.value = total.toFixed(2); // Formata o valor para 2 casas decimais
}

// Função para limpar o campo de quantidade e recalcular o total
function limparQuantidade(quantidadeInput, calcularFunc) {
    quantidadeInput.value = ''; // Limpa o campo de quantidade
    calcularFunc(); // Recalcula o total
}

// Função para adicionar os eventos de escuta
function adicionarEventos(precoInput, quantidadeInput, totalInput, moedaSelect, calcularFunc) {
    precoInput.addEventListener('input', calcularFunc);
    quantidadeInput.addEventListener('input', calcularFunc);
    moedaSelect.addEventListener('change', function() {
        limparQuantidade(quantidadeInput, calcularFunc);
    });
}

// Executa quando o DOM estiver completamente carregado
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os campos do formulário para a transação
    const precoInput = document.querySelector('input[name="precoTransacao"]');
    const quantidadeInput = document.querySelector('input[name="quantidadeTransacao"]');
    const totalInput = document.querySelector('input[name="totalTransacao"]');
    const moedaSelect = document.querySelector('select[name="moedaTransacao"]');

    // Seleciona os campos do formulário para a taxa
    const precotxInput = document.querySelector('input[name="precoTaxa"]');
    const quantidadetxInput = document.querySelector('input[name="quantidadeTaxa"]');
    const totaltxInput = document.querySelector('input[name="totalTaxa"]');
    const moedatxSelect = document.querySelector('select[name="moedaTaxa"]');

    // Adiciona os eventos de escuta para transações
    adicionarEventos(precoInput, quantidadeInput, totalInput, moedaSelect, function() {
        calcularTotal(precoInput, quantidadeInput, totalInput);
    });

    // Adiciona os eventos de escuta para taxas
    adicionarEventos(precotxInput, quantidadetxInput, totaltxInput, moedatxSelect, function() {
        calcularTotal(precotxInput, quantidadetxInput, totaltxInput);
    });
});

//Ocultar a carteira conforme tipo de transação
document.addEventListener('DOMContentLoaded', function() {
    const tipoTransacao = document.getElementById('tipoTransacao');
    const receivingWalletContainer = document.getElementById('receiving_wallet_container');
    const saidaWalletContainer = document.getElementById('saida_wallet_container');

    function toggleWalletContainers() {
        const selectedValue = tipoTransacao.value;

        // Condição para mostrar/ocultar a carteira de recebimento
        if (selectedValue === 'Venda') {
            receivingWalletContainer.style.display = 'none';
            saidaWalletContainer.style.display = 'block';
        } else if (selectedValue === 'Compra') {
            receivingWalletContainer.style.display = 'block';
            saidaWalletContainer.style.display = 'none';
        } else {
            receivingWalletContainer.style.display = 'block';
            saidaWalletContainer.style.display = 'block';
        }
    }

    // Inicializa a visibilidade com base no valor selecionado ao carregar a página
    toggleWalletContainers();

    // Adiciona evento de mudança ao dropdown
    tipoTransacao.addEventListener('change', toggleWalletContainers);
});



