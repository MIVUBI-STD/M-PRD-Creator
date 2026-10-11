---
id: document.foundation.voice-production
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Voice Production — Eleven v3

Status: active policy

Voice Production turns mechanically ready Voice Requirements into canonical Eleven v3 speech while preserving upstream meaning and intended acting.

Detailed craft lives in `kits/prd-creator/voice/PERFORMANCE-WRITING.md`.

## Entry

```text
Voice Requirements = voice_requirements_ready
→ Voice Production
```

## Ownership

```text
Voice Requirements
→ natural spoken-language pass
→ Actor Baseline / Voice Fit
→ Expression Coverage / Audio Tags
→ pronunciation/language strategy
→ duration + continuity planning
→ Communication / Expression / Character / Pronunciation conservation
→ Voice Script Readiness
→ work/voice-production.md
```

Voice Production preserves Owner ID, Moment ID, Type, Speaker, scope, required communication, exclusions, and authoritative timing truth from Voice Requirements.

## Canonical format

```text
# Voice Production
Source Voice Requirements: <revision> / work/voice-requirements.md | sha256:<sha>

Voice Cast:
- <Speaker>: <selected ElevenLabs voice or target profile>

### VO-... — <Line Title>
Type: <Voice Requirements Type>
Speaker: <Voice Requirements Speaker>
Estimated Duration: <production estimate>

```performance
<exact Eleven v3 payload>
```
```

Audio Tags are not mandatory syntax, but material expression must have sufficient direction.

## Craft boundaries

Voice Production may decide reversible craft such as wording, contractions, thought groups, punctuation/CAPS, Audio Tags, actor fit, pronunciation representation, Estimated Duration, Stability/Speed where supported, generation surface, and adjacent generation context.

It may not silently change Voice scope, Speaker, Channel, Trigger, Purpose, required communication, gameplay/lore/result/reward, or authoritative timing truth.

## Readiness

Set `voice_script_ready` only when:

- current Voice Requirements validate;
- every required Voice ID has one canonical production entry;
- Owner/Type/Speaker parity is exact;
- wording is natural for speaker/register;
- actor fit and Character Continuity are sound;
- Expression Coverage is complete;
- material pronunciation/language risks have a strategy;
- Estimated Duration is plausible and source timing truth is honored;
- connected narration/dialogue has appropriate continuity planning;
- Communication Conservation, Expression Conservation, Character Continuity Conservation when applicable, Pronunciation Conservation, and Voice Script Readiness pass;
- exact Voice Requirements SHA binding is current.

## Generation routing

```text
independent Voice ID → Eleven v3 TTS
connected same-speaker narration → TTS + relevant adjacent context
same Moment + multiple speakers + response dependency → Text to Dialogue
long-form editorial work → current ElevenCreative Studio when useful
```

Generation grouping/context is production routing, not new canonical identity.

A weak isolated take should be compared with same-content candidates/regeneration before rewriting otherwise-correct canonical wording. Actual audio quality requires heard evidence.

## Stop rule

Stop when requested Voice Production scope is current. Do not add parallel Voice schemas, expression manifests, settings databases, scorecards, or duplicate acceptance layers.