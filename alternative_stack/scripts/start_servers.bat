@echo off
REM Start both the FastAPI backend and React frontend in separate terminals.
REM Run this script from anywhere — it uses its own location to find the project.

set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%..\backend
set FRONTEND_DIR=%SCRIPT_DIR%..\frontend

echo Starting FastAPI backend...
start "FastAPI Backend" cmd /k "cd /d %BACKEND_DIR% && python -m uvicorn app.main:app --reload"

echo Starting React frontend...
start "React Frontend" cmd /k "cd /d %FRONTEND_DIR% && npm install && npm run dev"

echo.
echo Both servers are starting in separate windows.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
