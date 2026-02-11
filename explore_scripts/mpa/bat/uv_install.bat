@echo off

echo Removing existing .venv...
if exist "%DEFAULT_PROJ_ROOT%\.venv" rmdir /s /q "%DEFAULT_PROJ_ROOT%\.venv"

echo Syncing dependencies with uv...
cd /d "%DEFAULT_PROJ_ROOT%" && uv sync
