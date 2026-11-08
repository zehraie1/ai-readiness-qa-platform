---
name: playwright-api-automation
description: Build deterministic Playwright API checks for this project; apply when after API is implemented.
---
# Playwright Api Automation

## Purpose and scope
Build deterministic Playwright API checks. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: after API is implemented. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
API spec, permissions, test strategy. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Seed isolated accounts; exercise auth/ownership/validation/concurrency; assert DTOs and status; cleanup.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: tests/api/, tests/fixtures/. Keep proposed versus implemented status explicit.

## Verification
Run tests against isolated DB. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
No answer-key leakage. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
