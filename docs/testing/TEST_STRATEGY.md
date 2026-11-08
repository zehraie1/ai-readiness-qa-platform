# Quality and Playwright TypeScript strategy — PLANNED ONLY

## Test pyramid and environments
Backend pytest/HTTPX domain, auth, persistence and API integration tests against disposable PostgreSQL; frontend Vitest/React Testing Library component tests; Playwright TypeScript browser and API flows with seeded isolated accounts. Chromium baseline, Firefox/WebKit after CI budget approval. Never use production data or destructive tests on live systems.

## Planned Playwright layout
`tests/e2e/` participant/admin journeys; `tests/api/` auth, contracts, attempts; `tests/fixtures/` typed authenticated fixtures and API setup/teardown; `tests/pages/` minimal reusable abstractions; `tests/data/` deterministic builders. Future `playwright.config.ts` will configure baseURL, retries, HTML report, traces and screenshot on failure. Not created now because it would be executable test configuration.

## Required scenarios
- Track selection: four tracks, 10 common + 10 matching role-specific, no duplicate question IDs.
- Start/save/resume/review/submit; persisted order, unanswered UI, confirm dialog, no edits after submit.
- Deterministic score and competency/recommendation rules only after approved fixtures exist.
- Invalid option, wrong question, wrong owner, unauthorized admin, pre-submit answer-key leakage.
- Double/concurrent submit, stale writes, transaction rollback and unique result.
- Admin create/edit/review/validate/publish/retire; missing evidence and duplicate mapping failures.
- Response DTOs, error envelopes, pagination, 401/403/404/409/422 behavior.
- Responsive layouts, keyboard/focus, accessible chart alternatives, `@axe-core/playwright` supplemented by manual review.
- Seed idempotency, test isolation, cleanup, CI trace/report retention without secrets.

## Locator and reliability policy
Prefer `getByRole`, `getByLabel`, scoped `getByText`; use test IDs only where semantics insufficient. No arbitrary sleeps, brittle CSS/XPath or order-dependent tests. Prefer API setup and teardown. Pin approved test bank versions and scoring fixtures.

## Evidence and release gates
Report actual commands, environment, commit, passed/failed/skipped counts, artifacts, accessibility exceptions and open risks. All coverage here is planned; no tests have been executed.
