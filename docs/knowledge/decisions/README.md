---
id: document.knowledge.decisions.router
class: DOCUMENT
domain: knowledge
role: ROUTER
authority: CANONICAL
lifecycle: ACTIVE
---

# Decision Index

This directory stores durable repository/product decisions whose reasons must survive future sessions.

**Current work starts from the exact repository HEAD and relevant topic commits, not historical decision prose.** `../../../planning/development.md` records future/current development intent, never implementation status. Use `../ownership.md` and `../source-authority.md` to locate the current canonical contract.

## Current Durable Decisions

| Decision | Current status / owner |
|---|---|
| Repository development uses `develop` for working commits, `Local` as clean squash-milestone history with exactly one commit per approved update, and `main` as explicit merge-commit release history | [clean-local-squash-history.md](clean-local-squash-history.md) |
| The public PRD-Creator repository stores the system; live project packages remain ignored/local or external/private | [project-data-boundary.md](project-data-boundary.md) |
| PRD-Creator uses one categorized implementation package under `kits/prd-creator/` while Project/PRD and Voice semantics remain separate | Current architecture; see [Product Boundaries](../../foundation/00-product-boundaries.md), [Ownership](../ownership.md), and [kit routing](../../../kits/prd-creator/AGENTS.md) |
| Golden reference remains the binding PRD-core visual/runtime prototype while semantic child cardinality follows project meaning | [golden-reference-fidelity.md](golden-reference-fidelity.md), refined by [adaptive-semantic-composition.md](adaptive-semantic-composition.md) |
| Package 2.0 uses one canonical validation API, exact acceptance SHA binding, real YAML parsing, stable Production Asset/Voice identity, shared parsers, and domain-specific engine modules | [source-code-hardening-2.0.md](source-code-hardening-2.0.md) |
| Root skills remain semantic/product-contract owners; pure renderer/validator mechanics stay with exact implementation owners | [technical-ownership-boundary.md](technical-ownership-boundary.md) |
| Do not add frameworks, compatibility layers, extra skills, schemas, artifacts, or proof machinery without a demonstrated need | [anti-overdevelopment-simplification.md](anti-overdevelopment-simplification.md) |
| Formal durable change records require a real cross-owner/migration/compatibility threshold | [recording-policy.md](recording-policy.md) |
| Repository verification remains small, deterministic, and limited to repeatable repository invariants | [operating-parity-gates.md](operating-parity-gates.md), now historical/refined by current repository structure |

## Historical / Superseded Context

- [buildit-parity-reassessment.md](buildit-parity-reassessment.md) records a former parity-remediation phase. It is not active work unless the current user instruction or a verified current plan explicitly reopens it.
- [operating-parity-gates.md](operating-parity-gates.md) contains captured Phase 1–3 terminology and paths. Current routing/verification owners override stale captured paths.

Git history and explicitly retained legacy references are the recovery mechanism for retired long-form decisions and older architecture. Do not keep live compatibility paths solely for archaeology.

## How to Read Decisions

```text
Need current task/status?
→ exact current source + relevant topic commits; planning only for intended future work

Need current owner?
→ ../ownership.md

Need source/state precedence?
→ ../source-authority.md

Need why a durable current boundary exists?
→ this index → matching decision file

Need old rationale/provenance only?
→ historical review / retained legacy history
```

A historical decision may be true for the boundary it proved while still containing old names, paths, or delivery surfaces. Current owners always win for execution.

## Recording Rule

Create or materially update a decision only when the reason must survive sessions and cannot be represented cleanly by current state/owner documentation alone. Ordinary fixes, bounded revisions, temporary implementation notes, and active task status do not become durable decisions.

See [recording-policy.md](recording-policy.md) for the threshold.
