#!/bin/bash
# Startup script for Library Management System on Linux/Mac

echo "===================================="
echo " Library Management System Startup"
echo "===================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python is installed"
echo

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip for Python 3"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip3 show fastapi &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
    echo "Dependencies installed successfully"
else
    echo "Dependencies are already installed"
fi
echo

echo "Select an option:"
echo "1. Run Console Application"
echo "2. Run Web API Server"
echo "3. Run Tests"
echo "4. Exit"
echo

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Starting Console Application..."
        echo
        python3 main.py
        ;;
    2)
        echo "Starting Web API Server..."
        echo "Server will be available at: http://localhost:8000"
        echo "API Documentation will be available at: http://localhost:8000/docs"
        echo
        echo "Press Ctrl+C to stop the server"
        echo
        uvicorn api:app --reload --host 0.0.0.0 --port 8000
        ;;
    3)
        echo "Running Tests..."
        echo
        pytest -v
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
