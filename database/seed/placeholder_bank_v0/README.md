# placeholder_bank_v0 — DRAFT / UNVERIFIED PLACEHOLDER

**Not research-backed. Development and test use only (ADR-010).**

- 50 original `[DRAFT]` questions: 10 common (`questions/common.json`) + 10 per track (`manual_qa`, `automation_qa`, `sdet`, `qa_lead`).
- Single-answer, four-option MCQ (DEC-04). Template order = file order: common at positions 1–10, track questions at 11–20 (DEC-05).
- Competencies use `PH_` codes; recommendation text is placeholder. The scoring policy `v1-simple` reflects the **approved** DEC-02 rules.
- `content_provenance = placeholder_unverified` drives a permanent UI banner; the seeder refuses `APP_ENV=production`.

Replace with approved content once DEC-01 / DEC-03 text are signed off.
