# Molly

How to quckly start with Ollama on Rasberry pi5. the projects is tested on this stack:
- Rasberry pi5 8Gb RAM
- Debian GNU/Linux 12 (bookworm)
- Docker 29.3.0
- containerd.io 2.2.2.1

## start ollama
this start ollama without GPU support, CPU only
  ```
  sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name molly ollama/ollama
  ```

## load models
Two models are loaded, one small code model, and a text embedding model for vector DB knowledge storage
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
    - check if LLM works
      ```
      curl http://localhost:11434/api/generate -X POST -H "Content-Type: application/json" \
      -d '{
          "model": "qwen2.5-coder:0.5b",
          "prompt": "Ciao",
          "stream": false
      }'
      ```
    - check if embedder works
      ```
      curl http://localhost:11434/api/embeddings   -d '{
        "model": "nomic-embed-text",
        "prompt": "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
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
  # Dockerfile
  FROM ollama/ollama

  RUN ollama serve & \
    sleep 5 && \
    ollama pull nomic-embed-text && \
    ollama pull qwen2.5-coder:0.5b
  ``` 


## orchestrate with docker compose
below a Dockercompose snippet optimized for Rasberry pi5.
Rasberry pi5 CPU has 4 cores, so threads are limited to 4

```
services:
  ollama:
    image: molly:latest
    container_name: molly
    restart: unless-stopped

    ports:
      - "11434:11434"

    environment:
      - OLLAMA_NUM_THREADS=4 
```
