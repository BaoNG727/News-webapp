@echo off
echo ==========================================
echo    Django News Portal - Collect Static Files
echo ==========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ==========================================
echo    Static Files Collected!
echo ==========================================
pause
