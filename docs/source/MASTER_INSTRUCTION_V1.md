# PROJECT 01 — AI READINESS & QUALITY ENGINEERING ASSESSMENT PLATFORM

> **Master implementation brief for Claude Code.** This document defines what to build, how to organise Claude Code agents and skills, and the order in which to deliver the work. It is **not** an assertion that any feature, tool, skill, test or deployment already exists.
>
> **Project boundary:** This is an independently developed professional development goal for a Quality Engineering practitioner. It is **not** an official employer product, is not affiliated with or endorsed by any named organisation, and must not use employer logos, proprietary design tokens, confidential information or internal systems without permission.

I want you to act as a **Principal Software Architect, Senior Full-Stack Engineer, Product Owner, Quality Engineering Lead, UX/UI Design Systems Engineer, Database Architect, Security Reviewer, Playwright Automation Architect, DevOps Engineer, and Claude Code Agent/Skills Engineer**.

Work on **one application**: the AI Readiness & Quality Engineering Assessment Platform. Build its full-stack application and its **Playwright TypeScript UI/API test automation**. Do not create the other projects, training exercises or unrelated frameworks from the TaskPilot example.

## 1. Project Objective and Operating Principles

Build a **real, deployable, responsive, accessible, professional web application** that assesses AI-related knowledge and practical Quality Engineering readiness for different QA roles.

The application **assesses knowledge about AI but does not require an AI model or AI service at runtime**. Question delivery, marking, competency scores, readiness levels and learning recommendations must be deterministic, explainable and testable. **Claude Code is the development assistant, not an application dependency.** Do not add LLM APIs, chatbots, prompt submissions, AI scoring or external model calls unless a later, explicitly approved requirement changes this scope.

Primary outcomes:

1. Demonstrate an end-to-end professional software development lifecycle: discovery, requirements, architecture, design, implementation, verification and deployment.
2. Deliver a polished employee-facing assessment experience and a permission-controlled administrative interface.
3. Use a research-backed, original question bank and transparent, versioned scoring rules.
4. Provide meaningful, evidence-based results and rule-based improvement recommendations.
5. Build a maintainable Playwright TypeScript framework for UI, API, accessibility-focused and regression testing.
6. Deploy to a controlled-access environment suitable for demonstrating the professional development goal.

**Non-goals:** task management, student workshops, an official company assessment product, enterprise HR integration, predictive AI, invented external benchmarks, public employee rankings, Selenium/Cucumber/Java automation, microservices, and excessive authentication complexity.

**Source-of-truth rule:** Treat the approved project research, competency framework, question bank, scoring specification, BRD and SRS as authoritative **only when those artifacts are actually supplied or verified in the repository**. Never invent their exact wording, question answers, benchmark numbers, scoring thresholds, weights or citations. If absent, create a clearly marked draft and request approval before treating it as final.

## 2. Required Technology Stack — Current, Stable, Compatible

Before generating installation commands, **verify current official documentation, stable releases, compatibility matrices and security advisories**. Prefer maintained stable versions, lock dependencies and record verified versions in an architecture decision record (ADR). Do not assume the newest major release is compatible with every dependency.

### Frontend

- **React + TypeScript + Vite** for a clean frontend/backend separation and straightforward Render static-site deployment.
- **Tailwind CSS**, using the version-compatible setup documented by Tailwind.
- **shadcn/ui** as the accessible component foundation; verify compatibility with the selected React/Tailwind versions.
- **React Router** for navigation and guarded routes.
- **TanStack Query** for API caching, loading, retries and invalidation.
- **TanStack Table** for admin question tables and assessment history.
- **React Hook Form + Zod** for forms and client-side validation.
- **Lucide React** for icons and **Recharts** for accessible, clearly labelled results charts.
- A **typed fetch client** or compatible OpenAPI-generated TypeScript client; do not introduce Axios without a clear reason.
- **Vitest + React Testing Library** for frontend unit/component tests.

### Backend

