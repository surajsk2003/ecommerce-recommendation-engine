#!/bin/bash
set -e

echo "🚀 Starting Railway deployment..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --settings=ecommerce_rec.settings_prod --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --settings=ecommerce_rec.settings_prod --noinput

# Create superuser if it doesn't exist (optional)
echo "👤 Creating admin user..."
python manage.py shell --settings=ecommerce_rec.settings_prod << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('ADMIN_USERNAME', ***REMOVED***)
email = os.environ.get('ADMIN_EMAIL', '***REMOVED***')
password = os.environ.get('ADMIN_PASSWORD', '***REMOVED***')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser {username} created")
else:
    print(f"ℹ️  Superuser {username} already exists")
EOF

# Populate sample data if DATABASE_POPULATE is set
if [ "$DATABASE_POPULATE" = "true" ]; then
    echo "🌱 Populating sample data..."
    python manage.py populate_sample_data --settings=ecommerce_rec.settings_prod
fi

echo "✅ Railway startup completed!"

# Start the application with gunicorn
echo "🌐 Starting gunicorn server..."
exec gunicorn ecommerce_rec.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info