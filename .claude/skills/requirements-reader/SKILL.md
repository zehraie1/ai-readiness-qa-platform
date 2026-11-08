---
name: requirements-reader
description: Trace every request to Master and approved evidence for this project; apply when new requirement, conflict or scope change.
---
# Requirements Reader

## Purpose and scope
Trace every request to Master and approved evidence. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: new requirement, conflict or scope change. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
Master, research source register, SRS. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Build requirement/source matrix; flag missing evidence; compare acceptance criteria; log decisions.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/requirements/ and docs/decisions/. Keep proposed versus implemented status explicit.

## Verification
Review every requirement ID and source line. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
Do not infer approved scoring or evidence. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
