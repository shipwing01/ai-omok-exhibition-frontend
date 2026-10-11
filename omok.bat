@echo off
cd /d "%~dp0"
start "AI Omok Local Server" cmd /k "py -m http.server 5500"
timeout /t 2 /nobreak >nul
start "" "http://localhost:5500"
exit