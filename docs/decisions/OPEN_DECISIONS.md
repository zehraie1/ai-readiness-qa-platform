# Approval gates and unresolved decisions

| ID | Decision / missing evidence | Current status | Required before |
|---|---|---|---|
| D-01 | Approved Assessment Research with sources and licence checks | MISSING | Content finalisation |
| D-02 | Approved competency taxonomy and role mapping | MISSING | Bank publication/scoring |
| D-03 | Approved original 50-question bank, correct options, explanations, evidence | MISSING | Production assessments |
| D-04 | Approved 100-point scoring: common/role weights, missing answers, rounding, thresholds | **APPROVED V1** (DEC-02, `docs/source/MASTER_INSTRUCTION_V1_DECISIONS.md` §4.4) | Implemented in Slice 1 |
| D-05 | Approved deterministic recommendation rule set | **TRIGGER APPROVED V1** (<60%, DEC-03); text PENDING SOURCE VERIFICATION | Real recommendation text |
| D-06 | Authentication/session provider, invite/registration, admin provisioning | **DIRECTION APPROVED V1** (DEC-07); Slice 1 mechanism in ADR-008; seed-only provisioning | Live deployment |
| D-07 | Retake rules, time limits, incomplete submission policy | **CORE APPROVED V1** (DEC-06: save/resume, all 20 required, retakes). Slice 1 defaults P1–P8 below | Attempt lifecycle finalisation |
| D-08 | Data retention, deletion and privacy notice | UNDECIDED | Live deployment |
| D-09 | Current library versions, Claude Code conventions, Render cost/region/access | UNVERIFIED | Install/deploy |
| D-10 | Optional exports and cross-version comparisons | UNAPPROVED | Feature scope |

All examples below are **proposals**, not approved policy. Do not infer missing decisions from examples. Capture owner, date, evidence, impact and explicit approval for each item.

## Slice 1 owner-approved defaults (approved with the Slice 1 implementation plan, 2026-11-08)

| # | Item | Default |
|---|---|---|
| P1 | Concurrent in-progress attempts | At most one per (participant, track); `POST /attempts` returns the existing one |
| P2 | Correct answers after submit | Not shown |
| P3 | Cross-user attempt access | 404 `ATTEMPT_NOT_FOUND` (non-disclosure) |
| P4 | Incomplete submission | 409 `ATTEMPT_INCOMPLETE` with `details.unanswered_positions` |
| P5 | Repeated submission | 200 with the identical stored result |
| P6 | Administrators taking assessments | Not permitted (403) |
| P7 | Session lifetime | 12 hours absolute |
| P8 | Time limits | None |

D-01/D-02/D-03 remain **MISSING**: Slice 1 uses a clearly marked DRAFT/UNVERIFIED placeholder bank (ADR-010) that must never be published to production.
