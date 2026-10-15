import matplotlib.pyplot as plt
import streamlit as st

from dados import tabela_regioes, tabela_ufs
from estilo import COR_NEUTRA, COR_SERIE, COR_TEXTO, aplicar_estilo, formatar, mostrar

aplicar_estilo()

st.title("Mercado cervejeiro brasileiro em 2025")
st.caption("Produção, cervejarias e empregos formais. Fontes: Anuário da Cerveja 2026 (MAPA) e Novo CAGED.")

regioes = tabela_regioes()
ufs = tabela_ufs()

escolha = st.selectbox("Região", ["Brasil"] + sorted(regioes.index))

if escolha == "Brasil":
    volume = regioes["volume_litros"].sum()
    cervejarias = regioes["n_cervejarias"].sum()
    empregos = regioes["estoque_empregos"].sum()
    ufs_escolhidas = ufs
else:
    volume = regioes.loc[escolha, "volume_litros"]
    cervejarias = regioes.loc[escolha, "n_cervejarias"]
    empregos = regioes.loc[escolha, "estoque_empregos"]
    ufs_escolhidas = ufs[ufs["regiao"] == escolha]

coluna_1, coluna_2, coluna_3, coluna_4 = st.columns(4)
coluna_1.metric("Produção", f"{formatar(volume / 1e9, 2)} bi L")
coluna_2.metric("Cervejarias registradas", formatar(cervejarias))
coluna_3.metric("Empregos formais", formatar(empregos))
coluna_4.metric(
    "Média por cervejaria",
    f"{formatar(volume / cervejarias / 1e6, 1)} mi L",
    help="Volume produzido dividido pelo número de cervejarias registradas.",
)

if escolha != "Brasil":
    pct_volume = volume / regioes["volume_litros"].sum() * 100
    pct_cervejarias = cervejarias / regioes["n_cervejarias"].sum() * 100
    st.markdown(
        f"O **{escolha}** tem **{formatar(pct_cervejarias, 1)}%** das cervejarias do país "
        f"e produz **{formatar(pct_volume, 1)}%** do volume."
    )

st.subheader("Produção por região")
fig, ax = plt.subplots(figsize=(8, 3.2))
cores = [COR_SERIE if escolha in ("Brasil", regiao) else COR_NEUTRA for regiao in regioes.index]
valores = regioes["volume_litros"] / 1e9
ax.barh(regioes.index, valores, color=cores, height=0.6)
for posicao, valor in enumerate(valores):
    ax.text(valor + 0.1, posicao, f"{formatar(valor, 2)} bi L", va="center", fontsize=9, color=COR_TEXTO)
ax.invert_yaxis()
ax.set_xlim(0, valores.max() * 1.18)
ax.set_xlabel("Volume em 2025 (bilhões de litros)")
ax.grid(axis="y", visible=False)
fig.tight_layout()
mostrar(fig)

st.subheader("Cervejarias e empregos por UF")
tabela = (
    ufs_escolhidas.sort_values("n_cervejarias", ascending=False)
    .rename(columns={"uf": "UF", "regiao": "Região", "n_cervejarias": "Cervejarias", "estoque_empregos": "Empregos"})
)
st.dataframe(tabela, hide_index=True, width="stretch")

st.caption(
    "Cervejarias: Anuário 2026, Gráfico 2. Empregos: estoque de 2025 na subclasse CNAE 1113-5/02 "
    "(fabricação de cervejas e chopes), Anuário 2026, Tabela 16."
)
