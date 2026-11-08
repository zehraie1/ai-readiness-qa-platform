# Parameterized query catalogue — design examples, not production queries

1. **Track question set:** join `assessment_templates` → `template_questions` → `question_revisions`, filter `bank_version_id=:version_id`, `track_id=:track_id`, published status; order by `position`; verify 10 common/10 role-specific and exactly 20 before creating attempt.
2. **Own history:** `SELECT id,status,started_at,submitted_at FROM assessment_attempts WHERE participant_id=:current_user_id ORDER BY started_at DESC,id DESC LIMIT :limit OFFSET :offset`; bind server-authenticated identity, not a client-supplied user ID.
3. **Dashboard counts:** `SELECT status,count(*) FROM assessment_attempts WHERE participant_id=:current_user_id GROUP BY status`.
4. **Competency aggregates:** join frozen attempt questions and immutable submitted answers to approved scoring policy; do not compute from mutable current bank. Formula is blocked by D-04.
5. **Weak competency rules:** join `competency_scores` to approved `recommendation_rules` with bound score thresholds and matching rule version; D-05 blocks exact SQL.
6. **Admin filtering:** join revisions/templates with `WHERE (:track IS NULL OR track_id=:track) AND (:competency IS NULL OR competency_id=:competency) ...`; pagination and permission checks required.
7. **Bank validation:** count category by template and flag counts !=10, null evidence, missing competency/correct option, duplicate logical IDs, invalid revision references; reject publish in a transaction.

## Transaction sketch
`BEGIN; SELECT ... FROM assessment_attempts WHERE id=:attempt_id AND participant_id=:actor FOR UPDATE;` validate state and completeness; if already submitted return existing immutable result; otherwise compute using frozen snapshot, insert score once under unique attempt constraint, update state and timestamp, `COMMIT`. Roll back on any failure. This is a proposed algorithm, not executable implementation.

## Schema review issues
Need explicit bank/revision publication immutability enforcement; option schema and JSON validation; template/track common-vs-specific applicability; exact scoring policy JSON schema; database-level status transition constraints; safe retention/deletion; authentication provider mapping; immutable snapshot constraints. Do not treat reference DDL as an approved migration.
