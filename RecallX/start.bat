@echo off
REM RecallX - Quick Start Batch Script for Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           RecallX - AI Memory Recall Assistant             ║
echo ║      Starting Application in 3 seconds...                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [✓] Dependencies installed
) else (
    echo [✓] Dependencies already installed
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                 Starting Flask Server...                   ║
echo ║                                                            ║
echo ║    Open your browser to: http://localhost:5000            ║
echo ║                                                            ║
echo ║    Press CTRL+C to stop the server                        ║
echo ║                                                            ║
echo ║    Features:                                              ║
echo ║    • 3 sample topics with pre-generated questions         ║
echo ║    • Interactive forgetting curve visualization           ║
echo ║    • Stress-based recall testing                          ║
echo ║    • Performance analytics and readiness score            ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Start the Flask application
python app.py

pause
