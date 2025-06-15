from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
import re
import pickle
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

model = SentenceTransformer('all-MiniLM-L6-v2')
faiss_index = faiss.read_index("./database/faiss_index.idx")
with open("./database/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

def query_constituicao(pergunta):
    embedding = model.encode(pergunta).tolist()
    embedding_array = np.array([embedding]).astype('float32')
    distances, indices = faiss_index.search(embedding_array, k=15)
    context_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

    match = re.search(r'(artigo|art\.?)\s*(\d+)', pergunta, re.IGNORECASE)
    artigo_num = match.group(2) if match else None

    if artigo_num:
        padroes = [
            rf'\bArtigo\s+{artigo_num}[ºoº\.]?\b',
            rf'\bArt\.?\s*{artigo_num}[ºoº\.]?\b',
            rf'\b{artigo_num}[ºoº\.]?\b'
        ]
        for chunk in chunks:
            for p in padroes:
                if re.search(p, chunk, re.IGNORECASE) and chunk not in context_chunks:
                    context_chunks.insert(0, chunk)
                    break

    return context_chunks[:10]

def ask_groq(pergunta, context):
    if not context:
        return "❌ Não posso responder com base nas informações disponíveis."

    system_prompt = "Você é um assistente jurídico especializado na Constituição da República Portuguesa. Responda às perguntas apenas com base no contexto fornecido."
    user_prompt = f"**Pergunta**: {pergunta}\n\n**Contexto**:\n{context}"

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 700
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            print("🔎 Erro detalhado da API:", e.response.text)
        return f"❌ Erro ao contactar o servidor: {str(e)}"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    pergunta = data.get("pergunta", "")
    context_chunks = query_constituicao(pergunta)
    context = "\n\n".join(context_chunks)
    resposta = ask_groq(pergunta, context)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")