- **Python** on a currently supported stable version compatible with the selected libraries.
- **FastAPI + Pydantic v2** for REST APIs, schemas, validation and OpenAPI.
- **SQLAlchemy 2.x + Alembic** for database access and migrations.
- **Uvicorn** (or a verified supported production server configuration).
- **pytest + HTTPX** for unit/integration/API tests.
- A modular monolith with API routers, schemas, services, repositories/data-access and domain policies; avoid needless layers.
- Structured logging, health/readiness checks, request IDs and configuration through environment variables.

### Database

- **PostgreSQL**, with version selected based on current hosting compatibility.
- Explicit schema constraints, indexes, foreign keys, migrations and idempotent, deterministic synthetic seeds.
- Transactions and concurrency-safe submission handling.
- Prefer PostgreSQL for integration tests; use disposable isolated test databases where practical.

### Playwright and Quality Tooling

- **Playwright Test + TypeScript** for end-to-end browser testing and API request tests.
- Chromium as the baseline; Firefox/WebKit coverage according to agreed CI budget.
- Playwright traces, HTML reports, screenshots on failure and CI artifacts.
- `@axe-core/playwright` where appropriate to supplement (not replace) manual accessibility review.
- ESLint, Prettier, TypeScript strict mode, Ruff, Python type checks as appropriate, dependency/security checks and GitHub Actions.

### Development and Delivery

- **Claude Code** as the agentic development environment; **not Cursor**.
- Root **`CLAUDE.md`**, optional scoped `CLAUDE.md` guidance, **`.claude/agents/`**, **`.claude/skills/<skill-name>/SKILL.md`**, and **`.claude/settings.json`** where supported by verified Claude Code documentation.
- Git, GitHub, GitHub Actions, optional Jira-ready artifacts, Mermaid, Render static frontend, Render backend service and managed PostgreSQL.
- Optional open-source UI/agent references (inspect licensing, maintenance and installation instructions before adopting):
  - https://github.com/hungdqdesign/ui-ux-pro-max-skill
  - https://github.com/vercel-labs/agent-skills
- Treat reference repositories as **inspiration only**; do not claim they are installed, copy unreviewed instructions, or silently import code or brand assets.

## 3. Independent UI Design System and Design Intelligence

Create an **original, neutral, professional Quality Engineering SaaS identity**. Do not use the employer name, logo, official colours, proprietary website layouts, or imply affiliation. Use the descriptive project title until an original product name is approved; do not use TaskPilot or the previously suggested informal product name.

### Design principles

- Professional, trustworthy, modern, restrained, evidence-led and task-focused.
- **Dashboard:** refined enterprise SaaS composition with dark navy sidebar, light content area, clear cards, concise metrics, meaningful charts and restrained iconography.
- **Assessment:** distraction-free one-question-at-a-time flow, prominent progress, readable choices, keyboard support, save/resume feedback and explicit submission confirmation.
- **Admin:** information-dense but accessible tables, filters, edit workflows, publishing controls and audit-friendly metadata.
- Avoid gimmicky AI illustrations, visual clutter, excessive gradients, animations that obstruct tasks, colour-only meaning and deceptive performance claims.

### Proposed independent design tokens (starting point; validate contrast)

| Token | Value | Intended use |
|---|---|---|
| `--navy-900` | `#17243B` | Sidebar, high-emphasis headings |
| `--blue-600` | `#2563EB` | Primary actions, focus accents |
| `--blue-700` | `#1D4ED8` | Hover/pressed actions |
| `--canvas` | `#F8FAFC` | Main app background |
| `--surface` | `#FFFFFF` | Cards, forms, dialogs |
| `--text-primary` | `#0F172A` | Primary text |
| `--text-muted` | `#475569` | Supporting text |
| `--border` | `#E2E8F0` | Dividers and controls |
| `--success` | `#0F766E` | Success with accessible text pairing |
| `--warning` | `#B45309` | Warning with accessible text pairing |
| `--danger` | `#B91C1C` | Errors and destructive actions |

