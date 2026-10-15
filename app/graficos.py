"""Gráficos do dashboard. Cada função recebe os dados prontos e devolve uma figura do matplotlib."""

import matplotlib.pyplot as plt

from estilo import COR_FUNDO, COR_GRADE, COR_QUEDA, COR_SEGUNDA, COR_SERIE, COR_TEXTO, COR_TEXTO_2, formatar


def grafico_lorenz(lorenz):
    fig, (ax_geral, ax_zoom) = plt.subplots(1, 2, figsize=(9, 4))

    for ax in (ax_geral, ax_zoom):
        ax.plot([0, 100], [0, 100], color=COR_TEXTO_2, linewidth=1, linestyle="--")
        ax.plot(
            lorenz["pop_acumulada"] * 100, lorenz["volume_acumulado"] * 100,
            color=COR_SERIE, linewidth=2, marker="o", markersize=6,
            markeredgecolor=COR_FUNDO, markeredgewidth=1.5,
        )
        ax.set_ylim(0, 100)
        ax.set_xlabel("Cervejarias, das menores\npara as maiores (% acumulado)")

    ax_geral.set_xlim(0, 100)
    ax_geral.set_ylabel("Volume produzido (% acumulado)")
    ax_geral.set_title("Curva completa", loc="left", color=COR_TEXTO, fontsize=11)
    ax_geral.text(50, 56, "Igualdade perfeita", color=COR_TEXTO_2, rotation=40, fontsize=9)
    ax_geral.axvspan(90, 100, color=COR_SERIE, alpha=0.08, linewidth=0)

    ax_zoom.set_xlim(90, 100)
    ax_zoom.set_title("Detalhe: as 10% maiores", loc="left", color=COR_TEXTO, fontsize=11)
    ax_zoom.annotate(
        "99% menores: 57,5%\n1% maiores: 42,5%", xy=(99, 57.51), xytext=(91, 72),
        color=COR_TEXTO, fontsize=9, arrowprops=dict(arrowstyle="-", color=COR_TEXTO_2, linewidth=0.8),
    )
    ax_zoom.annotate(
        "90% menores: 0,5%", xy=(90, 0.5), xytext=(90.6, 22),
        color=COR_TEXTO, fontsize=9, arrowprops=dict(arrowstyle="-", color=COR_TEXTO_2, linewidth=0.8),
    )
    fig.tight_layout()
    return fig


def grafico_comparacao(comparacao):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    posicoes = range(len(comparacao))

    ax.hlines(
        posicoes, comparacao["min_2024_retificado"], comparacao["max_2024_retificado"],
        color=COR_SEGUNDA, alpha=0.25, linewidth=9, label="2024, faixa possível com a revisão",
    )
    ax.scatter(
        comparacao["pct_volume_2024"], posicoes, color=COR_SEGUNDA, s=60,
        edgecolor=COR_FUNDO, linewidth=1.5, zorder=3, label="2024, como publicado",
    )
    ax.scatter(
        comparacao["pct_volume_2025"], posicoes, color=COR_SERIE, s=60,
        edgecolor=COR_FUNDO, linewidth=1.5, zorder=4, label="2025",
    )
    ax.set_yticks(list(posicoes), [f"{p:.0f}% maiores" for p in comparacao["pct_cervejarias"]])
    ax.invert_yaxis()
    ax.set_xlim(40, 102)
    ax.set_xlabel("Participação no volume nacional (%)")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=8)
    fig.tight_layout()
    return fig


def grafico_regioes(regioes):
    regioes = regioes.sort_values("producao_media_litros", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    posicoes = range(len(regioes))

    ax.hlines(posicoes, regioes["pct_cervejarias"], regioes["pct_volume"], color=COR_GRADE, linewidth=3, zorder=1)
    ax.scatter(
        regioes["pct_cervejarias"], posicoes, color=COR_SEGUNDA, s=70,
        edgecolor=COR_FUNDO, linewidth=1.5, zorder=3, label="% das cervejarias",
    )
    ax.scatter(
        regioes["pct_volume"], posicoes, color=COR_SERIE, s=70,
        edgecolor=COR_FUNDO, linewidth=1.5, zorder=3, label="% do volume produzido",
    )
    for posicao, media in zip(posicoes, regioes["producao_media_litros"]):
        ax.text(63, posicao, f"{formatar(media / 1e6, 1)} mi L", va="center", fontsize=9, color=COR_TEXTO)
    ax.text(63, -0.6, "Produção média\npor cervejaria", fontsize=8, color=COR_TEXTO_2, va="bottom")

    ax.set_yticks(list(posicoes), regioes.index)
    ax.set_ylim(len(regioes) - 0.5, -0.5)
    ax.set_xlim(0, 60)
    ax.set_xlabel("Participação no total nacional (%)")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=9)
    fig.tight_layout()
    fig.subplots_adjust(right=0.82)
    return fig


