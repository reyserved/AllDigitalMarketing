#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR"
WORKSPACE_ROOT="$(cd "$APP_DIR/../.." && pwd)"

VENV_DIR="$APP_DIR/.venv"
REQUIREMENTS_FILE="$APP_DIR/requirements.txt"
APP_FILE="$APP_DIR/app.py"
MIN_PORT=8501
MAX_PORT=8520

log() {
  printf '[seo-benchmark-launcher] %s\n' "$1"
}

fail() {
  printf '[seo-benchmark-launcher] ERROR: %s\n' "$1" >&2
  exit 1
}

check_python() {
  if ! command -v python3 >/dev/null 2>&1; then
    fail "python3 is not installed or not available in PATH. Install Python 3 and retry."
  fi
}

create_or_reuse_venv() {
  if [[ ! -d "$VENV_DIR" ]]; then
    log "Creating virtual environment at: $VENV_DIR"
    python3 -m venv "$VENV_DIR" || fail "Failed to create virtual environment. Ensure Python venv module is available."
  else
    log "Reusing existing virtual environment: $VENV_DIR"
  fi

  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    fail "Virtual environment python executable not found at $VENV_DIR/bin/python"
  fi
}

install_dependencies() {
  log "Installing/updating app dependencies from: $REQUIREMENTS_FILE"
  "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE" || fail "Dependency installation failed. Check network/PyPI access and retry."
}

is_port_free() {
  local port="$1"
  "$VENV_DIR/bin/python" - "$port" <<'PY'
import socket
import sys

port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.2)
result = sock.connect_ex(("127.0.0.1", port))
sock.close()
# result != 0 means port is not accepting TCP connections and is likely free.
sys.exit(0 if result != 0 else 1)
PY
}

pick_port() {
  local port
  for port in $(seq "$MIN_PORT" "$MAX_PORT"); do
    if is_port_free "$port"; then
      printf '%s\n' "$port"
      return 0
    fi
  done
  return 1
}

open_browser() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then
    (
      sleep 2
      open "$url" >/dev/null 2>&1 || true
    ) &
  else
    log "macOS 'open' command is unavailable. Open this URL manually: $url"
  fi
}

launch_app() {
  local port="$1"
  local url="http://localhost:${port}"

  log "Workspace: $WORKSPACE_ROOT"
  log "App: $APP_FILE"
  log "Venv: $VENV_DIR"
  log "Selected port: $port"
  log "Launching URL: $url"
  log "Press Ctrl+C to stop the app."

  open_browser "$url"

  exec "$VENV_DIR/bin/streamlit" run "$APP_FILE" --server.port "$port" --server.headless true
}

main() {
  check_python
  create_or_reuse_venv
  install_dependencies

  local selected_port
  if ! selected_port="$(pick_port)"; then
    fail "No free port found in range ${MIN_PORT}-${MAX_PORT}. Free one of these ports and retry."
  fi

  launch_app "$selected_port"
}

main "$@"
