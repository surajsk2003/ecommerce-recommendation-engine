FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn for production
RUN pip install gunicorn

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --settings=ecommerce_rec.settings_prod || true

EXPOSE 8000

# Make startup script executable
RUN chmod +x railway_start.sh

# Use startup script for Railway
CMD ["./railway_start.sh"]