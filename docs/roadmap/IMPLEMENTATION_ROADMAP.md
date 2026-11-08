# Approval-gated implementation roadmap — no work started

**First Claude Code session: Plan Mode only.** This package prepares documentation across phases but does not authorize executing phases. Master V1 requires one phase at a time and explicit `Next`; preserve this for future delivery.

| Phase | Work after explicit approval | Exit gate |
|---|---|---|
| 1 | Verify official stack versions and compatibility; risk register; approve ADRs | Owner accepts architecture/versions |
| 2 | Reconcile approved research, BRD/SRS, permissions, backlog, scoring dependencies | Owner signs off requirements and source register |
| 3 | Review repo scaffold and original design system; prototypes/specs | Owner approves UX and accessibility patterns |
| 4 | Finalize architecture, ERD, schema, API/OpenAPI and Mermaid | ADR/API/schema review approved |
| 5 | Verify Claude Code conventions and agent/skill behavior | Safe permissions and agent routing validated |
| 6 | Produce vertical-slice implementation plan and task checkpoints | Explicit approval to start coding |
| 7 | Implement backend, database, React UI and unit/integration tests by small vertical slices | Executed evidence, security/a11y reviews |
| 8 | Implement Playwright UI/API, GitHub Actions, approved Render staging/production deployment | Test evidence and live restricted-access smoke |
| 9 | Final audit, traceability, evidence, demo and limitations | Owner accepts final deliverable |

## Suggested vertical slices once Phase 7 is approved
1. Authentication and roles; 2. Published question templates and versioned content; 3. Start/save/resume; 4. Atomic submission and approved scoring; 5. Results/recommendations; 6. Admin governance; 7. Dashboard/reporting; 8. Quality hardening. Each slice: migration → API → UI → tests → review. Stop for missing source/policy decisions.

## Mandatory stop conditions
No approved research/question bank/scoring; unverified dependencies; unexpected architecture change; permission/security ambiguity; destructive command; production publish/deploy; real personal data; unresolved conflicts. Request explicit approval rather than assuming.
