#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
PID_FILE="$CLAUDE_DIR/jupyter.pid"

# Limpa jupyter-mcp-server orfaos (parent ja morreu) para nao acumular
# entre sessoes. Instancias ativas de outros projetos sao preservadas.
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='jupyter-mcp-server.exe'\" -ErrorAction SilentlyContinue | ForEach-Object { if (-not (Get-Process -Id \$_.ParentProcessId -ErrorAction SilentlyContinue)) { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue } }" >/dev/null 2>&1

if [ -f "$PID_FILE" ]; then
  PID=$(tr -d '[:space:]' < "$PID_FILE")
  if [ -n "$PID" ]; then
    powershell -NoProfile -Command "Stop-Process -Id $PID -Force -ErrorAction SilentlyContinue; Get-CimInstance Win32_Process -Filter \"ParentProcessId=$PID\" | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1
  fi
  rm -f "$PID_FILE"
fi

exit 0
