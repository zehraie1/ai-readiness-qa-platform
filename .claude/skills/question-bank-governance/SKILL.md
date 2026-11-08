---
name: question-bank-governance
description: Manage original evidence-backed question lifecycle for this project; apply when content authoring, review, publication.
---
# Question Bank Governance

## Purpose and scope
Manage original evidence-backed question lifecycle. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: content authoring, review, publication. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
Approved research, taxonomy, bank and source register. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Check source licences; review answer/explanation; validate mappings; publish immutable version with audit.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/research/, backend/. Keep proposed versus implemented status explicit.

## Verification
50 unique questions, 10 common + 10 per track, evidence complete. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
Never fabricate research or copy exam questions. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
