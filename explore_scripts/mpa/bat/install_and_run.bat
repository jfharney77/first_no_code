@echo off

call "%~dp0config.bat"
call "%~dp0uv_install.bat"

wt new-tab --title "%SERVICE_PM_NAME% - %P_M_SERVER_PORT%" cmd /k "cd /d \"%DEFAULT_PROJ_ROOT%\" && uv sync && uv run --env-file \"%DEFAULT_PROJ_ROOT%\.env\" python \"%DEFAULT_PROJ_ROOT%\%P_M_SERVER_PATH%\"" ; new-tab --title "%SERVICE_ITM_NAME% - %I_T_M_SERVER_PORT%" cmd /k "cd /d \"%DEFAULT_PROJ_ROOT%\" && uv sync && uv run --env-file \"%DEFAULT_PROJ_ROOT%\.env\" python \"%DEFAULT_PROJ_ROOT%\%I_T_M_SERVER_PATH%\"" ; new-tab --title "%SERVICE_OM_NAME% - %O_M_SERVER_PORT%" cmd /k "cd /d \"%DEFAULT_PROJ_ROOT%\" && uv sync && uv run --env-file \"%DEFAULT_PROJ_ROOT%\.env\" python \"%DEFAULT_PROJ_ROOT%\%O_M_SERVER_PATH%\""
