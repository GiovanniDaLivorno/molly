# === Molly Dockerfile ===

FROM ollama/ollama

# Add metadata to the image.
LABEL org.opencontainers.image.authors="giod <giovanni.mumolo@yahoo.com>"

# Create user 'giod'
RUN useradd -m giod

# Switch to user 'gio'
USER giod

# Start ollama in background so models are pulled during image build.
# The sleep is a workaround to give the server time to initialize.
RUN ollama serve & \
    sleep 5 && \
    ollama pull nomic-embed-text && \
    ollama pull qwen2.5-coder:0.5b
