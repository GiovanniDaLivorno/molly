### simple RAG pipeline for data ingestion and retrieval using Ollama and ChromaDB

import os
import sys
import ollama
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("codebase")

# health_check performs initial validation of dependencies and environment
def health_check(root):
    print("Performing health checks...")
    
    # Check if root directory exists
    if not os.path.exists(root):
        raise ValueError(f"Root directory {root} does not exist")
    
    # Check Ollama service and required model
    try:
        models = ollama.list()
        model_names = [m['name'] for m in models['models']]
        if 'nomic-embed-text' not in model_names:
            raise ValueError("Required model 'nomic-embed-text' not available. Available models: " + ', '.join(model_names))
        print("✓ Ollama service is running and model is available")
    except Exception as e:
        raise ValueError(f"Ollama health check failed: {e}")
    
    # Check ChromaDB connectivity
    try:
        collections = client.list_collections()
        print(f"✓ ChromaDB connected, found {len(collections)} collections")
    except Exception as e:
        raise ValueError(f"ChromaDB health check failed: {e}")
    
    print("All health checks passed.\n")

# read_files walks through the directory tree starting from 'root'
# and yields paths to files with specific extensions.
def read_files(root):
    for path, _, files in os.walk(root):
        for f in files:
            if f.endswith((".py", ".js", ".ts", ".go", ".java")):
                yield os.path.join(path, f)

# chunk_code splits input text into smaller chunks of a specified size.
def chunk_code(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]


###############################################################################
# main execution takes an optional command-line argument for the root directory.
root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd() # current directory is the default

# Run health checks before processing
health_check(root)

for file in read_files(root):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue

    chunks = chunk_code(code)

    for i, chunk in enumerate(chunks):
        try:
            emb = ollama.embeddings(
                model="nomic-embed-text",
                prompt=chunk
            )["embedding"]
        except Exception as e:
            print(f"Error embedding chunk {i} from {file}: {e}")
            continue

        try:
            collection.add(
                embeddings=[emb],
                documents=[chunk],
                ids=[f"{file}:{i}"]
            )
        except Exception as e:
            print(f"Error adding to collection for {file}:{i}: {e}")
            continue