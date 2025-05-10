FROM python:3.10-slim

WORKDIR /app

# Copia tudo
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Expondo a porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação Streamlit
CMD ["streamlit", "run", "frontend/frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
