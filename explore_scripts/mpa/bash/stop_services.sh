#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/config.sh"

stop_service() {
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

stop_service $P_M_SERVER_PORT "$SERVICE_PM_NAME"
stop_service $I_T_M_SERVER_PORT "$SERVICE_ITM_NAME"
stop_service $O_M_SERVER_PORT "$SERVICE_OM_NAME"
