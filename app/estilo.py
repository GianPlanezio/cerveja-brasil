"""Cores, estilo dos gráficos e formatação de números, iguais aos dos notebooks."""

import matplotlib.pyplot as plt

COR_SERIE = "#2a78d6"
COR_SEGUNDA = "#eb6834"
COR_QUEDA = "#e34948"
COR_NEUTRA = "#b9b8b1"
COR_TEXTO = "#0b0b0b"
COR_TEXTO_2 = "#52514e"
COR_GRADE = "#e4e3df"
COR_FUNDO = "#fcfcfb"


def aplicar_estilo():
    plt.rcParams.update({
        "figure.facecolor": COR_FUNDO,
        "axes.facecolor": COR_FUNDO,
        "axes.edgecolor": COR_GRADE,
        "axes.labelcolor": COR_TEXTO_2,
        "xtick.color": COR_TEXTO_2,
        "ytick.color": COR_TEXTO_2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": COR_GRADE,
        "grid.linewidth": 0.8,
        "font.size": 10,
    })


def formatar(numero, casas=0):
    """Formata um número no padrão brasileiro: 15688083191.69 -> '15.688.083.191,69'."""
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar(fig):
    """Exibe uma figura do matplotlib no Streamlit e libera a memória dela."""
    import streamlit as st

    st.pyplot(fig)
    plt.close(fig)
