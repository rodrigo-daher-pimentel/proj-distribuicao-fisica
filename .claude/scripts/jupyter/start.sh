#!/usr/bin/env bash
set -u

PORT=8888
TOKEN=427fe4d67f724674110862ccee05d08a
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
PROJECT_DIR="$(dirname "$CLAUDE_DIR")"
LOG_OUT="$CLAUDE_DIR/jupyter.log"
LOG_ERR="$CLAUDE_DIR/jupyter.err.log"
PID_FILE="$CLAUDE_DIR/jupyter.pid"
HEALTH_URL="http://127.0.0.1:$PORT/api?token=$TOKEN"
MAX_WAIT=20

health_check() {
  curl -fsS -m 3 "$HEALTH_URL" >/dev/null 2>&1
}

kill_orphan_mcp_servers() {
  # Mata jupyter-mcp-server cujo parent ja morreu (orfaos de sessoes anteriores).
  # Nao derruba instancias ativas de outros projetos Claude Code rodando em paralelo.
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='jupyter-mcp-server.exe'\" -ErrorAction SilentlyContinue | ForEach-Object { if (-not (Get-Process -Id \$_.ParentProcessId -ErrorAction SilentlyContinue)) { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue } }" >/dev/null 2>&1
}

kill_process_on_port() {
  powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort $PORT -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id \$_.OwningProcess -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1
  sleep 1
}

kill_orphan_mcp_servers

if health_check; then
  exit 0
fi

# Porta ocupada mas API nao responde: processo zumbi, derrubar antes de relancar.
if (echo > /dev/tcp/127.0.0.1/$PORT) 2>/dev/null; then
  kill_process_on_port
fi

WIN_PROJECT_DIR=$(cygpath -w "$PROJECT_DIR")
WIN_LOG_OUT=$(cygpath -w "$LOG_OUT")
WIN_LOG_ERR=$(cygpath -w "$LOG_ERR")
WIN_PID_FILE=$(cygpath -w "$PID_FILE")

powershell -NoProfile -Command "\$p = Start-Process -PassThru -WindowStyle Hidden -FilePath 'jupyter' -ArgumentList 'lab','--port','$PORT','--IdentityProvider.token','$TOKEN','--ip','127.0.0.1','--no-browser' -WorkingDirectory '$WIN_PROJECT_DIR' -RedirectStandardOutput '$WIN_LOG_OUT' -RedirectStandardError '$WIN_LOG_ERR'; \$p.Id | Out-File -Encoding ascii '$WIN_PID_FILE'" >/dev/null 2>&1

# Espera a API responder antes de devolver controle ao Claude Code,
# para que o MCP server nao tente conectar num Jupyter ainda inicializando.
for _ in $(seq 1 $MAX_WAIT); do
  if health_check; then
    exit 0
  fi
  sleep 1
done

exit 1
