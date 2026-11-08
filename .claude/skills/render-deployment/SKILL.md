---
name: render-deployment
description: Plan approved Render release for this project; apply when after owner approves hosting.
---
# Render Deployment

## Purpose and scope
Plan approved Render release. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: after owner approves hosting. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
Deployment design, auth ADR, verified Render docs. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Verify costs/regions/networking; configure secrets; plan CI release, migration, rollback and smoke.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: docs/deployment/. Keep proposed versus implemented status explicit.

## Verification
Restricted access and live smoke only when executed. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
No assumed free tier or premature deployment. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
