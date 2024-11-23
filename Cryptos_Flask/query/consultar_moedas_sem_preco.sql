--consulta para ver se tem moeda sem consulta de preço

WITH numbers AS (
    SELECT 1 AS num
    UNION ALL
    SELECT num + 1 FROM numbers WHERE num < 100
)
SELECT num AS missing_price_crypto_id
FROM numbers
WHERE num NOT IN (SELECT price_crypto_id FROM prices)
ORDER BY num;
