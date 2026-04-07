# Molly

Molly project is for learning ollama, small LLM, text embeddings, etc. etc. runnng locally in a container. 
Configurations are optimzed and tested on
- Rasberry pi5 8Gb RAM (without AI Hat+ module)
- Debian GNU/Linux 12 (bookworm)
- Docker 29.3.0
- containerd.io 2.2.2.1

start working in three steps 

## 1 build molly docker image 

create an image for your host machine's CPU architecture
```
docker build -t molly .
```

## 2 run it
```
  sudo docker run -d -v ollama:/home/gio/.ollama -p 11434:11434 --name molly molly:latest
```

## 3 test if it work
- get models list
   - from molly container or
     ```
     sudo docker exec -it molly bash
     ollama ls
     exit
     ```

   - from your docker host
     ```
     http://localhost:11434/api/tags
     ```

- check if LLM respond
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
    "prompt": "The quick brown fox jumps over the lazy dog"
    }'
   ```

## alternative docker image build

- start ollama without GPU (CPU only)
  ```
  sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name molly ollama/ollama
  ```

- load models (a small code LLM and an embedding model)
  ```
  sudo docker exec -it molly ollama run qwen2.5-coder:0.5b
  sudo docker exec -it molly ollama run nomic-embed-text:latest
  ```

- create molly image directly from the container
  ```
  docker commit ollama molly
  docker images
  ```
  
## Bonus: create an image for a specific CPU architecture

to create an images for a CPU architecture different from the one you are running docker on you need to use Docker Buildx.
Here the instruction are for building a ARM64 image on a x86_64 docker host


- enable QEMU emulation
  ```
  docker run --rm --privileged tonistiigi/binfmt --install all
  ```

- create a buildx builder and start it
  ```
  docker buildx create --use --name molly-builder
  docker buildx inspect --bootstrap
  ```

- then build the ARM64 image
- ARM CPU architecture 
  ```
  docker buildx build --platform linux/arm64 -t molly:arm64 --load .
  ```

- If you want a single multi-architecture image pushed to a registry instead of local images:

```
docker buildx build --platform linux/amd64,linux/arm64 -t <your-dockerhub-user>/molly:latest --push .
```

