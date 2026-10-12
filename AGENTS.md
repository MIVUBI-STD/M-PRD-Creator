# Workspace Agent Routing

PRD-Creator is repository-backed system memory. Current explicit user intent and current repository/project authority outrank chat history. Use the smallest owner and proof set that can settle the task.

## Canonical workflow names

Use these names everywhere in current policy, routing, handoff, and user-facing explanation:

```text
Project Setup
→ Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements when Voice is justified
→ Voice Production
→ Voice Delivery
```

Numeric labels are not workflow names. Numeric prefixes in `docs/foundation/` are file-ordering only. Numeric markers in generated PRD navigation are document-section ordinals only; the capability name is always **Production Assets**.

Do not reintroduce numbered stage aliases in current operating documentation.

## Work-mode boundary

Select one mode from the requested outcome before opening a specialist or mutating files:

- **INSPECT (Plan):** understand/recover/compare only; repository and client project remain read-only.
- **SYSTEM DEVELOPMENT (Development):** improve PRD-Creator policy, code, architecture, tooling, or knowledge on `develop`; use the existing `development-brief` skill.
- **PROJECT PRODUCTION (Production Execution):** design a new map from an authorized brief or revise *one explicitly selected* project PRD; the map need not exist. Do not silently modify repository implementation.
- **MAINTENANCE:** correct a bounded, evidenced defect at its first wrong owner; no adjacent feature-building.
- **VALIDATION:** examine existing source, product contracts and evidence without rewriting accepted source or expectations solely to claim PASS.

A production issue discovered during PROJECT PRODUCTION is not automatic authorization for SYSTEM DEVELOPMENT. A system improvement is not automatic approval to revise live project data. An unqualified “continue” preserves the active topic and mode. Root policies and existing three specialist skills remain the only active routing owners; mode labels are not new persisted states.

For SYSTEM DEVELOPMENT, the **Development Operating Standard** and architecture-first integration policy are owned only by [Development Workflow](docs/knowledge/work-modes/development.md). Build a coherent owner-to-consumer path before expanding routine tests. This never permits unverified claims, unsafe mutations, or lost approval/Golden compatibility.

## Core routing

| Intent | Mode | Start |
|---|---|---|
| Inspect, understand, recover, decide | Plan | current state + smallest owner; read-only unless change requested |
| Create/revise project PRD or Voice deliverables | Production Execution | matching semantic specialist only when needed + smallest active owner |
| Change PRD-Creator policy, workflow, approved Golden/design system, renderer, validator, schema, tooling, repository mechanics | Development | `development-brief` + exact owner |
| Fix bounded bug, regression, stale routing/docs, behavior-preserving defect | Maintenance | concrete failure or explicit target → first wrong owner |

Production work does not become Development merely because tools or generated files are involved. There is one authority, quality, and proof system; task size changes scope, not standards.

## Boot

### Observe / recover

```text
AGENTS.md
→ CONTEXT.md
→ current topic commits + exact owner
→ smallest owner needed
→ report current understanding
→ STOP
```

Read `GITHUB_RULES.md` only when GitHub mutation/history/CI/promotion behavior can affect the task.

### Maintenance / bounded change

```text
concrete failure or explicit target
→ first wrong owner
→ exact owner
→ GITHUB_RULES.md before material GitHub mutation
→ smallest falsifiable proof
→ STOP
```

### Development

```text
AGENTS.md
→ CONTEXT.md
→ current topic commits + exact owner
→ development-brief
→ exact owner
→ GITHUB_RULES.md before material GitHub mutation
```

### Production Execution

```text
new map brief / materially uncertain design meaning
→ project-document-production for game-design options when needed
→ Project Requirements → approved design choices
→ PRD Production for buildable specification

bounded approved PRD revision
→ smallest changed canonical owner
→ only invalidated downstream owners

PRD presentation-only issue with correct meaning
→ document/DESIGN-CONTRACT.md
→ exact implementation owner when required

Voice meaning / communication / performance work
→ voice-production when semantic craft judgment is needed
→ Voice Requirements | Voice Production | Voice Delivery as appropriate
```