- Typography: **Inter** with sensible system fallbacks; scale for display, page heading, section heading, body, label and caption.
- Spacing: 4/8/12/16/24/32/48/64 px; consistent layout and whitespace.
- Radii: 8 px controls, 12 px cards; clear borders, restrained shadows.
- Responsive layout: mobile-first, tablet and desktop; sidebar collapses to accessible navigation on small screens.
- Accessibility: **WCAG 2.2 AA target**, keyboard operability, visible focus, semantic landmarks, labelled inputs, accessible charts and reduced-motion support.
- Prefer design tokens and reusable shadcn/ui-based components over one-off styling.

### Required design-system deliverables

Document tokens, typography, spacing, elevation, component states, responsive rules, accessibility patterns and interaction rules. Implement reusable `Button`, `Input`, `Select`, `RadioGroup`, `Card`, `Dialog`, `Alert`, `Badge`, `Tabs`, `Table`, `Pagination`, `Progress`, `Skeleton`, `EmptyState`, `ScoreCard`, `CompetencyChart`, `QuestionCard`, `AssessmentStepper`, `ResultSummary` and `ConfirmSubmitDialog` as appropriate. Prefer accessible roles/names in Playwright; use stable `data-testid` only when semantic selectors are insufficient.

## 4. Application Functional Requirements

### 4.1 Roles and permissions

Assessment personas: **Manual QA Engineer, Automation QA Engineer, SDET, QA Lead**. These are *assessment tracks*, not automatically system permissions.

System access roles: **Participant** and **Administrator**. A participant can access only their own assessments/results; an administrator can manage approved content/configuration and view authorised aggregate reporting. Define the permissions matrix before implementation. Use a simple secure authentication solution suitable for controlled-access deployment; never rely solely on frontend route guards. Avoid exposing real employee data or assuming company SSO.

### 4.2 Participant dashboard

- Welcome/overview and selected QA assessment track.
- Assessment status: not started, in progress, submitted/completed.
- Start/resume assessment and most recent score if available.
- Competency snapshot, strengths and areas for improvement.
- Assessment history and rule-based learning recommendations.
- Helpful loading, empty, error and permission-denied states.

### 4.3 Assessment workflow

- Select/confirm QA role and review instructions before starting.
- **20 questions per assessment: 10 common + 10 role-specific**, drawn from the approved bank; four role tracks imply **10 shared + 40 role-specific = 50 unique questions** when the bank follows this structure.
- One question at a time with four answer options **only if that matches the approved bank schema**.
- Progress display, previous/next, unanswered state, save/resume and review-before-submit.
- Server-authoritative assessment attempt state, question order and answer persistence.
- Deterministic question selection and ordering for reproducible testing; if randomisation is added, persist the seed/order and never change a live attempt.
- No answer keys or correct answers in participant-facing API responses before submission.
- Explicit final confirmation, idempotent submission and prevention of answer edits after final submission.
- Appropriate rules for time limits, retakes and incomplete attempts **only after product approval**; do not invent policies.

### 4.4 Scoring, readiness and recommendations

- **100-point overall scale** using a documented, deterministic calculation and the approved scoring specification.
- Clearly distinguish overall score, common knowledge score, role-specific score and competency-level performance.
- Readiness labels, weights, thresholds, rounding and handling of missing answers must come from the approved scoring artifact. If absent, propose a transparent provisional scheme for approval; do not present it as an established benchmark.
- Explain how each score is calculated and ensure identical answers always yield identical results for the same assessment version.
- Generate recommendations through a versioned rules table mapping competency gaps/score ranges to predefined learning actions.
- Never describe internal readiness levels as externally validated industry benchmarks without supporting evidence.

### 4.5 Results and reporting

- Overall score out of 100 and transparent readiness descriptor.
- Competency breakdown with accessible chart and text/table alternative.
- Strengths, improvement areas and deterministic recommendations.
- Assessment date, role, attempt ID and scoring/content version.
- Assessment history; comparison across attempts only when versions are meaningfully comparable.
- Optional export/print if approved; avoid collecting unnecessary personal data.

### 4.6 Administrator interface

