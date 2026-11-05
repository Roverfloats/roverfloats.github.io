@echo off
set "ROOT=%~dp0"

start "" /min cmd /c "cd /d "%ROOT%backend" && py server.py"
start "" /min cmd /c "cd /d "%ROOT%frontend" && npm run dev"

timeout /t 3 /nobreak >nul
start "" "http://localhost:5173"
