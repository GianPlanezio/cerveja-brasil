SELECT
  ano,
  mes,
  sigla_uf,
  indicador_fora_prazo,
  COUNTIF(saldo_movimentacao = 1) AS admissoes,
  COUNTIF(saldo_movimentacao = -1) AS desligamentos,
  SUM(saldo_movimentacao) AS saldo
FROM `basedosdados.br_me_caged.microdados_movimentacao`
WHERE ano BETWEEN 2020 AND 2025
  AND cnae_2_subclasse = '1113502'
GROUP BY ano, mes, sigla_uf, indicador_fora_prazo
ORDER BY ano, mes, sigla_uf