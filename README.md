# 🤖 Chatbot com LLM (Meta-Llama 3.1)

Este projeto é uma aplicação web interativa que permite ao utilizador conversar com uma LLM (Large Language Model) em português. Utiliza o modelo **Meta-Llama-3.1-8B-Instruct-Turbo** através da API da [Together](https://api.together.xyz/), com backend em Flask e frontend moderno com Bootstrap.

---

## 🧩 Tecnologias utilizadas

* Python 3 + Flask
* API Together (LLM)
* HTML, CSS, JavaScript (Vanilla)
* Bootstrap 5
* .env para variáveis sensíveis

---

## 🚀 Como executar localmente

### 1. Clonar o repositório

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

> ⚠️ O ficheiro `requirements.txt` deve conter:
>
> ```
> flask
> python-dotenv
> requests
> ```

### 3. Criar o ficheiro `.env`

Cria um ficheiro `.env` na raiz do projeto com o seguinte conteúdo:

```env
TOGETHER_API_KEY=sua_chave_aqui
```

### 4. Iniciar o servidor

```bash
python app.py
```

Acede ao navegador em `http://127.0.0.1:5000`

---

## 🗂️ Estrutura de ficheiros

```
.
├── app.py               # Servidor Flask
├── services.py          # Interação com a API LLM
├── templates/
│   └── index.html       # Interface web
├── static/
│   ├── main.js          # Lógica de frontend
│   └── style.css        # Estilos visuais
├── .env                 # Variáveis de ambiente 
└── requirements.txt     # Dependências Python
```

---

## 💬 Funcionalidades

* Interface moderna e responsiva
* Comunicação em tempo real com LLM
* Indicador de digitação animado
* Separação visual entre mensagens do utilizador e do bot