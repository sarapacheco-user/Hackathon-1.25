FROM python:3.10-slim

WORKDIR /app

# Copia tudo, inclusive o requirements.txt
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app/app.py"]
