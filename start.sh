#!/bin/bash
# start.sh
echo "🚀 Starting application..."
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔧 Running migrations..."
flask db upgrade

echo "🌐 Starting server..."
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 2 --threads 4 wsgi:app