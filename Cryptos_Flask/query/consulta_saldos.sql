SELECT 
    w.wallet_name AS carteira,
    w.wallet_user_id AS usuario,
    c.crypto_name AS crypto,
    wb.balance AS quantidade,
    p.price AS preço,
    (wb.balance * p.price) AS valor
FROM 
    wallets w
JOIN 
    wallet_balances wb ON w.wallet_id = wb.balance_wallet_id
JOIN 
    cryptocurrencies c ON c.crypto_id = wb.balance_crypto_id
JOIN 
    prices p ON p.price_crypto_id = c.crypto_id
JOIN 
	users u on u.user_id = w.wallet_user_id 
JOIN 
    (
        SELECT 
            price_crypto_id, 
            MAX(price_consult_datetime) AS latest_timestamp
        FROM 
            prices
        GROUP BY 
            price_crypto_id
    ) latest_prices_subquery ON 
        p.price_crypto_id = latest_prices_subquery.price_crypto_id 
        AND p.price_consult_datetime = latest_prices_subquery.latest_timestamp
WHERE 
    wb.balance > 0
    AND w.wallet_user_id = 9001
ORDER BY 
    w.wallet_name, 
    c.crypto_name;

