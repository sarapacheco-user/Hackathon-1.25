# Hackathon-1.25

## Documentação referente ao software e processos realizados durante o desenvolvimento 
<p><a href="https://docs.google.com/document/d/13Mq4_E7nHVVTti5fNme2gb14C4IDbfMn1a73ul8kFL0/edit?tab=t.0#heading=h.rgn9e3azl2ay">Documentação</a></p>

# 🥗 ShareBite – Combate ao Desperdício de Alimentos com Tecnologia e Incentivo Social

**ShareBite** é uma aplicação desenvolvida durante a quinta edição do hackathon do IDP com o objetivo de combater o desperdício de alimentos por meio da validação de produtos com base em critérios da ANVISA e incentivo à doação por empresas e restaurantes. O sistema conta com um backend em Flask, banco de dados MongoDB e integração com inteligência artificial.

---

## 🚀 Funcionalidades

- ✅ **Validação de alimentos**: API que verifica se os dados informados sobre alimentos estão dentro dos critérios de segurança da ANVISA.
- 📦 **Cadastro e listagem de produtos e empresas** doadores.
- 📊 **Dashboard de registros validados** (histórico).
- 🤖 **Integração com IA (Google Gemini)** para geração de ideias e apoio ao projeto.
- 💰 **Proposta de incentivo fiscal** para empresas doadoras, baseada no programa Nota Legal do Distrito Federal (DF).

---

## 📁 Principais tecnologias usadas

- **Python 3 + Flask**
- **MongoDB (com PyMongo)**
- **Docker**
- **Google Gemini API (IA)**
  
## Equipe
- **Fábio Luis de Carvalho Terra**
- **Sara Pacheco de Azevedo**
- **Felipe Barroso**
- **Pietro Branco**

## Como executar o projeto

Clonar o repositório do GitHub

git clone https://github.com/Felipebc2/Hackathon-1.25.git
cd Hackathon-1.25

Fazer o download dos requirements

pip install -r requirements.txt

Subir os containers do Docker

docker compose up -d --build

Criar o arquivo da API KEY

Acessar o link https://aistudio.google.com/app/apikey e fazer login com sua conta google
No canto superior direito da tela clicar no botão Criar chave de API
Criar um arquivo .env com a chave de API gerada pelo gemini
Clonar o repositório do GitHub
```
git clone https://github.com/Felipebc2/Hackathon-1.25.git
cd Hackathon-1.25
```
Fazer o download dos requirements
```
pip install -r requirements.txt
```
Subir os containers do Docker
```
docker compose up -d --build
```
Criar o arquivo da API KEY
```
Acessar o link https://aistudio.google.com/app/apikey e fazer login com sua conta google
No canto superior direito da tela clicar no botão Criar chave de API
Criar um arquivo .env com a chave de API gerada pelo gemini

echo "GEMINI_API_KEY=suaAPI-KEY " > .env
```
Rodar o frontend do sistema
```
streamlit run ./frontend/frontend.py
```
echo "GEMINI_API_KEY=suaAPI-KEY " > .env

Rodar o frontend do sistema

streamlit run ./frontend/home.py
