#!/bin/bash
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔧 Running migrations and collecting static files..."
./render_start.sh