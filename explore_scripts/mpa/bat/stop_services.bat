@echo off
setlocal enabledelayedexpansion

call "%~dp0config.bat"

if "%~1"=="samewindow" (
    call :stop_service_simple %P_M_SERVER_PORT% "%SERVICE_PM_NAME%"
    call :stop_service_simple %I_T_M_SERVER_PORT% "%SERVICE_ITM_NAME%"
    call :stop_service_simple %O_M_SERVER_PORT% "%SERVICE_OM_NAME%"
    call :stop_service_simple %C_S_A_R_M_SERVER_PORT% "%SERVICE_CSARM_NAME%"
    call :stop_service_simple %I_A_R_M_SERVER_PORT% "%SERVICE_IARM_NAME%"
    call :stop_service_simple %O_I_M_SERVER_PORT% "%SERVICE_OIM_NAME%"
    call :stop_service_simple %PR_M_SERVER_PORT% "%SERVICE_PRM_NAME%"
    call :stop_service_simple %T_A_M_SERVER_PORT% "%SERVICE_TAM_NAME%"
    call :stop_service_simple %T_B_M_SERVER_PORT% "%SERVICE_TBM_NAME%"
    call :stop_service_simple %T_D_M_SERVER_PORT% "%SERVICE_TDM_NAME%"
    call :stop_service_simple %T_E_M_SERVER_PORT% "%SERVICE_TEM_NAME%"
    call :stop_service_simple %V_M_SERVER_PORT% "%SERVICE_VM_NAME%"
    call :stop_service_simple %W_MJ_SERVER_PORT% "%SERVICE_WMJ_NAME%"
) else (
    call :stop_service_tabs %P_M_SERVER_PORT% "%SERVICE_PM_NAME%"
    call :stop_service_tabs %I_T_M_SERVER_PORT% "%SERVICE_ITM_NAME%"
    call :stop_service_tabs %O_M_SERVER_PORT% "%SERVICE_OM_NAME%"
    call :stop_service_tabs %C_S_A_R_M_SERVER_PORT% "%SERVICE_CSARM_NAME%"
    call :stop_service_tabs %I_A_R_M_SERVER_PORT% "%SERVICE_IARM_NAME%"
    call :stop_service_tabs %O_I_M_SERVER_PORT% "%SERVICE_OIM_NAME%"
    call :stop_service_tabs %PR_M_SERVER_PORT% "%SERVICE_PRM_NAME%"
    call :stop_service_tabs %T_A_M_SERVER_PORT% "%SERVICE_TAM_NAME%"
    call :stop_service_tabs %T_B_M_SERVER_PORT% "%SERVICE_TBM_NAME%"
    call :stop_service_tabs %T_D_M_SERVER_PORT% "%SERVICE_TDM_NAME%"
    call :stop_service_tabs %T_E_M_SERVER_PORT% "%SERVICE_TEM_NAME%"
    call :stop_service_tabs %V_M_SERVER_PORT% "%SERVICE_VM_NAME%"
    call :stop_service_tabs %W_MJ_SERVER_PORT% "%SERVICE_WMJ_NAME%"
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
