import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import streamlit as st

# Carrega variáveis do ambiente (.env)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrado no .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

client = MongoClient("mongodb://localhost:27017/")
db = client["hackathon"]

@st.cache_data(ttl=600)
def carregar_dados_mongo():
    return {
        "empresas": list(db["empresas"].find({}, {"_id": 0})),
        "produtos": list(db["produtos"].find({}, {"_id": 0})),
        "validacao": list(db["validacao"].find({}, {"_id": 0}))
    }

def analisar_como_inspetor(form_data):
    tipo = form_data["type"]
    temp = form_data["temperature"]
    dias = form_data["days_since_preparation"]

    dados = carregar_dados_mongo()

    exemplos_empresas = dados["empresas"][:2]
    exemplos_produtos = dados["produtos"][:2]
    exemplos_validacao = dados["validacao"][:2]

    from pathlib import Path
    current_dir = Path(__file__).resolve().parent
    template_path = current_dir / "prompt_template.txt"

    with open(template_path, "r", encoding="utf-8") as f:
      template = f.read()

    prompt = template.format(
        tipo=tipo,
        temp=temp,
        dias=dias,
        produtos=exemplos_produtos,
        validacoes=exemplos_validacao,
        empresas=exemplos_empresas
    )

    resposta = model.generate_content(prompt)
    return resposta.text
