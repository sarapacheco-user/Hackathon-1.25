FROM python:3.10-slim

WORKDIR /app

# Starts off by only copying the requirements.txt
COPY requirements.txt .

# Installs dependencies, also upon cache if requirements.txt has not changed
RUN pip install --no-cache-dir -r requirements.txt

# Copies the rest of the files 
COPY . .

EXPOSE 5000

CMD ["python", "app/app.py"]