- Admin overview: question counts by track/competency, published bank version, assessment completion aggregates and data quality warnings.
- Question management: create, view, edit, archive, filter and search; role applicability, competency, difficulty (if approved), four options, correct option, explanation, source/evidence reference, status and version.
- **Draft → review → published → retired** content lifecycle, with publishing validation and immutable snapshots for submitted attempts.
- Scoring and recommendation configuration, with explicit versioning and safe change controls.
- Audit-friendly records of content edits and publishing actions.
- Use aggregate reports by default; no unnecessary employee ranking or sensitive HR decisions.

### 4.7 Research-backed content governance

- Map questions to the approved competency framework and original research evidence register.
- Reference frameworks such as ISTQB AI-related syllabi, NIST AI RMF and other approved sources accurately, with citations where licensed/appropriate.
- Write **original** questions; do not reproduce copyrighted certification examination items.
- Every published question must have an unambiguous answer, explanation, competency mapping and review status.
- Separate source claims, internal interpretations and proposed product policy.

## 5. REST API Contracts and Validation

Use versioned endpoints under `/api/v1`, FastAPI-generated OpenAPI, typed request/response DTOs, pagination, filtering, consistent error envelopes and explicit authentication/authorisation. These are **proposed contracts**, to refine during the API design phase.

### Identity and profile

- `GET /api/v1/me` — current participant and access permissions.
- Authentication endpoints depend on the approved auth approach; do not design insecure custom password storage.

### Assessment catalog and attempts

- `GET /api/v1/assessment-tracks` — available QA tracks and public metadata.
- `POST /api/v1/attempts` — start an attempt for an approved track; returns attempt metadata and permitted question payload.
- `GET /api/v1/attempts/{attempt_id}` — resume own attempt and saved responses.
- `PUT /api/v1/attempts/{attempt_id}/answers/{question_id}` — upsert answer while open.
- `GET /api/v1/attempts/{attempt_id}/review` — unanswered/answered summary, no leaked keys.
- `POST /api/v1/attempts/{attempt_id}/submit` — atomic, idempotent submission and scoring.
- `GET /api/v1/attempts` — paginated own history.
- `GET /api/v1/attempts/{attempt_id}/results` — authorised results after submission.
- `GET /api/v1/attempts/{attempt_id}/recommendations` — rule-based recommendations.

### Participant dashboard

- `GET /api/v1/dashboard/summary` — current user's statuses and summary metrics.

### Admin endpoints (administrator-only)

- `GET /api/v1/admin/questions` and `POST /api/v1/admin/questions`.
- `GET /api/v1/admin/questions/{id}` and `PATCH /api/v1/admin/questions/{id}`.
- `POST /api/v1/admin/question-banks/{version_id}/validate`.
- `POST /api/v1/admin/question-banks/{version_id}/publish`.
- `GET /api/v1/admin/competencies`.
- `GET /api/v1/admin/scoring-configurations`.
- `GET /api/v1/admin/recommendation-rules`.
- `GET /api/v1/admin/dashboard/summary`.

### Operational endpoints

- `GET /health` — liveness; `GET /ready` — readiness where supported.

### API quality rules

- Define OpenAPI schemas, success codes, 400/401/403/404/409/422 behaviour and a stable error shape (`code`, `message`, optional `details`, `request_id`).
- Validate server-side: ownership, role, published version, allowed question IDs, option membership, attempt state, answer cardinality and submission completeness policy.
- Apply transactions, database uniqueness constraints and idempotency semantics to avoid duplicate attempts/submissions or inconsistent scores.
- Prevent insecure direct object references and answer-key leakage; apply rate limits where appropriate.
- Produce an OpenAPI-derived or otherwise type-checked frontend client and contract tests; keep API/UI versions aligned.

## 6. Data Model, SQL, Migrations and Synthetic Seed Data

### Proposed core entities

- `users` — minimal profile and system role, with auth provider identifier as appropriate.
- `assessment_tracks` — four QA role tracks.
- `competencies` — approved taxonomy and descriptions.
- `question_bank_versions` — draft/published/retired version metadata.
- `questions` — stable logical question IDs and bank membership.
- `question_revisions` — immutable question text/options/correct option/explanation/evidence/competency mappings.
- `assessment_templates` / `assessment_template_questions` — approved 10-common + 10-role-specific composition per track/version.
- `assessment_attempts` — participant, track, snapshot/version, status, timestamps, persisted question order.
- `attempt_answers` — attempt/question/selected option and timestamps; unique per attempt/question.
- `score_results` / `competency_scores` — immutable results, scoring policy version and breakdown.
- `scoring_policies` — versioned weights, thresholds and rounding rules.
- `recommendation_rules` / `result_recommendations` — versioned rules and generated recommendations.
- `content_audit_events` — admin changes and publication events.

