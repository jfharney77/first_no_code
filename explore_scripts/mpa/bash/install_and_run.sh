#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

. "$SCRIPT_DIR/config.sh"
. "$SCRIPT_DIR/uv_install.sh"

WIN_PROJ_ROOT=$(wslpath -w "$DEFAULT_PROJ_ROOT")
wt.exe new-tab --title "$SERVICE_PM_NAME - $P_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv sync && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$P_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_ITM_NAME - $I_T_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$I_T_M_SERVER_PATH\"" \; new-tab --title "$SERVICE_OM_NAME - $O_M_SERVER_PORT" cmd /k "cd /d \"$WIN_PROJ_ROOT\" && uv run --env-file \"$WIN_PROJ_ROOT\\.env\" python \"$WIN_PROJ_ROOT\\$O_M_SERVER_PATH\""
