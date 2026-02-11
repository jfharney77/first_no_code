@echo off

set "DEFAULT_PROJ_ROOT=%~dp0.."

call "%~dp0uv_install.bat"

uv run --env-file "%DEFAULT_PROJ_ROOT%\.env" python "%DEFAULT_PROJ_ROOT%\src\servers\m\g\p_m\basic\app.py"
