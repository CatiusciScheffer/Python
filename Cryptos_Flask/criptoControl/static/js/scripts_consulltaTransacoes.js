document.addEventListener('DOMContentLoaded', function() {
    function calcularTotalTransacao(row) {
        // Obtém os valores dos campos da linha
        var quantidade = parseFloat(row.querySelector('.quantidade').innerText) || 0;
        var preco = parseFloat(row.querySelector('.preco').innerText) || 0;
        var totalMoeda = parseFloat(row.querySelector('.total-moeda').innerText) || 0;
        var totalTaxa = parseFloat(row.querySelector('.total-taxa').innerText) || 0;
        
        // Calcula o total da transação
        var totalTransacao = totalMoeda + totalTaxa;

        // Atualiza o campo Total Transação
        row.querySelector('.total-transacao').innerText = totalTransacao.toFixed(2);
    }

    // Obtém todas as linhas da tabela
    var linhas = document.querySelectorAll('table tbody tr');
    
    // Itera sobre as linhas e calcula o total
    linhas.forEach(function(linha) {
        calcularTotalTransacao(linha);
    });
});
