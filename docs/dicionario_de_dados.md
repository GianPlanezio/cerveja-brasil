# Dicionário de dados

Descrição de cada arquivo em `data/processed`, gerado pelos notebooks `01_extracao.ipynb` e `02_qualidade_dos_dados.ipynb`.

## Convenções

- **Formato:** CSV separado por vírgula, codificação UTF-8, ponto como separador decimal e sem separador de milhar.
- **Volumes de cerveja:** sempre em litros.
- **Porcentagens:** de 0 a 100. Por exemplo, `42.49` significa 42,49%.
- **Variações (`variacao_pct`):** variação percentual em relação ao ano anterior, também de 0 a 100. Nos arquivos de 2025 é a variação 2024→2025; nos de 2024, a variação 2023→2024.
- **`ano_referencia`:** ano a que os dados se referem, não o ano da publicação. O Anuário da Cerveja 2026 traz dados de 2025; o Anuário 2025, dados de 2024.
- **`fonte`:** publicação, tabela e página de origem de cada linha. Valores digitados de imagens trazem "(digitado da imagem)".
- **`origem` e `observacao`:** aparecem quando uma linha foi calculada ou corrigida neste projeto, e explicam como.

Os problemas encontrados nas fontes, e as decisões tomadas para cada um, estão em [`registro_inconsistencias.csv`](registro_inconsistencias.csv).

## Índice

| Arquivo | Conteúdo | Ano | Fonte |
| --- | --- | --- | --- |
| `tabela_16_empregos_uf_2025.csv` | Empregos no setor por UF | 2025 | Anuário 2026 |
| `tabela_17_producao_regiao_2025.csv` | Produção por região | 2025 | Anuário 2026 |
| `tabela_18_producao_media_regiao_2025.csv` | Cervejarias e produção média por região | 2025 | Anuário 2026 |
| `tabela_19_concentracao_2025.csv` | Concentração da produção | 2025 | Anuário 2026 |
| `tabela_20_puro_malte_2025.csv` | Puro malte e demais cervejas | 2025 | Anuário 2026 |
| `tabela_21_estilos_2025.csv` | Produção por estilo | 2025 | Anuário 2026 |
| `tabela_22_caracteristicas_2025.csv` | Produção por característica | 2025 | Anuário 2026 |
| `tabela_23_abrangencia_2025.csv` | Produção por abrangência de comercialização | 2025 | Anuário 2026 |
| `grafico_02_cervejarias_uf_2025.csv` | Cervejarias por UF | 2025 | Anuário 2026 |
| `producao_regiao_2024.csv` | Produção por região | 2024 | Anuário 2025 |
| `producao_media_regiao_2024.csv` | Cervejarias e produção média por região | 2024 | Anuário 2025 |
| `concentracao_2024.csv` | Concentração da produção | 2024 | Anuário 2025 |
| `puro_malte_2024.csv` | Puro malte e demais cervejas | 2024 | Anuário 2025 |
| `estilos_2024.csv` | Produção por estilo | 2024 | Anuário 2025 |
| `caracteristicas_2024.csv` | Produção por característica | 2024 | Anuário 2025 |
| `abrangencia_2024.csv` | Produção por abrangência de comercialização | 2024 | Anuário 2025 |
| `comex_insumos_mensal_2015_2025.csv` | Comércio exterior de malte e lúpulo | 2015–2025, mensal | Comex Stat |
| `comex_cerveja_mensal_2015_2025.csv` | Comércio exterior de cerveja | 2015–2025, mensal | Comex Stat |
| `caged_cerveja_mensal_2020_2025.csv` | Admissões e desligamentos no setor por UF | 2020–2025, mensal | Novo CAGED |
| `reconciliacao_variacoes_2024.csv` | Volumes de 2024 implícitos nas variações do Anuário 2026 | 2024 | Calculado |

---

## Anuário da Cerveja 2026 (ano-referência 2025)

Extraído do PDF com `pdfplumber`, exceto o Gráfico 2, digitado da imagem. Total nacional de 2025: **15.688.083.191,69 litros**.

### tabela_16_empregos_uf_2025.csv

