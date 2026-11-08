# Architecture decision records (proposed unless noted)

## ADR-001 Modular monolith — PROPOSED from Master
Context: small single application. Decision: React static frontend, FastAPI modular backend and PostgreSQL. Consequence: simple deployment and transactional domain logic; scale later only with evidence.

## ADR-002 Deterministic assessment engine — MASTER DIRECTION
No runtime AI. Versioned bank, fixed question order and scoring policy per attempt. Requires approved formula and bank before implementation.

## ADR-003 Versioned immutable content — PROPOSED
Use logical questions and immutable revisions, published template snapshots, attempt question order, result policy version. Consider database enforcement strategy during detailed design.

## ADR-004 Authentication — OPEN
Options: maintained auth library/provider or secure managed identity. Evaluate cookie/session/CSRF, invite flow, admin provisioning, Render compatibility and cost. No selection yet.

## ADR-005 Version/hosting verification — OPEN
Verify official Claude Code frontmatter, permissions, skill discovery; Node/React/Tailwind/Vite compatibility; Python/FastAPI/Pydantic; PostgreSQL/Render options, pricing and regions. No version numbers or compatibility claims verified.

## ADR-006 Testing strategy — PROPOSED
pytest/HTTPX, Vitest/RTL, Playwright UI/API with isolated PostgreSQL and axe accessibility checks; Chrome baseline; expand browser matrix based on CI budget.

## ADR-007 Scoring thresholds — BLOCKED
100-point scale required; exact weight, threshold, rounding, missing answers and readiness descriptors need approved scoring artifact. Do not implement a provisional algorithm as production policy.
