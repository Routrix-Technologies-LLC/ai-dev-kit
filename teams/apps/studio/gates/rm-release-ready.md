> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# RM-RELEASE-READY: Release Readiness

Agent: `release-manager`

**Trigger**: At `/app-release` after the other release gates have returned, and at `/app-hotfix` before deploy. Always on in lean and full modes. Never overrides a blocking verdict from another gate.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Version, channels and platforms being shipped
- Release checklist path (`docs/release/<version>.md`) and changelog diff
- Results of QL-RELEASE-QUALITY, SL-SECURITY-REVIEW and SL-PRIVACY (verdict lines)
- Packaging, signing and notarization or store status per platform; release notes path
- Rollout and rollback plan; monitoring and on-call or contact for the first days

**Prompt**:
> "Decide whether the release mechanics are ready. Check:
> (1) Do all required release gates show a passing verdict on this exact version? A blocking verdict (BLOCK, NOT READY, NO GO and the like) means NO GO. A CONCERNS verdict means CONCERNS. A NOT ASSESSED verdict, or a gate skipped by review mode, means your answer is at best NOT ASSESSED, never GO; a problem you find yourself takes its own word first.
> (2) Is each artifact built reproducibly from the tagged source, signed with the right identity, and verified to install and launch on a clean machine or device for each platform and channel (installers, store packages, containers, deployments)?
> (3) Are the version number, changelog and release notes correct, accurate about changes and known issues, and consistent with the store listings?
> (4) Is the rollout staged where the channel allows it, with a defined halt condition and a tested rollback or downgrade path, including data and schema compatibility?
> (5) Is monitoring in place to detect a bad release quickly (crash and error rates, key flows), and is someone responsible for watching it?
> (6) Are store, certificate, domain and approval lead times accounted for, and does the user retain the final act of publishing or deploying?
> Return GO, CONCERNS [list], or NO GO [blockers]."

**Verdicts**: GO / CONCERNS / NO GO

GO means no issues, proceed. CONCERNS means issues that do not block, listed. NO GO means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `RM-RELEASE-READY: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the release checklist, or the results of the other release gates.
