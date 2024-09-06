WITH latest_prices AS (
    SELECT 
        price_crypto_id, 
        MAX(price_consult_datetime) AS latest_timestamp
    FROM prices
    GROUP BY price_crypto_id
)

SELECT 
    w.wallet_name AS carteira,
    c.crypto_name AS crypto,
    wb.balance AS quantidade,
    p.price AS preço,
    (wb.balance * p.price) AS valor
FROM wallet_balances wb
JOIN wallets w ON wb.balance_wallet_id = w.wallet_id
JOIN cryptocurrencies c ON wb.balance_crypto_id = c.crypto_id
JOIN prices p ON c.crypto_id = p.price_crypto_id
JOIN latest_prices lp ON p.price_crypto_id = lp.price_crypto_id
    AND p.price_consult_datetime = lp.latest_timestamp
ORDER BY w.wallet_name;
