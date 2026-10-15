import streamlit as st

from dados import emprego, importacao_cerveja, insumos, segmentos
from estilo import aplicar_estilo, formatar, mostrar
from graficos import grafico_emprego, grafico_importacao, grafico_insumo, grafico_segmentos

aplicar_estilo()

st.title("Tendências de consumo")
st.caption("Fontes: Anuários da Cerveja 2025 e 2026 (MAPA), Comex Stat (MDIC) e Novo CAGED (MTE).")

tabela_segmentos = segmentos().set_index("segmento")
serie_insumos, anual_insumos = insumos()
dados_emprego = emprego()
anual_importacao, registros_corrigidos = importacao_cerveja()

puro_malte = tabela_segmentos.loc["Puro malte"]
sem_gluten = tabela_segmentos.loc["Sem glúten"]
malte_2025 = anual_insumos[(anual_insumos["produto"] == "malte") & (anual_insumos["ano"] == 2025)].iloc[0]
estoque_dezembro = dados_emprego["estoque_dezembro"]


def pontos(depois, antes):
    diferenca = depois - antes
    return f"{'+' if diferenca >= 0 else '−'}{formatar(abs(diferenca), 1)} p.p."


coluna_1, coluna_2, coluna_3, coluna_4 = st.columns(4)
coluna_1.metric(
    "Puro malte",
    f"{formatar(puro_malte['pct_total_2025'], 1)}%",
    delta=pontos(puro_malte["pct_total_2025"], puro_malte["pct_total_2024"]),
    delta_color="off",
    help="Participação no volume total produzido, 2025 contra 2024.",
)
coluna_2.metric(
    "Sem glúten",
    f"{formatar(sem_gluten['pct_total_2025'], 2)}%",
    delta=pontos(sem_gluten["pct_total_2025"], sem_gluten["pct_total_2024"]),
    delta_color="off",
    help="Participação no volume total produzido, 2025 contra 2024.",
)
coluna_3.metric(
    "Malte importado",
    f"{formatar(malte_2025['toneladas'] / 1e6, 2)} mi t",
    delta=f"{formatar(malte_2025['variacao_pct'], 1)}%",
    delta_color="off",
    help="Importação de malte em 2025 e variação sobre 2024.",
)
coluna_4.metric(
    "Emprego formal",
    formatar(estoque_dezembro[2025]),
    delta=f"{formatar((estoque_dezembro[2025] / estoque_dezembro[2024] - 1) * 100, 1)}%",
    delta_color="off",
    help="Empregos na fabricação de cervejas e chopes em dezembro de 2025, e variação sobre dezembro de 2024.",
)

aba_segmentos, aba_insumos, aba_emprego, aba_importacao = st.tabs(
    ["Segmentos", "Malte e lúpulo", "Emprego", "Importação de cerveja"]
)

with aba_segmentos:
    mostrar(grafico_segmentos(tabela_segmentos.reset_index()))
    st.markdown(
        "Variação da **participação** de cada segmento no volume total, que mede quanto ele cresceu além do mercado. "
        "O **puro malte** passou de 24,7% para 29,2% do volume, e o **sem glúten** quintuplicou. "
        "A cerveja **sem álcool** oscila de forma implausível entre os anos (0,8%, 4,9% e 1,3%), "
        "o que sugere mudança na forma de declarar, e não é tratada como tendência."
    )

with aba_insumos:
    escolha = st.radio("Insumo", ["Malte", "Lúpulo"], horizontal=True)
    produto = "malte" if escolha == "Malte" else "lupulo"
    mostrar(grafico_insumo(serie_insumos, produto))

    tabela = anual_insumos[anual_insumos["produto"] == produto].set_index("ano")
    tabela = tabela[["toneladas", "variacao_pct", "usd_por_kg"]].rename(
        columns={"toneladas": "Toneladas", "variacao_pct": "Variação (%)", "usd_por_kg": "US$ por kg"}
    )
    st.dataframe(tabela.round(2).sort_index(ascending=False), width="stretch")
    st.markdown(
        "A importação de malte **não acompanhou o puro malte**: caiu 12,5% em 2025, para o menor volume desde 2018, "
        "enquanto o puro malte ganhou participação. Parte do malte usado no Brasil é produzida no país."
    )

with aba_emprego:
    mostrar(grafico_emprego(dados_emprego["indice_mensal"], dados_emprego["indices"]))
    st.markdown(
        "O emprego tem trajetória própria: pico em dezembro de 2022, estabilidade em 2023 e 2024 e queda em 2025, "
        "nas cinco regiões. A produção de 2025 caiu 8,8% sobre o total revisado de 2024 e cresceu 2,2% sobre o original, "
        "então não é possível dizer qual das duas o emprego acompanha."
    )

with aba_importacao:
    mostrar(grafico_importacao(anual_importacao))
    variacao_publicada = (anual_importacao.loc[2025, "litros"] / anual_importacao.loc[2024, "litros"] - 1) * 100
    variacao_corrigida = (anual_importacao.loc[2025, "litros_corrigido"] / anual_importacao.loc[2024, "litros_corrigido"] - 1) * 100
    st.markdown(
        f"Como publicada, a importação de cerveja cresceu **{formatar(variacao_publicada)}%** em 2025. "
        "O salto vem de uma única declaração de cerveja sem álcool importada dos EUA em dezembro de 2025. "
        f"Corrigidos os {registros_corrigidos} registros com quantidade incoerente com o peso, "
        f"a variação é de **{formatar(variacao_corrigida, 1)}%**."
    )
