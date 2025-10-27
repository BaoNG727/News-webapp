@echo off
echo ==========================================
echo    Django News Portal - Run Tests
echo ==========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Running Django tests...
echo.
python manage.py test

echo.
echo ==========================================
echo    Tests Complete!
echo ==========================================
pause
