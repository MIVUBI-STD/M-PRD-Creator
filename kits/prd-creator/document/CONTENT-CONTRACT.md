# PRD Semantic Content Contract

`work/content.md` is the canonical owner of PRD meaning. `work/render-data.json` is a strict machine projection of that meaning. Generated HTML is presentation only.

This file owns **what the PRD must communicate**. Visual/page composition is owned by [DESIGN-CONTRACT.md](DESIGN-CONTRACT.md).

## Authority

Project meaning follows:

1. current explicit user instruction;
2. approved project decisions;
3. current authoritative source;
4. exact ready Project Requirements revision;
5. representation references only for structure/quality.

Every material concern must resolve as:

```text
Defined | Explicit No | Not Applicable | Blocked
```

## Material conservation

PRD Production may rewrite wording and choose representation inside approved surfaces. It may not delete independently actionable meaning for brevity or sample-count fidelity.

Conserve every resolved rule that changes production or observable behavior, including conditions/exceptions, timing/counts, scoring/results, fail/retry/recovery, reset/interruption, shared/local ownership, build/spatial constraints, approved technical constraints, and required player-visible/system results.

Do not reintroduce incidental as-built evidence intentionally excluded by Project Requirements unless it is an approved constraint.

## Semantic document family

The generated PRD retains its approved document structure and ordinals. These ordinals are presentation order, not workflow names.

```text
Overview
Gameplay Flow
Development
Gameplay Packages
Production Assets when present
```

For `N` gameplay packages, PRD-core page count remains `6 + 4N`; child-card/beat/note counts are data-driven.

## Stable semantic questions

Overview must establish Session Model, Target Playtime, Game Structure, chronological journey summary, and project-wide gameplay direction.

Gameplay Overview keeps:

```text
Gameplay Context
Main Objective
Result
```

Gameplay Information keeps:

```text
Game Purpose
Gameplay Time
Starting Condition
End Condition
Fail Condition
Scoring Criteria / Completion Result
```

Result mode remains explicit:

```text
scored | completion_only
```

Level Design communicates spatial/build responsibility, design flow, complete build requirements, and applicable constraints.

Developer communicates runtime responsibility, lifecycle, implementation requirements, result handling, interruption/reset/reuse/handoff, and runtime invariants.

## Behavioral conservation

For complex or revised gameplay, use [Behavioral Working Model](reasoning/BEHAVIOR.md)
and applicable [domain concerns](reasoning/CAPABILITIES.md) to check whether
approved conditions, events, effects, state/resource ownership and outcomes
are represented consistently across Gameplay, Level Design and Developer.

The working model is a temporary semantic interpretation, never additional
canonical content or render-data fields. Scenario questions, critique and
unsupported assumptions cannot be converted into project decisions in the
PRD. Missing authoritative decisions return to Project Requirements; missing
representation of approved meaning is repaired in `work/content.md`.
Different wording alone is not a contradiction.

## Requirement location trace — optional, explicit, reviewable

A material requirement may be located in canonical content with a standalone comment
immediately before the relevant substantive paragraph:

```markdown
## Developer — Session Recovery

<!-- PRD-TRACE: REQ-014 -->
A disconnect ends the running session and resets the assigned arena.
```

The marker points to the current `REQ-014` entry in `state/requirement-register.yaml`. It is not visible in the Golden PRD core; it travels with canonical `content.md` and therefore changes `canonical_content_sha256` when edited. Never attach a marker to a heading or empty prose to inflate coverage. A requirement may legitimately appear in multiple role sections; use a marker before each relevant substantive statement.

The existing read-only trace audit compares explicit marker IDs with the current register, reports exact line locations and missing/unknown IDs, and prepares Gameplay–Level Design–Developer comparisons. Once any marker is used, all current material REQ entries must be located or mechanical validation fails. Legacy projects with no markers remain mechanically compatible but are reported as `unreviewed`.

**Location is not semantic proof.** `mapped_unverified` never establishes source fidelity, material conservation, correct scoring/reset behavior, or human approval. Continue integrated semantic review and exact-byte PRD Handoff acceptance.

## Targeted revision — explicit prior requirement snapshot

When one approved requirement register changes, use the read-only `tools/prd.py revision`
operator with the exact **previous** register and the current project package. The
revision comparison returns added, removed, modified and unchanged REQ identities,
changed fields, known `work/content.md` locations, orphaned markers and current
Project Requirements / render-data SHA binding status.

A current trace marker is **only a location**, not proof of semantic correctness
or a guarantee that downstream dependencies are unaffected. When no valid mapping
exists, return `scope_unknown` rather than guessing which PRD paragraphs are safe
to keep or rewrite. Register formatting-only changes still invalidate exact-byte
bindings, but do not automatically require semantic content rewriting.

Do not persist a second REQ registry, auto-rewrite canonical PRD source, delete
removed requirements' prose without review, or infer a previous approved snapshot
from generated HTML. Reconcile existing Project Requirements authority and accepted
content before re-rendering and renewing PRD Handoff.

## Adaptive cardinality

Use the smallest child cardinality that preserves all material distinctions. Do not add filler to match reference counts or merge distinct rules merely for compactness.

## Strict projection boundary

```text
Project Requirements revision
+ content.md bytes
→ strict render-data vocabulary
→ deterministic renderer
```

The projection must bind `canonical_content_sha256`, use only `shared/render_schema.py` fields, carry resolved result mode explicitly, preserve stable IDs, and maintain bilingual numeric/identity invariants when applicable.

The renderer must not recover historical aliases, infer missing semantic meaning, create scoring/completion meaning, or copy Golden sample facts.

If canonical meaning is incomplete, return the affected slice to **Project Requirements**. If meaning is complete but cannot fit the approved presentation grammar, the design/projection layer is the first wrong owner.

## Writing

Prefer direct subject/action/result wording, specific project nouns, semantic note titles, chronological flow when chronology matters, and detail in the owning role. Avoid generator narration, generic numbered note labels, vague ownership verbs, and repetitive cross-role restatement.

## PRD Production completion

PRD Production completes only when:

- Project Requirements remain bound to current requirement bytes;
- `content.md` satisfies this contract;
- `render-data.json` binds current content and requirement bytes;
- no material project decision was silently introduced;
- semantic cardinality is conserved;
- deterministic rendering succeeds;
- no unresolved placeholder remains.

**PRD Handoff**, not renderer success, decides accepted production readiness.
