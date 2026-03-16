### simple RAG pipeline

import os
import ollama
import chromadb

client = chromadb.Client()
collection = client.create_collection("codebase")

def read_files(root):
    for path, _, files in os.walk(root):
        for f in files:
            if f.endswith((".py", ".js", ".ts", ".go", ".rs", ".java")):
                yield os.path.join(path, f)

def chunk_code(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

for file in read_files("~/ws"): ## ~/ws is my coding workspace
    with open(file) as f:
        code = f.read()

    chunks = chunk_code(code)

    for i, chunk in enumerate(chunks):
        emb = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )["embedding"]

        collection.add(
            embeddings=[emb],
            documents=[chunk],
            ids=[f"{file}:{i}"]
        )