#!/bin/sh
# Container entrypoint: migrate, seed (idempotent), then serve. Fails fast on any error.
set -eu
cd /app/backend
alembic upgrade head
python -m app.cli seed --profile "${SEED_PROFILE:-demo}"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" \
  --proxy-headers --forwarded-allow-ips="*" --no-server-header
