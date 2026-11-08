---
name: frontend-development
description: Implement approved React vertical slices for this project; apply when only after implementation approval.
---
# Frontend Development

## Purpose and scope
Implement approved React vertical slices. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: only after implementation approval. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
API contract, UX, approved ADRs. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Verify versions; implement typed client; routes/components; loading/error states; Vitest; review a11y.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: frontend/. Keep proposed versus implemented status explicit.

## Verification
Run actual lint/typecheck/unit/build after setup. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
No client scoring or leaked answer keys. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
