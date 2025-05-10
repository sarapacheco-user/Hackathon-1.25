import streamlit as st
import requests

st.title("Validador de Alimentos para Doação")

tipo = st.selectbox("Tipo de alimento", ["refeicao_pronta", "fruta"])
temperatura = st.number_input("Temperatura (°C)", step=1)
dias = st.number_input("Dias desde o preparo", step=1)
has_mold = st.selectbox("Tem bolor?", ["false", "true"]) if tipo == "fruta" else None

if st.button("Validar"):
    payload = {
        "type": tipo,
        "temperature": temperatura,
        "days_since_preparation": dias
    }
    if has_mold is not None:
        payload["has_mold"] = has_mold == "true"

    res = requests.post("http://127.0.0.1:5000/validate", json=payload)
    if res.status_code == 200:
        resposta = res.json()
        st.subheader("Resultado")
        st.json(resposta)
    else:
        st.error("Erro ao se conectar com o servidor Flask.")
