import streamlit as st
import requests
from gemini.gemini_chat import analisar_como_inspetor
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Validação de Doações", layout="centered")
st.title("Formulário de Viabilidade para Doação de Alimentos")

# FORMULÁRIO
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

    tipoComida = st.selectbox("Qual o tipo da comida a ser doada?", ["Quente", "Resfriada", "Congelada"])
    tempoPreparada = st.number_input("Há quanto tempo a comida foi preparada?", min_value=0, step=1)
    grandezaTempo = st.selectbox("Unidade de tempo", ["horas", "dias"])
    temperatura = st.number_input("Informe a temperatura atual da comida (°C)", step=1)

    enviar = st.form_submit_button("Enviar")

# LÓGICA APÓS ENVIO
if enviar:
    # Tradução do tipo para API
    tipo_api = tipoComida.lower()
    if tipo_api == "quente":
        tipo_api = "refeicao_pronta"
    elif tipo_api == "resfriada":
        tipo_api = "resfriada"
    elif tipo_api == "congelada":
        tipo_api = "congelada"

    # Conversão de tempo para dias
    dias = round(tempoPreparada / 24, 2) if grandezaTempo == "horas" else tempoPreparada

    # Construção do payload
    payload = {
        "type": tipo_api,
        "temperature": temperatura,
        "days_since_preparation": dias
    }

    # Chamada à API Flask
    try:
        res = requests.post("http://localhost:5000/validate", json=payload)

        if res.status_code == 200:
            resultado = res.json()

            # BANNER VISUAL PARA RESULTADO
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

            # Justificativas
            st.markdown("**Justificativas Técnicas (Regras Fixas):**")
            for msg in resultado["messages"]:
                st.markdown(f"- {msg}")
        else:
            st.error(f"Erro {res.status_code}: {res.text}")
            st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível se conectar ao servidor Flask.")
        st.stop()

    # IA (GEMINI)
    st.markdown("---")
    st.subheader("Parecer Técnico da IA (Inspetor ANVISA)")

    with st.spinner("Consultando parecer da IA (Gemini)..."):
        resposta_ia = analisar_como_inspetor(payload)
        placeholder = st.empty()
        parcial = ""

        for c in resposta_ia:
            parcial += c
            placeholder.markdown(parcial + "▌")
            time.sleep(0.01)

        placeholder.markdown(parcial)
