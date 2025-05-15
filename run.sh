#!/bin/bash

pip install -r requirements.txt

# To Build Docker files

docker compose up -d --build

# To Create the API Key

echo "GEMINI_API_KEY=yourapikey" > .env

# To Run the appliction

streamlit run ./frontend/home.py
