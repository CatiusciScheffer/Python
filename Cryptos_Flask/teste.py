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

    // Seleciona o elemento que contém a seção "Sobre a Taxa"
    const section_crypto_fee = document.getElementById('section_crypto_fee');
    
    // Seleciona os campos ocultos para IDs
    const carteriaSaidaIdInput = document.getElementById('payment_wallet_id');
    const carteriaRecebimentoIdInput = document.getElementById('carteriaRecebimentoTransacao_id');

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

    // Adiciona os eventos de escuta para transações
    adicionarEventos(precoInput, quantidadeInput, totalInput, moedaSelect, function() {
        calcularTotal(precoInput, quantidadeInput, totalInput);
    });

    // Adiciona os eventos de escuta para taxas
    adicionarEventos(crypto_fee_priceInput, crypto_fee_quantityInput, total_feeInput, crypto_feeSelect, function() {
        calcularTotal(crypto_fee_priceInput, crypto_fee_quantityInput, total_feeInput);
    });

    // Ocultar a carteira conforme tipo de transação
    const transaction_type = document.getElementById('transaction_type');
    const section_wallet_received = document.getElementById('receiving_wallet_container');
    const section_wallet_payment = document.getElementById('saida_wallet_container');

    function toggleWalletContainers() {
        const selectedValue = transaction_type.value;

        // Condição para mostrar/ocultar a carteira de recebimento
        if (selectedValue === 'Venda') {
            section_wallet_received.style.display = 'block';
            section_wallet_payment.style.display = 'block';
            section_crypto_fee.style.display = 'block'; // Mostra a seção "Sobre a Taxa"
        } else if (selectedValue === 'Compra' || selectedValue === 'Saldo') {
            section_wallet_received.style.display = 'block';
            section_wallet_payment.style.display = 'none';
    
            if (selectedValue === 'Saldo') {
                section_crypto_fee.style.display = 'none'; // Oculta a seção "Sobre a Taxa" se for "Saldo"
            } else {
                section_crypto_fee.style.display = 'block'; // Mostra a seção "Sobre a Taxa" se for "Compra"
            }
        } else {
            section_wallet_received.style.display = 'block';
            section_wallet_payment.style.display = 'block';
            section_crypto_fee.style.display = 'block'; // Mostra a seção "Sobre a Taxa"
        } 
    }

    // Inicializa a visibilidade com base no valor selecionado ao carregar a página
    toggleWalletContainers();

    // Adiciona evento de mudança ao dropdown
    transaction_type.addEventListener('change', toggleWalletContainers);

   // Atualiza os campos ocultos com base na seleção das carteiras
    const carteriaSaidaSelect = document.getElementById('payment_wallet');
    carteriaSaidaSelect.addEventListener('change', function() {
        const carteriaSaidaIdInput = document.getElementById('payment_wallet');
        carteriaSaidaIdInput.value = this.value; // Atualiza o valor do campo oculto
    });

    const carteriaRecebimentoSelect = document.getElementById('receiving_wallet');
    carteriaRecebimentoSelect.addEventListener('change', function() {
        const carteriaRecebimentoIdInput = document.getElementById('carteriaRecebimentoTransacaoId');
        carteriaRecebimentoIdInput.value = this.value; // Atualiza o valor do campo oculto
    });
    
});