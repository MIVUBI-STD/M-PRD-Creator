---
id: document.knowledge.source-authority
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Source Authority

Use this note only when source/state precedence for a claim is unclear. Repository/file ownership lives in `ownership.md`; work-mode routing lives in root `AGENTS.md`.

Detailed Project Requirements source recovery lives in `kits/prd-creator/intake/SOURCE-INTAKE.md`.

## Project authority chain

```text
current explicit user instruction
→ approved project decisions
→ authoritative project source
→ Project Requirements / approved project model
→ canonical PRD meaning
   └─ Production Assets requirements when present
→ PRD Handoff acceptance
→ Voice Requirements
→ Voice Production
→ Voice Delivery / derived project HTML / audio evidence
```

Authority decreases downstream. Generated/derived artifacts do not repair or outrank upstream meaning.

Generated PRD pages are not the normal discovery authority for Production Assets. PRD meaning and Production Assets are separate canonical projections of the same approved project model.

## Material user instructions

A material user instruction is authoritative even when it arrives only in chat. Persist it in the existing project source/requirement model so future sessions do not depend on chat history alone.

Do not create a fake source file for a chat instruction or one source entry per sentence; group one coherent material instruction/decision set when practical.

## Source classes

- **authoritative** — may establish current project facts within scope;
- **approved decision/state** — resolves or supersedes project meaning within scope;
- **supporting** — context/evidence but does not outrank authority;
- **reference/Golden** — approved structure/quality only within contract;
- **generated/derived** — presentation/projection/evidence only.

## Partial supersession

Use source-level `superseded` only when the whole source is replaced. If a later instruction changes one claim/section, keep the original source available and resolve only the affected requirement/claim.

## Project source/state roles

```text
originals / provenance / inspection coverage
→ source inventory

explicit + recovered requirements / exclusions / topology / terminology
→ Project Requirements

canonical PRD meaning
→ work/content.md

canonical Production Assets when present
→ work/asset-requirements.md

render-data / HTML / AI-side projections
→ derived only

acceptance / handoff
→ PRD Handoff
```

## Voice source/state roles

```text
accepted PRD Handoff
→ upstream project authority

work/voice-requirements.md
→ Voice Requirements

work/voice-production.md
→ Voice Production

project HTML
→ derived presentation

voice acceptance/state
→ Voice Delivery / continuation evidence
```

Downstream Voice work may not invent or silently repair missing project/gameplay truth.

## Reference / Golden boundary

References can establish demonstrated presentation, structure, tone, or quality only within their recorded contract. They cannot establish current project facts, mechanics/scoring, quantities, speaker rules, asset style/lore, or current-project correctness.

## Conflict rule

If material authorities conflict and precedence does not resolve them safely:

```text
UNKNOWN
→ identify both claims
→ identify affected requirement/output
→ resolve through the correct current owner
```

Never choose silently because one source looks newer, more complete, or more polished.