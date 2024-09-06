SELECT 
    t.*, 
    pw.wallet_name AS payment_wallet_name, 
    rw.wallet_name AS receiving_wallet_name, 
    cp.crypto_name AS crypto_payment_name, 
    cr.crypto_name AS crypto_receive_name, 
    cf.crypto_name AS crypto_fee_name
FROM transactions t
LEFT JOIN wallets pw ON t.payment_wallet_id = pw.wallet_id
LEFT JOIN wallets rw ON t.receiving_wallet_id = rw.wallet_id
LEFT JOIN cryptocurrencies cp ON t.crypto_payment_id = cp.crypto_id
LEFT JOIN cryptocurrencies cr ON t.crypto_receive_id = cr.crypto_id
LEFT JOIN cryptocurrencies cf ON t.crypto_fee_id = cf.crypto_id;
