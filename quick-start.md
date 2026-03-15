# Quick Start

My setup:
- Rasberry pi5 8Gb RAM
- Debian GNU/Linux 12 (bookworm)
- Docker 29.3.0
- containerd.io 2.2.2.1

## start ollama
without GPU (CPU only)
  ```
  sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name molly ollama/ollama
  ```

## load models
- small code LLM
  ```
  sudo docker exec -it molly ollama run qwen2.5-coder:0.5b
  ```
- text embeddings model
  ```
    sudo docker exec -it molly ollama run nomic-embed-text:latest
  ```

## check if working
  - inside molly container 
    ```
      sudo docker exec -it molly bash
      ollama ls
      exit
    ```

  - from your machine
    - get models list: ```http://localhost:11434/api/tags```
    - check LLM
      ```
      curl http://localhost:11434/api/generate -X POST -H "Content-Type: application/json" \
      -d '{
          "model": "qwen2.5-coder:0.5b",
          "prompt": "Ciao",
          "stream": false
      }'
      ```
    - check embedder
      ```
      curl http://localhost:11434/api/embeddings   -d '{
        "model": "nomic-embed-text",
        "prompt": "The quick brown fox jumps over the lazy dog"
      }'
      ```

## create a docker image
- directly from your container
  ```
  docker commit ollama molly
  docker images
  ```

- from Dockerfile ``` docker build -t molly```
  
  ```
  FROM ollama/ollama

  RUN ollama serve & \
    sleep 5 && \
    ollama pull nomic-embed-text && \
    ollama pull qwen2.5-coder:0.5b
  ```
- run it
    ```
    sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name molly molly:latest
  ```


