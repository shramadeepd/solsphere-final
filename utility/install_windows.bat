@echo off
echo ========================================
echo SolSphere Utility Windows Installer
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - Good!
) else (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo Installing SolSphere Utility as Windows Service...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorLevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Copy configuration template if .env doesn't exist
if not exist ".env" (
    echo Creating configuration file...
    copy config.template .env
    echo.
    echo IMPORTANT: Please edit .env file with your configuration
    echo Backend URL, API key, and other settings need to be configured
    echo.
)

REM Install as Windows service
echo Installing as Windows Service...
python install_service.py
if %errorLevel% neq 0 (
    echo ERROR: Failed to install Windows service
    echo.
    echo You can still run the utility manually:
    echo   .venv\Scripts\activate
    echo   python src\main.py
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The SolSphere Utility is now installed as a Windows service.
echo.
echo Service Details:
echo - Name: SolSphereUtility
echo - Status: Running
echo - Auto-start: Enabled
echo.
echo To manage the service:
echo - Check status: sc query SolSphereUtility
echo - Start: sc start SolSphereUtility
echo - Stop: sc stop SolSphereUtility
echo - Uninstall: python install_service.py uninstall
echo.
echo The utility will automatically:
echo - Start when Windows boots
echo - Monitor system health
echo - Send data to your backend API
echo - Restart on failure
echo.
echo Check Windows Event Viewer for logs.
echo.
pause 