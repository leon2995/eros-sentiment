FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/hf_cache \
    TOKENIZERS_PARALLELISM=false \
    OMP_NUM_THREADS=1

# Torch en version CPU-only: evita descargar ~2GB de dependencias CUDA
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install -r requirements.txt

# Precarga del modelo dentro de la imagen (arranque sin descargas)
COPY download_model.py .
RUN python download_model.py

COPY main.py .

# Railway inyecta $PORT; localmente cae a 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
