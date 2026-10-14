"""Funções de cálculo usadas nos notebooks e no dashboard do projeto."""

import pandas as pd


def pontos_lorenz(pct_maiores, pct_volume):
    """Converte pontos de concentração em pontos da curva de Lorenz.

    O Anuário informa quanto as MAIORES cervejarias produzem: "os 1% maiores
    produzem 42,49% do volume". A curva de Lorenz parte das MENORES: "os 99%
    menores produzem 57,51%". A conversão é feita trocando cada fatia pelo
    seu complemento.

    Parâmetros
    ----------
    pct_maiores : lista de porcentagens das maiores cervejarias (de 0 a 100)
    pct_volume  : lista de porcentagens do volume produzido por elas (de 0 a 100)

    Retorna
    -------
    DataFrame com as colunas `pop_acumulada` e `volume_acumulado`, ambas de 0 a 1,
    ordenado do ponto (0, 0) ao ponto (1, 1).
    """
    pontos = [(0.0, 0.0), (1.0, 1.0)]
    for p, v in zip(pct_maiores, pct_volume):
        pontos.append((1 - p / 100, 1 - v / 100))

    curva = pd.DataFrame(pontos, columns=["pop_acumulada", "volume_acumulado"])
    return curva.sort_values("pop_acumulada").reset_index(drop=True)


def gini_trapezios(pop_acumulada, volume_acumulado):
    """Índice de Gini a partir de pontos da curva de Lorenz, pela regra dos trapézios.

    Gini = 1 - 2 × (área sob a curva de Lorenz). A área é aproximada por
    trapézios entre pontos vizinhos.

    Com poucos pontos, o resultado é um LIMITE INFERIOR: a curva real é
    convexa e fica abaixo das retas que ligam os pontos, então a área real
    é menor e o Gini real é maior.
    """
    x = list(pop_acumulada)
    y = list(volume_acumulado)

    area = 0.0
    for i in range(len(x) - 1):
        largura = x[i + 1] - x[i]
        altura_media = (y[i] + y[i + 1]) / 2
        area += largura * altura_media

    return 1 - 2 * area


def variacao_pct(atual, anterior):
    """Variação percentual entre dois valores: (atual / anterior - 1) × 100."""
    return (atual / anterior - 1) * 100