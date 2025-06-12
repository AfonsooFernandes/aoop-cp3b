from flask import Flask, render_template, request, jsonify
from services import chat_with_llm
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(force=True)
    pergunta = data.get("pergunta")

    if not pergunta:
        return jsonify({"erro": "Campo 'pergunta' é obrigatório"}), 400

    resposta = chat_with_llm(pergunta)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)