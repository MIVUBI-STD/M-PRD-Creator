## Purpose

Describe the one logical outcome this pull request delivers.

## Target boundary

- [ ] `develop` work / review only
- [ ] `develop` → `Local` verified integration promotion
- [ ] `Local` → `main` stable promotion

## Scope

**Changed owners:**

**Intentionally not changed:**

## Verification

- [ ] Cheapest relevant local/static proof completed
- [ ] Repository Verify when applicable
- [ ] PRD Verify when applicable
- [ ] Voice Verify when applicable
- [ ] Local promotion gate for `develop` → `Local`
- [ ] Stable release gate for `Local` → `main`

Manual promotion acceptance (there are no automatic workflow checks):

- [ ] `develop → Local`: dispatch `Local Promotion Verify` on `develop` with this PR number and attach successful run URL.
- [ ] `Local → main`: dispatch `Release Verify` on `Local` with this PR number and attach successful run URL.
- [ ] Recorded gate evaluated the current PR test-merge candidate; head/base are unchanged since that run.

Evidence / relevant result:

## Repository hygiene

- [ ] No credentials, private client/source material, or live project package data added
- [ ] No generated/transfer-only artifact was promoted to source of truth
- [ ] No unrelated cleanup/refactor was bundled into this change
- [ ] Package version was changed only if the product/contract version rule requires it

## Local promotion contract

For `develop` → `Local` promotion:

- [ ] This PR represents one approved logical update
- [ ] Merge method will be **Squash and merge**
- [ ] Result must add exactly **one** new commit to `Local`
- [ ] After merge, `develop` will be synchronized/reset to the resulting `Local` HEAD before new work begins

Do not continue development from the pre-squash commit chain after promotion.

## Stable main promotion contract

For `Local` → `main` promotion:

- [ ] Source branch is `Local`
- [ ] `Stable release gate` passes on the pull-request merge candidate
- [ ] Merge method will be a normal **merge commit**
- [ ] The resulting `main` stable marker will not be synchronized back into `Local` or `develop`

`Local` intentionally does not absorb main-only stable-marker commits merely to satisfy ancestry. Stable verification must validate the merge candidate instead.

Publishing rule: a new protected `v*` tag and GitHub Release is created only when this stable state includes an approved PRD-Creator feature/capability change. Governance, CI, ruleset, documentation, and maintenance-only promotions remain untagged.
