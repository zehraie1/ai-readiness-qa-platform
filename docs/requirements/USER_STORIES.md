# Jira-ready backlog — DRAFT

**Epic:** EPIC-01 AI Readiness & QE Assessment Platform. Definition of Ready: approved requirement and dependencies, UI/API contract, testable criteria, owner. Definition of Done: implementation, tests run and evidenced, permissions, a11y, docs, review.

| Story | Priority | Dependencies | Acceptance (Given / When / Then) |
|---|---|---|---|
| US-01 Participant access | P0 | D-06 | Given authenticated participant / when requesting another user's attempt / then access is denied without disclosure |
| US-02 Start assessment | P0 | D-02,D-03 | Given published valid bank / when selecting track / then server persists exactly 10 common and 10 matching role questions |
| US-03 Save and resume | P0 | US-02 | Given open attempt / when saving valid answer and resuming / then same question order and answer return |
| US-04 Submit | P0 | D-04,D-07 | Given eligible open attempt / when confirming submit twice / then exactly one immutable result exists |
| US-05 Results | P0 | D-04,D-05 | Given submitted attempt / when requesting results / then approved versioned score and accessible breakdown display |
| US-06 Dashboard/history | P1 | US-04 | Given participant / when opening dashboard / then only own attempts appear |
| US-07 Admin governance | P0 | D-01,D-02,D-03 | Given draft invalid bank / when publishing / then validation blocks and reports missing evidence |
| US-08 API protection | P0 | D-06 | Given unauthorised caller / when calling admin endpoint / then 401/403 as appropriate |
| US-09 Playwright | P0 | test environment | Given isolated seed / when running smoke and API suites / then reproducible assertions and CI artifacts are produced |
| US-10 Deployment | P1 | D-08,D-09 | Given approved deployment / when release completes / then restricted access and live smoke checks are verified |

Technical tasks for each story: schema/transaction, DTO/service, UI state, unit/integration/Playwright tests, accessibility/security review, traceability/evidence. Do not mark Done until tests actually run.
