#!/bin/bash

set -e

echo "🚀 Starting SmartCommerce AI Deployment..."

# Configuration
ENVIRONMENT="${1:-development}"

# Build and deploy
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🚢 Deploying to production..."
    docker-compose -f docker-compose.prod.yml up -d --build
    
elif [ "$ENVIRONMENT" = "staging" ]; then
    echo "🧪 Deploying to staging..."
    docker-compose -f docker-compose.yml up -d --build
    
else
    echo "🛠️ Deploying to development..."
    docker-compose up -d --build
fi

# Health checks
echo "🩺 Performing health checks..."
sleep 30

if curl -f http://localhost/health; then
    echo "✅ Application is healthy!"
else
    echo "❌ Health check failed!"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "🌐 Application: http://localhost"
echo "📊 Monitoring: http://localhost:3001"