import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from gemini.gemini_chat import analisar_como_inspetor
import time
import os
import sys

# Caminhos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
infoProdutos = "./database/Produtos.csv"

# CONFIGURAÇÃO
st.set_page_config(page_title="Validação de Doações", layout="centered")
st.title("Validação de Doações de Alimentos")

# ========== FORMULÁRIO ==========
st.header("Formulário de Viabilidade para Doação")

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
        else:
            st.error(f"Erro {res.status_code}: {res.text}")
            st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Erro: Não foi possível se conectar ao servidor Flask.")
        st.stop()

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