Refine the ERD to avoid redundant tables while preserving published-question immutability, reproducibility and data integrity. Prefer database-level constraints and indexes on foreign keys, status, participant history and question filtering.

### Seed strategy

1. Load **only approved** research-backed competencies, the 50-question structure and scoring configuration if source artifacts are available.
2. If the actual question bank is missing, create a **clearly labelled synthetic/demo dataset**, not a fabricated reproduction of the researched bank; require approval before production publication.
3. Include exactly four tracks and verify 10 shared + 10 unique role-specific questions per track in the approved baseline.
4. Seed deterministic demo participants, admins, draft/published bank versions, sample in-progress/submitted attempts, scores and recommendation examples; **no real employee information**.
5. Make seeds idempotent, rerunnable and environment-aware; never seed demo passwords or secret keys into production.
6. Provide explicit migration, seed, reset and rollback guidance, with destructive operations restricted to development/test environments.

### SQL and query requirements

Provide representative PostgreSQL DDL, foreign keys, unique constraints, indexes and transaction boundaries; include parameterised SQL/SQLAlchemy queries for:

- Selecting the approved question set for a role and bank version.
- Retrieving a participant's own attempts with pagination.
- Counting completed/in-progress assessments for dashboard cards.
- Computing competency score aggregates from immutable submitted answers.
- Fetching weak competencies and matching recommendation rules.
- Admin question filtering by role, competency, status and bank version.
- Validating question-bank completeness and detecting missing evidence/duplicate mappings.

Never rely on frontend-only scoring or unrestricted admin queries.

## 7. Playwright Automation — Part of This Project

Implement **Playwright TypeScript UI + API automation** for the application as a first-class project workstream. This is the Playwright capability inspired by the source example's Project 02; **do not create a separate TaskPilot/TestPilot product**.

### Framework structure and patterns

- `tests/e2e/` — participant and admin user journeys.
- `tests/api/` — authentication/permissions, contracts, validation and attempt lifecycle.
- `tests/fixtures/` — typed fixtures, authenticated contexts, seeded test accounts and API helpers.
- `tests/pages/` or `tests/components/` — lightweight page/component abstractions only when useful.
- `tests/data/` — deterministic test data builders; avoid dependence on production records.
- `playwright.config.ts` — base URL, projects, retries, traces, reporter and CI settings.
- Prefer `getByRole`, `getByLabel`, `getByText` with appropriate scoping; use `data-testid` for difficult-to-target nonsemantic elements.
- Avoid fixed sleeps and brittle CSS/XPath selectors; use auto-waiting and reliable assertions.

### Minimum test coverage

- Role selection and the correct 10-common/10-role-specific composition.
- Starting, answering, saving, resuming, reviewing and submitting an assessment.
- Correct deterministic score, competency breakdown and recommendations.
- Empty/unanswered answers, invalid options, double submission and stale-state conflicts.
- Participant cannot access another participant's attempts/results.
- Participant cannot call admin APIs or open admin pages.
- Admin draft/edit/review/publish workflow and bank validation failures.
- API response schemas, HTTP status codes, error envelopes and data integrity.
- Responsive smoke tests, keyboard navigation and automated accessibility checks.
- Seed isolation, repeatable runs, test data cleanup and non-flaky CI execution.

Use **API setup/teardown** and isolated database/test environments where practical. Include smoke, regression and API test tags/projects, CI artifacts and a clear local execution guide. Never run destructive tests against production.

## 8. Claude Code Agentic Architecture, CLAUDE.md and Skills

**Do not create `.cursor/` or Cursor rules.** Use the **currently documented Claude Code conventions** after verifying them. The project root `CLAUDE.md` is the primary durable project instruction file. Keep it concise and point to deeper reference documents rather than duplicating the full master brief.

