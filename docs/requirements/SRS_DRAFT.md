# Software requirements specification — DRAFT

## Functional requirements
| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-01 | Authenticate and enforce Participant/Administrator server permissions | Must | Master §4.1 |
| FR-02 | Select exactly one of four QA tracks | Must | §4.1/4.3 |
| FR-03 | Compose 20 questions (10 common + 10 track-specific) from approved published bank | Must | §4.3 |
| FR-04 | Persist ordered questions, save/resume answers, one-question navigation and review | Must | §4.3 |
| FR-05 | Confirm submission; submit atomically/idempotently; lock answers afterward | Must | §4.3 |
| FR-06 | Compute deterministic 100-point results from approved versioned policy | Must, BLOCKED | §4.4 |
| FR-07 | Return role/common/competency breakdown and versioned recommendations | Must, BLOCKED | §4.4/4.5 |
| FR-08 | Display dashboard/history and accessible result alternatives | Must | §4.2/4.5 |
| FR-09 | Admin draft/review/publish/retire questions and versions, with audit | Must | §4.6 |
| FR-10 | Admin aggregate dashboard and content validation | Must | §4.6 |
| FR-11 | Versioned API and documented errors; no pre-submit answer keys | Must | §5 |
| FR-12 | Deterministic synthetic test seeds, isolated Playwright UI/API testing | Must | §6/7 |

## Nonfunctional requirements
NFR-01 WCAG 2.2 AA target, keyboard and responsive support.
NFR-02 Server-side authorization/ownership; secure secrets, HTTPS, no sensitive logging.
NFR-03 Immutable published content references and scored result snapshots.
NFR-04 Reproducible deterministic question ordering and score outcomes.
NFR-05 Structured logging, request IDs, health and readiness endpoints.
NFR-06 Typed API/UI contracts, strict TypeScript and testable Python modules.
NFR-07 Migration-safe, transaction-safe PostgreSQL persistence and isolated tests.
NFR-08 CI quality gates and documented rollback before deployment.

## Pending specification details
Auth provider, scoring formula/weights/thresholds/rounding, answer incompleteness policy, retakes, time limits, recommendation mapping, retention, final question option cardinality subject to approved bank schema. These are not silently decided here.
