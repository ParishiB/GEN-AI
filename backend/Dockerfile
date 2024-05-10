# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for PostgreSQL connection
ENV POSTGRES_USER=parishiieb
ENV POSTGRES_PASSWORD=A82brOlJyMWd
ENV POSTGRES_HOST=ep-shy-resonance-a59aitl2.us-east-2.aws.neon.tech
ENV POSTGRES_DB=calendly

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi asyncpg openai uvicorn

# Expose the port the FastAPI application runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
