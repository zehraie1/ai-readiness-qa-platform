# REST API v1 contract

## Slice 1 — IMPLEMENTED (2026-11-08)
The authoritative machine-readable contract is FastAPI's generated OpenAPI (`GET /openapi.json`, UI at `/docs`
outside production); the frontend's typed client is generated from it (`frontend/src/api/schema.d.ts`, `make gen-api`).

Auth: server-side session cookie `airqa_session` (HttpOnly, SameSite=Lax), ADR-008. Unsafe `/api/*` methods require an
allow-listed `Origin`/`Referer` (`403 CSRF_REJECTED`). No registration endpoint.

| Method | Path | Permission | Success | Errors |
|---|---|---|---|---|
| POST | `/auth/login` `{email,password}` | Public | 200 `MeOut` + cookie | 401 `INVALID_CREDENTIALS` (same for unknown email/wrong password/inactive), 422, 429 `TOO_MANY_ATTEMPTS` + `Retry-After` |
| POST | `/auth/logout` | Authenticated | 204, session revoked | 401 |
| GET | `/me` | Authenticated | 200 `{id,email,display_name,role,permissions}` | 401 |
| GET | `/assessment-tracks` | Authenticated | 200 four tracks `{id,name,description,question_count,available,content_provenance}` | 401 |
| POST | `/attempts` `{track_id}` | Participant | 201 new / 200 existing in-progress (P1) `AttemptOut` | 403, 404 `TRACK_NOT_FOUND`, 409 `NO_PUBLISHED_TEMPLATE`/`NO_SCORING_POLICY`, 422 |
| GET | `/attempts?status=&limit=&offset=` | Participant (own) | 200 `{items,total,limit,offset}`, limit ≤ 50 | 403, 422 |
| GET | `/attempts/{id}` | Owner | 200 safe payload (no keys) | 404 `ATTEMPT_NOT_FOUND` |
| PUT | `/attempts/{id}/answers/{question_id}` `{selected_option_id}` | Owner, in progress | 200 `{question_id,selected_option_id,answered_count,updated_at}` | 404 `ATTEMPT_NOT_FOUND`/`QUESTION_NOT_IN_ATTEMPT`, 409 `ATTEMPT_CLOSED`, 422 `INVALID_OPTION` |
| GET | `/attempts/{id}/review` | Owner | 200 `{total,answered,unanswered_positions,items}` | 404 |
| POST | `/attempts/{id}/submit` | Owner | 200 `ResultOut`; repeat returns identical body (P5) | 404, 409 `ATTEMPT_INCOMPLETE` (`details.unanswered_positions`) |
| GET | `/attempts/{id}/results` | Owner, submitted | 200 `ResultOut` (stored snapshot, never recomputed) | 404, 409 `RESULTS_NOT_AVAILABLE` |
| GET | `/attempts/{id}/recommendations` | Owner, submitted | 200 list | 404, 409 |
| GET | `/admin/competencies` | Administrator | 200 list | 401, 403 |
| GET | `/dashboard/summary` | Participant (own data) | 200 track statuses, latest competency snapshot, score history with versions | 401, 403 |
| GET | `/admin/dashboard/summary` | Administrator | 200 aggregates only: completion by track, average score, band distribution, question coverage, data-quality warnings | 401, 403 |
| GET | `/health`, `/ready` (outside `/api/v1`) | Public | 200 | 503 if DB unreachable |

Cross-user access returns 404 indistinguishable from a missing attempt (P3). Administrators receive 403 on attempt
endpoints (P6). Every error: `{code, message, details, request_id}`, `request_id` = `X-Request-ID` response header;
validation errors never echo submitted input; 500s are sanitised (`INTERNAL_ERROR`).

Contract tests: `backend/tests/api/*`, `tests/api/*.spec.ts`.

---

## Original proposal (remaining endpoints are later phases)

Base `/api/v1`; authentication mechanism unresolved. JSON request/response DTOs typed by FastAPI/Pydantic and consumed by generated or typed fetch client. Never send `correct_option_id`, grading metadata, explanation revealing keys, or hidden scoring data before submission.

| Method | Path | Permission | Expected behavior |
|---|---|---|---|
| GET | `/me` | Authenticated | Profile and access role |
| GET | `/assessment-tracks` | Authenticated | Four approved tracks |
| POST | `/attempts` | Participant | Start from published template; snapshot 20 ordered questions |
| GET | `/attempts/{attempt_id}` | Owner | Resume with saved choices and safe question payload |
| PUT | `/attempts/{attempt_id}/answers/{question_id}` | Owner/open | Validate option and upsert answer |
| GET | `/attempts/{attempt_id}/review` | Owner | Answered/unanswered flags, no keys |
| POST | `/attempts/{attempt_id}/submit` | Owner | Atomic idempotent submission; completeness policy pending |
| GET | `/attempts` | Participant | Paginated own history |
| GET | `/attempts/{attempt_id}/results` | Owner/submitted | Immutable versioned results |
| GET | `/attempts/{attempt_id}/recommendations` | Owner/submitted | Approved rule-based learning actions |
| GET | `/dashboard/summary` | Participant | Own summary only |
| GET,POST | `/admin/questions` | Admin | Filter/create draft revisions |
| GET,PATCH | `/admin/questions/{id}` | Admin | Read/edit under lifecycle rules |
| POST | `/admin/question-banks/{version_id}/validate` | Admin | Completeness/evidence checks |
| POST | `/admin/question-banks/{version_id}/publish` | Admin | Publish after validation/approval |
| GET | `/admin/competencies` | Admin | Approved taxonomy |
| GET | `/admin/scoring-configurations` | Admin | Versioned policies |
| GET | `/admin/recommendation-rules` | Admin | Versioned rules |
| GET | `/admin/dashboard/summary` | Admin | Aggregates only |
| GET | `/health`, `/ready` | Operational | Liveness/readiness; no secrets |

## Example provisional shapes (illustrative only)
`POST /attempts`: `{ "track_id": "manual_qa" }`; response `{ "id": "uuid", "status": "in_progress", "question_count": 20, "questions": [{ "id": "uuid", "position": 1, "prompt": "...", "options": [{"id":"A","text":"..."}] }] }`.
`PUT /attempts/{id}/answers/{question_id}`: `{ "selected_option_id": "A" }`.
`POST /attempts/{id}/submit`: returns submitted attempt and results reference; repeated calls return same result, not duplicate score.
Error: `{ "code": "ATTEMPT_CLOSED", "message": "Assessment already submitted", "details": null, "request_id": "..." }`.

## Error matrix
400 malformed business request; 401 unauthenticated; 403 forbidden; 404 missing/hidden unauthorized resource (consistent non-disclosure policy to approve); 409 stale state/closed attempt; 422 invalid schema/option; 5xx sanitized server errors. Success codes: GET 200, create 201, answer 200/204, submit 200 on idempotent repeat (initial code subject to approval). Rate limits and pagination caps to define.

## Contract review gates
Resolve auth/session/CSRF, request DTOs, option cardinality, incomplete submission, question identifiers and bank version consistency, pagination defaults, error code catalogue, OpenAPI generated client versioning, idempotency behavior and contract tests. Do not claim this document is a generated OpenAPI specification.
