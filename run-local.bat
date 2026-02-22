@echo off
chcp 65001 >nul
echo ========================================
echo 东莞采购雷达 - 本地运行脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python，请安装 Python 3.10+
    pause
    exit /b 1
)

echo [2/4] 安装/更新依赖...
python -m pip install -r requirements.txt -q

echo [3/4] 运行爬虫...
python main.py
if errorlevel 1 (
    echo 爬虫运行失败！
    pause
    exit /b 1
)

echo [4/4] 推送到 GitHub...
git add index.html
git commit -m "update: 本地自动更新 - %date% %time%"
git push origin gh-pages

echo.
echo ========================================
echo 完成！页面已更新到 GitHub Pages
echo ========================================
pause
