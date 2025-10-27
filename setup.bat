@echo off
echo ==========================================
echo    Django News Portal - Auto Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.x from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Checking Python version...
python --version
echo.

REM Create virtual environment if not exists
if not exist "venv" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo [2/6] Virtual environment already exists. Skipping...
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/6] Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create .env file if not exists
if not exist ".env" (
    echo [5/6] Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created! Please edit it with your settings.
) else (
    echo [5/6] .env file already exists. Skipping...
)
echo.

REM Run migrations
echo [6/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo ==========================================
echo    Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo   1. Edit .env file with your SECRET_KEY and settings
echo   2. Create superuser: python manage.py createsuperuser
echo   3. Run server: run.bat or python manage.py runserver
echo.
echo Press any key to create superuser now...
pause >nul

echo.
echo Creating superuser...
python manage.py createsuperuser

echo.
echo ==========================================
echo    All Done! You can now run the server.
echo    Use: run.bat
echo ==========================================
pause
