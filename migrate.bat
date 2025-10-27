@echo off
echo ==========================================
echo    Django News Portal - Database Migration
echo ==========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Backup database
echo [1/3] Creating database backup...
if exist "db.sqlite3" (
    copy /Y db.sqlite3 db.sqlite3.backup
    echo Database backed up to db.sqlite3.backup
) else (
    echo No database found to backup.
)
echo.

REM Make migrations
echo [2/3] Creating migrations...
python manage.py makemigrations
echo.

REM Apply migrations
echo [3/3] Applying migrations...
python manage.py migrate
echo.

echo ==========================================
echo    Migration Complete!
echo ==========================================
pause
