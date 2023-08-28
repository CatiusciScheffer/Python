-- SQLite
SELECT os_id, os_dtServico, os_codCliente, os_cliente, os_codServico, os_descServico, os_qtd, os_vlrUnit, os_total, os_descrComplementar, os_faturado,
       SUM(os_qtd) as total_quantidade,
       SUM(os_vlrUnit) as total_valor_unitario,
       SUM(os_total) as total_valor_total
FROM tb_ordens_servicos
WHERE os_faturado = 'NÃO'
GROUP BY os_cliente, os_codServico
ORDER BY os_cliente