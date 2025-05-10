from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["meubanco"]
collection = db["usuarios"]

@app.route("/")
def home():
    return jsonify({"msg": "API Flask rodando com MongoDB"})

@app.route("/usuarios")
def listar_usuarios():
    usuarios = list(collection.find({}, {"_id": 0}))
    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)