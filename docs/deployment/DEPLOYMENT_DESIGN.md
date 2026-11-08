# GitHub/Render deployment design — NOT DEPLOYED

Single private GitHub monorepo. Planned GitHub Actions: lint/typecheck/test frontend; lint/pytest/migration review backend; OpenAPI contract checks; isolated Playwright UI/API smoke; dependency/secret scans; sanitized artifacts. Protected main branch, PR checks, manual deployment approval.

Target: Render static React/Vite frontend, Render FastAPI web service and managed PostgreSQL with restricted access, backups and separate staging/production credentials. HTTPS, CORS allowlist, secure session/cookies as appropriate to auth ADR, least privilege, secrets via environment. Do not assume URL secrecy is access control. Verify official Render pricing, regions, private networking, service support and backup options before finalizing `render.yaml`.

Rollback: versioned frontend/backend release, compatible Alembic migration plan, DB backup/restore exercise, smoke and authorization verification. Never automatically run destructive downgrade in production. No `render.yaml`, CI workflow or deployment commands are active in this planning package.
