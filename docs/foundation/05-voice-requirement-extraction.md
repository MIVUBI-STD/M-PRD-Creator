---
id: document.foundation.voice-requirements
class: DOCUMENT
domain: foundation
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Voice Requirements

Status: active policy

Voice Requirements converts one accepted `handoff_ready` PRD state into justified player-facing Voice requirements. It owns Voice scope, stable placement identity, communication intent, and authoritative timing truth. It does not write final performance text.

## Entry

```text
PRD Handoff = handoff_ready
→ capture accepted PRD revision + exact render-data SHA
→ Voice Requirements
```

## Canonical output

```text
work/voice-requirements.md
```

Every included Voice ID defines:

- Owner ID;
- Moment ID + reader-facing Moment;
- Type;
- Function;
- Necessity;
- Speaker;
- Channel;
- Trigger;
- Purpose;
- Must communicate;
- Must not add/repeat;
- Source refs;
- optional authoritative Timing Constraint.

Stable identity:

```text
Owner ID → Moment ID → Voice ID
```

Production Assets uses the same Owner + Moment identity when Voice is presented in the consolidated project document.

## Extraction sequence

```text
current PRD Handoff PASS
→ identify player-facing communication system
→ identify justified Voice moments
→ remove UI-only / redundant / unsupported moments
→ assign stable placement identity
→ preserve communication + exclusions + source timing truth
→ mechanically validate voice_requirements_ready
→ Voice Production
```

A project/package may legitimately have zero Voice moments.

## Boundary

Voice Requirements owns **what must be communicated**. Voice Production owns spoken wording, actor selection/profile, performance tags, Estimated Duration, Stability/settings, pronunciation strategy, and generation surface/context.

Use `needs_upstream_decision` when Speaker, Channel, Trigger, Purpose, placement, required communication, result/reward, terminology/sequence, or authoritative timing truth remains materially unresolved.

## Completion

Voice Requirements is complete when `voice_requirements_ready` mechanically passes, or accepted evidence supports `no_voice_required`. Stop before performance writing.