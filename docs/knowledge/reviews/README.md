---
id: document.knowledge.reviews.router
class: DOCUMENT
domain: knowledge
role: ROUTER
authority: CANONICAL
lifecycle: ACTIVE
---

# Review Register

Updated: 2026-09-08

Review bodies preserve what was observed at capture time. This register explains their present relevance; historical findings do not authorize new work without a current instruction or a verified development decision.

The dated validation snapshot at this directory root is historical evidence, not current repository proof. Historical audits live under `history/`; current behavior is determined by the exact source HEAD and relevant completed tests.

## Review index

| Evidence / review | Current meaning |
|---|---|
| [Production Engineering Quality Audit](history/production-engineering-quality-audit.md) | Historical useful evidence; theoretical hardening items are not an active backlog. |
| [BuildIT Current Parity Gap Audit](history/buildit-current-parity-gap-audit.md) | Historical/reference evidence only; BuildIT is not a feature checklist or current remediation program. |
| [Technical Ownership Refinement Audit](history/technical-ownership-refinement-audit.md) | Historical implemented evidence for semantic/technical ownership separation. |
| [Operating Architecture Parity Audit](history/operating-architecture-parity-audit.md) | Historical implemented evidence for earlier governance/routing correction. |
| [Operating Parity Acceptance](history/operating-parity-acceptance.md) | Historical partial acceptance evidence; old full-parity framing is not current policy. |
| [System Integration Proof](history/system-integration-proof.md) | Historical Flow 2→7 real-project integration evidence; does not substitute for current project state. |
| [Archived Retirement Audit](history/archived-retirement-audit.md) | Historical implemented evidence supporting retired-builder removal. |
| [Validation Snapshot — 2026-09-09](current-validation.md) | Historical proof from that date only; do not use as today's status. |
| [Repository Quality / AI-Slop Audit — 2026-08-14](history/repository-quality-audit-2026-08-14.md) | Historical completed-remediation evidence. Remaining conditional items live only in `planning/backlog.md` and are not active unless promoted. |

Use [audit-template.md](audit-template.md) only when a new review is actually justified; reviews are not routine ceremony.

## Durable anti-overdevelopment boundary

[Anti-Overdevelopment Simplification Decision](../decisions/anti-overdevelopment-simplification.md) remains a current engineering boundary:

```text
useful discipline/reference
≠ permission to add equivalent machinery
```

## Historical integrity rule

```text
review body        → capture-time observation/evidence
reviews/README     → current interpretation of that evidence
current-validation → dated historical proof, not current status
reviews/history    → historical review bodies
decisions          → durable chosen rationale/rule where needed
topic commits       → actual source-work continuity
planning/           → current and future development intent
Git history        → superseded implementation detail when no separate archive is needed
```

Do not rewrite old audits to pretend they reached today's conclusion. Do not execute an old finding merely because its wording sounds urgent.
