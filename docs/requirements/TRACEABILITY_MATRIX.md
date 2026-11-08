# Requirements-to-tests traceability

Slice 1 rows reference implemented, executed tests (2026-11-08). Later-phase rows remain planned.

| Requirement | Test cases | Implemented tests | Status |
|---|---|---|---|
| FR-01 roles/ownership | TC-005, TC-006 | `backend/tests/api/test_attempts.py::test_other_participant_cannot_see_or_change_attempt`, `test_tracks_and_rbac.py`, `test_auth.py`; `tests/api/ownership.spec.ts`, `admin-rbac.spec.ts`; `tests/e2e/login.spec.ts` (admin denied participant pages) | Slice 1 |
| FR-02, FR-03 tracks & composition | TC-001, TC-002 | `test_tracks_and_rbac.py`, `test_attempts.py::test_start_returns_20_questions_*`, `test_common_questions_shared_and_role_questions_disjoint`, `integration/test_migrations_and_seed.py::test_bank_invariants_hold`; `tests/api/tracks.spec.ts`, `attempt-composition.spec.ts` | Slice 1 |
| FR-04 save/resume/review | TC-003, TC-004, TC-007 | `test_attempts.py` (save/change, review, invalid option, key leak); `tests/e2e/assessment-flow.spec.ts`, `tests/api/answer-key-leak.spec.ts`, `validation.spec.ts` | Slice 1 |
| FR-05 atomic idempotent submit | TC-008 | `test_submit_and_results.py`, `integration/test_concurrency.py`; `tests/api/double-submit.spec.ts` | Slice 1 |
| FR-06, FR-07 scoring & recommendations | TC-009, TC-010 | `unit/test_scoring_engine.py`, `test_submit_and_results.py::test_known_pattern_gives_exact_expected_result`; `tests/e2e/results.spec.ts` | Slice 1 |
| FR-08 dashboard | — | Minimal history/resume covered by `test_retake_creates_new_attempt_and_history`, `assessment-flow.spec.ts`; summary endpoint pending | Partial |
| FR-09, FR-10 admin governance | TC-011 | — | Later phase |
| FR-11 API contract | TC-015 | `test_health_and_errors.py`; `tests/api/error-envelope.spec.ts` | Slice 1 |
| FR-12 seeds/isolation | TC-014 | `integration/test_migrations_and_seed.py::test_seed_is_idempotent`; per-worker Playwright accounts | Slice 1 |
| NFR accessibility/responsive | TC-012, TC-013 | `tests/e2e/keyboard.spec.ts`, `tests/e2e/a11y.spec.ts` (axe WCAG 2.2 AA tags); Vitest component tests. **Manual accessibility review not yet performed.** | Partial |
| NFR security | — | Argon2 hashing, session revocation/expiry, CSRF origin check, no input echo: `test_auth.py`, `unit/test_security.py`. Login rate limiting **not implemented** (required before deployment). | Partial |
