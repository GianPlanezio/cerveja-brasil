import streamlit as st

from dados import concentracao, tabela_regioes
from estilo import aplicar_estilo, formatar, mostrar
from graficos import grafico_comparacao, grafico_lorenz, grafico_regioes

aplicar_estilo()

st.title("Concentração da produção")
st.caption("Fontes: Anuários da Cerveja 2025 e 2026 (MAPA), tabelas 18 e 19.")

dados = concentracao()
comparacao = dados["comparacao"]
fatia_1pct = comparacao.loc[comparacao["pct_cervejarias"] == 1].iloc[0]

coluna_1, coluna_2, coluna_3 = st.columns(3)
coluna_1.metric(
    "Índice de Gini (2025)",
    f"≥ {formatar(dados['gini_2025'], 2)}",
    help="De 0 (todas produzem igual) a 1 (uma só produz tudo). Calculado com seis pontos da curva, "
         "por isso é um limite inferior: a concentração real é igual ou maior.",
)
coluna_2.metric(
    "Volume do 1% maior",
    f"{formatar(fatia_1pct['pct_volume_2025'], 1)}%",
    delta=f"{formatar(fatia_1pct['pct_volume_2025'] - fatia_1pct['pct_volume_2024'], 1)} p.p. sobre 2024",
    delta_color="off",
    help="Comparação com o valor publicado para 2024. Com a revisão do total de 2024, a queda vai "
         "de praticamente zero a 10,9 pontos, mas a fatia caiu em qualquer cenário.",
)
coluna_3.metric("Volume das 90% menores", "0,5%")

aba_lorenz, aba_anos, aba_regioes = st.tabs(["Curva de Lorenz", "2024 × 2025", "Regiões"])

with aba_lorenz:
    mostrar(grafico_lorenz(dados["lorenz_2025"]))
    st.markdown(
        "A curva mostra quanto do volume as cervejarias produzem, acumulando das menores para as maiores. "
        "Quanto mais longe da diagonal, maior a concentração. Toda a concentração acontece nas 10% maiores: "
        "as outras 90% produzem, juntas, só 0,5% do volume."
    )

with aba_anos:
    mostrar(grafico_comparacao(comparacao))
    st.markdown(
        f"Com os mesmos pontos (1% a 5%), o Gini passou de **{formatar(dados['gini_2024'], 3)}** em 2024 "
        f"para **{formatar(dados['gini_2025_comparavel'], 3)}** em 2025. "
        "O 1% maior perdeu participação em qualquer cenário da revisão do total de 2024; "
        "para as fatias de 2% a 5%, a direção não pode ser determinada. **A concentração não aumentou.**"
    )

with aba_regioes:
    mostrar(grafico_regioes(tabela_regioes()))
    st.markdown(
        "Quando o ponto azul fica à direita do laranja, a região produz mais do que o número de cervejarias sugere: "
        "poucas fábricas grandes, como no Nordeste. À esquerda, muitas cervejarias pequenas, como no Sul."
    )
