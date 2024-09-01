document.addEventListener('DOMContentLoaded', function() {
    function calculartotal_paid(row) {
        // Obtém os valores dos campos da linha
        var quantidade = parseFloat(row.querySelector('.quantidade').innerText) || 0;
        var preco = parseFloat(row.querySelector('.preco').innerText) || 0;
        var totalMoeda = parseFloat(row.querySelector('.total-crypto').innerText) || 0;
        var total_fee = parseFloat(row.querySelector('.total-taxa').innerText) || 0;
        
        // Calcula o total da transação
        var total_paid = totalMoeda + total_fee;

        // Atualiza o campo Total Transação
        row.querySelector('.total-transacao').innerText = total_paid.toFixed(2);
    }

    // Obtém todas as linhas da tabela
    var linhas = document.querySelectorAll('table tbody tr');
    
    // Itera sobre as linhas e calcula o total
    linhas.forEach(function(linha) {
        calculartotal_paid(linha);
    });
});
