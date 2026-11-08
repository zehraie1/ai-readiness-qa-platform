# REST API v1 contract — PROPOSED, not implemented

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
