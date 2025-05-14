#!/bin/bash

pip install -r requirements.txt

# Subir os containers do Docker

docker compose up -d --build

# Criar o arquivo da API KEY

echo "GEMINI_API_KEY=yourapikey > .env

# Rodar o frontend do sistema

streamlit run ./frontend/home.py