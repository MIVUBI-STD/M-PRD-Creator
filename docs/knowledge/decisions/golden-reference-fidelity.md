---
id: document.knowledge.decisions.golden-reference-fidelity
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Golden Reference Fidelity and Material Conservation

Date: 2026-08-12  
Refined: 2026-09-08  
Status: current

## Context

A representative AFTERSHOCK v2.4 regeneration kept the expected 30-page family and reused the Golden visual CSS/runtime, yet materially diverged from the approved document. The generated `<main>` was substantially thinner: dense requirement lists, table rows/cells, glossary coverage, and multi-paragraph gameplay explanation were compressed or omitted even though the outer page shell still matched.

Git history also showed two independent drift sources:

1. the full approved Golden HTML had been replaced in the active runtime path by a cleaned/reconstructed interpretation;
2. renderer helpers/tests had normalized Golden IDs/classes (`phase-*`, `quarry-*`, exact global IDs) into generic aliases and then tested those aliases as if they were correct.

That allowed a generated document to look approximately related to the reference while no longer using the same approved composition contract.

## Decision

The exact approved Golden artifact is both the canonical reference and the default runtime source.

The repository now keeps one tracked Golden path:

```text
template/golden-reference.html
→ canonical Golden evidence + default runtime source
```

Current approved Git blob:

```text
2050b965768489feda98373c2920bbee8c7093b3
```

A cleaned, normalized, reconstructed, generic alternative, or separately maintained runtime copy is not an acceptable replacement.

During generation, the renderer may create a temporary project-specific prepared copy through `TemplateAdapter`. That temporary file is derived execution state only; it is never checked in and never becomes another Golden authority.

The renderer may make only bounded project-specific changes in that temporary representation: sample identity metadata removal, localStorage namespacing, project metadata binding, navigation replacement, page-content replacement, glossary-data replacement, and render revision binding. The checked-in Golden CSS/runtime/DOM vocabulary remains unchanged except when actual browser evidence proves a bounded presentation defect and the user approves the matching Golden correction.

The Golden Reference remains **presentation/structure authority only**. It never supplies project-specific mechanics, story, scoring, counts, or implementation facts.

Flow 3 must separately conserve every independently actionable material rule recovered from project authority. Humanize/concise writing may shorten wording, but may not delete or flatten distinct conditions, values, exceptions, recovery behavior, scoring/reset rules, build constraints, glossary meaning, or observable results.

Flow 4 therefore requires the current compact gates:

```text
Semantic Readiness: PASS   # includes Golden Placement
Material Conservation: PASS
Visual sanity: PASS | NOT PROVEN, according to actual evidence
```

Critical/Major findings still block handoff. Golden placement is evaluated inside Semantic Readiness instead of being persisted as a duplicate `Golden Fidelity` gate.

## Why exact runtime reuse is required

The earlier idea of keeping a separate “maintainable runtime shell” was still too permissive. In practice it invited silent normalization of:

- `flow-start` into alternate IDs;
- `shared-systems`, `shared-data-reset`, and `phase-development` into `global-*` aliases;
- `phase-nav-*` into `package-nav-*`;
- `phase-context-grid` and `quarry-*` component names into generic grids/tables;
- package glossary coverage into role-filtered subsets.

Those changes were not harmless internals because the approved CSS/JS targets those exact names and because they changed what the Golden Reference actually demonstrated.

Using the exact Golden bytes as the runtime source avoids a second presentation implementation. Project facts remain safely dynamic because the renderer replaces only project-owned surfaces (`<main>`, navigation, glossary data, document metadata) rather than treating reference-project facts as authority.

Keeping only one tracked Golden file further removes alias drift without changing output. PRD regression now proves default rendering is byte-identical to rendering with the canonical Golden explicitly selected.

## Material-detail conservation

Page-count and component-presence checks can prove a shell while missing destructive semantic compression. Therefore shape parity alone is not enough.

For every independent source rule recovered in Flow 2, Flow 3 must retain one owned readable representation. Structured multi-rule content stays structured rather than being flattened into a single summary sentence for convenience.

## Responsive refinement

Actual Chromium QA of the Clockwork delivery exposed one bounded Golden presentation defect at `1000×1000`: the six-column `Complete Gameplay Journey` overflowed its readable area. The approved correction changes only the intermediate-width Golden CSS so `761–1100px` renders that journey as three columns × two rows. Widths above `1100px` keep six columns and the existing `<=760px` mobile rule remains unchanged.

This refinement does not change page identities, DOM vocabulary, project meaning, gameplay, Voice content, or the 04 Production Assets contract. The canonical Golden remains the sole tracked runtime source and regenerated project HTML remains derived source-first.

## Supersedes / refines

This decision supersedes:

- the shorthand that the “approved PRD template is preserved as a shell” when that wording permits a reduced reconstruction;
- the initial 2026-08-12 split where the file then named `golden-sample.html` (now `golden-reference.html`) was exact but a separate runtime file could remain a cleaned interpretation;
- the later two-path alias arrangement where `golden-reference.html` and `runtime-template.html` intentionally carried identical bytes. The alias no longer provides value because the renderer can consume the canonical Golden directly and prepare its temporary runtime copy itself.

It refines “Golden References are references, not project requirements”:

- still true for project facts/mechanics;
- **not** true for the explicitly approved visible document composition, runtime DOM vocabulary, interaction behavior, and demonstrated information-density standard.

## Proof boundary

Repository and PRD CI prove exact artifact retention, Golden DOM projection contracts, default-vs-explicit Golden byte parity, material-conservation handoff gating, and deterministic generation behavior.

Browser-level visual claims require actual browser evidence for the exact artifact under review.