### Proposed repository layout

```text
ai-readiness-qa-platform/
├── CLAUDE.md
├── .claude/
│   ├── settings.json                 # Only documented, safe project settings
│   ├── agents/                       # Claude Code subagent definitions
│   │   ├── product-analyst.md
│   │   ├── solution-architect.md
│   │   ├── ui-design-reviewer.md
│   │   ├── frontend-engineer.md
│   │   ├── backend-engineer.md
│   │   ├── database-engineer.md
│   │   ├── api-contract-reviewer.md
│   │   ├── playwright-qa-engineer.md
│   │   ├── security-reviewer.md
│   │   └── devops-engineer.md
│   └── skills/
│       ├── requirements-reader/SKILL.md
│       ├── project-planning/SKILL.md
│       ├── design-system/SKILL.md
│       ├── ui-design/SKILL.md
│       ├── frontend-development/SKILL.md
│       ├── backend-development/SKILL.md
│       ├── database-management/SKILL.md
│       ├── api-contract-validation/SKILL.md
│       ├── assessment-domain-and-scoring/SKILL.md
│       ├── question-bank-governance/SKILL.md
│       ├── playwright-ui-automation/SKILL.md
│       ├── playwright-api-automation/SKILL.md
│       ├── test-case-generation/SKILL.md
│       ├── security-and-accessibility/SKILL.md
│       ├── git-workflow/SKILL.md
│       ├── render-deployment/SKILL.md
│       └── documentation-and-diagrams/SKILL.md
├── frontend/
├── backend/
├── database/
├── tests/
├── docs/
│   ├── requirements/
│   ├── research/
│   ├── design-system/
│   ├── architecture/
│   ├── api/
│   ├── testing/
│   ├── deployment/
│   └── decisions/
├── scripts/
├── .github/workflows/
├── render.yaml
├── .env.example
└── README.md
```

### Agent responsibilities and coordination

- **Product analyst:** requirements, personas, user stories, acceptance criteria and research traceability.
- **Solution architect:** architecture, boundaries, API/data decisions, ADRs and integration risks.
- **UI design reviewer:** independent design system, accessibility, UX consistency and responsive design.
- **Frontend engineer:** typed React components, routes, forms, API integration and frontend tests.
- **Backend engineer:** FastAPI services, validation, authorization, scoring and backend tests.
- **Database engineer:** schema, constraints, migrations, query performance and seeds.
- **API contract reviewer:** OpenAPI/TypeScript compatibility, error contracts and backward compatibility.
- **Playwright QA engineer:** UI/API automation, fixtures, deterministic tests and reports.
- **Security reviewer:** secrets, privacy, permissions, unsafe exposure and deployment risk.
- **DevOps engineer:** GitHub Actions, Render, environment configuration and deployment verification.

Use **specialist agents for bounded tasks**, not uncontrolled simultaneous edits. Assign a single owner to each change, define input/output contracts, require review before cross-layer changes and integrate work through explicit checkpoints. Where the installed Claude Code version supports agent delegation, tools, permission controls and hooks, configure them according to official documentation; otherwise provide a safe manual equivalent. **Do not invent agent frontmatter keys, hooks or CLI flags.**

### Required contents of root `CLAUDE.md`

Include: project mission and non-goals; approved tech stack; repository map; source-of-truth hierarchy; assessment invariants; design-system conventions; backend/API/data rules; Playwright strategy; secure-development rules; safe shell commands; test/check commands; definition of done; and links to skills/docs. Explicitly forbid fabricated evidence, real employee data, copied certification questions, secret commits, Cursor-specific configuration and unapproved AI runtime integrations.

### Skill specification

For **each** `.claude/skills/<name>/SKILL.md`, supply documented YAML frontmatter only if required/supported by the verified Claude Code version, followed by:

1. Purpose and scope.
2. When to invoke and when not to invoke.
3. Required inputs and source-of-truth files.
4. Step-by-step implementation procedure.
5. Expected outputs and file locations.
6. Verification commands/checklist.
7. Common failure modes, security/accessibility cautions and handoff requirements.

