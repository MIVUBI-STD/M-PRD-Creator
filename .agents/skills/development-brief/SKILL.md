---
name: development-brief
description: Front door for non-trivial PRD-Creator repository/system Development. Recover current continuity, identify the first wrong owner, bound the smallest complete change, define falsifiable acceptance criteria and cheapest sufficient proof, then execute. Do not use for normal Project Requirements → Voice Delivery production work.
---

# Development Brief

Use when changing how PRD-Creator itself works: policy, skills, workflow, renderer/validator behavior, repository structure, shared tooling, or machine contracts. Normal project production uses the matching production owner instead.

Root `AGENTS.md` owns work mode, authority, continuity, canonical workflow naming, action intent, and branch behavior. `GITHUB_RULES.md` owns GitHub mutation/verification mechanics.

The mandatory implementation discipline lives in [Development Workflow](../../../docs/knowledge/work-modes/development.md#development-operating-standard). Apply its DEFINE → INVESTIGATE → DESIGN → IMPLEMENT → VERIFY → COMMIT + STOP sequence before material changes. Prefer a coherent vertical integration batch over small speculative test/framework additions. The protected three-branch model remains `develop → Local → main`; do not promote implicitly.

## Development contract

Before writing, establish only:

```text
Goal / actual requirement
First wrong owner
In scope / out of scope
Acceptance criteria: 2–5
Cheapest sufficient proof
Unresolved material decision, only if one remains
```

A user-proposed implementation is evidence about the requirement, not automatically the required architecture.

## Procedure

1. **Recover actual state** — follow Development boot, inspect current behavior, resolve stale continuation vs implementation, and do not ask users to repeat recoverable state.
2. **Diagnose** — separate semantic requirement, implementation, test, workflow, and derived-output failures; fix the first wrong owner; `No change required` is valid.
3. **Bound** — preserve valid behavior outside affected scope, define falsifiable acceptance criteria, use the cheapest proof, and ask only for unrecoverable material decisions.
4. **Specialize only when useful**:
   - Project Requirements / PRD Production / Production Assets / PRD Handoff semantic-system change → optionally add `project-document-production`;
   - Voice Requirements / Voice Production / Voice Delivery semantic-system change → optionally add `voice-production`;
   - pure technical mechanics with correct semantics → package `AGENTS.md` + exact implementation owner.
5. **Execute through completion** — implement reversible scope, follow only invalidated dependencies, use `GITHUB_RULES.md` for mutation/verification, and update `planning/development.md` only when actual repository development intent changes; commit metadata and current source remain execution evidence.

## User-facing form

```text
Tujuan:
Hasil yang dituju:
Tidak diubah:
Cara memastikan benar:
```

A straightforward change needs only a short progress statement. Internal planning is not another deliverable.

Stop when the requested scope is complete and evidence supports the claim.