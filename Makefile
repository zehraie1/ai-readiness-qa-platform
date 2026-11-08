# Local development / test commands. See README.md.
PY := backend/.venv/bin/python
.PHONY: setup db-up db-down migrate seed seed-test api web test test-backend test-web test-e2e gen-api lint reset-dev

setup:          ## one-time: env file, venv, npm installs, Playwright browser
	./scripts/dev-setup.sh

db-up:
	docker compose up -d --wait db

db-down:
	docker compose down

migrate:
	cd backend && .venv/bin/alembic upgrade head

seed:           ## demo accounts (admin@example.com, participant1/2@example.com)
	cd backend && .venv/bin/python -m app.cli seed --profile dev

seed-test:      ## e2e accounts used by Playwright
	cd backend && .venv/bin/python -m app.cli seed --profile test

reset-dev:      ## delete all attempts/results (development only)
	cd backend && .venv/bin/python -m app.cli reset-dev --yes

api:
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000

web:
	cd frontend && npm run dev

lint:
	cd backend && .venv/bin/ruff check . && .venv/bin/ruff format --check .
	cd frontend && npm run lint && npm run typecheck

test-backend:   ## uses TEST_DATABASE_URL (airqa_test), recreated per run
	cd backend && .venv/bin/pytest

test-web:
	cd frontend && npm run lint && npm run typecheck && npm test && npm run build

test-e2e: migrate seed-test
	npx playwright test

test: test-backend test-web test-e2e

gen-api:        ## regenerate frontend/src/api/schema.d.ts from a running API
	cd frontend && npm run gen:api
