#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_PROJ_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
export DEFAULT_PROJ_ROOT

SERVICE_PM_NAME="p_m_1"
SERVICE_ITM_NAME="i_t_m_1"
SERVICE_OM_NAME="o_m"

P_M_SERVER_PORT=6006
I_T_M_SERVER_PORT=6001
O_M_SERVER_PORT=6009

P_M_SERVER_PATH="src/servers/m/g/p_m/basic/app.py"
I_T_M_SERVER_PATH="src/servers/m/g/i_t_m/basic/app.py"
O_M_SERVER_PATH="src/servers/m/g/o_m/basic/app.py"

. "$SCRIPT_DIR/initialize.sh"
