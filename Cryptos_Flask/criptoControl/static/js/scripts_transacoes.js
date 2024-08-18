document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os campos do formulário para a transação
    const precoInput = document.querySelector('input[name="precoTransacao"]');
    const quantidadeInput = document.querySelector('input[name="quantidadeTransacao"]');
    const totalInput = document.querySelector('input[name="totalTransacao"]');
    const moedaSelect = document.querySelector('select[name="moedaTransacao"]');
    
    // Seleciona os campos do formulário para a taxa
    const precoTaxaInput = document.querySelector('input[name="precoTaxa"]');
    const quantidadeTaxaInput = document.querySelector('input[name="quantidadeTaxa"]');
    const totalTaxaInput = document.querySelector('input[name="totalTaxa"]');
    const moedaTaxaSelect = document.querySelector('select[name="moedaTaxa"]');
    
    // Seleciona os campos ocultos para IDs
    const carteriaSaidaIdInput = document.getElementById('carteriaSaidaTransacao_id');
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

    // Atualiza o preço da moeda selecionada na transação
    moedaSelect.addEventListener('change', function() {
        const cryptocurrencyId = this.value;
        fetch(`/get_price/${cryptocurrencyId}`)
            .then(response => response.json())
            .then(data => {
                precoInput.value = data.price;
                calcularTotal(precoInput, quantidadeInput, totalInput);
            });
    });

    // Atualiza o preço da moeda selecionada na taxa
    moedaTaxaSelect.addEventListener('change', function() {
        const cryptocurrencyId = this.value;
        fetch(`/get_price/${cryptocurrencyId}`)
            .then(response => response.json())
            .then(data => {
                precoTaxaInput.value = data.price;
                calcularTotal(precoTaxaInput, quantidadeTaxaInput, totalTaxaInput);
            });
    });

    // Adiciona os eventos de escuta para transações
    adicionarEventos(precoInput, quantidadeInput, totalInput, moedaSelect, function() {
        calcularTotal(precoInput, quantidadeInput, totalInput);
    });

    // Adiciona os eventos de escuta para taxas
    adicionarEventos(precoTaxaInput, quantidadeTaxaInput, totalTaxaInput, moedaTaxaSelect, function() {
        calcularTotal(precoTaxaInput, quantidadeTaxaInput, totalTaxaInput);
    });

    // Ocultar a carteira conforme tipo de transação
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

    // Atualiza os campos ocultos com base na seleção das carteiras
    const carteriaSaidaSelect = document.getElementById('carteriaSaidaTransacao');
    carteriaSaidaSelect.addEventListener('change', function() {
        carteriaSaidaIdInput.value = this.value; // Atualiza o valor do campo oculto
    });

    const carteriaRecebimentoSelect = document.getElementById('carteriaRecebimentoTransacao');
    carteriaRecebimentoSelect.addEventListener('change', function() {
        carteriaRecebimentoIdInput.value = this.value; // Atualiza o valor do campo oculto
    });
});
