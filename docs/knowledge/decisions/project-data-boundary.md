---
id: document.knowledge.decisions.project-data-boundary
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Public System / Project Data Boundary

Status: current

## Decision

The public PRD-Creator repository stores the reusable **system**. Live project/client production packages are retained outside the tracked system tree.

`workspace/active/` and `workspace/archive/` remain the runtime path convention for local execution, but their project subdirectories are ignored by Git. Only workspace guidance is committed.

## Why

A project package can contain source inventories, requirement registers, approved decisions, canonical PRD/Voice work, generated HTML/context, and other material whose visibility is governed by the project/client rather than by PRD-Creator itself.

Keeping system code and live project data in one public history creates unnecessary exposure and makes the repository's responsibility less clear.

## Allowed retention

Project packages may live:

- locally under ignored workspace paths;
- in a separate private/authorized repository;
- in another approved storage location.

A deliberately sanitized project may be committed later as a public example only when its visibility and purpose are explicit.

## Historical material

This boundary prevents new project-package tracking. It does not claim to remove bytes already present in Git history or another branch.

History rewriting, secret rotation, repository-visibility changes, and destructive data removal are separate security operations and require explicit authorization.

## Non-goals

This decision does not change:

- project package structure;
- Flow 2–7 semantics;
- delivery paths inside a project package;
- the ability to run PRD-Creator against `workspace/active/<project>/` locally;
- approved Golden/reference assets that intentionally belong to the system package.
