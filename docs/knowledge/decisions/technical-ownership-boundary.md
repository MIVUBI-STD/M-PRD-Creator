---
id: document.knowledge.decisions.technical-ownership
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Technical Ownership Boundary

Updated: 2026-08-10
Status: accepted durable decision

## Context

P0.1 introduced repeatable executable production contracts for both Project Document and Voice Production. The current BuildIT comparison then exposed an unresolved ownership question: whether renderer, validator, DOCX builder, dependency, test, and CI failures should create a new reusable technical root specialist or remain with smaller module/repository owners.

Canonical audit evidence:

`../reviews/technical-ownership-refinement-audit.md`

## Decision

Keep the current three repository-wide root skills, but narrow the two production specialists to **semantic/product-contract ownership**.

```text
development-brief
project-document-production
voice-production
```

Pure technical Maintenance does not require a root specialist by default.

### Semantic/product contract

Use the matching root semantic specialist when the wrong behavior changes or misrepresents product meaning, authority, acceptance, or the contract of the derived artifact.

Examples:

- source/recovered requirement/canonical PRD meaning;
- what PRD pages/data must represent;
- development-readiness/handoff semantics;
- Voice moment scope / Voice ID-Type contract;
- final performance wording;
- what the Voice artifact/delivery gate is supposed to represent.

### Module-local executable mechanics

When semantics are already correct and the defect is mechanical, route directly to the nearest kit and exact implementation owner.

Examples:

- deterministic HTML marker replacement or output mechanics;
- PRD validator implementation bug;
- DOCX pagination/XML/paragraph formatting bug;
- Voice parser/validator implementation bug.

Maintenance may use no root specialist when nearest `AGENTS.md` plus the implementation owner is sufficient.

### Shared repository engineering

Repository-wide dependency/test/CI concerns are owned by:

```text
requirements.lock.txt
tests/
tools/
.github/workflows/
```

They are not another production semantic domain and do not justify a root production-tooling/Python specialist.

## Skill Audit Result

Candidate technical root skill:

`DROP AS ROOT SKILL + MOVE TO MODULE-LOCAL / REPOSITORY ENGINEERING`

Current skills:

- `development-brief` → `KEEP`;
- `project-document-production` → `KEEP`, narrowed to semantic/product-contract ownership;
- `voice-production` → `KEEP`, narrowed to semantic/product-contract ownership.

The three-skill freeze therefore remains valid after P0.2. The earlier broad wording that renderer/validator/builder surfaces automatically belong to the semantic specialist is superseded where it implied mandatory root-skill ownership for pure mechanics.

## Why

1. PRD HTML rendering and Voice DOCX generation do not share one reusable artifact/runtime contract beyond generic Python execution.
2. A Python/tooling specialist would be selected by implementation technology rather than proved semantic/technical cause.
3. P0.1 already demonstrated a smaller shared owner for dependency/test/CI concerns.
4. The real DOCX blank-page defect was correctly repaired in builder mechanics without changing Voice semantics.
5. No repeated cross-kit technical failure currently demonstrates a missing reusable technical specialist procedure.

## Tradeoffs

Benefits:

- semantic specialists remain focused;
- technical Maintenance can reach the actual code owner with less context;
- no new skill exists merely to mirror BuildIT's TypeScript/Bun/runtime specialist count;
- repository engineering remains independently enforceable.

Cost:

- nearest kit `AGENTS.md` must carry a stronger contributor/verification contract;
- investigators must distinguish product-contract failure from executable-mechanics failure before routing.

## Validation

P0.2 acceptance requires:

- root routing/skill docs agree on the narrowed boundary;
- both kit-local `AGENTS.md` describe implementation structure and exact verification commands;
- the existing three-skill invariant remains enforced;
- `Repository Verify` passes;
- `Production Verify` passes because kit governance files are part of its watched surface.

## Follow-up

After P0.2 proof, move to **P1 — Production Engineering Quality Audit**. P1 may discover a future technical ownership gap, but it must not pre-create a specialist before evidence exists.
