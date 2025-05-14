import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Adiciona o caminho da pasta pai (../) ao sys.path para permitir importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gemini.gemini_chat import analisar_como_inspetor

infoProdutos = "./database/Produtos.csv"

st.set_page_config(page_title="formulario", layout="centered")
st.title("Validação de Doações de Alimentos")

with st.sidebar:
    "[![Open in GitHub](https://github.com/codespaces/badge.svg)](https://github.com/Felipebc2/Hackathon-1.25)"
    st.image("frontend/shareBiteLogo.png", caption=" ", use_container_width=True)

st.markdown("""
    Esse formulário foi feito com o intuito de validar alimentos excedidos para doações conforme as regulações da ANVISA,
    mas não substitui de maneira nenhuma qualquer inspeção formal governamental.

""")

with st.form("formViabilidadeDoacao"):
    tipo_alimento = st.selectbox("Tipo do alimento", ["Quente", "Resfriada", "Congelada"])
    temperatura_atual = st.number_input("Temperatura atual do alimento (°C)", step=1)
    tempo_preparo = st.number_input("Tempo desde o preparo", min_value=0, step=1)
    unidade_tempo = st.selectbox("Unidade de tempo", ["horas", "dias"])
    prazo_validade = st.checkbox("Está dentro do prazo de validade?")
    temperatura_adequada = st.checkbox("Temperatura adequada para conservação?")
    embalagem_integra = st.checkbox("A embalagem está íntegra ou com danos seguros?")
    alimento_integro = st.checkbox("O alimento está visualmente íntegro?")
    sem_contaminacao = st.checkbox("Não está contaminado ou estragado?")
    nutricional_preservada = st.checkbox("As propriedades nutricionais estão preservadas?")
    preparo_armazenado_apto = st.checkbox("Foi preparado e armazenado em menos de 6h após confeccionado?")
    eh_para_lactentes = st.checkbox("Este alimento é destinado a lactentes?")

    enviar = st.form_submit_button("Enviar")

if enviar:
    tipo_api = tipo_alimento.lower()
    if tipo_api == "quente":
        tipo_api = "refeicao_pronta"

    dias = round(tempo_preparo / 24, 2) if unidade_tempo == "horas" else tempo_preparo

    payload = {
        "tipo_alimento": tipo_alimento,
        "temperatura_atual": temperatura_atual,
        "tempo_preparo": dias,
        "unidade_tempo": unidade_tempo,
        "prazo_validade": prazo_validade,
        "temperatura_adequada": temperatura_adequada,
        "embalagem_integra": embalagem_integra,
        "alimento_integro": alimento_integro,
        "sem_contaminacao": sem_contaminacao,
        "nutricional_preservada": nutricional_preservada,
        "preparo_armazenado_apto": preparo_armazenado_apto,
        "eh_para_lactentes": eh_para_lactentes,
    }

    print("Payload enviado:", payload)

    try:
        res = requests.post("http://localhost:5000/validate", json=payload)
        if res.status_code == 200:
            resultado = res.json()
            st.markdown("---")
            st.subheader("Resultado da Validação por Regras Fixas")
            if resultado["valid"]:
                st.markdown(
                    "<div style='padding:1rem; background-color:#d4edda; color:#155724; font-size:24px; border-radius:5px;'>Apto para Doação</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div style='padding:1rem; background-color:#f8d7da; color:#721c24; font-size:24px; border-radius:5px;'>Não Apto para Doação</div>",
                    unsafe_allow_html=True
                )
            st.markdown("**Justificativas Técnicas (Regras Fixas):**")
            for msg in resultado["messages"]:
                st.markdown(f"- {msg}")
        else:
            st.error(f"Erro {res.status_code}: {res.text}")
            st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Erro: Não foi possível se conectar ao servidor Flask.")
        st.stop()

    st.markdown("---")
    st.subheader("Parecer Técnico da IA (Inspetor ANVISA)")
    with st.spinner("Consultando parecer da IA..."):
        resposta = analisar_como_inspetor(payload)
        placeholder = st.empty()
        parcial = ""
        for c in resposta:
            parcial += c
            placeholder.markdown(parcial + "▌")
            time.sleep(0.01)
        placeholder.markdown(parcial)
