@echo off
REM Startup script for Library Management System on Windows

echo ====================================
echo  Library Management System Startup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Check if requirements are installed
echo Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully
) else (
    echo Dependencies are already installed
)
echo.

echo Select an option:
echo 1. Run Console Application
echo 2. Run Web API Server
echo 3. Run Tests
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Console Application...
    echo.
    python main.py
) else if "%choice%"=="2" (
    echo Starting Web API Server...
    echo Server will be available at: http://localhost:8000
    echo API Documentation will be available at: http://localhost:8000/docs
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    uvicorn api:app --reload --host 0.0.0.0 --port 8000
) else if "%choice%"=="3" (
    echo Running Tests...
    echo.
    pytest -v
) else if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause
