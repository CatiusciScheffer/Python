document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os campos do formulário para a transação
    const precoInput = document.querySelector('input[name="crypto_payment_price"]');
    const quantidadeInput = document.querySelector('input[name="crypto_payment_quantity"]');
    const totalInput = document.querySelector('input[name="total_paid"]');
    const moedaSelect = document.querySelector('select[name="crypto_payment"]');

    // Seleciona os campos do formulário para a taxa
    const crypto_fee_priceInput = document.querySelector('input[name="crypto_fee_price"]');
    const crypto_fee_quantityInput = document.querySelector('input[name="crypto_fee_quantity"]');
    const total_feeInput = document.querySelector('input[name="total_fee"]');
    const crypto_feeSelect = document.querySelector('select[name="crypto_fee"]');

    // Seleciona os campos do formulário para o recebimento
    const crypto_receive_priceInput = document.querySelector('input[name="crypto_receive_price"]');
    const crypto_receive_quantityInput = document.querySelector('input[name="crypto_receive_quantity"]');
    const total_receivedInput = document.querySelector('input[name="total_received"]');
    const crypto_receiveSelect = document.querySelector('select[name="crypto_receive"]');

    // Função para calcular o total de uma transação
    function calcularTotal(precoInput, quantidadeInput, totalInput) {
        // Substitui vírgulas por pontos
        const preco = parseFloat(precoInput.value.replace(',', '.')) || 0;
        const quantidade = parseFloat(quantidadeInput.value.replace(',', '.')) || 0;
        const total = preco * quantidade;
        totalInput.value = total.toFixed(10); // Formata o valor para 2 casas decimais
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

    // Atualiza o preço da crypto selecionada na transação
    moedaSelect.addEventListener('change', function() {
        const cryptocurrencyId = this.value;
        fetch(`/get_price/${cryptocurrencyId}`)
            .then(response => response.json())
            .then(data => {
                precoInput.value = data.price;
                calcularTotal(precoInput, quantidadeInput, totalInput);
            });
    });

    // Atualiza o preço da crypto selecionada na taxa
    crypto_feeSelect.addEventListener('change', function() {
        const cryptocurrencyId = this.value;
        fetch(`/get_price/${cryptocurrencyId}`)
            .then(response => response.json())
            .then(data => {
                crypto_fee_priceInput.value = data.price;
                calcularTotal(crypto_fee_priceInput, crypto_fee_quantityInput, total_feeInput);
            });
    });

    // Atualiza o preço da crypto selecionada no recebimento
    crypto_receiveSelect.addEventListener('change', function() {
        const cryptocurrencyId = this.value;
        fetch(`/get_price/${cryptocurrencyId}`)
            .then(response => response.json())
            .then(data => {
                crypto_receive_priceInput.value = data.price;
                calcularTotal(crypto_receive_priceInput, crypto_receive_quantityInput, total_receivedInput);
            });
    });

    // Adiciona os eventos de escuta para transações
    adicionarEventos(precoInput, quantidadeInput, totalInput, moedaSelect, function() {
        calcularTotal(precoInput, quantidadeInput, totalInput);
    });

    // Adiciona os eventos de escuta para taxas
    adicionarEventos(crypto_fee_priceInput, crypto_fee_quantityInput, total_feeInput, crypto_feeSelect, function() {
        calcularTotal(crypto_fee_priceInput, crypto_fee_quantityInput, total_feeInput);
    });

    // Adiciona os eventos de escuta para recebimentos
    adicionarEventos(crypto_receive_priceInput, crypto_receive_quantityInput, total_receivedInput, crypto_receiveSelect, function() {
        calcularTotal(crypto_receive_priceInput, crypto_receive_quantityInput, total_receivedInput);
    });

    // Ocultar a carteira conforme tipo de transação
    const transaction_type = document.getElementById('transaction_type');
    const section_wallet_received = document.getElementById('receiving_wallet_container');
    const section_wallet_payment = document.getElementById('saida_wallet_container');
    const section_crypto_fee = document.getElementById('section_crypto_fee');
    const section_crypto_received = document.getElementById('section_crypto_received');
    const section_crypto_payment = document.getElementById('section_crypto_payment');

    function toggleWalletContainers() {
        const selectedValue = transaction_type.value;

        // Condição para mostrar/ocultar elementos
        if (selectedValue === 'Saldo') {
            section_wallet_received.style.display = 'block';
            section_wallet_payment.style.display = 'none';
            section_crypto_fee.style.display = 'none';
            section_crypto_received.style.display = 'block';
            section_crypto_payment.style.display = 'none';
        } else if (selectedValue === 'Transferência'){
            section_wallet_received.style.display = 'block';
            section_wallet_payment.style.display = 'block';
            section_crypto_fee.style.display = 'block';
            section_crypto_received.style.display = 'block';
            section_crypto_payment.style.display = 'none';
        } else {
            section_wallet_received.style.display = 'block';
            section_wallet_payment.style.display = 'block';
            section_crypto_fee.style.display = 'block';
            section_crypto_received.style.display = 'block';
            section_crypto_payment.style.display = 'block';
        }
    }

    // Inicializa a visibilidade com base no valor selecionado ao carregar a página
    toggleWalletContainers();

    // Adiciona evento de mudança ao dropdown
    transaction_type.addEventListener('change', toggleWalletContainers);

    // Atualiza os campos ocultos com base na seleção das carteiras
    const carteriaSaidaSelect = document.getElementById('payment_wallet');
    carteriaSaidaSelect.addEventListener('change', function() {
        document.getElementById('hidden_payment_wallet_id').value = this.value;
    });

    const carteriaRecebimentoSelect = document.getElementById('receiving_wallet');
    carteriaRecebimentoSelect.addEventListener('change', function() {
        document.getElementById('hidden_carteriaRecebimentoTransacao_id').value = this.value;
    });

});
