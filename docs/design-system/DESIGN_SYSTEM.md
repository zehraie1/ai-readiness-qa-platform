
# Original UI design system — DRAFT

Identity: independent professional Quality Engineering SaaS. Do not use employer or TaskPilot branding.

## Tokens (proposed; validate actual contrast)
`--navy-900:#17243B; --blue-600:#2563EB; --blue-700:#1D4ED8; --canvas:#F8FAFC; --surface:#FFFFFF; --text-primary:#0F172A; --text-muted:#475569; --border:#E2E8F0; --success:#0F766E; --warning:#B45309; --danger:#B91C1C`.
Typography Inter with system fallbacks; spacing 4/8/12/16/24/32/48/64px; radius 8px controls, 12px cards. Use restrained shadows, visible focus, no color-only statuses, reduced motion.

## Layouts
Dashboard: navy collapsible navigation, light canvas, overview cards, status and history, text alternatives to charts. Assessment: one question per view, progress, four options only if approved schema confirms, keyboard next/back, save state, review and confirm dialog. Admin: dense but readable filterable tables, validation issues, version/status metadata and audit history.

## Component inventory
Button, Input, Select, RadioGroup, Card, Dialog, Alert, Badge, Tabs, Table, Pagination, Progress, Skeleton, EmptyState, ScoreCard, CompetencyChart, QuestionCard, AssessmentStepper, ResultSummary, ConfirmSubmitDialog. Document default/hover/focus/disabled/loading/error/success/empty states and accessible names. Prefer shadcn/ui and semantic Playwright locators.

## Responsive/accessibility
Mobile-first; proposed design review widths 375, 768 and 1280px (test viewports, not approved product breakpoints). WCAG 2.2 AA target; heading hierarchy, landmarks, focus return on dialogs, keyboard choice selection, errors tied to inputs, contrast review, chart data table and reduced-motion preferences. Accessibility review remains unperformed.
