> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# SL-PRIVACY: Privacy Review

Agent: `security-lead`

**Trigger**: After `/app-privacy-review`, and at `/app-release` or `/app-store-prep` when the release collects, stores or shares personal data differently from the last reviewed version. Always on in lean and full modes when data handling changed, and whenever the user runs `/app-privacy-review`.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Privacy record path (`docs/security/privacy.md`) with the data inventory and flows
- Threat model path
- Store privacy declarations or data-safety forms drafted, per store
- Third-party SDKs and services that receive data; analytics and crash-reporting configuration
- Jurisdictions and audiences (for example children, health, region) if known

**Prompt**:
> "Review privacy for this app and release. Check:
> (1) Is every category of personal or sensitive data inventoried with purpose, lawful basis or consent, storage location, retention and who can access it?
> (2) Does the data actually collected by the code (including SDKs, analytics, crash reports, logs, clipboard and device identifiers) match the inventory and the declared store forms? List mismatches.
> (3) Is consent collected before collection, revocable and respected on each platform, and are platform permission prompts justified by a user-visible purpose?
> (4) Can the user export and delete their data, and does deletion reach backups, third parties and local copies within the stated retention?
> (5) Are transfers and third-party processors identified, with data minimized and with agreements or terms checked?
> (6) Do the store listings and the in-app privacy text say the same true thing, and are age and regional requirements addressed?
> Return CLEAR, CONCERNS [list], or BLOCK [blockers]."

**Verdicts**: CLEAR / CONCERNS / BLOCK

CLEAR means no issues, proceed. CONCERNS means issues that do not block, listed. BLOCK means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `SL-PRIVACY: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the privacy record or the store declarations being judged.
