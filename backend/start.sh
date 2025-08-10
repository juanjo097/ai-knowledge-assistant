#!/usr/bin/env bash
set -euo pipefail

# 🚀 AI Knowledge Assistant Backend Startup Script

echo "🚀 Starting AI Knowledge Assistant Backend..."

# Go to the script's directory
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Dependency files
REQ_FILE="requirements.txt"
REQ_HASH_FILE="venv/.requirements.sha256"

# --- Helpers -----------------------------------------------------------------
hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    # macOS fallback
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

install_requirements() {
  local force="${1:-false}"

  if [ ! -f "$REQ_FILE" ]; then
    echo "ℹ️  $REQ_FILE not found, skipping dependency installation."
    return 0
  fi

  local new_hash; new_hash="$(hash_file "$REQ_FILE")"
  local old_hash=""; [ -f "$REQ_HASH_FILE" ] && old_hash="$(cat "$REQ_HASH_FILE")"

  if [ "$force" = "true" ] || [ "$new_hash" != "$old_hash" ]; then
    echo "📥 Installing dependencies from $REQ_FILE ..."
    "$PY" -m pip install --upgrade pip setuptools wheel
    "$PY" -m pip install -r "$REQ_FILE"
    echo "$new_hash" > "$REQ_HASH_FILE"
    echo "✅ Dependencies installed/updated."
  else
    echo "✅ Dependencies are up to date (no changes in $REQ_FILE)."
  fi
}
# -----------------------------------------------------------------------------

# Ensure venv exists
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found. Please create and activate it first:"
  echo "   python3 -m venv venv"
  echo "   source venv/bin/activate"
  echo "   pip install -r requirements.txt"
  exit 1
fi

# Activate venv
echo "📦 Activating virtual environment..."
# shellcheck disable=SC1091
source venv/bin/activate

# Ensure we use venv Python
PY="venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "❌ Could not find venv Python executable."
  exit 1
fi

# Flags
FORCE_REINSTALL="false"
while [[ ${1:-} ]]; do
  case "$1" in
    --reinstall|--force) FORCE_REINSTALL="true" ;;
    *) echo "⚠️  Unknown option: $1" ;;
  esac
  shift
done

# Install/update dependencies according to requirements.txt
install_requirements "$FORCE_REINSTALL"

# Start the app
echo "🌐 Starting Flask application..."
echo "   The app will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

exec "$PY" run.py
