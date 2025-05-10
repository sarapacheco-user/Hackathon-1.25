from flask import Flask, request, jsonify
from validator.engine import validate
from pymongo import MongoClient
from datetime import datetime

# Conexão com o MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["hackathon"]

@app.route("/validate", methods=["POST"])
def validar():
    data = request.get_json()
    is_valid, messages = validate(data)
    db.validacao.insert_one({
        "input": data,
        "valid": is_valid,
        "messages": messages,
        "timestamp": datetime.utcnow()
    })
    return jsonify({"valid": is_valid, "messages": messages})

@app.route("/alimentos", methods=["GET"])
def listar_validacoes():
    registros = list(db.validacao.find({}, {"_id": 0}))
    return jsonify(registros)

@app.route("/empresas", methods=["GET"])
def listar_empresas():
    registros = list(db.empresas.find({}, {"_id": 0}))
    return jsonify(registros)

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    registros = list(db.produtos.find({}, {"_id": 0}))
    return jsonify(registros)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)