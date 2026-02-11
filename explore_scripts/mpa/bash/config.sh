#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_PROJ_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
export DEFAULT_PROJ_ROOT

SERVICE_PM_NAME="p_m_1"
SERVICE_ITM_NAME="i_t_m_1"
SERVICE_OM_NAME="o_m"
SERVICE_CSARM_NAME="c_s_a_r_m"
SERVICE_IARM_NAME="i_a_r_m"
SERVICE_OIM_NAME="o_i_mmmm"
SERVICE_PRM_NAME="pr_m"
SERVICE_TAM_NAME="t_a_m"
SERVICE_TBM_NAME="t_b_m"
SERVICE_TDM_NAME="t_d_m"
SERVICE_TEM_NAME="t_e_m"
SERVICE_VM_NAME="v_m"
SERVICE_WMJ_NAME="w_mj"

P_M_SERVER_PORT=6006
I_T_M_SERVER_PORT=6001
O_M_SERVER_PORT=6009
C_S_A_R_M_SERVER_PORT=6013
I_A_R_M_SERVER_PORT=6017
O_I_M_SERVER_PORT=6011
PR_M_SERVER_PORT=6007
T_A_M_SERVER_PORT=6010
T_B_M_SERVER_PORT=6015
T_D_M_SERVER_PORT=6016
T_E_M_SERVER_PORT=6012
V_M_SERVER_PORT=6014
W_MJ_SERVER_PORT=6008

P_M_SERVER_PATH="src/servers/m/g/p_m/basic/app.py"
I_T_M_SERVER_PATH="src/servers/m/g/i_t_m/basic/app.py"
O_M_SERVER_PATH="src/servers/m/g/o_m/basic/app.py"
C_S_A_R_M_SERVER_PATH="src/servers/m/g/c_s_a_r_m/basic/app.py"
I_A_R_M_SERVER_PATH="src/servers/m/g/i_a_r_m/basic/app.py"
O_I_M_SERVER_PATH="src/servers/m/g/o_i_m/basic/app.py"
PR_M_SERVER_PATH="src/servers/m/g/pr_m/basic/app.py"
T_A_M_SERVER_PATH="src/servers/m/g/t_a_m/basic/app.py"
T_B_M_SERVER_PATH="src/servers/m/g/t_b_m/basic/app.py"
T_D_M_SERVER_PATH="src/servers/m/g/t_d_m/basic/app.py"
T_E_M_SERVER_PATH="src/servers/m/g/t_e_m/basic/app.py"
V_M_SERVER_PATH="src/servers/m/g/v_m/basic/app.py"
W_MJ_SERVER_PATH="src/servers/m/g/w_mj/basic/app.py"

. "$SCRIPT_DIR/initialize.sh"
