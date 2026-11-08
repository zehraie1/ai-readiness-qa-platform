---
name: project-planning
description: Create gated, phased plans for this project; apply when before any implementation phase.
---
# Project Planning

## Purpose and scope
Create gated, phased plans. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: before any implementation phase. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
Master, roadmap, open decisions. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. List deliverables; order dependencies; assign one owner; define stop gates and test evidence; seek approval.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/roadmap/. Keep proposed versus implemented status explicit.

## Verification
Verify plan respects phase-by-phase Next gate. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
No coding in Plan Mode. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