Do not broad-read the repository or replay the complete workflow for bounded work.

## Authority

Use the nearest authority for each claim:

1. current explicit user instruction;
2. approved project-specific decisions;
3. authoritative project source;
4. normalized current project/requirement state;
5. accepted canonical PRD / Voice source for downstream scope;
6. durable repository/foundation policy;
7. active package procedure;
8. Golden/reference material for demonstrated representation/quality only;
9. generated output, reviews, Git history, and chat as supporting evidence.

Material conflicts remain `UNKNOWN` until reconciled. Golden/reference material never supplies another project's facts.

## First wrong owner

```text
project/source meaning wrong                → Project Requirements
canonical PRD meaning wrong                 → PRD Production
resource requirement wrong                  → Production Assets
PRD acceptance/handoff wrong                → PRD Handoff
Voice scope/communication intent wrong       → Voice Requirements
Voice wording/performance/pronunciation      → Voice Production
Voice acceptance/delivery evidence wrong     → Voice Delivery
meaning correct, implementation wrong        → implementation owner
implementation correct, test stale           → test
implementation/test correct, CI wrong        → workflow / repository policy
derived artifact wrong                       → upstream canonical owner
```

Do not repair upstream defects with renderer defaults, generated-file patches, or compatibility layers.

## Canonical and derived state

```text
source / approved decisions
→ normalized state
→ canonical work
→ derived artifact
→ acceptance evidence
```

Never hand-patch generated `prd.html`, `context.md`, or `index.json` to hide an upstream defect.

## Topic-based continuation

For a new chat or an explicit resume, pin the exact repository/branch HEAD, identify the requested **topic**, inspect relevant topic commits and current owner/consumer source, and distinguish completed work from unresolved claims. Do not turn the latest unrelated commit or a historical planning note into automatic work authorization. Chat memory and generated notes are orientation, never repository authority.

Material development commits carry `Work`, `State`, and `Proof` metadata (plus `Unresolved`/`Next` when useful) under `GITHUB_RULES.md`. These describe the bounded commit unit, not the entire feature or a second task-status database.

## Repository continuity

- `CONTEXT.md` → stable product/repository orientation.
- `planning/development.md` → current/future repository development intent, only when the topic matches.
- `docs/knowledge/decisions/` → durable rationale.
- `docs/foundation/` → durable production policy.
- `kits/prd-creator/` → detailed production procedure and implementation.
- project package → project facts/state/output.
- reviews/history → evidence only when needed.

## Branches

```text
develop  → active repository development
Local    → verified integration baseline; develop→Local uses squash
main     → stable history; Local→main requires explicit stable promotion
```

After an approved `develop → Local` squash, synchronize `develop` to the resulting `Local` HEAD before new development. Version tags/releases are separate publishing actions for approved feature/capability changes.

## User-facing communication

Default to concise result-first reporting. Use the canonical workflow names above; do not translate them into numbered aliases.

## Product boundaries

- PRD-Creator owns **pre-build game/map design**, not inspection or QA of an existing Minecraft world. A map file is never a mandatory input to a new design.
- Game Design/System Design are reasoning responsibilities inside Project Requirements and PRD Production, **not** extra persisted workflow names.
- Design Handoff means a specification can guide implementation; it is **not** evidence of gameplay, multiplayer capacity or device performance PASS.

- `kits/prd-creator/` is the single product package for Project Requirements through Voice Delivery, with Production Assets as a bounded capability.
- Project/PRD and Voice remain separate semantic domains.
- Root skills own reusable semantic judgment; package owners hold detailed procedure.
- `kits/prd-creator/AGENTS.md` owns package file/mechanical routing.
- Repository engineering owns shared dependency, regression, CI, and governance contracts.
- Live project packages are not tracked in the public system repository; `workspace/` is a local/external mount convention.

Stop when requested scope is complete and the cheapest sufficient evidence supports the claim.
