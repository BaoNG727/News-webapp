@echo off
echo ==========================================
echo    Django News Portal - Development Server
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if migrations are needed
echo.
echo Checking for database migrations...
python manage.py makemigrations --check --dry-run >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Pending migrations detected!
    echo Running migrations...
    python manage.py makemigrations
    python manage.py migrate
    echo.
)

REM Start development server
echo.
echo ==========================================
echo    Starting Development Server...
echo    Server will be available at:
echo    http://127.0.0.1:8000/
echo.
echo    Press Ctrl+C to stop the server
echo ==========================================
echo.

python manage.py runserver

pause
