import google.generativeai as genai

genai.configure(api_key="AIzaSyBOxM6zDmBuSz7cyYv45zPEkdSaW8ZqB_Y")

model = genai.GenerativeModel("models/gemini-1.5-flash")

response = model.generate_content("Estou participando de um hackathon e meu grupo decidiu criar uma aplicação para evitar que comidas sejam desperdiçadas através da doação de alimentos que estejam de acordo com os padrões de qualidade da Anvisa. O que você acha dessa ideia? Quais poderiam ser pontos atrativos para o usuário e para o restaurante que está doando os alimentos? Quais funcionalidades poderiam ser interessantes para a aplicação?")

print(response.text)