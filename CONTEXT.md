# PRD-Creator Context

Status: active production system  
Development branch: `develop`  
Verified integration baseline: `Local`  
Stable branch: `main`

PRD-Creator converts uneven project discussion/source material into one approved project model, development-ready PRD documentation, bounded Production Assets, and optional downstream Voice Production.

## Canonical workflow

Use one naming system everywhere:

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

These are the only current workflow names. Numeric prefixes in foundation filenames and generated PRD navigation are ordering only, never alternate names for workflow boundaries or capabilities.

## Authority shape

```text
current user instruction
+ approved decisions
+ authoritative project source
→ Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ optional Voice Requirements
→ Voice Production
→ Voice Delivery / derived evidence
```

Authority decreases downstream. Generated artifacts never repair or outrank canonical source. If downstream work exposes missing upstream meaning, reopen only the affected owner.

## Branch model

```text
develop → active repository Development
Local   → verified integration baseline; one squash commit per approved update
main    → stable repository history
```

`develop → Local` requires Local Promotion Verify and squash. After promotion, synchronize `develop` to the resulting `Local` HEAD. `Local → main` requires explicit stable promotion and the Stable release gate. Version tags/releases are separate publishing actions.

## Product package

`kits/prd-creator/` owns the production workflow:

```text
intake/             Project Requirements
document/           PRD Production + PRD Handoff contracts
production-assets/  Production Assets
voice/              Voice Requirements + Voice Production + Voice Delivery
shared/             strict machine schemas and shared primitives
renderer/           deterministic PRD + Production Assets rendering/delivery
validator/          PRD, handoff, and Voice mechanical gates
template/           one approved canonical Golden source
```

`shared/` centralizes machine behavior only; it does not become semantic authority.

## Project-data boundary

The public repository owns the system, not live client/project production data. `workspace/active/` and `workspace/archive/` are ignored local/external mount conventions. Do not commit credentials, private client material, live requirement state, or generated client output without an explicit visibility decision.

## Golden boundary

The approved Golden artifact is binding for PRD-core representation until explicitly changed. It supplies structure/quality evidence only and never another project's gameplay facts, counts, timings, lore, scoring, speakers, or implementation decisions.

## Canonical output lifecycle

```text
state/source-inventory.yaml
state/requirement-register.yaml
state/intake-state.yaml
        ↓
work/content.md
work/render-data.json
work/asset-requirements.md       # when Production Assets are required
        ↓
work/acceptance.md
state/handoff-state.yaml
        ↓
optional Voice work/state
        ↓
output/README.md
output/v<document.version>/prd.html
output/v<document.version>/context.md
output/v<document.version>/index.json
```

Generated output is replaceable projection; canonical state/work remains upstream.

## Repository map

```text
AGENTS.md            routing, authority, continuity, branch kernel
GITHUB_RULES.md      GitHub execution and repository mutation discipline
CONTEXT.md           this stable orientation
planning/development.md  topic-scoped development intent only
docs/foundation/     durable production policy
docs/knowledge/      decisions, ownership, evidence, historical context
.agents/skills/      reusable semantic judgment
kits/prd-creator/    product procedure + implementation
tests/ + tools/      deterministic verification/operator facade
.github/             CI and promotion gates
```

For a new Development session, inspect the current topic's commits and exact owner; read `planning/development.md` only when its active scope is relevant. For normal Production Execution, use the matching production skill and smallest project owner instead of broad-reading repository context.