#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

. "$SCRIPT_DIR/config.sh"

if [ "$1" = "samewindow" ]; then
    . "$SCRIPT_DIR/uv_install.sh"

    PIDFILE="$DEFAULT_PROJ_ROOT/.service_pids"
    > "$PIDFILE"

    echo "Starting all services in the current terminal..."

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$P_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_PM_NAME started on port $P_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$I_T_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_ITM_NAME started on port $I_T_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$O_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_OM_NAME started on port $O_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$C_S_A_R_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_CSARM_NAME started on port $C_S_A_R_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$I_A_R_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_IARM_NAME started on port $I_A_R_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$O_I_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_OIM_NAME started on port $O_I_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$PR_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_PRM_NAME started on port $PR_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$T_A_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_TAM_NAME started on port $T_A_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$T_B_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_TBM_NAME started on port $T_B_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$T_D_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_TDM_NAME started on port $T_D_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$T_E_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_TEM_NAME started on port $T_E_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$V_M_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_VM_NAME started on port $V_M_SERVER_PORT (PID: $!)"

    uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/$W_MJ_SERVER_PATH" &
    echo "$!" >> "$PIDFILE"
    echo "$SERVICE_WMJ_NAME started on port $W_MJ_SERVER_PORT (PID: $!)"

    echo "All services running. PIDs saved to $PIDFILE"
    echo "Press Ctrl+C to stop."
    wait
else
    rm -rf "$DEFAULT_PROJ_ROOT/.venv"
    WIN_PROJ_ROOT=$(wslpath -w "$DEFAULT_PROJ_ROOT")
    wt.exe new-tab --title "$SERVICE_PM_NAME - $P_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv sync && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$P_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_ITM_NAME - $I_T_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$I_T_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_OM_NAME - $O_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$O_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_CSARM_NAME - $C_S_A_R_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$C_S_A_R_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_IARM_NAME - $I_A_R_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$I_A_R_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_OIM_NAME - $O_I_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$O_I_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_PRM_NAME - $PR_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$PR_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_TAM_NAME - $T_A_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$T_A_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_TBM_NAME - $T_B_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$T_B_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_TDM_NAME - $T_D_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$T_D_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_TEM_NAME - $T_E_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$T_E_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_VM_NAME - $V_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$V_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_WMJ_NAME - $W_MJ_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$W_MJ_SERVER_PATH\""
fi
