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



