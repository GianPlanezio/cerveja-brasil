"""Leitura dos dados do dashboard. Cada função lê os CSVs de data/processed uma vez e guarda o resultado em cache."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.metricas import gini_trapezios, pontos_lorenz, variacao_pct

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DADOS = RAIZ / "data" / "processed"

TOTAL_2025 = 15_688_083_191.69
TOTAL_2024_ORIGINAL = 15_344_065_267.36
TOTAL_2024_RETIFICADO = 17_210_754_610.75


@st.cache_data
def ler(nome_arquivo):
    return pd.read_csv(PASTA_DADOS / nome_arquivo)


@st.cache_data
def tabela_regioes():
    """Volume, cervejarias, produção média e empregos por região, em 2025."""
    t18 = ler("tabela_18_producao_media_regiao_2025.csv")
    t16 = ler("tabela_16_empregos_uf_2025.csv")
    uf_regiao = ler("grafico_02_cervejarias_uf_2025.csv")[["uf", "regiao"]]

    empregos = t16.merge(uf_regiao, on="uf").groupby("regiao")["estoque_empregos"].sum()
    regioes = t18.set_index("regiao")[["volume_litros", "n_cervejarias", "producao_media_litros"]].join(empregos)
    regioes["pct_volume"] = regioes["volume_litros"] / regioes["volume_litros"].sum() * 100
    regioes["pct_cervejarias"] = regioes["n_cervejarias"] / regioes["n_cervejarias"].sum() * 100
    return regioes.sort_values("volume_litros", ascending=False)


@st.cache_data
def tabela_ufs():
    """Cervejarias e empregos por UF, em 2025."""
    cervejarias = ler("grafico_02_cervejarias_uf_2025.csv")[["uf", "regiao", "n_cervejarias"]]
    empregos = ler("tabela_16_empregos_uf_2025.csv")[["uf", "estoque_empregos"]]
    return cervejarias.merge(empregos, on="uf")


@st.cache_data
def concentracao():
    """Curva de Lorenz, índices de Gini e comparação 2024 × 2025 (mesmas contas do notebook 03)."""
    conc_2025 = ler("tabela_19_concentracao_2025.csv")
    conc_2024 = ler("concentracao_2024.csv")
    conc_2025_comparavel = conc_2025[conc_2025["pct_cervejarias"] <= 5]

    lorenz_2025 = pontos_lorenz(conc_2025["pct_cervejarias"], conc_2025["pct_volume"])
    lorenz_2024 = pontos_lorenz(conc_2024["pct_cervejarias"], conc_2024["pct_volume"])
    lorenz_2025_comparavel = pontos_lorenz(conc_2025_comparavel["pct_cervejarias"], conc_2025_comparavel["pct_volume"])

    comparacao = conc_2024[["pct_cervejarias", "volume_litros", "pct_volume"]].merge(
        conc_2025_comparavel[["pct_cervejarias", "pct_volume"]],
        on="pct_cervejarias",
        suffixes=("_2024", "_2025"),
    )
    comparacao["min_2024_retificado"] = comparacao["volume_litros"] / TOTAL_2024_RETIFICADO * 100
    comparacao["max_2024_retificado"] = (
        (comparacao["volume_litros"] + TOTAL_2024_RETIFICADO - TOTAL_2024_ORIGINAL) / TOTAL_2024_RETIFICADO * 100
    ).clip(upper=100)

    return {
        "lorenz_2025": lorenz_2025,
        "gini_2025": gini_trapezios(lorenz_2025["pop_acumulada"], lorenz_2025["volume_acumulado"]),
        "gini_2024": gini_trapezios(lorenz_2024["pop_acumulada"], lorenz_2024["volume_acumulado"]),
        "gini_2025_comparavel": gini_trapezios(
            lorenz_2025_comparavel["pop_acumulada"], lorenz_2025_comparavel["volume_acumulado"]
        ),
        "comparacao": comparacao,
    }


# ---------------------------------------------------------------------------
# Tendências (mesmas contas do notebook 04)
# ---------------------------------------------------------------------------

TOTAL_2023 = 15_361_344_122.77              # Anuário 2025, texto da p. 49
SEM_ALCOOL_2024 = 757_444_322.53            # Anuário 2025, texto da p. 53
SEM_ALCOOL_2025 = 199_693_125.83            # Anuário 2026, Gráfico 18 (rótulo "Lager" trocado)
LIMITE_LITROS_POR_KG = (0.5, 2.0)


def _volume_de(df, coluna, comeca_com):
    filtro = df[coluna].str.lower().str.startswith(comeca_com)
    return df.loc[filtro, "volume_litros"].iloc[0]


@st.cache_data
def segmentos():
    """Participação de cada segmento no volume total de 2024 e 2025."""
    malte_2025 = ler("tabela_20_puro_malte_2025.csv")
    malte_2024 = ler("puro_malte_2024.csv")
    carac_2025 = ler("tabela_22_caracteristicas_2025.csv")
    carac_2024 = ler("caracteristicas_2024.csv")

    linhas = [
        ("Puro malte", _volume_de(malte_2024, "categoria", "cerveja puro malte"), _volume_de(malte_2025, "categoria", "cerveja puro malte")),
        ("Sem álcool", SEM_ALCOOL_2024, SEM_ALCOOL_2025),
    ]
    for nome, chave in [
        ("Sem glúten", "sem glúten"),
        ("Com fruta", "com fruta"),
        ("Com ervas e especiarias", "com ervas"),
        ("Com mel", "com mel"),
        ("Com café", "com café"),
    ]:
        linhas.append((nome, _volume_de(carac_2024, "caracteristica", chave), _volume_de(carac_2025, "caracteristica", chave)))

    tabela = pd.DataFrame(linhas, columns=["segmento", "volume_2024", "volume_2025"])
    tabela["pct_total_2024"] = tabela["volume_2024"] / TOTAL_2024_ORIGINAL * 100
    tabela["pct_total_2025"] = tabela["volume_2025"] / TOTAL_2025 * 100
    tabela["variacao_participacao_pct"] = variacao_pct(tabela["pct_total_2025"], tabela["pct_total_2024"])
    return tabela.sort_values("variacao_participacao_pct", ascending=False).reset_index(drop=True)


@st.cache_data
def insumos():
    """Importação mensal de malte e lúpulo (toneladas, com média móvel de 12 meses) e totais anuais."""
    importacao = ler("comex_insumos_mensal_2015_2025.csv")
    importacao = importacao[importacao["fluxo"] == "importacao"].copy()
    importacao["data"] = pd.to_datetime(importacao["data"])
    importacao["produto"] = importacao["sh4"].astype(str).map({"1107": "malte", "1210": "lupulo"})

    serie = importacao.pivot_table(index="data", columns="produto", values="kg_liquido", aggfunc="sum")
    serie = serie.asfreq("MS", fill_value=0) / 1_000
    for produto in ["malte", "lupulo"]:
        serie[f"{produto}_mm12"] = serie[produto].rolling(12).mean()

    anual = importacao.groupby(["produto", "ano"])[["kg_liquido", "valor_fob_usd"]].sum().reset_index()
    anual["toneladas"] = anual["kg_liquido"] / 1_000
    anual["usd_por_kg"] = anual["valor_fob_usd"] / anual["kg_liquido"]
    anual["variacao_pct"] = anual.groupby("produto")["kg_liquido"].pct_change() * 100
    return serie, anual


@st.cache_data
def emprego():
    """Estoque mensal de empregos reconstruído a partir do CAGED e índices de emprego e produção (2023 = 100)."""
    caged = ler("caged_cerveja_mensal_2020_2025.csv")
    caged["data"] = pd.to_datetime(caged["data"])
    estoque_final = ler("tabela_16_empregos_uf_2025.csv")["estoque_empregos"].sum()

    saldo_mensal = caged.groupby("data")["saldo"].sum().asfreq("MS", fill_value=0)
    estoque = estoque_final - (saldo_mensal.sum() - saldo_mensal.cumsum())
    emprego_medio = estoque.groupby(estoque.index.year).mean()

    indices = pd.DataFrame({
        "emprego_medio": emprego_medio,
        "producao_original": pd.Series({2023: TOTAL_2023, 2024: TOTAL_2024_ORIGINAL, 2025: TOTAL_2025}),
        "producao_retificada": pd.Series({2023: TOTAL_2023, 2024: TOTAL_2024_RETIFICADO, 2025: TOTAL_2025}),
    })
    indices = indices / indices.loc[2023] * 100

    estoque_dezembro = estoque[estoque.index.month == 12]
    estoque_dezembro.index = estoque_dezembro.index.year

    return {
        "estoque": estoque,
        "indice_mensal": estoque / emprego_medio[2023] * 100,
        "indices": indices,
        "estoque_dezembro": estoque_dezembro,
    }


@st.cache_data
def importacao_cerveja():
    """Importação anual de cerveja em litros, como publicada e corrigida pela regra de litros por kg."""
    cerveja = ler("comex_cerveja_mensal_2015_2025.csv")
    importacao = cerveja[cerveja["fluxo"] == "importacao"].copy()

    litros_por_kg = importacao["litros"] / importacao["kg_liquido"]
    suspeito = ~litros_por_kg.between(*LIMITE_LITROS_POR_KG)
    importacao["litros_corrigido"] = importacao["litros"].where(~suspeito, importacao["kg_liquido"])

    anual = importacao.groupby("ano")[["valor_fob_usd", "litros", "litros_corrigido"]].sum()
    anual["usd_por_litro_corrigido"] = anual["valor_fob_usd"] / anual["litros_corrigido"]
    return anual, int(suspeito.sum())
