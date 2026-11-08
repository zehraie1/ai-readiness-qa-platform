# Architecture decision records (proposed unless noted)

## ADR-001 Modular monolith — PROPOSED from Master
Context: small single application. Decision: React static frontend, FastAPI modular backend and PostgreSQL. Consequence: simple deployment and transactional domain logic; scale later only with evidence.

## ADR-002 Deterministic assessment engine — MASTER DIRECTION
No runtime AI. Versioned bank, fixed question order and scoring policy per attempt. Requires approved formula and bank before implementation.

## ADR-003 Versioned immutable content — PROPOSED
Use logical questions and immutable revisions, published template snapshots, attempt question order, result policy version. Consider database enforcement strategy during detailed design.

## ADR-004 Authentication — SUPERSEDED by ADR-008
Options: maintained auth library/provider or secure managed identity. Evaluate cookie/session/CSRF, invite flow, admin provisioning, Render compatibility and cost. No selection yet.

## ADR-005 Version/hosting verification — OPEN
Verify official Claude Code frontmatter, permissions, skill discovery; Node/React/Tailwind/Vite compatibility; Python/FastAPI/Pydantic; PostgreSQL/Render options, pricing and regions. No version numbers or compatibility claims verified.

## ADR-006 Testing strategy — PROPOSED
pytest/HTTPX, Vitest/RTL, Playwright UI/API with isolated PostgreSQL and axe accessibility checks; Chrome baseline; expand browser matrix based on CI budget.

## ADR-007 Scoring thresholds — APPROVED V1 (DEC-02)
5 points per correct answer, no partial/negative marking; all 20 answers required. Overall = correct × 5 (0–100); common and role-specific contributions 0–50 each. Competency % = correct ÷ assessed × 100, rounded to nearest whole number **half-up** (Decimal `ROUND_HALF_UP`, e.g. 12.5 → 13); zero denominator → "Not assessed". Bands: Foundation 0–39, Developing 40–59, Proficient 60–79, Advanced 80–100 (internal classification, not an external benchmark). At most one recommendation per assessed competency strictly below 60%, only if a rule exists. Implemented as a pure function in `backend/app/modules/scoring/engine.py`.

## ADR-008 Authentication (Slice 1) — APPROVED with Slice 1 plan
Email/password; password hashing via **pwdlib (Argon2)**; server-side sessions in `user_sessions` (random 32-byte token, only SHA-256 hash stored); cookie `airqa_session` `HttpOnly; SameSite=Lax; Path=/` (`Secure` via `COOKIE_SECURE`). Unsafe methods require an allow-listed `Origin`/`Referer` (CSRF defence). 12h absolute expiry. No self-registration; accounts provisioned by seed CLI only. fastapi-users rejected (maintenance mode, unnecessary registration/verification scope); JWT rejected (no revocation / XSS exposure in storage). Login rate limiting is required before any deployment.

## ADR-009 Pinned versions (Slice 1) — VERIFIED against PyPI/npm registries on 2026-11-08
Backend: Python 3.12, FastAPI 0.162, Pydantic 2.14, pydantic-settings 2.16, SQLAlchemy 2.1, Alembic 1.20, psycopg 3.3, pwdlib 0.3 (argon2), uvicorn 0.54, pytest 9.2, httpx 0.28, ruff 0.17. Frontend: React 19.3, Vite 8.3, TypeScript **5.9.3** (TS 7 not yet supported by openapi-typescript/typescript-eslint), Tailwind 4.3, React Router 8.5, TanStack Query 5.107, React Hook Form 7.91, Zod 4.6, Vitest 5.1. Tests: @playwright/test 1.65, @axe-core/playwright 4.14. Database: PostgreSQL 17 (Docker locally; confirm Render availability before deploy). shadcn/ui components are vendored by hand (copy-in pattern) on Radix primitives. Python tooling: venv + pip with pinned `requirements*.txt` (uv not installed).

## ADR-010 Placeholder question bank — APPROVED for development/test only
Until DEC-01 is satisfied, `database/seed/placeholder_bank_v0/` provides 50 original `[DRAFT]` questions, `PH_`-prefixed competencies and draft recommendation text, with `content_provenance = placeholder_unverified`. The UI shows a permanent draft banner and the seeder refuses to run with `APP_ENV=production`. It is not research-backed and must be replaced by approved content.

## ADR-011 Demo deployment (Render, single origin) — APPROVED 2026-11-08
`APP_ENV=demo` behaves like production (Secure cookies, CSP/HSTS, `/docs` and OpenAPI disabled) but allows the DRAFT placeholder bank (ADR-010) with a permanent banner. Demo accounts come only from the `demo` seed profile and require passwords ≥ 12 characters from environment variables. One Docker image (`Dockerfile`) serves the API and the built SPA from FastAPI, so the session cookie is first-party and no CORS is needed (resolves the Render cross-site cookie risk). `render.yaml` provisions a free web service + free PostgreSQL 17 (Frankfurt); the container runs migrations and the idempotent seed on start (free plan has no pre-deploy hook). `RENDER_EXTERNAL_URL` is added to the CSRF origin allow-list. Free-plan limits: the database expires after 30 days and the service sleeps when idle. Public repository: placeholder answer keys are visible in seed files — acceptable for the demo only; approved content (DEC-01) must never be committed to a public repository.

## ADR-012 Login throttling and security headers — APPROVED 2026-11-08
Failed sign-ins are recorded in `login_attempts` (migration 0002). Within a 15-minute window, 5 failures per email or 20 per client IP return `429 TOO_MANY_ATTEMPTS` with `Retry-After`; a successful sign-in clears that email's failures. Client IP comes from `X-Forwarded-For` via uvicorn `--proxy-headers` in the container. All responses carry `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` and COOP; production-like environments add CSP (`default-src 'self'`, `frame-ancestors 'none'`) and HSTS. Limits are configurable (`LOGIN_*`).
