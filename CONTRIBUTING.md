# Contributing

PRD-Creator is currently a personal/internal development repository. Public visibility is for development convenience and does not imply that external contributions or reuse are automatically accepted.

## Branch model

```text
develop
→ active repository development
→ working commits may be numerous

Local
→ verified integration / stable working baseline
→ exactly one commit per approved promoted update

main
→ stable repository history
→ may include untagged maintenance and tagged feature releases
```

Routine repository work happens on `develop`.

Do not make routine changes directly on `Local` or `main`.

### Promote `develop` → `Local`

Use a dedicated pull request when one coherent development outcome is ready for the stable working baseline.

The PR must:

- come from `develop`;
- pass `Local promotion gate`;
- represent one approved logical update;
- be merged with **squash merge** so the complete update becomes exactly one new commit on `Local`.

After squash merge, reset/synchronize `develop` to the resulting `Local` HEAD before starting the next development cycle.

```text
one approved develop → Local promotion
= exactly +1 commit on Local
```

#### Local clones after a squash promotion

A local clone may still point to the pre-squash `develop` commit chain after the remote branch has been synchronized to the new `Local` milestone. Before continuing work, first commit, stash, or otherwise preserve any local changes that still matter. Then resynchronize the local branch:

```bash
git fetch origin
git switch develop
git reset --hard origin/develop
```

Do not use the hard reset while uncommitted work still needs to be recovered. Do not merge or rebase `main` into `develop` merely to obtain main-only stable markers; normal development resumes from the synchronized remote `develop` branch.

### Promote `Local` → `main`

Use a dedicated stable pull request only when an explicitly approved update needs to become part of the stable repository state.

The PR must:

- come from `Local`;
- pass `Stable release gate`;
- be merged with a normal merge commit so `main` records the stable boundary explicitly.

Do not reset `Local` to the resulting `main` merge commit. `Local` remains the clean milestone sequence; `main` may contain main-only stable merge commits in addition to those milestones.

A `main` promotion does **not** automatically create a new repository version. Create a new protected `v*` tag and GitHub Release only when the stable state includes an approved PRD-Creator feature/capability change. Governance, CI, ruleset, documentation, and other maintenance-only promotions remain untagged.

Creating a Git tag or GitHub Release is always a separate explicit publishing action and is never automatic.

For material development, follow the single [Development Operating Standard](docs/knowledge/work-modes/development.md#development-operating-standard). The exact source owner and its consumers determine scope; source review is not executable validation. Material commits use `Work`, `State`, `Proof` and conditional `Unresolved`/`Next` metadata per [GITHUB_RULES.md](GITHUB_RULES.md). The three-branch promotion contract remains, but verification workflows are now manual-only on the updated branch.

## Before committing

Run the cheapest relevant proof for the changed claim.

Repository-level changes:

```bash
python tools/verify_repository.py
```

PRD executable changes use the PRD regression suite. Voice executable changes use the Voice regression suite. Promotion gates run the broader suites required at integration/stable boundaries.

## CI behavior — manual only

All five workflows on the updated branch use `workflow_dispatch` exclusively: no automatic push, PR, scheduled or chained execution. Keep the repository, PRD, Voice, browser and coverage checks intact.

- `Repository Verify`, `PRD Verify`, and `Voice Verify` can be dispatched manually against the chosen branch. No file path change starts a job automatically.
- For `develop → Local`, open a promotion PR, then dispatch `Local Promotion Verify` **on `develop`** with that open PR number. The gate verifies the exact current head and GitHub's merge-candidate SHA. Review a successful run before squash merge.
- For `Local → main`, open a stable PR, then dispatch `Release Verify` **on `Local`** with that PR number. Review the verified merge candidate before a normal merge commit.
- Re-run the gate if the PR's head or base changes. Source review and queued/in-progress checks are never executable PASS.
- `Local` and `main` retain their existing workflow definitions until properly promoted; do not claim all branches are manual-only before that. Branch protection and required checks are separate GitHub settings.

## Commit discipline

Working commits on `develop` may be as granular as needed for safe development, but each commit should still communicate useful intent where practical.

```text
feat:      new capability
fix:       behavior correction
refactor:  internal restructuring without intended behavior change
docs:      documentation/policy-only change
test:      test-only change
ci:        workflow/CI change
build:     dependency/toolchain change
release:   explicit versioned release/publish state
chore:     bounded maintenance when no better category fits
```

`Local` is milestone history: one approved promotion equals one squash commit. `main` is stable history: stable promotions may add merge commits, while protected version tags/GitHub Releases are reserved for feature-bearing publish points.

Do not use transfer experiments, placeholder files, generated fragments, or temporary helper architecture as permanent repository history.

## Project-data boundary

The public PRD-Creator repository tracks the production **system**, not live project packages.

Project-specific packages under `workspace/active/<project>/` and `workspace/archive/<project>/` are ignored by Git and must be retained locally or in a separate authorized/private location.

Do not add credentials, private client/source data, live project requirement registers, project outputs containing material not approved for public visibility, or temporary transfer payloads.

See `SECURITY.md` and `workspace/README.md`.

## Pull requests

Use `.github/PULL_REQUEST_TEMPLATE.md` and keep the PR scoped to one logical delivery. A `develop` → `Local` promotion PR must be squash-merged. A `Local` → `main` stable PR must pass `Stable release gate` and use a normal merge commit.

## License

The repository is not open source. External reuse, redistribution, or commercial use requires prior written permission from the copyright holder. See `LICENSE`.
