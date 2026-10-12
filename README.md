# PRD-Creator

PRD-Creator is an AI-assisted **Minecraft map Game Design and PRD production** system. It starts from a new project brief, goals, constraints and optional sources—even when **no map has been built**—and develops approved gameplay/system decisions into a development-ready PRD. Production Assets and Voice are optional downstream scopes. It does **not** build or QA a running Minecraft world.

## Canonical Workflow

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

These names are used consistently in repository policy, package docs, operator communication, and generated Production Assets navigation. Numbered stage aliases are not part of the current workflow vocabulary.

The generated PRD keeps `01 Overview`, `02 Gameplay Flow`, and `03 Development` only as document-section ordinals from the approved Golden design. **Production Assets is displayed by name, without a workflow number.**

Machine lifecycle states such as `handoff_ready`, `voice_requirements_ready`, `voice_script_ready`, and `voice_delivery_ready` are implementation state values only; they do not create alternate human workflow names.

## Start designing a new map

Provide the map's intended experience, audience, objectives and any known
constraints. This can be a short brief: a `.mcworld`, codebase or previously
built map is **not** required. The AI recovers what is already decided,
develops actionable game-design proposals for consequential gaps, and requests
approval only for material choices before writing the canonical specification.

The [single production workflow](docs/foundation/01-production-flow.md)
defines each flow's input, work, output and completion gate; the
[PRD production skill](kits/prd-creator/SKILL.md) routes actual project work.
Gameplay, Level Design and Developer describe what **should be built**, not
what is already implemented. Runtime testing belongs after PRD Handoff.

## Input → Output

| Input | Processing | Output |
|---|---|---|
| New map brief / current instruction | Project Requirements, including material Game Design proposals | approved requirement and design revision |
| Approved constraints / optional references | PRD Production | buildable Gameplay, Level Design and Developer specification |
| Approved gameplay/build needs | Production Assets | actionable resource requirements |
| Approved Voice needs | Voice Requirements → Voice Production → Voice Delivery | Eleven v3-ready Voice Production |

Normal delivery:

```text
output/
├── README.md
└── v<document.version>/
    ├── prd.html
    ├── context.md
    └── index.json
```

Generated delivery is never source of truth. Fix the first wrong canonical owner and regenerate.

## Branch Model

```text
develop  → default active repository development
Local    → clean verified integration baseline; one commit per approved update
main     → stable repository history
```

Normal `develop` → `Local` promotion uses a verified squash boundary. `Local` → `main` remains explicit stable promotion. Version tags/releases are created only for approved feature/capability releases.

Repository behavior is routed by [AGENTS.md](AGENTS.md); GitHub execution policy by [GITHUB_RULES.md](GITHUB_RULES.md).

## Repository Navigation and Continuity

Repository knowledge starts at [Documentation Router](docs/README.md), then the exact [Production Foundation](docs/foundation/README.md) or [Repository Knowledge](docs/knowledge/README.md) owner. Current/future development *intent* lives in [Planning](planning/README.md); implementation continuity belongs to current GitHub source and topic-specific commits, not an always-active `next-action` file.

Read-only document lookup (stdlib only; no persistent index or network calls):

```bash
python tools/repository_knowledge.py --summary
python tools/repository_knowledge.py --query "voice requirements" --domain foundation
python tools/repository_knowledge.py --id document.foundation.prd-production
```

Changes to approved project state may invalidate optional downstream acceptance. Route exact affected checks with the existing CLI:

```bash
python tools/prd.py impact state/requirement-register.yaml --project workspace/active/<project>/ --json
python tools/prd.py trace workspace/active/<project>/
python tools/prd.py revision workspace/active/<project>/ --before /path/to/previous-requirements.yaml
```

The `revision` command compares a caller-supplied prior register with the current
one; it does not create a history copy or modify project files. Known REQ locations
come from the existing trace audit and are not semantic PASS. Changed SHA bindings
and unmarked downstream dependencies still require their proper reviews.

This impact result identifies possibly affected checks, not a substitute for semantic approval, a browser observation, or heard audio. The three-branch model remains unchanged. Actions workflows on `develop` are manual-only (`workflow_dispatch`); the two promotion gates require matching open PR numbers. Existing workflow definitions on `Local` and `main` remain unchanged until formally promoted.

## Manual GitHub Actions

Use **Actions → workflow → Run workflow**, then select the exact branch. Repository, PRD and Voice checks need no PR. Run `Local Promotion Verify` on `develop`, or `Release Verify` on `Local`, with the matching open PR number. The gates inspect the PR test-merge candidate, and must be re-run if its head/base changes.

## Developer Quick Start

Prerequisite: **Python 3.11**.

```bash
python -m pip install -r requirements.lock.txt -r requirements-dev.lock.txt
python -m pip check
python tools/verify_repository.py
ruff format --check kits/prd-creator tests tools
ruff check kits/prd-creator tests tools
mypy kits/prd-creator/shared kits/prd-creator/renderer kits/prd-creator/validator
python -m unittest discover -s tests -p "test_prd_*.py" -v
```

Generate / validate a project:

```bash
python kits/prd-creator/renderer/delivery.py workspace/active/<project>/
python kits/prd-creator/validator/validate.py workspace/active/<project>/
```

Project packages under `workspace/active/` / `workspace/archive/` are local/external production data and are not tracked in this public system repository.

## Package Architecture

```text
kits/prd-creator/
├─ intake/              Project Requirements
├─ document/            PRD Production + PRD Handoff
├─ production-assets/   Production Assets
├─ voice/               Voice Requirements + Voice Production + Voice Delivery
├─ shared/              strict machine contracts
├─ renderer/            deterministic rendering + transactional delivery
├─ validator/           canonical mechanical gates
└─ template/            protected Golden/runtime bytes
```

Core machine invariants remain unchanged:

```text
requirement-register bytes → approved_requirement_sha256
content.md bytes           → render-data.canonical_content_sha256
Owner ID → Moment ID       → AST / VO resource identity
PRD Handoff                → exact render-data + asset-requirements bindings
Voice Delivery             → exact voice-production binding
```

## Repository Map

```text
.agents/skills/      reusable semantic judgment
docs/foundation/     durable production policy
docs/knowledge/      continuation, ownership, decisions, evidence
kits/prd-creator/    production procedure + implementation
tests/               executable regression contracts
tools/               repository verification/operator facade
workspace/           local/external project-package mount convention
.github/             CI / ownership / release policy
```

## Working Principle

```text
identify mode
→ find first wrong/changed owner
→ read only required context
→ update canonical source
→ regenerate derived output once
→ run the proof that can falsify the changed claim
→ stop
```

The current package version is owned by [kits/prd-creator/README.md](kits/prd-creator/README.md). See [CHANGELOG.md](CHANGELOG.md) for product history.

## License

This repository is **not open source**. It is publicly accessible for development convenience, but use is restricted to the copyright holder and explicitly authorized collaborators. See [LICENSE](LICENSE).
