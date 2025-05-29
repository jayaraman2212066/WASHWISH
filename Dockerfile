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

# Create required directories and ensure they exist
RUN mkdir -p static/img/slider static/img/logo static/css static/js static/img/gallery static/img/icon media && \
    touch static/img/slider/slider-img-1.jpg && \
    touch static/img/slider/slider-img-2.jpg && \
    touch static/img/slider/slider-img-3.jpg

# Run migrations
RUN python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=detergee.settings
ENV DEBUG=false
ENV ALLOWED_HOSTS=washwish-production.up.railway.app

# Run the application
CMD gunicorn detergee.wsgi --bind 0.0.0.0:$PORT --workers 3 --threads 2 --timeout 120 --access-logfile - --error-logfile - --log-level info 