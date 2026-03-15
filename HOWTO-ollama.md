# HOWTO Ollama

Most of the content in this HOWTO is generic, however some of the settings are specific to my setup:
- Rasberry pi5 8Gb RAM
- Debian GNU/Linux 12 (bookworm)
- Docker 29.3.0
- containerd.io 2.2.2.1

## start ollama
- without GPU (CPU only)
  ```
  sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name molly ollama/ollama
  ```
- with GPU support
  ```
  sudo docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name molly ollama/ollama
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


## orchestrate with docker compose
below  services to your Dockercompose
```
services:
  # Ollama LLM server
  ollama:
    image: ollama/ollama:latest
    container_name: molly
    restart: unless-stopped

    # Expose Ollama API
    ports:
      - "11434:11434"

    # Persist downloaded models
    volumes:
      - ollama_data:/root/.ollama

    networks:
      - ai-net

    # Healthcheck ensures Ollama API is ready
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 5s
      timeout: 3s
      retries: 10

    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]   # enable GPU
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - OLLAMA_NUM_THREADS=8      # optional: limit CPU threads


  # One-time model pull service
  # Waits for Ollama to become healthy, then pulls model and exits
  ollama-init:
    image: ollama/ollama:latest
    container_name: ollama-init

    depends_on:
      ollama:
        condition: service_healthy  # Wait for API readiness

    volumes:
      - ollama_data:/root/.ollama  # Share model storage

    networks:
      - ai-net

    # Pull the model once and exit
    entrypoint: ["ollama", "pull", "qwen2.5-coder:0.5b"]

    restart: "no"
```
