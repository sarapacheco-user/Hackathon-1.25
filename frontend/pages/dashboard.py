import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from gemini.gemini_chat import analisar_como_inspetor
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Caminhos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
infoProdutos = "./database/Produtos.csv"

st.set_page_config(page_title="dashboard", layout="centered")
st.title("Análise Estatística")

st.markdown("""
    Abaixo estão gráficos e estatísticas dos alimentos do banco de dados.

""")

with st.sidebar:
    st.markdown(
        '[![Open in GitHub](https://github.com/codespaces/badge.svg)](https://github.com/Felipebc2/Hackathon-1.25)',
        unsafe_allow_html=True
    )
    st.image("frontend/shareBiteLogo.png", caption=" ", use_container_width=True)
    

st.header("Dashboard para visualização de estatísticas")

try:
    df = pd.read_csv(infoProdutos)

    if 'produto' in df.columns and 'quantidade' in df.columns:
        st.subheader("Quantidade Produto Excedido")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['produto'], df['quantidade'], color='skyblue')
        ax.set_title("Quantidade por Produto")
        ax.set_xlabel("Produto")
        ax.set_ylabel("Quantidade")
        ax.set_xticklabels(df['produto'], rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Colunas 'produto' e/ou 'quantidade' não encontradas.")

    if 'valido' in df.columns:
        st.subheader("Status das Doações")
        contagem = df['valido'].value_counts()
        contagem.index = contagem.index.map({True: "Foi doado", False: "Não foi doado"})

        fig2, ax2 = plt.subplots()
        contagem.plot(kind='bar', color=['green', 'red'], ax=ax2)
        ax2.set_title("Doações Realizadas")
        ax2.set_xticklabels(contagem.index, rotation=0)
        st.pyplot(fig2)
    else:
        st.warning("Coluna 'valido' não encontrada.")

except FileNotFoundError:
    st.error("Arquivo de produtos não encontrado.")