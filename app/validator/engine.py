import yaml
import os

def load_rules():
    path = os.path.join(os.path.dirname(__file__), "rules.yaml")
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def validate(payload):
    tipo = payload.get("type")
    rules = load_rules().get(tipo, [])
    erros = []

    for rule in rules:
        campo = rule["field"]
        operador = rule["operator"]
        valor = rule["value"]
        recebido = payload.get(campo)

        try:
            if not eval(f"{repr(recebido)} {operador} {repr(valor)}"):
                erros.append(rule["error_message"])
        except Exception as e:
            erros.append(f"Erro ao validar campo {campo}: {e}")

    if erros:
        return False, erros
    return True, ["Apto para doação."]
