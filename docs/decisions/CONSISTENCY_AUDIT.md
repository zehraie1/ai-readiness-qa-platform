# Package consistency audit — preparation-stage findings

- Source of truth: copied original Master V1 unchanged into `docs/source/`.
- Product scope: one application only; no TaskPilot/Cursor, runtime AI or employer branding.
- Track composition: four tracks, 20 per attempt, 10 shared + 40 role-specific = 50 unique approved baseline questions.
- Permissions: Participant vs Administrator independent from QA tracks.
- API: `/api/v1` contract remains proposed, not generated OpenAPI.
- Scoring: 100-point goal preserved; missing formula, thresholds and weights blocked.
- Data: proposed SQL and ERD share core entities; `attempt_questions` is an explicit design refinement to persist order. Detailed constraints and option schema remain to approve.
- Claude setup: agent/skill files have conventional YAML frontmatter but runtime discovery/permissions are NOT verified against an installed Claude Code version. `.claude/settings.json` is conservative and requires review.
- Verification: ZIP contents and structural checks may be performed; no app tests, schema migrations, library compatibility or live deployments have run.
- Master §12 phase rule: documentation prepared now per user request; Claude Code must still execute one phase at a time, awaiting `Next` and explicit approval.
