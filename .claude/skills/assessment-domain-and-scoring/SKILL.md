---
name: assessment-domain-and-scoring
description: Preserve deterministic assessment invariants for this project; apply when attempt/scoring changes.
---
# Assessment Domain And Scoring

## Purpose and scope
Preserve deterministic assessment invariants. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: attempt/scoring changes. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
Approved question bank, scoring artifact, Master §4. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Verify 10+10 template; snapshot revision/order; validate answer; atomic submit; score with approved policy; version recommendations.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/architecture/, backend/. Keep proposed versus implemented status explicit.

## Verification
Determinism, idempotency, concurrency and key-leak tests. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
BLOCK if scoring or bank approvals missing. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
