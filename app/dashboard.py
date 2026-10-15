import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

st.set_page_config(page_title="Mercado cervejeiro brasileiro", page_icon="🍺", layout="centered")

paginas = [
    st.Page("paginas/visao_geral.py", title="Visão geral", default=True),
    st.Page("paginas/concentracao.py", title="Concentração"),
    st.Page("paginas/tendencias.py", title="Tendências"),
]
st.navigation(paginas).run()
