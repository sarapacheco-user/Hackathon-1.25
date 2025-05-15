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

# Paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
infoProdutos = "./database/Produtos.csv"

st.set_page_config(page_title="dashboard", layout="centered")
st.title("Statistic Analysis")

with st.sidebar:
    st.markdown(
        '[![Open in GitHub](https://github.com/codespaces/badge.svg)](https://github.com/sarapacheco-user/Hackathon-1.25)',
        unsafe_allow_html=True
    )
    st.image("frontend/shareBiteLogo.png", caption=" ", use_container_width=True)

try:
    df = pd.read_csv(infoProdutos)

    if 'produto' in df.columns and 'quantidade' in df.columns:
        st.subheader("Amount of Exceded Product")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['produto'], df['quantidade'], color='skyblue')
        ax.set_title("Amount of Product")
        ax.set_xlabel("Product")
        ax.set_ylabel("Amount")
        ax.set_xticklabels(df['produto'], rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Rows 'produto' and/or 'quantidade' not found")

    if 'valido' in df.columns:
        st.subheader("Donation Status")
        contagem = df['valido'].value_counts()
        contagem.index = contagem.index.map({True: "Donated", False: "Not donated"})

        fig2, ax2 = plt.subplots()
        contagem.plot(kind='bar', color=['green', 'red'], ax=ax2)
        ax2.set_title("Donations made")
        ax2.set_xticklabels(contagem.index, rotation=0)
        st.pyplot(fig2)
    else:
        st.warning("Row 'valido'not found.")

except FileNotFoundError:
    st.error("Product file was not found")
