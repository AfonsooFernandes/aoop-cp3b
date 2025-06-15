# 📜 Constituição Portuguesa – Assistente Jurídico

Este projeto é um chatbot com interface web que responde a perguntas sobre a **Constituição da República Portuguesa**, utilizando **RAG (Retrieval-Augmented Generation)** com embeddings e um modelo LLM da Groq (LLaMA 4).

## 🧠 Tecnologias Utilizadas

- **Python + Flask** – Backend da API
- **SentenceTransformers + FAISS** – Indexação semântica do conteúdo da constituição
- **Groq API (LLaMA 4)** – LLM usado para gerar respostas
- **HTML + CSS + JS (Vanilla + Bootstrap)** – Interface moderna e responsiva
- **pdfplumber** – Extração do conteúdo do PDF
- **dotenv** – Gestão segura de variáveis como a API Key

## 📁 Estrutura do Projeto

```
chatbot/
├── backend/
│   ├── app.py
│   ├── embed_constituicao.py
│   ├── database/
│   │   ├── constituicao.pdf
│   │   ├── faiss_index.idx
│   │   ├── chunks.pkl
│   │   └── texto_extraido.txt
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── style.css
│   │   └── main.js
│   └── .env
├── README.md
```

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/AfonsooFernandes/aoop-cp3b.git
cd constituição-chatbot/backend
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` com sua chave da API da Groq:
```
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

4. Gere os embeddings do PDF:
```bash
python embed_constituicao.py
```

5. Inicie o servidor Flask:
```bash
python app.py
```

6. Acesse a aplicação no navegador:
```
http://localhost:5000
```

## 💬 Funcionalidades

- Interface intuitiva e responsiva para perguntas jurídicas
- Procura vetorial otimizada por FAISS
- Integração com modelo LLaMA 4 via Groq API
- Deteção de artigos específicos como.

## ✅ Exemplo de Perguntas
- `O que diz o Artigo 13.º?`
