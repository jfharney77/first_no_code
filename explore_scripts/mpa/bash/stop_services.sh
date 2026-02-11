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
    stop_service_samewindow $P_M_SERVER_PORT "$SERVICE_PM_NAME"
    stop_service_samewindow $I_T_M_SERVER_PORT "$SERVICE_ITM_NAME"
    stop_service_samewindow $O_M_SERVER_PORT "$SERVICE_OM_NAME"
else
    stop_service_tabs $P_M_SERVER_PORT "$SERVICE_PM_NAME"
    stop_service_tabs $I_T_M_SERVER_PORT "$SERVICE_ITM_NAME"
    stop_service_tabs $O_M_SERVER_PORT "$SERVICE_OM_NAME"
fi
