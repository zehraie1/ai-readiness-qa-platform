---
name: database-management
description: Design and migrate safe PostgreSQL schema for this project; apply when schema or migration work after approval.
---
# Database Management

## Purpose and scope
Design and migrate safe PostgreSQL schema. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: schema or migration work after approval. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
ERD, DDL proposal, approved policies. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Check constraints and versioning; create reviewed Alembic migrations; verify on disposable DB; plan rollback.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: database/ and backend/. Keep proposed versus implemented status explicit.

## Verification
Migration dry-run and seed rerun on isolated DB. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
Never reset production or seed demo secrets. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
