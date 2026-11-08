# AI Readiness & Quality Engineering Assessment Platform

**Status: v1.1 — assessment flow, participant & admin dashboards, security hardening, CI and a Render demo deployment.**
Admin content management (question lifecycle/publishing) is a later phase and needs separate approval.

> **Draft content:** the question bank in `database/seed/placeholder_bank_v0/` is an original,
> clearly marked **DRAFT / UNVERIFIED placeholder** (ADR-010). It is not research-backed and must be
> replaced by approved content (DEC-01) before any real assessment. The UI shows a permanent banner.

## Stack (versions pinned in ADR-009)
React 19 + TypeScript + Vite, Tailwind 4, shadcn-style components on Radix, React Router, TanStack Query,
React Hook Form + Zod · FastAPI, Pydantic v2, SQLAlchemy 2 + Alembic, pwdlib (Argon2) · PostgreSQL 17 ·
Playwright Test (TypeScript) + axe · pytest · Vitest + Testing Library.

## Local development
Prerequisites: Python 3.12+, Node 22+, Docker.

```bash
make setup        # .env, venv, npm installs, Playwright Chromium, DB up, migrate, seed (dev + test users)
make api          # FastAPI on http://localhost:8000  (docs at /docs)
make web          # Vite on http://localhost:5173     (proxies /api to :8000)
```

Demo accounts (passwords from `.env`: `SEED_ADMIN_PASSWORD` / `SEED_PARTICIPANT_PASSWORD`):
`participant1@example.com`, `participant2@example.com` (participants) and `admin@example.com` (administrator).
There is no self-registration; accounts are created only by the seed CLI.

Other commands: `make db-up | db-down | migrate | seed | seed-test | reset-dev | lint | gen-api`.

## Tests
| Command | What runs |
|---|---|
| `make test-backend` | pytest: unit (scoring engine, policy, security), integration (migrations, seed idempotency, DB constraints, concurrency), API (auth, throttling, security headers, SPA serving, RBAC, attempts, submission, results, dashboards, error envelope). Uses the separate `airqa_test` database. |
| `make test-web` | ESLint, `tsc`, Vitest component tests, production build |
| `make test-e2e` | Playwright projects `setup`, `api` (TC-001/002/004–008/015) and `chromium-e2e` (login, TC-003 flow, results, TC-012 keyboard/responsive, TC-013 axe). Starts API and web servers if not running. |

Playwright workers each use their own seeded account (`e2e-participant-NN`), so specs run in parallel safely.
Expected answers in tests are read from the seed JSON, never from the API.

## Deploy (Render, free plan)
The app ships as one Docker image: FastAPI serves both the API and the built React app (same origin).
1. Push this repository to GitHub.
2. Render Dashboard → **New → Blueprint** → select the repository. `render.yaml` creates the web service and a
   PostgreSQL 17 database (Frankfurt, free).
3. Enter `SEED_ADMIN_PASSWORD` and `SEED_PARTICIPANT_PASSWORD` (at least 12 characters) when prompted.
4. On start the container migrates, seeds the demo bank and accounts (idempotent) and serves the app.

Demo accounts: `demo-admin@example.com`, `demo-participant-1..3@example.com`. The deployed app runs with
`APP_ENV=demo` (ADR-011): production security settings, `/docs` disabled, DRAFT content banner shown.
Free plan: the service sleeps when idle (first request can take ~1 minute) and the free database expires after 30 days.

Local production-like check: `docker build -t airqa:local .` then run it with `DATABASE_URL` and both `SEED_*` passwords.

## CI
`.github/workflows/ci.yml` runs on pushes to `main` and on pull requests: backend (ruff, pytest with PostgreSQL),
frontend (lint, typecheck, Vitest, build) and Playwright (API + UI) with the HTML report uploaded as an artifact.

## Layout
```
backend/      FastAPI app (app/modules/{auth,tracks,content,attempts,scoring,results}), pytest suite
database/     Alembic migrations, docker init SQL, seed bank (placeholder_bank_v0)
frontend/     React SPA (src/pages, src/components, src/api with generated OpenAPI types)
tests/        Playwright: api/, e2e/, pages/ (page objects), fixtures/, data/
docs/         Requirements, ADRs, API contract, design system, test strategy, decisions
```

## Key rules (see CLAUDE.md and docs/architecture/ADRs.md)
- Answer keys never leave the backend before submission; participant DTOs have no key fields.
- Attempts bind to immutable question revisions, scoring policy and recommendation-rule versions.
- Submission is atomic and idempotent (row lock + `UNIQUE(score_results.attempt_id)`).
- Scoring (DEC-02): 5 points per correct answer; bands Foundation 0–39, Developing 40–59,
  Proficient 60–79, Advanced 80–100; competency % rounded half-up; one recommendation per competency < 60%.
- Every error uses `{code, message, details, request_id}` with a matching `X-Request-ID` header.
