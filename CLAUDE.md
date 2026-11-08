# AI Readiness & Quality Engineering Assessment Platform — Claude Code Instructions

## Mandatory operating mode
**PLANNING ONLY until the project owner explicitly approves implementation.** On first open, read `docs/source/MASTER_INSTRUCTION_V1.md`, `docs/decisions/OPEN_DECISIONS.md`, `docs/research/SOURCE_REGISTER.md`, and `docs/roadmap/IMPLEMENTATION_ROADMAP.md`. In Claude Code Plan Mode, inventory and reconcile these documents; propose a phased implementation plan and STOP. Do not create application source code, install dependencies, run migrations, commit, deploy, or publish content without explicit approval. An instruction to review or plan is not permission to build.

## Mission and boundaries
One independent, accessible, controlled-access QA AI-readiness assessment product. Claude Code is a development-time tool, **never** an application runtime dependency. No LLM API, employer integration, HR ranking, proprietary employer branding, microservices, Cursor configuration, copied certification exam questions or real employee records.

## Authoritative sources
1. Explicitly approved research, competency framework, question bank, scoring specification, BRD/SRS **when supplied**.
2. `docs/source/MASTER_INSTRUCTION_V1.md` for agreed product direction.
3. Approved ADRs and signed-off specifications.
4. Proposals in this starter package are **drafts**, not approvals. When documents conflict, log the conflict and ask rather than silently choosing.

## Invariants
Four assessment tracks: Manual QA Engineer, Automation QA Engineer, SDET, QA Lead. Access roles: Participant and Administrator, independent of tracks. Each assessment has 20 questions: 10 common plus 10 track-specific; baseline 50 unique questions. Correct answers never leave the backend before submission. Attempts persist order and answers; submitted results and published revisions are immutable. Atomic idempotent submission, ownership authorization, deterministic 100-point scoring governed by **approved** rules; no fabricated thresholds, weights or evidence.

## Planned stack (verify versions before installation)
React + TypeScript + Vite, Tailwind, shadcn/ui, React Router, TanStack Query/Table, React Hook Form + Zod, Lucide, Recharts, Vitest/RTL; Python + FastAPI/Pydantic v2, SQLAlchemy 2.x/Alembic, pytest/HTTPX; PostgreSQL; Playwright Test TypeScript + axe; GitHub Actions and Render. Modular monolith. Verify current official compatibility/security advisories before locking versions. No versions have been verified by this package.

## Repository ownership
`frontend/` future UI; `backend/` future API; `database/` future SQL/migrations; `tests/` future Playwright; `docs/` specifications; `.claude/agents/` delegated reviews; `.claude/skills/` task workflows. Folder placeholders are NOT implemented code.

## UX, API and data
Independent navy/light design tokens in `docs/design-system/`. WCAG 2.2 AA target; semantic controls, keyboard access, responsive states, accessible charts. Versioned `/api/v1`, typed DTOs, consistent error envelopes, server-side authorization, no answer-key leakage, no client-authoritative scoring. PostgreSQL constraints, immutable snapshots, least privilege, environment-specific synthetic seeds only.

## Quality gates
Review `docs/testing/TEST_STRATEGY.md`; cover backend unit/integration, frontend unit/component, Playwright UI/API, security/accessibility and reproducibility. Do not report tests as passing unless executed. Commands in `docs/roadmap/COMMANDS_PENDING_VERIFICATION.md` are proposals only; never run destructive commands against production.

## Agent workflow
Single accountable editor per change. Read relevant skill, make small plan, delegate narrow reviews, integrate sequentially, record actual evidence, stop for approvals on auth/scoring/question bank/deployment/architecture/destructive operations. `docs/roadmap/IMPLEMENTATION_ROADMAP.md` governs sequencing. Definition of Done: accepted criteria, API agreement, permissions, automated tests, accessibility, safe data changes, documentation, recorded evidence.

## Safe first response in Claude Code
Summarise supplied artifacts and missing approved research; verify local Claude Code conventions and dependency versions from official docs when access is available; propose Phase 1 plan, unresolved decisions, and file-by-file changes; ask for approval. **Do not implement.**
