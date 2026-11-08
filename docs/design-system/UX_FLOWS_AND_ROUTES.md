# UX routes and interaction specifications — PROPOSED

| Route | Audience | Intent |
|---|---|---|
| `/login` | Unauthenticated | Approved authentication handoff |
| `/` | Participant | Dashboard/status/history |
| `/assessments/tracks` | Participant | Select/confirm track |
| `/attempts/:id/questions/:position` | Owner | One-question navigation, save state |
| `/attempts/:id/review` | Owner | Answered/unanswered summary and confirm submit |
| `/attempts/:id/results` | Owner | Result, competency breakdown and recommendations |
| `/admin` | Administrator | Aggregate overview |
| `/admin/questions` | Administrator | Search/filter/create/edit |
| `/admin/banks/:versionId` | Administrator | Validate, review, publish or retire |
| `/forbidden` | Authenticated | Permission-denied explanation |

All routes proposed and subject to auth design. API is source of truth for permissions and attempts. UI states: loading skeleton, empty, recoverable API error, stale answer conflict, expired session, successful save, failed save, submit confirmation, already submitted. No frontend storage of answer keys. Result graphs need accessible table alternatives.
