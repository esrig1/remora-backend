FROM python:3.11

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Set WORKDIR
WORKDIR /code

# 1. Copy only requirements first for cache efficiency
COPY ./requirements.txt /code/requirements.txt

# 2. Install dependencies (uses cache if requirements.txt hasn't changed)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt

# 3. Copy the rest of the build context (respecting .dockerignore)
COPY . /code/

# Expose the HTTP port
EXPOSE 8000

# CMD for Uvicorn over HTTP (no SSL)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
