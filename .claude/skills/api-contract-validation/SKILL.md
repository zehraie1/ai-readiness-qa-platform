---
name: api-contract-validation
description: Maintain UI/API compatibility for this project; apply when endpoint or DTO change.
---
# Api Contract Validation

## Purpose and scope
Maintain UI/API compatibility. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: endpoint or DTO change. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
API spec, backend schemas, frontend client. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Review request/response/status; auth and leakage; generate typed contract; add contract tests.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/api/, backend/, frontend/. Keep proposed versus implemented status explicit.

## Verification
Compare OpenAPI to typed client and tests. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
No undocumented breaking changes. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
