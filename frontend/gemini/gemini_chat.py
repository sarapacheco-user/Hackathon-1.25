import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import streamlit as st

# Carrega variáveis do ambiente (.env)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrado no .env.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Conexão com MongoDB (ajuste conforme necessário: localhost ou mongo)
MONGO_URI = "mongodb://mongo:27017/"
client = MongoClient(MONGO_URI)
db = client["hackathon"]

@st.cache_data(ttl=600)
def carregar_dados_mongo():
    """
    Carrega e cacheia os dados das coleções por 10 minutos.
    """
    return {
        "empresas": list(db["empresas"].find({}, {"_id": 0})),
        "produtos": list(db["produtos"].find({}, {"_id": 0})),
        "validacao": list(db["validacao"].find({}, {"_id": 0}))
    }

def analisar_como_inspetor(form_data):
    """
    Usa Gemini para gerar um parecer técnico com base no template.

    Args:
        form_data (dict): Dados do formulário (tipo, temperatura, dias, etc.)

    Returns:
        str: Parecer técnico gerado pela IA.
    """
    # Carrega o template do prompt
    caminho_prompt = os.path.join(os.path.dirname(__file__), "prompt_template.txt")
    with open(caminho_prompt, "r", encoding="utf-8") as f:
        prompt_base = f.read()

    # Insere os dados do form no template
    prompt_final = prompt_base + f"""

Dados recebidos:
- Tipo: {form_data['type']}
- Temperatura: {form_data['temperature']}°C
- Dias desde o preparo: {form_data['days_since_preparation']}
"""

    resposta = model.generate_content(prompt_final)
    return resposta.text
