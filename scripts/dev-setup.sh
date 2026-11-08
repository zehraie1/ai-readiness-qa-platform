#!/usr/bin/env bash
# One-time local setup. Safe to re-run. Requires Python 3.12+, Node 22+, Docker.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env ] || cp .env.example .env
python3 -m venv backend/.venv
backend/.venv/bin/pip install -q --upgrade pip
backend/.venv/bin/pip install -q -r backend/requirements-dev.txt
(cd frontend && npm ci)
npm ci
npx playwright install chromium
docker compose up -d --wait db
(cd backend && .venv/bin/alembic upgrade head)
(cd backend && .venv/bin/python -m app.cli seed --profile dev)
(cd backend && .venv/bin/python -m app.cli seed --profile test)
echo "Setup complete. Run 'make api' and 'make web', then open http://localhost:5173"