Make skills **specific, actionable and reusable**, not generic prose. Verify Claude Code's actual discovery paths and invocation conventions before claiming any agent or skill is automatically loaded.

### Safe agentic workflow

1. Read `CLAUDE.md`, relevant requirements, design tokens and ADRs.
2. Inspect repository and verify tools/versions before editing.
3. Write a small plan with files to change, acceptance criteria and risk points.
4. Delegate narrowly scoped specialist work if supported and useful.
5. Implement a vertical slice (database → API → UI → automated tests).
6. Run checks; record actual command outputs and failures.
7. Review accessibility, security, data integrity and API contract compatibility.
8. Update documentation and hand off with changed files, evidence and unresolved issues.
9. Ask for approval before destructive commands, major dependencies, architecture changes, production deployment or publishing assessment content.

## 9. Architecture and Diagrams

Produce diagrams in `docs/architecture/` and keep them aligned with actual implementation:

- Full-stack architecture: browser → React static app → FastAPI → PostgreSQL.
- Claude Code **development-time** agent/skills workflow (separate from deployed runtime).
- Frontend route, component and state/data-fetching architecture.
- Backend API, domain services, authorization and persistence layers.
- PostgreSQL ERD with versioned question bank and immutable results.
- Participant assessment lifecycle and state transitions.
- Deterministic scoring and recommendations decision flow.
- Admin question review/publishing workflow.
- Playwright UI/API test architecture and CI pipeline.
- GitHub → Render deployment architecture and environment boundaries.

Provide Mermaid source (`.mmd` or Markdown Mermaid blocks), clear labels, accessible descriptions and an optional professionally styled architecture visual if explicitly requested. Never depict an AI runtime service or employer integration that does not exist.

## 10. GitHub, Render Deployment, Security and Privacy

Use a **single GitHub monorepo** with `frontend/`, `backend/`, `database/`, `tests/`, `docs/`, `.claude/`, `.github/` and `render.yaml`.

### Deployment target

- React/Vite build deployed as a **Render static site**.
- FastAPI deployed as a **Render web service**.
- Managed PostgreSQL deployed with restricted access and backups as appropriate.
- Configure frontend API URL, backend database URL, approved CORS origins, secret management, health checks and safe migration execution.
- Prefer private repository and **restricted application access**. A deployed URL may be publicly reachable even if not advertised; enforce authentication/authorization rather than relying on obscurity.
- Use HTTPS, secure cookies/session handling if applicable, strong credential practices, rate limiting, least privilege and no sensitive information in logs.
- No real employee records, employer proprietary materials, production credentials or confidential assessment answers in public repositories.
- Verify current Render service options, quotas, regions and prices; do not assume a free tier or claim a deployment is private without checking its access controls.

### GitHub Actions CI

- Frontend lint, typecheck, unit/component tests and build.
- Backend lint, typecheck (if configured), unit/integration tests and migration checks.
- API contract compatibility checks.
- Playwright smoke/API tests against an isolated environment.
- Dependency/security scanning and secrets checks where available.
- Upload test reports/traces without secrets or sensitive data.
- Protect main branch and use pull-request checks; deploy only from approved branches/workflows.

### Documentation

Document local setup, environment variables, service startup order, migrations, seeds, test commands, deployment, rollback, backup/recovery considerations, troubleshooting, hosting cost assumptions and controlled-access demo procedure.

## 11. Implementation Quality, Traceability and Acceptance

- Clean modular monolith, readable typed code, reusable UI components and consistent API schemas.
- Frontend and backend validation, meaningful error messages and correct HTTP status codes.
- Responsive and accessible UI, keyboard interaction, loading/empty/error/success states.
- Server-enforced access control and no answer-key leakage before submission.
- Transaction-safe, versioned and reproducible assessment scoring.
- Original research-backed questions with source traceability and documented review.
- Deterministic, idempotent seeds and isolated tests.
- Unit, integration, API, component, Playwright E2E and security/accessibility checks.
- ADRs for consequential decisions, requirements traceability matrix and test evidence.
- No invented test results, deployments, benchmark claims, tool installation or external verification.
- Avoid microservices, complex event buses, premature optimisation and unnecessary third-party services.

