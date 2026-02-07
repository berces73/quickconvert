#!/bin/bash

echo "🚀 Nexus Convert - Production Mode"
echo "===================================="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment aktif"
else
    echo "❌ Virtual environment bulunamadı!"
    echo "Lütfen önce start.sh ile kurulum yapın"
    exit 1
fi

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "❌ Gunicorn bulunamadı!"
    echo "Lütfen önce: pip install -r requirements.txt"
    exit 1
fi

echo "🔧 Gunicorn ile başlatılıyor..."
echo "📍 http://0.0.0.0:8000"
echo ""
echo "⚠️  Durdurmak için: Ctrl+C"
echo ""
echo "===================================="
echo ""

# Start with gunicorn
gunicorn --config gunicorn_config.py app:app
