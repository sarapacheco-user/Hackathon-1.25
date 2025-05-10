import streamlit as st
import requests
from gemini.gemini_chat import analisar_como_inspetor
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(page_title="Validação de Doações", layout="centered")
st.title("Formulário de Viabilidade para Doação de Alimentos")

with st.form("formViabilidadeDoacao"):
    st.markdown("""
    ### Tipos de Alimentos

    **Comidas Quentes**
    Alimentos prontos mantidos **acima de 60°C** após o preparo.
    Exemplos: arroz, carnes cozidas, sopas, feijão.

    **Comidas Resfriadas**
    Conservadas entre **0°C e 5°C**.
    Exemplos: saladas, frios, sobremesas refrigeradas, marmitas.

    **Comidas Congeladas**
    Temperaturas **iguais ou abaixo de -18°C**.
    Exemplos: lasanhas congeladas, carnes cruas congeladas, frutas congeladas.
    """)

    tipoComida = st.selectbox(
        "Qual o tipo da comida a ser doada?",
        options=["Quente", "Resfriada", "Congelada"]
    )

    tempoPreparada = st.number_input("Há quanto tempo a comida foi preparada?", min_value=0, step=1)
    grandezaTempo = st.selectbox("Unidade de tempo", options=["horas", "dias"])

    temperatura = st.number_input("Informe a temperatura atual da comida (°C)", step=1)

    enviar = st.form_submit_button("Enviar")

if enviar:
    # Tradução do tipo para API
    tipo_api = tipoComida.lower()  # transforma "Quente" → "quente"
    if tipo_api == "quente":
        tipo_api = "refeicao_pronta"
    elif tipo_api == "resfriada":
        tipo_api = "resfriada"
    elif tipo_api == "congelada":
        tipo_api = "congelada"


    # Conversão de tempo
    if grandezaTempo == "horas":
        dias = round(tempoPreparada / 24, 2)
    else:
        dias = tempoPreparada

    payload = {
        "type": tipo_api,
        "temperature": temperatura,
        "days_since_preparation": dias
    }

    res = requests.post("http://localhost:5000/validate", json=payload)

    resposta = res.json()
    st.success("Resultado da Validação por Regras Fixas:")
    st.json(resposta)

    # Envia o mesmo payload para o Gemini
    st.markdown("---")
    st.subheader("Parecer Técnico da IA (Inspetor ANVISA)")

    with st.spinner("Consultando parecer da IA (Gemini)..."):
        resposta = analisar_como_inspetor(payload)

        placeholder = st.empty()
        parcial = ""

        for c in resposta:
            parcial += c
            placeholder.markdown(parcial + "▌")
            time.sleep(0.01)  # ajuste para deixar mais rápido ou mais lento

        placeholder.markdown(parcial)


    if res.status_code == 200:
        resposta = res.json()
        st.success("Resultado da Validação:")
        st.json(resposta)
    else:
        st.error(f"Erro {res.status_code}: {res.text}")
