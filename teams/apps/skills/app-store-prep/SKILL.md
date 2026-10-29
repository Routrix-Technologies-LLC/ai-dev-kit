---
name: app-store-prep
description: "Draft a store submission package for an app: listing text, screenshot plan, privacy and data declarations, age and content ratings, review notes, pricing and in-app purchase setup, and a response to a rejection. Drafts only; the user submits. Use when the user says store listing, App Store, Google Play, Microsoft Store, Mac App Store, extension store, Flathub, submission, review notes, privacy labels, or pastes a store rejection."
argument-hint: "[app] [store or 'all'] [draft | rejection] [--review solo|lean|full]"
user-invocable: true
---

# App Store Prep

Builds everything a store submission needs as a reviewable draft, checks it against the store's current published rules and against the app's own privacy record, and says honestly what is still missing. It never submits, never signs in to a store console, and never writes credentials.

Writes: `docs/release/store/<store>.md` (template `store-listing.md`), one per store. In `rejection` mode it appends a dated "Rejection response" section to that file.
Next: `/app-privacy-review` (if the data record is missing or stale), `/app-release` (the submission itself is an act there), `/app-a11y-audit`, `/app-i18n`.

## When to use and when not to

- Use before the first submission to a store, before a release that changes permissions, data collection, pricing or purchases, and after a rejection.
- Not for the release decision (`/app-release`), the privacy analysis itself (`/app-privacy-review`; this skill reconciles with it), or the build and signing (`desktop-packaging-engineer` through `/app-release`).
- Stores that apply to the app come from `studio.yaml` `platforms` and the user; `web`, `backend` and `cli` apps usually have no store. If none applies, say so and stop.

## Inputs

- `studio.yaml` (`platforms`, `stack`, `app.summary`, `rules`); `docs/product/brief.md` or `vision.md`; `docs/security/privacy.md`; `docs/security/threat-model.md` if present; the newest accessibility and i18n reports; the app's manifest and permission declarations; the dependency and SDK list from the lock files.
- **Store list:** propose from `platforms` (see table), then ask the user to confirm. Never assume a store.
- **Store rules are facts that change.** Every rule, size, limit and requirement in the draft carries a source URL and the date it was checked. Do not write one from memory. If a rule cannot be fetched now, mark the item `NOT SOURCEABLE` and let it make the verdict NOT ASSESSED.
- Credentials, demo-account passwords and signing assets are never written to the file; the file says where they are supplied out of band.

## Store routing

