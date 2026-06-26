@echo off
title LLM Wiki Launcher
echo ====================================================
echo  Shinsung Tongsang FONE PI - LLM Wiki Launcher
echo ====================================================
echo.

REM Move to script directory
cd /d "%~dp0"

echo [1/3] Running wiki auto indexing...
python tools\wiki_auto_index.py --no-log

echo.
echo [2/3] Starting wiki watcher (background)...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\start_wiki_watcher.ps1

echo.
echo [3/3] Starting LLM wiki web service (background)...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\start_web_service.ps1

echo.
echo ====================================================
echo  Launch Process Completed!
echo  - Port Check: Please open .wiki_state\web.port
echo ====================================================
echo.
pause
