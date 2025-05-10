#!/bin/bash

pip install -r requirements.txt

# Subir os containers do Docker

docker compose up -d --build

# Criar o arquivo da API KEY

echo "GEMINI_API_KEY=AIzaSyBOxM6zDmBuSz7cyYv45zPEkdSaW8ZqB_Y " > .env

# Rodar o frontend do sistema

streamlit run ./frontend/frontend.py
