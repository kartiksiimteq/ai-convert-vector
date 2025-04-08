#!/bin/bash

echo "🚀 Starting build process..."

# Optional: create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "🧪 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt


# echo "👨‍💻 Running in development mode with auto-reload..."
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
