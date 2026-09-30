FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system build tools required by some Python packages
# Example: annoy needs a C++ compiler when a prebuilt wheel is unavailable.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first so Docker can cache this layer.
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code.
COPY . .

# Expose port for FastAPI API.
EXPOSE 8000

# Run the server.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
