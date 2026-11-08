# Proposed access matrix — subject to authentication approval

| Resource/action | Participant | Administrator |
|---|---|---|
| View own profile, dashboard, attempts and results | Own only | Own only if also participating; not implied |
| Start, answer, submit assessment | Own only | Not automatically permitted |
| View other participants' identifiable results | Denied | Denied by default; explicit approved scope needed |
| View aggregate statistics | Denied | Allowed (authorized aggregate only) |
| Draft/review/publish questions and policies | Denied | Allowed with audit and change control |
| View pre-submit correct answers | Denied | Allowed only in protected content-management routes |
| Access another user's attempt by ID | Denied | Denied by default |

Backend enforces every permission; frontend route guards are only a UX convenience. Never infer access permissions from QA track.
