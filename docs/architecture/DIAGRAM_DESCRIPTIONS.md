# Diagram accessible descriptions

01 Runtime: browsers load static frontend, call FastAPI over HTTPS; API persists in PostgreSQL.
02 Claude workflow: instructions and evidence feed Plan Mode; approval is mandatory before implementation and each next phase.
03 Frontend: router renders participant/admin screens; typed query client calls backend; shared accessible components.
04 Backend: API validation and authorization precede domain services and database persistence.
05 ERD: users own attempts; versioned templates point to immutable question revisions; answers and immutable scores link to attempts; rules generate recommendations.
06 Attempt lifecycle: not started → in progress ↔ review → submitted; only submitted is final.
07 Scoring: absent approved policy blocks execution; otherwise atomic scoring and recommendation match persist once.
08 Publication: draft/review/validation/publish/retire with immutable prior snapshots.
09 CI: isolated test DB supports Playwright; frontend/backend checks and sanitized artifacts feed gate.
10 Deployment: approved CI deploys separate static frontend and API with restricted PostgreSQL; not currently deployed.
