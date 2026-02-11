@echo off
setlocal enabledelayedexpansion

call "%~dp0config.bat"

if "%~1"=="samewindow" (
    call :stop_service_simple %P_M_SERVER_PORT% "%SERVICE_PM_NAME%"
    call :stop_service_simple %I_T_M_SERVER_PORT% "%SERVICE_ITM_NAME%"
    call :stop_service_simple %O_M_SERVER_PORT% "%SERVICE_OM_NAME%"
) else (
    call :stop_service_tabs %P_M_SERVER_PORT% "%SERVICE_PM_NAME%"
    call :stop_service_tabs %I_T_M_SERVER_PORT% "%SERVICE_ITM_NAME%"
    call :stop_service_tabs %O_M_SERVER_PORT% "%SERVICE_OM_NAME%"
)
goto :eof

:stop_service_simple
set "PORT=%~1"
set "NAME=%~2"
set "PID="

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT% ^| findstr LISTENING') do set "PID=%%a"

if defined PID (
    echo Stopping !NAME! on port !PORT!, PID: !PID!...
    taskkill /PID !PID! /F
) else (
    echo No service found running on port !PORT! [!NAME!].
)
goto :eof

:stop_service_tabs
set "PORT=%~1"
set "NAME=%~2"
set "TAB_PID="

for /f "usebackq delims=" %%a in (`powershell -Command "$p = Get-NetTCPConnection -LocalPort %PORT% -ErrorAction SilentlyContinue | Select-Object -First 1; if ($p) { $proc = Get-Process -Id $p.OwningProcess; while ($proc.Parent -and $proc.Parent.ProcessName -ne 'WindowsTerminal') { $proc = $proc.Parent }; $proc.Id }"`) do set "TAB_PID=%%a"

if defined TAB_PID (
    echo Stopping !NAME! on port !PORT! and closing tab, PID: !TAB_PID!...
    taskkill /PID !TAB_PID! /F /T
) else (
    echo No service found running on port !PORT! [!NAME!].
)
goto :eof
