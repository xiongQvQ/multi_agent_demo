FROM python:3.11-slim

# Prevents Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OUTPUT_DIR=/data \
    PORT=8501 \
    HOST=0.0.0.0

WORKDIR /app

# System deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install first (better layer caching)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create non-root user and output dir
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p ${OUTPUT_DIR} \
    && chown -R appuser:appuser ${OUTPUT_DIR}

# Copy source
COPY . .

# Permissions
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT}

# Default to Streamlit UI (honor PORT env)
CMD ["sh", "-c", "streamlit run ui/app.py --server.port=${PORT} --server.address=0.0.0.0"]
