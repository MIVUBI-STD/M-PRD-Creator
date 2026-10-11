# PRD Creator

**Version:** 3.1.3

PRD Creator turns project evidence/discussion into one revision-bound project model, canonical PRD, required Production Assets, and optional Voice Production in one versioned delivery.

## Version rule

```text
PATCH  backward-compatible product/contract fix
MINOR  additive backward-compatible capability
MAJOR  incompatible product/machine contract change
NO BUMP clarification, naming cleanup, CI/repository hygiene, project-only revision
```

This naming normalization is intentionally **NO BUMP**: machine contracts, IDs, lifecycle states, Golden presentation, and artifact formats remain unchanged.

## Canonical workflow names

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

These names are canonical in both repository reasoning and user/operator communication. Numbered stage aliases are retired from current policy. Generated PRD section numbers remain document ordinals only.

## Product flow

```text
sources / current instruction
→ Project Requirements
→ exact requirement-revision binding
→ PRD Production
   ├─ canonical content.md
   └─ strict render-data projection
→ Production Assets when concrete resources are required
→ PRD Handoff
→ Voice Requirements when justified
→ Voice Production
   ├─ Actor Baseline / Voice Fit
   ├─ natural spoken wording
   ├─ Expression Coverage / Audio Tags
   ├─ pronunciation/language strategy
   └─ continuity / generation routing
→ Voice Delivery
→ one current project HTML
```

## Key contracts

```text
Project Requirements
requirement-register bytes → approved_requirement_sha256

PRD Production
content.md bytes → render-data.canonical_content_sha256

Production Assets
Owner ID → Moment ID → AST / VO resource identity

PRD Handoff
exact Render Data + optional Asset Requirements acceptance

Voice Production
voice-production → exact Voice Requirements SHA

Voice Delivery
exact Voice Production acceptance
```

## Package map

```text
kits/prd-creator/
├─ SKILL.md
├─ AGENTS.md
├─ README.md
├─ intake/              Project Requirements
├─ document/            PRD Production + PRD Handoff
├─ production-assets/   Production Assets + non-dialogue SFX craft
├─ voice/               Voice Requirements + Voice Production + Voice Delivery
├─ shared/              strict machine contracts
├─ renderer/            deterministic rendering + transactional delivery
├─ validator/           mechanical gates
└─ template/            protected Golden/runtime source
```

## Canonical owners

| Meaning | Artifact | Owner |
|---|---|---|
| source / requirement revision | `state/source-inventory.yaml`, `requirement-register.yaml`, `intake-state.yaml` | `intake/SOURCE-INTAKE.md` |
| PRD semantic meaning | `work/content.md` | `document/CONTENT-CONTRACT.md` |
| strict render projection | `work/render-data.json` | `shared/render_schema.py` + `renderer/CONTRACT.md` |
| Golden grammar | `template/golden-reference.html` | `document/DESIGN-CONTRACT.md` |
| Production Assets | `work/asset-requirements.md` when required | `production-assets/CONTRACT.md` |
| ElevenLabs non-dialogue SFX | derived production context | `production-assets/SOUND-EFFECTS.md` |
| PRD Handoff | `work/acceptance.md`, `state/handoff-state.yaml` | `document/VALIDATION.md` |
| Voice Requirements | `work/voice-requirements.md` | `voice/EXTRACTION.md` |
| Voice Production | `work/voice-production.md` | `voice/PERFORMANCE-WRITING.md` |
| Voice Delivery | `work/voice-acceptance.md`, `state/voice-state.yaml` | `voice/VALIDATION.md` |

## Voice model

### Actor / Character Continuity

Recurring Speakers use one internal actor baseline: identity/timbre, native cadence, baseline energy/projection, emotional/projection range, language/accent, persona/social stance, no-drift boundary, and pronunciation risk. Each Moment is a performance delta from that baseline.

### Naturalness + Expression

```text
actor fit
→ natural spoken wording
→ thought-group prosody
→ Expression Coverage
```

Audio Tags are deliberate acting controls. Zero tags can be correct for a true baseline line; material emotion/subtext/projection/pacing/reaction/transition must have sufficient direction.

### Language & Pronunciation

Detect materially risky names, terminology, acronyms, numbers/dates/symbols, foreign/code-switched terms, and repeated technical vocabulary. Use normal text → explicit spoken form → IPA/phoneme → pronunciation dictionary as needed.

### Candidate iteration

One weak nondeterministic take does not prove the canonical prompt is wrong. Compare same-content candidates first; after a repeated defect is established, change one variable class at a time.

### Settings

```text
Stability: Natural baseline
Creative: intentional extra expressive range
Robust: consistency over directional responsiveness
Enhance: OFF on reviewed prompts by default
```

## Voice readiness

```text
Communication Conservation
+ Expression Conservation
+ Character Continuity Conservation when applicable
+ Pronunciation Conservation
→ Voice Script Readiness
```

Actual generated-audio quality still requires heard evidence.

## Renderer boundaries

- one strict render-data vocabulary;
- renderer does not invent missing semantics;
- Golden template remains protected;
- Production Assets join only through stable Owner/Moment/Resource identity;
- delivery publishes complete version directories transactionally.

## Operator CLI

Use `impact` for read-only affected-check planning. Adding `--project` inspects which optional Handoff/Voice files actually exist; it does **not** assert stale SHAs or execute a semantic review.

```bash
python tools/prd.py impact state/requirement-register.yaml --project workspace/active/<project>/ --json
python tools/prd.py status workspace/active/<project>/
python tools/prd.py build workspace/active/<project>/
python tools/prd.py validate workspace/active/<project>/
python tools/prd.py handoff workspace/active/<project>/
python tools/prd.py voice workspace/active/<project>/
```

Mechanical PASS does not establish semantic, visual, naturalness, expression, pronunciation, or audio-quality proof.

For production use start from `SKILL.md`. For implementation defects start from `AGENTS.md` and the smallest exact technical owner.