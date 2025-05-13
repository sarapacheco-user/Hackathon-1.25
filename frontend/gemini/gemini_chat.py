import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import streamlit as st


### Configuração do Streamlit com .env e APIKEY diretamente sendo chamada no código
### Se você quiser usar o .env, descomente as linhas abaixo e coloque no .env a API.

    # Carrega variáveis do ambiente (.env)
    #load_dotenv()
    #api_key = os.getenv("GEMINI_API_KEY")

    #if not api_key:
    #    raise ValueError("GEMINI_API_KEY não encontrado no .env")

    #genai.configure(api_key=api_key)

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
    tipo = form_data["tipo_alimento"]
    temp = form_data["temperatura_atual"]
    dias = form_data["tempo_preparo"]
    prazo = form_data["prazo_validade"]
    temp_ideal = form_data["temperatura_adequada"]
    embalagem = form_data["embalagem_integra"]
    alimento_integro = form_data["alimento_integro"]
    sem_contaminacao = form_data["sem_contaminacao"]
    nutricional_preservada = form_data["nutricional_preservada"]
    preparo_armazenado_apto = form_data["preparo_armazenado_apto"]
    eh_para_lactentes = form_data["eh_para_lactentes"]
    unidade_tempo = form_data["unidade_tempo"]

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
        tipo_alimento=tipo,
        temperatura_atual=temp,
        tempo_preparo=dias,
        prazo_validade=prazo,
        temperatura_adequada=temp_ideal,
        embalagem_integra=embalagem,
        alimento_integro=alimento_integro,
        sem_contaminacao=sem_contaminacao,
        nutricional_preservada=nutricional_preservada,
        preparo_armazenado_apto=preparo_armazenado_apto,
        eh_para_lactentes=eh_para_lactentes,
        unidade_tempo=unidade_tempo,

        produtos=exemplos_produtos,
        validacoes=exemplos_validacao,
        empresas=exemplos_empresas
    )

    resposta = model.generate_content(prompt)
    return resposta.text
