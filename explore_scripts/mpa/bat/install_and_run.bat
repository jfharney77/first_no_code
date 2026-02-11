@echo off

call "%~dp0config.bat"
call "%~dp0uv_install.bat"

if "%~1"=="samewindow" (
    echo Starting all services in the current terminal...

    start /b uv run --env-file "%DEFAULT_PROJ_ROOT%\.env" python "%DEFAULT_PROJ_ROOT%\%P_M_SERVER_PATH%"
    echo %SERVICE_PM_NAME% started on port %P_M_SERVER_PORT%

    start /b uv run --env-file "%DEFAULT_PROJ_ROOT%\.env" python "%DEFAULT_PROJ_ROOT%\%I_T_M_SERVER_PATH%"
    echo %SERVICE_ITM_NAME% started on port %I_T_M_SERVER_PORT%

    start /b uv run --env-file "%DEFAULT_PROJ_ROOT%\.env" python "%DEFAULT_PROJ_ROOT%\%O_M_SERVER_PATH%"
    echo %SERVICE_OM_NAME% started on port %O_M_SERVER_PORT%

    echo All services running. Press Ctrl+C to stop.
    pause >nul
) else (
    wt new-tab --title "%SERVICE_PM_NAME% - %P_M_SERVER_PORT%" cmd /k "cd /d \"%DEFAULT_PROJ_ROOT%\" && uv sync && uv run --env-file \"%DEFAULT_PROJ_ROOT%\.env\" python \"%DEFAULT_PROJ_ROOT%\%P_M_SERVER_PATH%\"" ; new-tab --title "%SERVICE_ITM_NAME% - %I_T_M_SERVER_PORT%" cmd /k "cd /d \"%DEFAULT_PROJ_ROOT%\" && uv sync && uv run --env-file \"%DEFAULT_PROJ_ROOT%\.env\" python \"%DEFAULT_PROJ_ROOT%\%I_T_M_SERVER_PATH%\"" ; new-tab --title "%SERVICE_OM_NAME% - %O_M_SERVER_PORT%" cmd /k "cd /d \"%DEFAULT_PROJ_ROOT%\" && uv sync && uv run --env-file \"%DEFAULT_PROJ_ROOT%\.env\" python \"%DEFAULT_PROJ_ROOT%\%O_M_SERVER_PATH%\""
)
