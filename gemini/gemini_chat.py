import google.generativeai as genai

genai.configure(api_key="AIzaSyBOxM6zDmBuSz7cyYv45zPEkdSaW8ZqB_Y")  # substitua pela sua

model = genai.GenerativeModel("models/gemini-1.5-flash")

def analisar_como_inspetor(form_data):
    tipo = form_data["type"]
    temp = form_data["temperature"]
    dias = form_data["days_since_preparation"]

    prompt = f"""
Você é um inspetor da ANVISA e precisa avaliar a doação de um alimento com as seguintes informações:

- Tipo: {tipo}
- Temperatura atual: {temp}°C
- Dias desde o preparo: {dias}

Diga se pode ou não ser doado. Em seguida, explique com base nas regras sanitárias da ANVISA.
Dê também um percentual estimado de viabilidade para doação, como se fosse uma nota de conformidade.
Responda de forma clara, objetiva e técnica.
"""

    resposta = model.generate_content(prompt)
    return resposta.text
