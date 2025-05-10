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

# ABAS
aba_form, aba_dashboard = st.tabs(["Formulário", "Dashboards"])

# ========== FORMULÁRIO ==========
with aba_form:
    st.header("Formulário de Viabilidade para Doação")

    with st.form("formViabilidadeDoacao"):
        tipoComida = st.selectbox("Tipo do alimento", ["Quente", "Resfriada", "Congelada"])
        temperatura = st.number_input("Temperatura atual do alimento (°C)", step=1)
        tempo = st.number_input("Tempo desde o preparo", min_value=0, step=1)
        unidade_tempo = st.selectbox("Unidade de tempo", ["horas", "dias"])
        is_lactente = st.checkbox("Este alimento é destinado a lactentes?")

        st.markdown("### Regras Técnicas da ANVISA")
        prazo_validade = st.checkbox("Está dentro do prazo de validade?")
        temperatura_conservacao = st.checkbox("Temperatura adequada para conservação?")
        temperatura_congelado = st.checkbox("Se congelado, está a -18°C ou menos?")
        embalagem_integra = st.checkbox("A embalagem está íntegra ou com danos seguros?")
        integridade_visual = st.checkbox("O alimento está visualmente íntegro?")
        seguranca_sanitaria = st.checkbox("Não está contaminado ou estragado?")
        propriedades_nutricionais = st.checkbox("As propriedades nutricionais estão preservadas?")
        tempo_preparo_apto = st.checkbox("Foi preparado há menos de 6h e armazenado corretamente?")
        autorizacao_lactente = st.checkbox("Tem autorização sanitária?") if is_lactente else False

        enviar = st.form_submit_button("Enviar")

    if enviar:
        tipo_api = tipoComida.lower()
        if tipo_api == "quente":
            tipo_api = "refeicao_pronta"

        dias = round(tempo / 24, 2) if unidade_tempo == "horas" else tempo

        payload = {
            "type": tipo_api,
            "temperature": temperatura,
            "days_since_preparation": dias,
            "prazo_validade": prazo_validade,
            "temperatura_conservacao": temperatura_conservacao,
            "temperatura_congelado": temperatura_congelado,
            "embalagem_integra": embalagem_integra,
            "integridade_visual": integridade_visual,
            "seguranca_sanitaria": seguranca_sanitaria,
            "propriedades_nutricionais": propriedades_nutricionais,
            "tempo_preparo_apto": tempo_preparo_apto,
            "autorizacao_lactente": autorizacao_lactente
        }

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

# ========== DASHBOARD ==========
with aba_dashboard:
    st.header("Análise de Dados dos Produtos")

    try:
        df = pd.read_csv(infoProdutos)

        if 'produto' in df.columns and 'quantidade' in df.columns:
            st.subheader("Quantidade Produto Excedido")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(df['produto'], df['quantidade'], color='skyblue')
            ax.set_title("Quantidade por Produto")
            ax.set_xlabel("Produto")
            ax.set_ylabel("Quantidade")
            plt.xticks(rotation=45)
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
            plt.xticks(rotation=0)
            st.pyplot(fig2)
        else:
            st.warning("Coluna 'valido' não encontrada.")

    except FileNotFoundError:
        st.error("Arquivo de produtos não encontrado.")
