FROM python:3.10-slim

WORKDIR /app

# Copies everything
COPY . .

# Installs the dependencies
RUN pip install -r frontend/requirements.txt

# Exposes Streamlit's standard
EXPOSE 8501

# Command to start the Streamlit application
CMD ["streamlit", "run", "frontend/home.py", "--server.port=8501", "--server.address=0.0.0.0"]
