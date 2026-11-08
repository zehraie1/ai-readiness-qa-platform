---
name: security-and-accessibility
description: Review security and WCAG 2.2 AA target for this project; apply when auth/UI/API/deployment review.
---
# Security And Accessibility

## Purpose and scope
Review security and WCAG 2.2 AA target. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: auth/UI/API/deployment review. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
Permissions matrix, UX, deployment, threat boundaries. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Threat-model IDOR and leakage; inspect secrets/CORS/CSRF; keyboard/focus/contrast/axe/manual plan; record findings.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/testing/, docs/decisions/. Keep proposed versus implemented status explicit.

## Verification
Evidence-backed findings and risk acceptance. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
Automated axe does not prove full accessibility. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
