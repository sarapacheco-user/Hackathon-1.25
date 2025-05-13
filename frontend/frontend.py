import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from gemini.gemini_chat import analisar_como_inspetor
import time
import os
import sys

### Configuração do Streamlit com .env e APIKEY diretamente sendo chamada no código
### Se você quiser usar o .env, descomente as linhas
    #from dotenv import load_dotenv
    #load_dotenv()

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
