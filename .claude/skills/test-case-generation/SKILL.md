---
name: test-case-generation
description: Derive tests from requirements and risk for this project; apply when after requirement approval or during test planning.
---
# Test Case Generation

## Purpose and scope
Derive tests from requirements and risk. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: after requirement approval or during test planning. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
SRS, user stories, traceability, policy decisions. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Enumerate positive/negative/boundary cases; map IDs; identify fixture needs; record blocked tests.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/testing/. Keep proposed versus implemented status explicit.

## Verification
Coverage matrix reviewed; no orphan critical requirements. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
Do not invent expected score without approved fixture. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
