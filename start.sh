#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo 'Python 3 required'; exit 1; }
command -v npm >/dev/null || { echo 'Node.js/npm required'; exit 1; }
if [ ! -d .venv ]; then python3 -m venv .venv; fi
. .venv/bin/activate
pip install -q -r backend/requirements.txt
if [ ! -d frontend/node_modules ]; then (cd frontend && npm install --no-audit --no-fund); fi
export PYTHONPATH="$PWD/backend"
python -c 'from fieldcore.core import init;init()'
uvicorn api.main:app --app-dir backend --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
trap 'kill "$BACKEND_PID" 2>/dev/null || true' EXIT
printf '\nApplication: http://localhost:3000\nBackend: http://localhost:8000/api/health\n'
cd frontend
npm run dev
