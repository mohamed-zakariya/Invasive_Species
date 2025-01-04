# Use an official Python slim image as a base with version 3.10.15
FROM python:3.10.15-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first (to leverage Docker layer caching)
COPY requirements.txt /app/requirements.txt

# Create a virtual environment and install dependencies
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the application port (5000 for Flask)
EXPOSE 5000

# Add a HEALTHCHECK to monitor the container's health
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Set the default command to start the app
CMD ["python", "app.py"]
