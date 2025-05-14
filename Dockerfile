FROM python:3.10-slim

WORKDIR /app

# Copia só o requirements.txt primeiro
COPY requirements.txt .

# Instala as dependências, aproveitando o cache se o requirements.txt não mudou
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o restante dos arquivos
COPY . .

EXPOSE 5000

CMD ["python", "app/app.py"]