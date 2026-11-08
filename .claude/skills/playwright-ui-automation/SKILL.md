---
name: playwright-ui-automation
description: Build stable browser E2E tests for this project; apply when after approved UI and test environment.
---
# Playwright Ui Automation

## Purpose and scope
Build stable browser E2E tests. This skill does not grant permission to implement. The project owner must explicitly approve each implementation phase.

## When to use / when not
Use: after approved UI and test environment. Do not use for unrelated projects, speculative content, or unapproved application implementation.

## Required inputs
UX flows, test strategy, seeded data. Always read `CLAUDE.md`, `docs/source/MASTER_INSTRUCTION_V1.md`, and `docs/decisions/OPEN_DECISIONS.md`. If approved research is needed and missing, stop and log the dependency.

## Procedure
1. Confirm current phase, approval state and input provenance.
2. Inventory existing files and check current official documentation where external compatibility matters.
3. Use API fixtures; role-based locators; test start/resume/submit/admin; attach traces; clean data.
4. Produce a narrow file-by-file plan and request approval before implementing changes.
5. After approved work, review security, accessibility, data integrity and cross-layer contracts.
6. Record actual verification evidence, unresolved risks and handoff to the next owner.

## Outputs
Expected files: tests/e2e/, tests/fixtures/. Keep proposed versus implemented status explicit.

## Verification
Run smoke/regression with real reports. Only claim a command passed when it actually ran; otherwise mark NOT RUN. Review against the Master and requirement IDs.

## Common failures and handoff
No fixed sleeps or production tests. Never invent citations, installed tools, test results or approved decisions. Handoff includes scope, file list, evidence, missing approvals and next action.
