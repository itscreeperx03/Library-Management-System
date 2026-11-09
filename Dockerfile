# Multi-stage production Dockerfile for Athena LMS
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application source
COPY . .

# Environment configuration
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Production launch command
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "--threads", "2", "wsgi:application"]
