import os
import requests
from dotenv import load_dotenv

load_dotenv() 

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

def chat_with_llm(pergunta):
    if not TOGETHER_API_KEY:
        return "Chave da API Together não encontrada. Verifica o ficheiro .env"

    url = "https://api.together.xyz/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Responde como um assistente útil em português."},
            {"role": "user", "content": pergunta}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Erro ao contactar a API da Together: {e}")
        return "Erro ao contactar a LLM remota."