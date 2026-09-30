FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system build tools required by some Python packages.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code.
COPY . .

# Expose port for Streamlit dashboard.
EXPOSE 8501

# Run Streamlit dashboard.
CMD ["streamlit", "run", "frontend/dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
