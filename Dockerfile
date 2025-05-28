FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create required directories
RUN mkdir -p static/img/slider static/img/logo static/css static/js static/img/gallery static/img/icon

# Copy static files
COPY static/img/slider/* static/img/slider/
COPY static/img/logo/* static/img/logo/
COPY static/css/* static/css/
COPY static/js/* static/js/
COPY static/img/gallery/* static/img/gallery/
COPY static/img/icon/* static/img/icon/

# Collect static files
RUN python manage.py collectstatic --noinput

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV DJANGO_SETTINGS_MODULE=detergee.settings

# Run the application
CMD gunicorn detergee.wsgi --bind 0.0.0.0:$PORT 