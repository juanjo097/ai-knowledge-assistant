#!/bin/sh
set -eu

# Monorepo Dev Runner (POSIX sh) — uses ./backend/start.sh and Vite in frontend
# Usage:
#   ./dev.sh             # run backend + frontend
#   ./dev.sh --install   # install frontend deps if missing, then run
#
# Optional overrides:
#   FRONT_PORT=5173 BACK_PORT=5000 VITE_API_BASE=http://localhost:5000 ./dev.sh

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
BACK_DIR="$ROOT_DIR/backend"
FRONT_DIR="$ROOT_DIR/frontend"

FRONT_PORT=${FRONT_PORT:-5173}
BACK_PORT=${BACK_PORT:-5000}

DO_INSTALL=0
case "${1:-}" in
  --install|-i) DO_INSTALL=1 ;;
  *) ;;
esac

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }

# --- backend/start.sh checks ---
if [ ! -f "$BACK_DIR/start.sh" ]; then
  log "ERROR: backend/start.sh not found at $BACK_DIR/start.sh"
  exit 1
fi
if [ ! -x "$BACK_DIR/start.sh" ]; then
  log "ERROR: backend/start.sh is not executable. Run: chmod +x backend/start.sh"
  exit 1
fi

# --- validate/create .env ---
ensure_env() {
  env_dir="$1"
  name="$2"
  if [ -f "$env_dir/.env" ]; then
    log "$name: .env OK"
    return
  fi
  if [ -f "$env_dir/.env.example" ]; then
    cp "$env_dir/.env.example" "$env_dir/.env"
    log "$name: .env created from .env.example → $env_dir/.env (please review values)"
    return
  fi
  log "ERROR: $name: .env missing and no .env.example to copy from. Create $env_dir/.env"
  exit 1
}

# --- frontend: install if needed ---
ensure_frontend() {
  cd "$FRONT_DIR"
  if [ "$DO_INSTALL" -eq 1 ] || [ ! -d node_modules ]; then
    log "Installing frontend dependencies..."
    npm install
  fi
  cd "$ROOT_DIR"
}

run_frontend() {
  log "Starting frontend at http://localhost:$FRONT_PORT"
  cd "$FRONT_DIR"
  if [ -z "${VITE_API_BASE:-}" ]; then
    export VITE_API_BASE="http://localhost:$BACK_PORT"
  fi
  npm run dev -- --port "$FRONT_PORT"
}

run_backend() {
  log "Starting backend via ./backend/start.sh"
  cd "$BACK_DIR"
  PORT="$BACK_PORT" FLASK_RUN_PORT="$BACK_PORT" ./start.sh
}

# --- main ---
ensure_env "$BACK_DIR" "backend"
ensure_env "$FRONT_DIR" "frontend"
ensure_frontend

# shut both down on exit
trap 'echo; log "Shutting down..."; kill 0 2>/dev/null || true' INT TERM EXIT

log "Launching servers (Ctrl+C to stop)"
(run_backend) &
BACK_PID=$!
(run_frontend) &
FRONT_PID=$!

wait "$BACK_PID" "$FRONT_PID"
