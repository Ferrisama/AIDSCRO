# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    libqhull-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies and build the React app
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Change back to the app directory
WORKDIR /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME AIDSCRO

# Run app.py when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]