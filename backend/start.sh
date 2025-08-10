#!/bin/bash

# AI Knowledge Assistant Backend Startup Script

echo "🚀 Starting AI Knowledge Assistant Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Dependencies not installed. Installing now..."
    pip install -r requirements.txt
fi

# Start the Flask application
echo "🌐 Starting Flask application..."
echo "   The app will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

python run.py
