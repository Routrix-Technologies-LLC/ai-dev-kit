> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# SL-THREAT-MODEL: Threat Model Review

Agent: `security-lead`

**Trigger**: After `/app-threat-model` writes `docs/security/threat-model.md`, and when architecture changes a trust boundary, adds an integration or changes the data handled.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Threat model path and the data-flow diagram it uses
- Architecture document path
- Data inventory or privacy record path, if any
- Stories created from mitigations

**Prompt**:
> "Review this threat model. Check:
> (1) Does the data-flow diagram show every actor, process, data store and trust boundary the architecture has, including update channels, IPC, plugins, third-party services and build and distribution pipelines?
> (2) Is each boundary analyzed across the STRIDE categories, with realistic abuse cases for the app's actual platforms (a malicious web page, local user or process, other app on the device, network attacker, compromised dependency, stolen device)?
> (3) Does each high-impact threat have a concrete mitigation tied to a component, a story or an ADR, and an owner, rather than 'follow best practices'?
> (4) Are secrets, credentials, tokens and personal data handled per platform storage facilities (OS keystores, Keychain, Keystore, server vault), with transport and at-rest protection stated?
> (5) Are residual risks and accepted risks written down with who accepted them, and are assumptions (for example 'the OS sandbox holds') stated?
> (6) Is it measurable against a standard such as OWASP ASVS or MASVS, so the audit can later verify each mitigation?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `SL-THREAT-MODEL: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the threat model or the architecture it models.
