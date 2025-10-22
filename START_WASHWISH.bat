@echo off
title WashWish Laundry Management System
color 0B
cls

echo.
echo ============================================
echo    WashWish Laundry Management System
echo ============================================
echo.

cd /d "d:\PROJECT_RENDER\WASHWISH"

echo [1/4] Checking system...
python manage.py check >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: System check failed!
    echo Please ensure Django is installed: pip install -r requirements.txt
    pause
    exit /b 1
)
echo SUCCESS: System check passed

echo.
echo [2/4] Setting up database...
python manage.py migrate >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Database setup failed!
    pause
    exit /b 1
)
echo SUCCESS: Database ready

echo.
echo [3/4] Preparing application...
python manage.py collectstatic --noinput >nul 2>&1
python manage.py populate_data >nul 2>&1
echo SUCCESS: Application ready

echo.
echo [4/4] Starting server...
echo.
echo ============================================
echo    SERVER INFORMATION
echo ============================================
echo URL: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo Username: admin
echo Password: admin123
echo ============================================
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

start http://127.0.0.1:8000

echo.
echo Server starting... Press Ctrl+C to stop
echo ============================================
echo.

python manage.py runserver 127.0.0.1:8000