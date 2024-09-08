document.addEventListener('DOMContentLoaded', function() {
    function calculartotal_paid(row) {
        // Obtém os valores dos campos da linha
        var quantidade = parseFloat(row.querySelector('.quantidade').innerText) || 0;
        var preco = parseFloat(row.querySelector('.preco').innerText) || 0;
        var totalMoeda = parseFloat(row.querySelector('.total-crypto').innerText) || 0;
        var total_fee = parseFloat(row.querySelector('.total-taxa').innerText) || 0;
        
        // Log para depuração
        console.log('Quantidade:', quantidade);
        console.log('Preço:', preco);
        console.log('Total Moeda:', totalMoeda);
        console.log('Total Taxa:', total_fee);

        // Calcula o total da transação
        var total_paid = totalMoeda + total_fee;

        // Atualiza o campo Total Transação
        var totalTransacaoElement = row.querySelector('.total-transacao');
        if (totalTransacaoElement) {
            totalTransacaoElement.innerText = total_paid.toFixed(2);
        } else {
            console.error('Elemento para total-transacao não encontrado.');
        }
    }

    // Obtém todas as linhas da tabela
    var linhas = document.querySelectorAll('table tbody tr');
    
    // Verificação de linhas encontradas
    if (linhas.length === 0) {
        console.error('Nenhuma linha encontrada na tabela.');
    } else {
        // Itera sobre as linhas e calcula o total
        linhas.forEach(function(linha) {
            calculartotal_paid(linha);
        });
    }
});
