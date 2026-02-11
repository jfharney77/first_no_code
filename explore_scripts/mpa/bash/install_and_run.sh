#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

. "$SCRIPT_DIR/config.sh"
. "$SCRIPT_DIR/uv_install.sh"

if [ "$1" = "samewindow" ]; then
    echo "Starting all services in the current terminal..."

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$P_M_SERVER_PATH" &
    echo "$SERVICE_PM_NAME started on port $P_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$I_T_M_SERVER_PATH" &
    echo "$SERVICE_ITM_NAME started on port $I_T_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$O_M_SERVER_PATH" &
    echo "$SERVICE_OM_NAME started on port $O_M_SERVER_PORT (PID: $!)"

    echo "All services running. Press Ctrl+C to stop."
    wait
else
    WIN_PROJ_ROOT=$(wslpath -w "$DEFAULT_PROJ_ROOT")
    wt.exe new-tab --title "$SERVICE_PM_NAME - $P_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv sync && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$P_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_ITM_NAME - $I_T_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$I_T_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_OM_NAME - $O_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$O_M_SERVER_PATH\""
fi
