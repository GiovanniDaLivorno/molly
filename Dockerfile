# === Dockerfile for Molly ===
# Builds a container image that prefetches ollama models for faster startup.
#

FROM ollama/ollama

# Add metadata to the image.
LABEL org.opencontainers.image.authors="Gio <gio@example.com>"

# Start ollama in background so models are pulled during image build.
# The sleep is a simple workaround to give the server time to initialize.
RUN ollama serve & \
    sleep 5 && \
    ollama pull nomic-embed-text && \
    ollama pull qwen2.5-coder:0.5b
