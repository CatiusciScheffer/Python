SELECT 
    w.wallet_name AS Carteira,
	c.crypto_symbol AS Moeda,    
    SUM(t.crypto_receive_quantity * t.crypto_receive_price) / SUM(t.crypto_receive_quantity) AS 'DCA'
FROM 
    transactions t
JOIN 
    wallets w ON t.receiving_wallet_id = w.wallet_id
JOIN 
    users u ON u.user_id = w.wallet_user_id 
JOIN 
    cryptocurrencies c ON t.crypto_receive_id = c.crypto_id
WHERE 
    t.transaction_type = 'Compra' OR t.transaction_type = 'Saldo'
    AND u.user_id = 9000
GROUP BY 
    c.crypto_symbol, w.wallet_name;

