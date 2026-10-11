# Project Workspace

`workspace/` is a **local/external mount convention** for project-specific production packages. The public PRD-Creator repository tracks the system; it does not track live project/client package contents.

Reusable behavior belongs under `kits/prd-creator/`. Durable workflow policy belongs under `docs/foundation/`.

## Lifecycle

```text
current project           → workspace/active/<project>/
inactive retained project → workspace/archive/<project>/
```

Project subdirectories are ignored by Git. Keep their actual bytes locally or in a separate authorized/private repository or storage location.

A project moves to `archive/` only when its active production status actually ends. Do not archive merely to make the workspace look smaller.

### Selecting a project

Multiple project packages may be available locally at the same time.

```text
user explicitly names project
→ use that exact project package

current conversation clearly establishes one project
→ continue that project

multiple available projects + request is ambiguous
→ ask which project before changing project state
```

Do not infer project focus from directory order, filename order, commit recency, or whichever package a tool opened most recently.

## Canonical Project Artifacts

```text
Project Requirements
state/source-inventory.yaml
state/requirement-register.yaml
state/intake-state.yaml

PRD Production — document sections 01–03
work/content.md
work/render-data.json

Production Assets, when justified
work/asset-requirements.md

PRD Handoff
work/acceptance.md
state/handoff-state.yaml

Voice Requirements / Voice Production / Voice Delivery, only after formal handoff
state/voice-state.yaml
work/voice-requirements.md
work/voice-production.md
work/voice-acceptance.md

Versioned delivery
output/README.md
output/v<document.version>/prd.html
output/v<document.version>/context.md
output/v<document.version>/index.json
```

Normal delivery:

```bash
python kits/prd-creator/renderer/delivery.py \
  workspace/active/<project>/
```

PRD mechanical validation uses `kits/prd-creator/validator/validate.py`. PRD → Voice handoff uses `kits/prd-creator/validator/validate_handoff.py` only at that boundary. Voice mechanical validation uses `kits/prd-creator/validator/validate_voice.py` only when Voice scope exists.

## Approved preview exception

`approved_preview` is an intentional pre-handoff retained state, not a synonym for `development_ready` or `handoff_ready`.

- `state/intake-state.yaml` must explicitly record the preview status/approval.
- A preview package may retain canonical `state/` + `work/` material and the approved preview artifact without the formal versioned `output/` bundle or `state/handoff-state.yaml`.
- `approved_preview` never authorizes Voice Requirements automatically.
- Formal downstream Voice handoff still requires `handoff_ready`.

## Retention and security

Keep project files because they preserve current production truth, required evidence, or an intentionally retained deliverable—not because they once existed during processing.

Do not commit live project packages into this public repository. In particular, treat the following as project data unless explicit visibility approval says otherwise:

- source files and source inventories;
- requirement registers and project state;
- client/project decisions;
- canonical PRD/Voice work;
- generated project HTML/context/index output;
- approval/evidence containing project-specific information.

The Git ignore rules prevent new project subdirectories from being tracked accidentally. They do not erase project material already present in historical commits. History rewriting or repository-visibility changes are separate operations requiring explicit authorization.

See `../SECURITY.md` for the public-repository data boundary.

## Version Rule

`document.version` is project/release metadata, not an edit counter.

```text
document.version: 1.0.0
→ output/v1.0.0/
```

A downstream-only Production Assets or Voice presentation refresh may regenerate the current version when accepted PRD meaning did not enter a new declared revision.

## Authority Rule

```text
source evidence + current user instruction + approved decisions
→ approved project model
   ├─ canonical PRD core
   └─ optional non-Voice Production Assets requirements
→ PRD Handoff acceptance
→ optional Voice requirements + canonical Voice Production
→ versioned derived delivery
```

Derived delivery may be regenerated. Never patch `prd.html`, `context.md`, or `index.json` as source truth; fix the canonical owner and regenerate only the invalidated projection.
