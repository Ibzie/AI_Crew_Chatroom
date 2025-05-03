# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/conversations

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the PORT environment variable explicitly
ENV PORT=5000

# Run the Flask app on the PORT that Render provides
CMD ["python", "frontend/app.py"]