### Jira-ready traceability

Prepare an Epic for the platform, focused stories for participant flow, content governance, scoring, dashboard, admin, security, deployment and Playwright automation; include acceptance criteria in Given/When/Then form, technical tasks, priorities, dependencies, Definition of Ready/Done and a requirements-to-tests traceability matrix. Jira integration is optional; **do not require or claim a connected Jira account**.

### Definition of Done

A feature is done only when: acceptance criteria are met; backend and frontend agree on contracts; relevant automated tests pass; permissions/validation are checked; keyboard/accessibility and responsive states are reviewed; migrations and seeds are safe; documentation is updated; and evidence of verification is recorded. A deployment is done only after a successful live smoke check and confirmation that access is restricted as intended.

## 12. Deliverables — In This Exact Order

**Deliver one phase at a time. Start with Phase 1 only when this master instruction is executed in Claude Code. Wait for the user's explicit `Next` before proceeding.** Do not dump all deliverables into one response. The current request is **only to author this master Markdown file**, not to execute these phases.

**Phase 1 — Project Overview and Verified Technology Stack**  
Scope, personas, non-goals, application/runtime boundaries, current compatible tool versions, risks, success criteria and ADRs.

**Phase 2 — Requirements and Product Backlog**  
Research/source inventory, BRD/SRS alignment, competency and scoring dependencies, functional/nonfunctional requirements, permissions, user stories, acceptance criteria, Jira-ready backlog and traceability.

**Phase 3 — Professional Repository Structure and Design System**  
Full folder tree, original UI design tokens, component inventory, route map, dashboard/assessment/admin interaction specifications and accessibility criteria.

**Phase 4 — Architecture, ERD, API and Mermaid Diagrams**  
System architecture, backend/frontend boundaries, data model, assessment/scoring/admin flows, Playwright architecture, deployment topology and proposed OpenAPI contract.

**Phase 5 — Claude Code Agentic Configuration**  
Complete root `CLAUDE.md`, documented `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, verified settings/hooks where useful, delegation boundaries and verification checklists. **No Cursor files.**

**Phase 6 — Claude Code Development Master Prompt and Checkpoints**  
Executable development plan, vertical slices, prompts, implementation checkpoints, dependency verification, code-review gates and stop/approval rules.

**Phase 7 — Full-Stack Implementation**  
React frontend, FastAPI backend, PostgreSQL migrations and schema, approved/synthetic seed data, typed REST integration, assessment and scoring workflows, results dashboard, admin functionality, unit/integration tests and setup instructions.

**Phase 8 — Playwright Automation, GitHub CI and Render Deployment**  
Playwright TypeScript UI/API framework, deterministic fixtures, test scenarios and reports; GitHub repository workflow, CI/CD, secure Render deployment and verified smoke checks.

**Phase 9 — Final Quality Review and Goal Demonstration**  
Test strategy and coverage matrix, accessibility/security review, Definition of Done, requirement traceability, evidence pack, demo script, known limitations and professional development goal completion checklist.

## 13. Communication, Verification and Change Control

- Write **all generated project deliverables, code comments, agent definitions, skills, architecture diagrams and documentation in professional English** unless explicitly asked otherwise.
- Communicate decisions clearly for a working professional; do **not** frame this as a classroom exercise or address students.
- Distinguish **proposed**, **approved**, **implemented**, **tested** and **deployed** states.
- When input artifacts are missing, list the exact missing files/data and propose a reversible draft; do not silently replace research findings with assumptions.
- Before changing the agreed technology stack, design system, scoring policy, question bank, authentication model or hosting, explain the tradeoff and request approval.
- Record concrete commands and observed results; never claim tests passed or deployment succeeded without execution evidence.
- Use official documentation to verify current Claude Code, library and hosting conventions at the time of implementation.
- **Final goal:** a working, independently branded, access-controlled AI Readiness & Quality Engineering Assessment Platform, built using Claude Code as a development assistant, with a professional Playwright TypeScript automation suite and demonstrable end-to-end software engineering evidence.
