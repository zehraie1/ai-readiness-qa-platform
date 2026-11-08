---
name: ui-design
description: Specify participant/admin UX interactions for this project; apply when new route or workflow.
---
# Ui Design

## Purpose and scope
Specify participant/admin UX interactions. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: new route or workflow. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
UX routes, SRS, permission matrix. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Map user journey; loading/error/empty states; keyboard paths; confirm dialogs; review with design reviewer.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/design-system/. Keep proposed versus implemented status explicit.

## Verification
Check focus management, accessible labels and role guards. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
Never rely on UI-only authorization. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