Estoque de empregos formais na fabricação de cervejas e chopes (CNAE 1113-5/02), por UF. Uma linha por UF (27 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `uf` | texto | | Sigla da UF |
| `estoque_empregos` | inteiro | empregos | Empregos formais no fim do ano |
| `pct_empregos` | decimal | % | Participação da UF no total nacional |
| `variacao_texto` | texto | | Variação como impressa no Anuário, preservada para o caso do Amapá ("de 0 para 5") |
| `variacao_pct` | decimal | % | Variação do estoque em relação a 2024; vazia no Amapá, cuja base era zero |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** os valores coincidem com o Novo CAGED (ver `caged_cerveja_mensal_2020_2025.csv`), que provavelmente é a fonte original do Anuário.

### tabela_17_producao_regiao_2025.csv

Volume de produção declarado por região. Uma linha por região (5 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `regiao` | texto | | Nome da região |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_volume` | decimal | % | Participação no volume nacional |
| `variacao_pct` | decimal | % | Variação em relação a 2024 |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** a `variacao_pct` desta tabela usa o total **retificado** de 2024 (17,21 bilhões de litros), diferente das tabelas 20 e 23, que usam o original (15,34 bilhões). Ver `reconciliacao_variacoes_2024.csv`.

### tabela_18_producao_media_regiao_2025.csv

Volume, número de cervejarias e produção média por região. Uma linha por região (5 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `regiao` | texto | | Nome da região |
| `volume_litros` | decimal | litros | Volume produzido |
| `n_cervejarias` | inteiro | cervejarias | Cervejarias registradas no MAPA |
| `producao_media_litros` | decimal | litros por cervejaria | Volume ÷ número de cervejarias |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** as regiões aparecem em ordem diferente da Tabela 17. Junções devem usar a coluna `regiao`, nunca a posição da linha.

### tabela_19_concentracao_2025.csv

Pontos da curva de concentração: fatia do volume produzida pelas maiores cervejarias. Uma linha por ponto (6 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `pct_cervejarias` | decimal | % | Fatia das maiores cervejarias: 1, 2, 3, 4, 5 ou 10% |
| `volume_litros` | decimal | litros | Volume produzido por essa fatia |
| `pct_volume` | decimal | % | Participação desse volume no total nacional |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela ou trecho de texto de origem |
| `origem` | texto | | `tabela` para os pontos lidos da tabela; para o ponto de 10%, indica que o volume foi calculado (99,5% do total), já que o Anuário só informa a porcentagem |

**Cuidado:** são só seis pontos, então uma curva de Lorenz ou um índice de Gini calculados a partir deles são aproximações.

### tabela_20_puro_malte_2025.csv

Volume segundo a proporção de malte de cevada. Duas linhas.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `categoria` | texto | | "Cerveja Puro Malte ou 100% malte" ou "Demais cervejas" |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_volume` | decimal | % | Participação no volume nacional |
| `variacao_pct` | decimal | % | Variação em relação a 2024 |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** a `variacao_pct` usa o total **original** de 2024 e por isso não é comparável com a queda nacional de 8,85%. O "+21,01% do puro malte" é um teto; o indicador robusto é a participação (24,7% em 2024 e 29,2% em 2025). Ver o registro de inconsistências, item 1.

### tabela_21_estilos_2025.csv

Volume por estilo de cerveja. Uma linha por estilo (17 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `estilo` | texto | | Nome do estilo |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_entre_estilos` | decimal | % | Participação na soma dos estilos **desta tabela**, não no total nacional |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** o Anuário excluiu desta tabela os estilos com bilhões de litros, então os volumes não somam o total nacional. As categorias também diferem das de `estilos_2024.csv`.

### tabela_22_caracteristicas_2025.csv

Volume por característica da cerveja. Uma linha por característica (7 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `caracteristica` | texto | | Característica declarada (sem glúten, com fruta etc.) |
| `volume_litros` | decimal | litros | Volume produzido com essa característica |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** uma mesma cerveja pode ter mais de uma característica, então os volumes não somam o total nacional. "Com Madeiras Brasileiras" não é comparável com "Com madeira" de 2024.

### tabela_23_abrangencia_2025.csv

Volume segundo a abrangência de comercialização. Uma linha por faixa (5 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `abrangencia` | texto | | Faixa de abrangência, de microrregional a somente internacional |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_volume` | decimal | % | Participação no volume nacional |
| `variacao_pct` | decimal | % | Variação em relação a 2024 |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** como na Tabela 20, a `variacao_pct` usa o total **original** de 2024.

### grafico_02_cervejarias_uf_2025.csv

Cervejarias registradas por UF, digitadas do Gráfico 2. Uma linha por UF (27 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `uf` | texto | | Sigla da UF |
| `regiao` | texto | | Região da UF, acrescentada neste projeto |
| `n_cervejarias` | inteiro | cervejarias | Cervejarias registradas no MAPA |
| `variacao_pct` | decimal | % | Variação em relação a 2024 |
| `ano_referencia` | inteiro | | 2025 |
| `fonte` | texto | | Gráfico de origem |
| `observacao` | texto | | Nota sobre a legenda do gráfico, que indica 2023/2024 por engano |

---

## Anuário da Cerveja 2025 (ano-referência 2024)

As tabelas desta edição são imagens no PDF, então os valores foram digitados e conferidos pela soma com o total publicado de 2024: **15.344.065.267,36 litros**. Esse total foi depois retificado para 17.210.754.610,75 litros no Anuário 2026; os arquivos abaixo trazem os valores **como publicados**.

A numeração das tabelas difere da edição de 2026, por isso os arquivos são nomeados pelo conteúdo.

### producao_regiao_2024.csv

Volume de produção declarado por região. Uma linha por região (5 linhas). Mesmas colunas de `tabela_17_producao_regiao_2025.csv`, mais `observacao`.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `regiao` | texto | | Nome da região |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_volume` | decimal | % | Participação no volume nacional |
| `variacao_pct` | decimal | % | Variação em relação a 2023 |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |
| `observacao` | texto | | Preenchida no Centro-Oeste: a Tabela 17 imprime 1.074.137.071,79 L, e foi usado o valor da Tabela 18 e do texto |

### producao_media_regiao_2024.csv

Volume, número de cervejarias e produção média por região. Uma linha por região (5 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `regiao` | texto | | Nome da região |
| `volume_litros` | decimal | litros | Volume produzido |
| `n_cervejarias` | inteiro | cervejarias | Cervejarias registradas no MAPA |
| `producao_media_impressa` | decimal | litros por cervejaria | Valor impresso no Anuário, **incorreto** |
| `producao_media_calculada` | decimal | litros por cervejaria | Volume ÷ número de cervejarias, calculado neste projeto; usar esta |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |

### concentracao_2024.csv

Pontos da curva de concentração. Uma linha por ponto (5 linhas: 1% a 5%). Mesmas colunas de `tabela_19_concentracao_2025.csv`.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `pct_cervejarias` | decimal | % | Fatia das maiores cervejarias |
| `volume_litros` | decimal | litros | Volume produzido por essa fatia |
| `pct_volume` | decimal | % | Participação desse volume no total nacional |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |
| `origem` | texto | | `tabela` em todas as linhas |

### puro_malte_2024.csv

Volume segundo a proporção de malte de cevada. Duas linhas. Mesmas colunas de `tabela_20_puro_malte_2025.csv`.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `categoria` | texto | | "Cerveja Puro Malte ou 100% malte" ou "Demais cervejas" |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_volume` | decimal | % | Participação no volume nacional |
| `variacao_pct` | decimal | % | Variação em relação a 2023 |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |

### estilos_2024.csv

Volume por estilo de cerveja. Uma linha por estilo (27 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `estilo` | texto | | Nome do estilo |
| `volume_litros` | decimal | litros | Volume produzido |
| `variacao_pct` | decimal | % | Variação em relação a 2023; vazia na Cerveja Gruit, sem valor no Anuário |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |

**Cuidado:** ao contrário da edição de 2026, inclui todos os estilos e soma o total nacional. As categorias não são diretamente comparáveis com `tabela_21_estilos_2025.csv`.

### caracteristicas_2024.csv

Volume por característica da cerveja. Uma linha por característica (11 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `caracteristica` | texto | | Característica declarada |
| `volume_litros` | decimal | litros | Volume produzido com essa característica |
| `variacao_absoluta_litros` | decimal | litros | Diferença em relação a 2023 |
| `variacao_pct` | decimal | % | Variação em relação a 2023 |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |

### abrangencia_2024.csv

Volume segundo a abrangência de comercialização. Uma linha por faixa (5 linhas). Mesmas colunas e nomes de faixa de `tabela_23_abrangencia_2025.csv`.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `abrangencia` | texto | | Faixa de abrangência |
| `volume_litros` | decimal | litros | Volume produzido |
| `pct_volume` | decimal | % | Participação no volume nacional |
| `variacao_pct` | decimal | % | Variação em relação a 2023 |
| `ano_referencia` | inteiro | | 2024 |
| `fonte` | texto | | Tabela e página de origem |

---

## Comex Stat (MDIC)

Consultas feitas em 09/10/2026 no site do Comex Stat. Os arquivos brutos estão em `data/raw`. O Comex Stat revisa dados passados todo mês, então um download futuro pode diferir ligeiramente.

### comex_insumos_mensal_2015_2025.csv

Importação e exportação mensais de malte (SH4 1107) e lúpulo (SH4 1210). Uma linha por mês, fluxo e produto; meses sem movimento não aparecem.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `data` | data | | Primeiro dia do mês (AAAA-MM-01) |
| `ano` | inteiro | | Ano |
| `mes` | inteiro | | Mês, de 1 a 12 |
| `fluxo` | texto | | `importacao` ou `exportacao` |
| `sh4` | texto | | Código SH4: `1107` (malte) ou `1210` (lúpulo) |
| `descricao` | texto | | Descrição oficial do código |
| `valor_fob_usd` | inteiro | US$ FOB | Valor da mercadoria no porto de embarque |
| `kg_liquido` | inteiro | kg | Peso líquido |
| `fonte` | texto | | Fonte e data da consulta |

**Cuidado:** a exportação de malte e lúpulo é pequena e tem meses sem registro. Para séries contínuas, preencher os meses ausentes com zero.

### comex_cerveja_mensal_2015_2025.csv

Importação e exportação mensais de cerveja. Uma linha por mês, fluxo e NCM.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `data` | data | | Primeiro dia do mês (AAAA-MM-01) |
| `ano` | inteiro | | Ano |
| `mes` | inteiro | | Mês, de 1 a 12 |
| `fluxo` | texto | | `importacao` ou `exportacao` |
| `ncm` | texto | | `22030000` (cervejas de malte) ou `22029100` (cerveja sem álcool) |
| `descricao` | texto | | Descrição oficial do código |
| `valor_fob_usd` | inteiro | US$ FOB | Valor da mercadoria no porto de embarque |
| `kg_liquido` | inteiro | kg | Peso líquido declarado; **não usar** para cerveja |
| `litros` | inteiro | litros | Quantidade estatística, a medida usada para cerveja |
| `fonte` | texto | | Fonte e data da consulta |

**Cuidados:**

- O Anuário define cerveja como a **soma dos dois NCM**. Para reproduzir os números dele, somar as linhas dos dois códigos.
- O NCM 22029100 só existe desde 2017. Em 2015 e 2016 a série tem só o 22030000, então há uma quebra pequena em 2017.
- O kg líquido declarado é inconsistente com o volume em litros na exportação.

---

## Novo CAGED (MTE)

### caged_cerveja_mensal_2020_2025.csv

Movimentações de empregos formais na subclasse CNAE 1113-5/02 (fabricação de cervejas e chopes), por UF e mês. Obtido dos microdados via Base dos Dados (BigQuery) em 13/10/2026; a consulta está em `src/consulta_caged.sql`. Uma linha por mês e UF; combinações sem movimento não aparecem.

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `ano` | inteiro | | Ano |
| `mes` | inteiro | | Mês, de 1 a 12 |
| `uf` | texto | | Sigla da UF |
| `admissoes` | inteiro | empregos | Contratações no mês |
| `desligamentos` | inteiro | empregos | Demissões e outros desligamentos no mês |
| `saldo` | inteiro | empregos | Admissões − desligamentos |
| `data` | data | | Primeiro dia do mês (AAAA-MM-01) |
| `fonte` | texto | | Fonte e local da consulta |

**Cuidado:** o CAGED mede **fluxo** (movimentações no mês), não estoque. Para comparar com o estoque da Tabela 16, somar o saldo do ano.

---

## Arquivos calculados

### reconciliacao_variacoes_2024.csv

Volume de 2024 implícito em cada variação do Anuário 2026, comparado com o publicado no Anuário 2025. Gerado no notebook `02_qualidade_dos_dados.ipynb`. Uma linha por categoria (12 linhas).

| Coluna | Tipo | Unidade | Descrição |
| --- | --- | --- | --- |
| `tabela` | texto | | Tabela do Anuário 2026 de origem |
| `categoria` | texto | | Região, tipo de cerveja ou faixa de abrangência |
| `volume_litros_2025` | decimal | litros | Volume de 2025 (Anuário 2026) |
| `variacao_pct` | decimal | % | Variação 2024→2025 publicada no Anuário 2026 |
| `volume_litros_2024_publicado` | decimal | litros | Volume de 2024 publicado no Anuário 2025 |
| `volume_2024_implicito` | decimal | litros | Volume de 2025 ÷ (1 + variação/100) |
| `dif_pct_vs_publicado` | decimal | % | Diferença entre o implícito e o publicado; perto de zero indica que a variação usou a base original |

---

## Documentação

### registro_inconsistencias.csv

Fica em `docs`. Lista os problemas encontrados nas fontes, com a evidência e a decisão tomada. Colunas: `id`, `fonte`, `local`, `problema`, `evidencia`, `impacto` (alto, médio ou baixo) e `decisao`.
