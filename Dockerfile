# Use an official Python base image
FROM python:3.10-slim

# Set environment variables to prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Copy the application files into the container
COPY . /app/

# Install dependencies (and create a virtual environment)
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Expose ports for applications (e.g., Flask or Django server)
EXPOSE 5000

# Set environment variable to activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Set the default command to start the server (replace 'app.py' with your app's main file)
CMD ["python", "app.py"]
