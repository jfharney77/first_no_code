#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_PROJ_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
export DEFAULT_PROJ_ROOT

. "$SCRIPT_DIR/initialize.sh"
. "$SCRIPT_DIR/uv_install.sh"

uv run --env-file "$DEFAULT_PROJ_ROOT/.env" python "$DEFAULT_PROJ_ROOT/src/servers/m/g/p_m/basic/app.py"
