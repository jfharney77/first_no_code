#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/config.sh"

stop_service_samewindow() {
    PORT=$1
    NAME=$2

    PID=$(lsof -ti :$PORT 2>/dev/null || fuser $PORT/tcp 2>/dev/null)

    if [ -n "$PID" ]; then
        echo "Stopping $NAME on port $PORT (PID: $PID)..."
        kill $PID
    else
        echo "No service found running on port $PORT ($NAME)."
    fi
}

stop_service_tabs() {
    PORT=$1
    NAME=$2

    TAB_PID=$(powershell.exe -Command "\$p = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue | Select-Object -First 1; if (\$p) { \$proc = Get-Process -Id \$p.OwningProcess; while (\$proc.Parent -and \$proc.Parent.ProcessName -ne 'WindowsTerminal') { \$proc = \$proc.Parent }; \$proc.Id }" | tr -d '\r')

    if [ -n "$TAB_PID" ] && [ "$TAB_PID" != "" ]; then
        echo "Stopping $NAME on port $PORT and closing tab (PID: $TAB_PID)..."
        taskkill.exe /PID "$TAB_PID" /F /T
    else
        echo "No service found running on port $PORT ($NAME)."
    fi
}

if [ "$1" = "samewindow" ]; then
    PIDFILE="$DEFAULT_PROJ_ROOT/.service_pids"
    if [ -f "$PIDFILE" ]; then
        while read -r PID; do
            if kill -0 "$PID" 2>/dev/null; then
                echo "Stopping process (PID: $PID)..."
                kill "$PID" 2>/dev/null
                # Also kill child processes
                pkill -P "$PID" 2>/dev/null
            else
                echo "Process $PID is not running."
            fi
        done < "$PIDFILE"
        rm -f "$PIDFILE"
        echo "All services stopped."
    else
        echo "No PID file found at $PIDFILE. Services may not have been started with samewindow."
    fi
else
    stop_service_tabs $P_M_SERVER_PORT "$SERVICE_PM_NAME"
    stop_service_tabs $I_T_M_SERVER_PORT "$SERVICE_ITM_NAME"
    stop_service_tabs $O_M_SERVER_PORT "$SERVICE_OM_NAME"
    stop_service_tabs $C_S_A_R_M_SERVER_PORT "$SERVICE_CSARM_NAME"
    stop_service_tabs $I_A_R_M_SERVER_PORT "$SERVICE_IARM_NAME"
    stop_service_tabs $O_I_M_SERVER_PORT "$SERVICE_OIM_NAME"
    stop_service_tabs $PR_M_SERVER_PORT "$SERVICE_PRM_NAME"
    stop_service_tabs $T_A_M_SERVER_PORT "$SERVICE_TAM_NAME"
    stop_service_tabs $T_B_M_SERVER_PORT "$SERVICE_TBM_NAME"
    stop_service_tabs $T_D_M_SERVER_PORT "$SERVICE_TDM_NAME"
    stop_service_tabs $T_E_M_SERVER_PORT "$SERVICE_TEM_NAME"
    stop_service_tabs $V_M_SERVER_PORT "$SERVICE_VM_NAME"
    stop_service_tabs $W_MJ_SERVER_PORT "$SERVICE_WMJ_NAME"
fi
