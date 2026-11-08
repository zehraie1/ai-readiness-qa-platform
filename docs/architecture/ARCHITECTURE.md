# Architecture specification — PROPOSED, not implemented

## Runtime
Browser downloads React/Vite static assets from Render; frontend calls HTTPS `/api/v1` FastAPI backend on Render; backend accesses managed PostgreSQL using SQLAlchemy. No runtime LLM, Claude service, external HR/SSO assumed. Authentication approach unresolved. Separate environments and secrets; restrict CORS and DB access.

## Backend modules
API routers validate typed Pydantic DTOs and auth; services enforce attempt state, content publication, deterministic scoring and recommendation policies; repositories persist using SQLAlchemy transactions; PostgreSQL enforces FK, uniqueness and immutability through application controls and schema design. Avoid redundant layers.

## Frontend
React Router guarded UX; TanStack Query server-state; React Hook Form/Zod local validation; typed fetch/OpenAPI client; presentational components use design tokens. Backend authoritative for attempts and scores.

## Consistency guarantees
Persist ordered question revision IDs on attempt creation; freeze published revisions; no answer key in pre-submit DTO; upsert answer only in open attempt; atomic submission with row lock and unique result; policy/version snapshot; idempotent repeated submit; stable results across retakes only when comparability is approved.

## Failure modes
Expired session -> 401; forbidden ownership -> 403/404 per approved non-disclosure policy; invalid option -> 422; stale submitted attempt -> 409; database failure -> safe error with request ID; incomplete attempt -> approved policy (currently unresolved).

## Threat boundaries
Never trust client user ID, track authorization, scoring, attempt state or question IDs. Secrets in environment; no real employee data; rate limiting, audit and retention policy require design approval.
