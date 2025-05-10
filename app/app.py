from flask import Flask, request, jsonify
from validator.engine import validate
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB URI (ajustado ao serviço do Docker)
client = MongoClient("mongodb://mongo:27017/")
db = client["hackathon"]
collection = db["avaliacoes"]

@app.route("/validate", methods=["POST"])
def validar():
    data = request.get_json()
    is_valid, messages = validate(data)

    # Armazena no Mongo
    collection.insert_one({
        "input": data,
        "valid": is_valid,
        "messages": messages,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"valid": is_valid, "messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)