| Store | Platforms | Main things the draft must cover (verify each against the store's current docs) |
|---|---|---|
| Apple App Store | ios, macos | listing per locale, screenshot sizes per device class, privacy nutrition label, privacy manifest and required-reason API usage, age rating answers, export compliance, entitlements and permission purpose strings, review notes with a demo account, in-app purchase products, the equivalent-login-option rule where third-party sign-in exists (check the current guideline text), account deletion in app where accounts exist |
| Mac App Store | macos | all of the above plus sandbox entitlements justified one by one |
| Google Play | android | store listing, graphics set, data safety form, content rating questionnaire, target API requirement, app signing enrollment, testing track requirements, permissions declarations (sensitive ones need justification), ads and families policies if relevant |
| Microsoft Store | windows | package identity and packaging format, listing, age rating, capabilities declared (restricted ones need justification), pricing, certification notes |
| Browser extension stores | extension | single purpose statement, per-permission justification, privacy practices disclosure, remote code policy, screenshots and promo images |
| Flathub, Snap Store, other Linux stores | linux | AppStream metadata, license identifiers, sandbox permissions declared and justified, screenshots, release notes metadata; the submission mechanism (for Flathub a pull request to its repository) is the user's act |

`app-store-specialist` owns the rules; `privacy-specialist` the declarations; `content-designer` the words; `monetization-specialist` pricing and purchases.

## Phase 1: Resolve and inventory

Follow `orchestration.md` sections 1 and 2. Print the plan block. Gates (`gates/README.md`): `SL-PRIVACY` runs in Phase 5 at `lean` and `full` when the version's personal-data handling changed since the last reviewed one (unknown means ask), and always at `full`; `solo` prints `SL-PRIVACY skipped: solo mode`. No other gate; the checks below are the skill's own.

1. Confirm the stores and the mode: `draft` (default) or `rejection` (the user pastes the rejection message or its path; go to Phase 6).
2. Main session builds a facts sheet at `.studio/drafts/store-prep-<store>-facts.md` (local scratch): app name, bundle or package id, version, categories, supported OS floor from `min_targets`, permissions and entitlements found in the manifest (quote file and line), third-party SDKs found in the lock files, whether there are accounts, purchases, ads, user-generated content, children as audience, data sent off the device. Unknown values are written `UNKNOWN`; the user is asked, not guessed.
3. Check the privacy record: if `docs/security/privacy.md` is missing, or older than the last change to the dependency or permission list, the declarations section is NOT ASSESSED; recommend `/app-privacy-review` and continue with the rest.

## Phase 2: Policy and requirements (app-store-specialist)

Spawn `app-store-specialist` per store (parallel across stores), brief per `orchestration.md` section 3, output to `.studio/drafts/store-prep-<store>-app-store-specialist.md`. It uses WebSearch and WebFetch on the store's own official documentation and returns: the required fields with limits, the asset specs, the policies this app touches (from the facts sheet), the testing-track or review prerequisites, and a source URL and fetch date for each. It flags every place where the app as built appears to conflict with a policy (for example a permission with no stated purpose, an SDK that triggers a disclosure). Verify two of its quoted rules by fetching the cited page yourself; unverified rules are labelled UNVERIFIED in the draft.

## Phase 3: Drafts (parallel)

Spawn together, each writing its own scratch part (never the final file):

| Agent | Produces | Path |
|---|---|---|
| `content-designer` | name, subtitle or short description, long description, keywords or tags, "what's new", localized variants for the locales the app ships, within the limits from Phase 2; plain, accurate claims | `.studio/drafts/store-prep-<store>-content-designer.md` |
| `privacy-specialist` | the store's privacy and data declarations answered field by field from `docs/security/privacy.md` and the SDK list; a table of every data type with collected, shared, purpose, optional, retention | `.studio/drafts/store-prep-<store>-privacy-specialist.md` |
| `monetization-specialist` | pricing, trial and subscription terms, in-app products with ids and names, restore-purchases and cancellation behavior, paywall copy and ethics check; omitted if the app is free with no purchases (then record "free, no purchases: confirmed with user") | `.studio/drafts/store-prep-<store>-monetization-specialist.md` |
| `app-store-specialist` | screenshot plan (which screens and states, per required size and locale, capture method with no focus stealing or input injection, caption text), icon and graphic requirements, review notes (what the reviewer needs: how to reach each feature, demo account supplied out of band, hardware or server needed, explanations for permissions) | `.studio/drafts/store-prep-<store>-assets-app-store-specialist.md` |

Each reply uses the return contract. The privacy-specialist must reconcile against the actual data flows; where the inventory and the code disagree it says so rather than choosing one.

## Phase 4: Assemble and check

1. Main session merges the parts into `docs/release/store/<store>.md` using `store-listing.md`, one section per field with its limit, current length (count the characters of each text field), source, and status (DRAFTED, VERIFIED, NOT SOURCEABLE, USER INPUT NEEDED). A text field over its limit is a gap.
2. Cross-checks, each reported pass or fail with evidence: every permission or entitlement in the manifest has a stated purpose in the listing, review notes or declarations; every SDK that collects data appears in the declarations; the screenshots plan covers every required size and each shipped locale; the description makes no claim the app does not do (compare against the specs); prices and product ids match the monetization part; version and ids match the manifest.
3. Assets: screenshots that exist already are listed with dimensions (read them); missing ones stay in the plan as TO CAPTURE with the capture method. This skill does not fabricate store graphics.

## Phase 5: Verdict and handoff

Ask once for the set of decisions the drafts surfaced (names, claims, categories, rating answers, pricing). The user decides; record each answer. Present the missing-items list with owners. At `lean` and `full`, when personal-data handling changed, spawn `security-lead` for `SL-PRIVACY` (told to read `gates/sl-privacy.md`; context: `docs/security/privacy.md`, the drafted declarations per store, SDK list) and record the outcome under the store file's title. A BLOCK is a GAPS verdict. The user performs the submission; recommend `/app-release` for the act.

## Phase 6: Rejection mode

1. Read the rejection text and the draft file. Quote the cited guideline or policy and fetch its current wording from the official source (date it).
2. `app-store-specialist` classifies the rejection: a real defect, a metadata or declaration mismatch, a reviewer misunderstanding, a missing prerequisite, or an ambiguous request for more information. `privacy-specialist` is added if data or permissions are cited; `content-designer` if wording is.
3. Draft the response in the store's resolution-center style: factual, specific, respectful, referencing steps to reproduce, with what changed. Distinguish "we fixed X in build N" from "we believe this is a misunderstanding because". Never promise a fix that is not made. Draft the code or metadata changes as stories or a `/app-bugfix` suggestion.
4. Append the dated "Rejection response" section; the user sends it.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Content | listing, screenshots plan, privacy declarations, review notes | plus policy cross-checks with sources, monetization, locales | plus accessibility statements, age rating rationale, rejection playbook |
| Review (by review mode) | solo: none | lean: `SL-PRIVACY` when data handling changed | full: `SL-PRIVACY` |

Rigor never relaxes sourcing: every store rule is cited or marked NOT SOURCEABLE.

## Verdicts

First match wins, per store; the overall verdict is the worst store.

1. **GAPS:** a gate returned BLOCK; any required field is missing, over its limit, or conflicts with the manifest, the code or the privacy record; a permission has no purpose; a declaration is known to be wrong.
2. **NOT ASSESSED:** a rule could not be sourced, the privacy record is missing or stale, the SDK list could not be read, a required user input is unanswered, or an agent did not return.
3. **READY TO SUBMIT:** every required field is filled and within limits, every rule is sourced and dated, every cross-check passes, and the declarations match the privacy record. This is a statement about the draft, not about the store's decision.

## Report

```
Store prep: <app>  Stores: <list>  Mode: <draft|rejection>  Rigor: <r>  Review: <mode>
Per store: <store: n of n required fields drafted, n over limit, n sourced of n rules, cross-checks n of n pass>
Privacy record: <current | stale | missing>   Screenshots: <n of n sizes planned, n captured>
Verdict: <WORD> - <one line why>
Gates: <SL-PRIVACY: VERDICT> | none run (<mode, or data handling unchanged>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Draft only. Never submit, sign in to a console, or press a store button; the user submits.
- Never write credentials, demo-account passwords, keys or tokens into any file; say where they are supplied.
- Every store rule and limit is cited with a date from the official source, or marked NOT SOURCEABLE. No rule from memory.
- Never claim a feature, a rating or a data practice the specs, code and privacy record do not support.
- Parallel agents write separate scratch parts; only the main session writes the final file.
- Recommend the next skill; never start it.
