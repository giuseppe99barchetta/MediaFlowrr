# Use an official lightweight Python image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (if needed, optional)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential && \
#     rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else, excluding .env and unnecessary files
COPY . .

# Ensure .env is not included (for local dev convenience)
# You can also use a .dockerignore file for this

# Default command
CMD ["python", "main.py"]
