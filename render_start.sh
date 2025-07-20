#!/bin/bash
set -e

echo "🚀 Starting Render deployment..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --settings=ecommerce_rec.settings_prod --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --settings=ecommerce_rec.settings_prod --noinput

# Create superuser if credentials are provided
if [ "$ADMIN_USERNAME" ] && [ "$ADMIN_EMAIL" ] && [ "$ADMIN_PASSWORD" ]; then
    echo "👤 Creating admin user..."
    python manage.py shell --settings=ecommerce_rec.settings_prod << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('ADMIN_USERNAME')
email = os.environ.get('ADMIN_EMAIL') 
password = os.environ.get('ADMIN_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser {username} created")
else:
    print(f"ℹ️  Superuser {username} already exists")
EOF
fi

# Populate sample data if requested
if [ "$DATABASE_POPULATE" = "true" ]; then
    echo "🌱 Populating sample data..."
    python manage.py populate_sample_data --settings=ecommerce_rec.settings_prod || echo "Sample data population skipped"
fi

echo "✅ Render startup completed!"