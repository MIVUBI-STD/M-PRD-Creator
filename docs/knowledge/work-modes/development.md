---
id: document.knowledge.development
class: DOCUMENT
domain: knowledge
role: WORKFLOW
authority: CANONICAL
lifecycle: ACTIVE
---

# Development Workflow

Updated: 2026-08-30

This file is the human-readable lifecycle overview for **repository/system Development**. The canonical implementation procedure is `.agents/skills/development-brief/SKILL.md`; do not duplicate that procedure here.

Normal project Production Execution does **not** use this workflow.

## Entry

Non-trivial Development begins only after repository continuity is recovered:

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules
→ CONTEXT.md
→ topic-related commits + current owner
→ development-brief
```

`CONTEXT.md` protects stable boundaries. Git commits and current canonical source protect topic-based continuation; read `planning/development.md` only when the plan is relevant. The latest unrelated task never becomes default authority.

A read-only `amati / inspect / understand / recover context` request stops after context recovery/reporting and does not enter implementation.

## Development Operating Standard

This is the **single canonical owner** of PRD-Creator's SYSTEM DEVELOPMENT operating behavior. Root `AGENTS.md` selects the mode; `development-brief` invokes this policy without maintaining a second procedure.

1. **DEFINE:** normalize user intent into a bounded goal, observable acceptance, protected invariants, forbidden proxies, scope, and STOP condition. Distinguish explicit requirements from your interpretation.
2. **INVESTIGATE:** pin `develop` HEAD, current owner and real consumers. Separate observed source facts, inferred risks, and unresolved proof. No broad repository reading for reassurance.
3. **DESIGN:** choose in this order: no change → safely remove obsolete behavior → correct the current canonical owner → reuse → smallest complete addition. A new subsystem requires a proven responsibility and an actual consumer.
4. **IMPLEMENT:** finish the smallest coherent owner-to-consumer vertical path. Do not create duplicate parsers, registries, managers, aliases, workflow states, or compatibility layers to hide an upstream defect.
5. **VERIFY:** during unfinished BUILD, review current source contracts, imports, affected consumers, trust boundaries, and provenance. Open executable acceptance after the integrated production path exists, rather than creating per-edit test campaigns. Test earlier when delaying would risk security, data loss, irreversible mutation, or broken critical compatibility. Source review never equals an executed test PASS.
6. **COMMIT + STOP:** publish one valid logical outcome on `develop` with truthful `Work/State/Proof` metadata, verify new HEAD, disclose narrow unexecuted residue, and stop at the requested boundary. No automatic promotion to `Local` or `main`.

### Architecture-first integration boundary

Before calling a multi-owner BUILD coherent, trace **input → canonical owner → dependent consumer → operator-visible output** and check that no parallel current authority remains. At acceptance, use the smallest decisive positive/negative/end-to-end cases, and keep existing regression tests. A large diff is not proof of integration. A missing executable environment leaves exact claims `NOT EXECUTED`, not assumed reliable.

### Anti-AI-SLOP admission

For every new abstraction, state the specific repeated failure, canonical responsibility, real caller, invariant, simplest alternative considered, and what duplicate/legacy owner it replaces. Reject new abstractions without a current consumer. Do not use version-suffixed `-new`/`-v2` names for an unchanged responsibility; public schema/product versions are an exception when contractually required. Optimize cost to a **correct accepted result**, not code volume, docs count, test count, or architecture symmetry with Lazy-Developer.

## Lifecycle

```text
recover current context
→ development-brief grounds goal / method / authority / scope / proof
→ development needed?
   ├─ no → explain/reuse + minimum proof → STOP
   └─ yes
      → at most one useful semantic specialist
      → smallest relevant owner/source
      → smallest complete implementation
      → cheapest relevant proof
      → Acceptance POV + original-scope check
      → update only continuity/decision owner whose state actually changed
      → STOP
```

## Owner selection

Use `development-brief` alone when another specialist adds no semantic value.

```text
PRD/source/04/handoff system meaning
→ project-document-production

Voice scope/production/delivery system meaning
→ voice-production

pure technical mechanics with correct semantics
→ nearest kit AGENTS + exact implementation owner

shared dependency/test/CI mechanics
→ repository engineering owner
```

If investigation reveals a second independent problem, finish/reframe the first boundary before switching. Do not stack specialists because the full product eventually contains both PRD and Voice.

## Execution channel

GitHub mechanics, commit/history quality, retries, and GitHub proof boundaries are canonical in root `GITHUB_RULES.md`.

This workflow only adds the Development selection principle:

```text
bounded repository change fitting current GitHub capability
→ GitHub-capable channel

coordinated multi-file / patch-semantic / local build-runtime need
→ Local or Codex-style workspace with required capability

browser / audio / runtime acceptance claim
→ actual matching capability
```

Do not create temporary Actions, helper architecture, or extra repository files to emulate a missing capability.

## Continuity reconciliation

If a planning note or earlier commit's `Next` conflicts materially with current source/state:

```text
verify exact current owner
→ determine which record is stale
→ reconcile that owner
→ continue from actual current state
```

Do not implement a stale next step twice. Do not select a nearby TODO/audit finding as replacement work without explicit current authority.

## Completion

Before `Selesai`, re-check:

- original goal and out-of-scope boundary;
- 2–5 acceptance criteria from `development-brief`;
- whether actual proof supports the claimed status;
- whether any current continuity/decision owner truly changed.

Distinguish `implemented` from `verified` when browser/audio/runtime proof remains unavailable.

Do not create a planning note per task. `planning/development.md` records only material scope/intent changes; material development commits own recoverable topic-based proof. Durable decisions require the threshold in `../decisions/recording-policy.md`.

## Related

- [Work Routing](../work-routing.md)
- [Maintenance Workflow](maintenance.md)
- [Decision Recording Policy](../decisions/recording-policy.md)
