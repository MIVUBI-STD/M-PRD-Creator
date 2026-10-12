# PRD Handoff

`CONTENT-CONTRACT.md` owns semantic completeness. `DESIGN-CONTRACT.md` owns approved page/component grammar. This file owns the proof required to accept one current PRD revision and hand it downstream.

Mechanical implementation routing:

- `../validator/api.py` → complete PRD validation API;
- `../validator/prd_validation_engine.py` → source/projection/business checks;
- `../validator/html_contract.py` → derived HTML freshness/composition/navigation;
- `../shared/acceptance.py` → acceptance label/SHA primitives;
- `../validator/validate_handoff.py` → PRD Handoff gate.

## Sequence

```text
current Project Requirements revision
+ content.md
+ strict render-data projection
+ Production Assets source when present
→ mechanical validation
→ integrated semantic reconciliation/readiness
→ Material Conservation
→ targeted visual sanity when claimed
→ development_ready | handoff_ready
```

`development_ready` means current PRD/Production Assets meaning is accepted for implementation. `handoff_ready` additionally binds that revision to the current versioned delivery and is required before Voice Requirements.

## Mechanical validation

Run:

```bash
python kits/prd-creator/validator/validate.py workspace/active/<project>/
```

Mechanical validation proves deterministic facts including:

- Project Requirements binding matches current requirement bytes;
- render-data binds that exact revision and current `content.md` bytes;
- retained source provenance/hashes remain coherent;
- strict render schema and result mode are valid;
- Production Assets source is parseable and uses accepted Owner/Moment/Asset identity;
- generated HTML binds exact current canonical inputs;
- page/navigation/component markers and duplicate-ID/scoring checks remain valid.

Mechanical PASS does not prove semantic fidelity or browser visual quality.

## Trace review (read-only)

```bash
python tools/prd.py trace workspace/active/<project>/
```

The trace report reads the existing Project Requirements and canonical `content.md`; it writes no extra registry, source, or accepted output. Its per-package review cases expose actual Gameplay start/end/fail, Level
Design flow, Developer lifecycle/reset, selected result model and acceptance
wording side by side.

Review comparisons are returned only while current requirement-register
approval and render-data requirement/content SHA bindings agree. If either is
stale, the trace still reports source-to-content locations but returns empty
`review_cases` and explicit `review_approval_binding` /
`review_projection_binding` statuses. Fresh SHA bindings do **not** prove
schema completeness or semantic agreement.

An unannotated legacy PRD remains mechanically compatible, with `traceability.status=unreviewed`. When tracing is explicitly used, incomplete/unknown/detached markers fail PRD validation. Even fully located requirements return `mapped_unverified`, never semantic PASS. A reviewer must still judge meaning and any source conflict before setting the existing acceptance fields.

## Integrated semantic readiness

Review relevant concerns once: source fidelity, decision completeness, new-reader clarity, Level Design actionability, Developer actionability, quantitative/lifecycle coherence, cross-role coherence, content purity, and design placement.

```text
Semantic Readiness: PASS | FAIL
```

## Semantic reconciliation

```text
Project Requirements
→ content.md
→ strict render-data projection
→ visible PRD + Production Assets
```

Look for material LOSS, CONTRADICTION, UNSUPPORTED meaning, AMBIGUITY, or CROSS-ROLE DRIFT.

## Material Conservation

Verify changed/regenerated scope retains every resolved material condition, value, exception, recovery rule, result behavior, technical constraint, and role-owned requirement.

```text
Material Conservation: PASS | FAIL
```

## Visual sanity

Visual `PASS` requires actual rendered/browser evidence. Static HTML inspection may establish structure/freshness only. Scale browser proof to the actual changed surface.

## Acceptance record

`work/acceptance.md` authorizes exact bytes:

```text
# PRD Acceptance
Status: needs_revision | development_ready | handoff_ready
Mechanical: PASS | FAIL
Semantic Readiness: PASS | FAIL
Material Conservation: PASS | FAIL
Visual sanity: PASS | FAIL | NOT PROVEN
Findings: <only when findings exist>
Critical: N
Major: N
Accepted Render Data SHA256: <exact work/render-data.json SHA-256>
Accepted Asset Requirements SHA256: <exact work/asset-requirements.md SHA-256 | none>
```

Any edit to Render Data or Production Assets after review invalidates acceptance even if `document.version` is unchanged.

## Handoff

Only `handoff_ready` crosses into **Voice Requirements**.

```bash
python kits/prd-creator/validator/validate_handoff.py workspace/active/<project>/
```

`state/handoff-state.yaml` stays minimal:

```yaml
status: handoff_ready
accepted_prd_version: <X.Y.Z>
```

Handoff validation proves the canonical PRD validator still passes, accepted version matches current render data, deterministic artifacts exist, output metadata identifies the same revision, and acceptance binds exact current Render Data + Production Assets bytes.

## Targeted requirement revision review

```bash
python tools/prd.py revision workspace/active/<project>/ --before /path/to/previous-requirements.yaml
```

This report is read-only. `--before` must reference a distinct, explicitly
provided prior requirement-register snapshot; a missing baseline means that an
exact change cannot be proven. Identical parsed REQ records with changed bytes
are reported as `byte_only_change` because SHA-based acceptance may still be
stale. Changed requirements with explicit current trace locations return
`targeted_review_required` but **never** semantic PASS. Unmapped, added or
removed requirements, or an incomplete trace, yield `scope_unknown`.

Only locations demonstrated by existing REQ markers may be shown as known.
The plan must not claim that unmarked, cross-role, asset or Voice dependencies
are safe. `baseline_authority=NOT_VERIFIED_EXPLICIT_SNAPSHOT` explicitly
states that supplying an older register does not prove it was ever approved.
The `render_data_binding` is current only when *both* approved requirement
SHA and canonical `content.md` SHA match; it never proves semantic agreement. The operator reuses existing `impact` domain planning to recommend
which validation checks follow a byte change. All PRD source edits and
acceptance decisions remain separate authorized actions.

## Bounded revision

```text
approved change
→ first wrong owner
→ affected canonical source
→ deterministic rerender
→ mechanical validation
→ integrated review only for invalidated meaning
→ visual check only where changed/high-risk
→ new exact-byte acceptance
→ stop
```

Do not replay unaffected Project Requirements, packages, Voice, or Golden review for ceremony.