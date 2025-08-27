#!/bin/bash

# Cozy DoDo - Vacation Home Assistant Startup Script
# Author: AI Assistant
# Version: 1.0.0

echo "🏝 Cozy DoDo - Vacation Home Assistant Startup Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found, please install Python 3.8 or higher first"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 not found, please install pip first"
    exit 1
fi

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create .env file and add your OpenRouter API key:"
    echo "OPENROUTER_API_KEY=your_actual_api_key_here"
    echo ""
    echo "Continue starting service? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Continuing to start service..."
    else
        echo "Please configure .env file first"
        exit 1
    fi
fi

# Check if database has data
if [ ! -f "vacation_rentals.db" ] || [ ! -s "vacation_rentals.db" ]; then
    echo "📊 Database is empty or doesn't exist"
    echo "Checking for properties_simple.json..."
    
    if [ -f "properties_simple.json" ]; then
        echo "✅ Found properties_simple.json, importing data..."
        echo "This will import 300 properties with coordinates into the database"
        echo ""
        echo "Import data now? (y/n)"
        read -r import_response
        if [[ "$import_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo "🔄 Importing properties from JSON..."
            python3 import_properties.py --auto-import
            if [ $? -eq 0 ]; then
                echo "✅ Data import completed successfully!"
            else
                echo "❌ Data import failed. Please run 'python3 import_properties.py' manually"
                echo "Continue starting service? (y/n)"
                read -r continue_response
                if [[ ! "$continue_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                    echo "Please import data first"
                    exit 1
                fi
            fi
        else
            echo "⚠️  Skipping data import. You can run 'python3 import_properties.py' later"
        fi
    else
        echo "❌ Error: properties_simple.json not found"
        echo "This file contains the property data needed for the application"
        echo "Please ensure the file exists before running the application"
        exit 1
    fi
else
    echo "✅ Database exists and has data"
fi

# Check if port is occupied
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Warning: Port 8000 is already occupied"
    echo "Please stop the service occupying port 8000, or use another port"
    echo "Try using another port? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Please enter new port number (default: 8001):"
        read -r port
        port=${port:-8001}
    else
        echo "Please manually stop the service occupying port 8000"
        exit 1
    fi
else
    port=8000
fi

# Start service
echo "🚀 Starting FastAPI service..."
echo "Service address: http://127.0.0.1:$port"
echo "Frontend page: http://127.0.0.1:$port/static/index.html"
echo "API docs: http://127.0.0.1:$port/docs"
echo ""
echo "Press Ctrl+C to stop service"
echo "=========================================="

# Start uvicorn service
uvicorn api:app --reload --host 127.0.0.1 --port "$port"
