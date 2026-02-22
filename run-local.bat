@echo off
chcp 65001 >nul
echo ========================================
echo Dongguan Procurement Radar - Local Run
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python 3.10+
    pause
    exit /b 1
)

echo [2/4] Installing dependencies...
python -m pip install -r requirements.txt -q

echo [3/4] Running crawler...
python main.py
if errorlevel 1 (
    echo Crawler failed!
    pause
    exit /b 1
)

echo [4/4] Pushing to GitHub...
git add index.html
git commit -m "update: Local auto update - %date% %time%"
git push origin gh-pages

echo.
echo ========================================
echo Done! Page updated to GitHub Pages
echo ========================================
pause
