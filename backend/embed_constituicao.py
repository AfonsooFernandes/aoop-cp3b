from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pdfplumber
import re
import os

def clean_text(text):
    """Corrige erros comuns de OCR e limpa o texto."""
    corrections = {
        r'N Suppuém': 'Ninguém',
        r'constituigao': 'constituição',
        r'Artigp': 'Artigo',
        r'[Pp]ara\s+([0-9])': r'Para \1',
        r'(\d+)\.o': r'\1.º',
        r'(\d+)\.a': r'\1.ª',
        r'dignidade': 'dignidade',
        r'voluntade': 'vontade',
        r'soberana': 'soberana',
        r'sociedade': 'sociedade',
        r'justa': 'justa',
        r'dignidale': 'dignidade',
        r'soberan[ae]': 'soberana',
        r'vontad[ae]': 'vontade',
        r'socied[ae]': 'sociedade',
    }
    for wrong, correct in corrections.items():
        text = re.sub(wrong, correct, text, flags=re.IGNORECASE)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'(Artigo \d+.º|PREÂMBULO)', r'\n\1\n', text, flags=re.IGNORECASE)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extrai texto do PDF com tratamento de erros."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"O arquivo {pdf_path} não foi encontrado.")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
            if not text.strip():
                raise ValueError("O PDF está vazio ou o texto não pôde ser extraído.")
            print("Texto extraído (primeiras 1000 caracteres):\n", text[:1000])
            try:
                with open("texto_extraido.txt", "w", encoding="utf-8") as f:
                    f.write(text)
            except IOError as e:
                print(f"Erro ao guardar texto_extraido.txt: {str(e)}")
            return clean_text(text)
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

def chunk_text(text, max_length=3000):
    """Divide o texto em pedaços com no máximo max_length caracteres."""
    chunks = []
    current_chunk = ""
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    with open("chunks_debug.txt", "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"Chunk {i}:\n{chunk}\n\n")
    return chunks

def create_embeddings(pdf_path="constituicao.pdf"):
    """Cria embeddings do texto do PDF e armazena no FAISS."""
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        raise Exception(f"Erro ao carregar o modelo SentenceTransformer: {str(e)}")
    
    try:
        os.makedirs("./database", exist_ok=True)
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("Nenhum chunk foi criado a partir do texto.")

        embeddings = [model.encode(chunk).tolist() for chunk in chunks]
        embeddings_array = np.array(embeddings).astype('float32')

        dimension = embeddings_array.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_array)
        
        faiss.write_index(index, "./database/faiss_index.idx")
        with open("./database/chunks.pkl", "wb") as f:
            import pickle
            pickle.dump(chunks, f)
        print(f"Embeddings criados com sucesso! {len(chunks)} pedaços armazenados no FAISS.")
    except Exception as e:
        raise Exception(f"Erro durante a criação de embeddings: {str(e)}")

if __name__ == "__main__":
    try:
        create_embeddings()
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")