def grafico_segmentos(segmentos):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    posicoes = range(len(segmentos))
    valores = segmentos["variacao_participacao_pct"]
    cores = [COR_SERIE if valor > 0 else COR_QUEDA for valor in valores]

    ax.barh(list(posicoes), valores, color=cores, height=0.6)
    ax.axvline(0, color=COR_TEXTO_2, linewidth=0.8)
    for posicao, valor in zip(posicoes, valores):
        deslocamento = 8 if valor > 0 else -8
        alinhamento = "left" if valor > 0 else "right"
        texto = f"{'+' if valor > 0 else '−'}{formatar(abs(valor))}%"
        ax.text(valor + deslocamento, posicao, texto, va="center", ha=alinhamento, fontsize=9, color=COR_TEXTO)

    ax.set_yticks(list(posicoes), segmentos["segmento"])
    ax.set_ylim(len(segmentos) - 0.5, -0.5)
    ax.set_xlim(-140, 480)
    ax.set_xlabel("Variação da participação no volume total, 2024 → 2025 (%)")
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return fig


def grafico_insumo(serie, produto):
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(serie.index, serie[produto], color=COR_SERIE, alpha=0.3, linewidth=1, label="Mensal")
    ax.plot(serie.index, serie[f"{produto}_mm12"], color=COR_SERIE, linewidth=2, label="Média móvel de 12 meses")
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Importação (toneladas)")
    ax.yaxis.set_major_formatter(lambda valor, _: formatar(valor))
    ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=2)
    fig.tight_layout()
    return fig


def grafico_emprego(indice_mensal, indices):
    import pandas as pd

    fig, ax = plt.subplots(figsize=(8, 3.8))
    meio_do_ano = pd.to_datetime([f"{ano}-07-01" for ano in [2023, 2024, 2025]])

    ax.plot(indice_mensal.index, indice_mensal, color=COR_SERIE, linewidth=2, label="Emprego formal (mensal)")
    ax.vlines(
        meio_do_ano[1], indices.loc[2024, "producao_original"], indices.loc[2024, "producao_retificada"],
        color=COR_SEGUNDA, alpha=0.35, linewidth=6, label="Produção 2024: base original à revisada",
    )
    ax.scatter(
        meio_do_ano, indices.loc[2023:2025, "producao_retificada"], color=COR_SEGUNDA, s=50,
        edgecolor=COR_FUNDO, linewidth=1.5, zorder=3, label="Produção anual (2024 revisada)",
    )
    ax.scatter(
        [meio_do_ano[1]], [indices.loc[2024, "producao_original"]], color=COR_FUNDO, edgecolor=COR_SEGUNDA,
        linewidth=1.5, s=50, zorder=3, label="Produção 2024 (base original)",
    )
    ax.axhline(100, color=COR_TEXTO_2, linewidth=0.8, linestyle=":")
    ax.set_ylabel("Índice (média de 2023 = 100)")
    ax.legend(loc="upper left", frameon=False, fontsize=8, ncol=2)
    fig.tight_layout()
    return fig


def grafico_importacao(anual):
    fig, ax = plt.subplots(figsize=(8, 3.6))
    anos = anual.index
    ax.plot(anos, anual["litros"] / 1e6, color=COR_QUEDA, linewidth=1.5, linestyle="--", marker="o", markersize=5,
            label="Como publicado")
    ax.plot(anos, anual["litros_corrigido"] / 1e6, color=COR_SERIE, linewidth=2, marker="o", markersize=5,
            label="Corrigido (litros/kg entre 0,5 e 2)")
    ax.annotate(
        "Um único registro:\n19,4 milhões de L\ndeclarados para 21 t", xy=(2025, anual.loc[2025, "litros"] / 1e6),
        xytext=(2019.6, 40), color=COR_TEXTO, fontsize=9,
        arrowprops=dict(arrowstyle="-", color=COR_TEXTO_2, linewidth=0.8),
    )
    ax.set_xticks(list(anos))
    ax.tick_params(axis="x", labelsize=8)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Importação de cerveja (milhões de L)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    fig.tight_layout()
    return fig
