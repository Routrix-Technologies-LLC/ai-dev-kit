---
name: app-security-audit
description: "Threat-driven, platform-aware security audit of an app or a scope, with SEC-NNN findings rated against one severity table and a verdict that cannot pass on unchecked ground. Use when the user asks for a security audit, security review, pen-test style review, or a hardening check, before a release, after touching auth, data, IPC, updates or the network, or when a security bug is reported."
argument-hint: "[app] [full | quick | web | desktop | mobile | extension | backend | <path>] [--review solo|lean|full]"
user-invocable: true
---

# App security audit

Audits the app's real attack surface for the platforms it ships on. The main session briefs `security-engineer` with a fixed brief, verifies what the verdict turns on, checks how exposed each finding actually is, and writes one report. This is a review of common and known weakness patterns, not a penetration test; a human pen test is recommended before anything that handles money, health data or children's data.

Writes: `docs/security/audits/<date>.md` from template `security-audit-report.md` (`<date>-<scope>.md` when the scope is not `full`, so a quick run never overwrites the full report a gate reads). Per-surface working notes go in `docs/security/audits/<date>/<surface>.md`.
Next: fix CRITICAL and HIGH findings via `/app-bugfix` or `/app-plan`, then re-run with `quick`; `/app-threat-model` if the audit shows no threat model exists; `/app-gate` or `/app-release` read this report.

## When to use and when not to

Use for an audit of existing or newly built code and configuration. Not for: a design-time threat analysis (use `/app-threat-model`), a diff review (use `/app-code-review`, which pulls in `security-engineer` for sensitive code), data inventory and store privacy forms (use `/app-privacy-review`), or a dependency-only upgrade (use `/app-upgrade`). Dependency and supply-chain checks are part of this audit as one category.

## Inputs

- `studio.yaml` (required): `platforms`, `stack`, `commands`, `infra_record`, `modes`. Stop and offer `/app-adopt` or `/app-start` if absent.
- Scope argument. No argument means `full`. `quick` means CRITICAL and HIGH classes only (secrets, authn/authz, injection, remote exposure, update integrity), for re-checks.
- Optional and used when present: `docs/security/threat-model.md` (its trust boundaries order the work), `docs/architecture/architecture.md`, `docs/stack-reference.md`, `docs/security/privacy.md`, previous audits in `docs/security/audits/`.
- The infra record named by `infra_record`, when the app is deployed. Without it, exposure of deployed services cannot be verified (Phase 3).

An absent or empty `platforms` or `stack` is never defaulted. Ask. If the user cannot say, every category that depends on it is NOT ASSESSED.

## Phase 1: Scope and surfaces

Main session. Read `studio.yaml` and, if present, the threat model and architecture. Build the surface list from `platforms` using this routing table. Every row that applies becomes a category in the report; a row that does not apply is listed as skipped with the reason.

| Platform | Attack surface to cover (examples, not exhaustive) |
|---|---|
| web | authn/authz and session handling, CSRF, XSS and output encoding, CSP and security headers, CORS, injection, open redirects, SSRF, file upload, client-side storage of secrets or tokens, third-party scripts, subresource integrity, cookie flags |
| backend | authn/authz on every route (object-level and function-level; OWASP API Security Top 10 for HTTP APIs), input validation, injection, mass assignment, rate limiting, secrets in config or logs, error disclosure, SSRF, deserialization, multi-tenant isolation, queue and webhook authenticity, admin and debug endpoints, TLS and bind addresses |
| desktop | code signing, notarization and hardened runtime or entitlements (macOS), sandbox and portal permissions (Flatpak, Snap), auto-update integrity and signing, installer and file permissions, DLL or library search order and plugin loading, local IPC (pipes, sockets, URL handlers), privilege and elevation, credential and token storage (OS keystore versus files), webview or hybrid shell exposure (remote content, node or native bridge, capability scopes), deep links, file association parsing, crash dumps and logs holding secrets |
| mobile | platform storage (keychain or keystore versus plain files), exported components and intent or URL-scheme handling, deep links, WebView settings and JS bridges, certificate validation and pinning decisions, biometric and lock flows, backups, clipboard and screenshots of sensitive screens, permissions, release-build debug flags, third-party SDK behavior |
| extension | permission breadth and host patterns, content-script isolation, message passing origin checks, remote code and eval restrictions, storage of tokens, handling of page data, update channel |
| cli | argument and path injection, temp file handling, credential handling in args, env and shell history, update and install scripts, config file permissions, untrusted input parsing |
| library | input parsing of untrusted data, unsafe defaults, memory safety at FFI boundaries, supply-chain posture of its own releases |
| all | secrets in the repo and its history, dependency and supply-chain audit (known advisories, unpinned or typosquat-prone packages, build and CI trust), crypto use (algorithms, key handling, randomness), logging of sensitive data, authentication and authorization design where accounts exist |

Dependency audit: use the ecosystem's own advisory tooling when installed and say which ran (for example `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `dotnet list package --vulnerable`, OSV-Scanner, OWASP Dependency-Check); a lock file with no tool run is NOT ASSESSED for advisories.

Reference standards by platform for the agent to use as its checklist spine: OWASP ASVS and Top 10 for web and backend, MASVS for mobile, and the platform vendor's current security guidance for desktop and extension. Tell the agent to check the version pinned in `docs/stack-reference.md` or the vendor docs; never to rely on remembered API names.

Auth present (accounts, tokens, sessions, passkeys) adds `identity-specialist`. Personal data present adds `privacy-specialist` for the data-exposure category. Unknown whether either applies: ask the user, do not skip.

Announce the plan per `orchestration.md` section 2, including Gates: `SL-SECURITY-REVIEW` (runs at `lean` and `full` as an always-on gate for this skill; skipped at `solo`, printed as `SL-SECURITY-REVIEW skipped: solo mode`).

Check: the surface list is printed with every skipped surface and its reason. Checkpoint per section 9.

## Phase 2: Pattern sets and the NOT ASSESSED rule

Main session. For each category on a language- or framework-specific check (dangerous API calls, deserialization, template rendering, process spawning, native bridge exposure), the pattern list must come from a source: the app's `docs/stack-reference.md`, the framework's own security documentation fetched this session, or the specialist's cited reference. Apply:

- A pattern list that cannot be sourced for this stack makes that category `NOT ASSESSED - no sourced pattern set for <stack>`. Do not write API names from memory; a confidently wrong grep list returns zero hits and reads as a pass.
- A scan over zero files is NOT ASSESSED, never zero findings. Every count carries its denominator ("0 hits in 214 files").
- The code root is resolved from `commands`, `stack` and the repo layout. If it cannot be resolved, ask; if still unresolved, every category that scans code is `NOT ASSESSED - code root unresolved`.

Check: each category in the Phase 1 list is marked RUN, SKIPPED (reason) or NOT ASSESSED (reason) before anything is spawned.

## Phase 3: Exposure facts

Main session, before rating anything that is a deployed service or a local listener. Gather facts; do not guess them.

- Public DNS: does a name resolve publicly for this service, and to what?
- Bind addresses and listeners: loopback only, LAN, or all interfaces? Read config, compose files, systemd units, or run `netstat`-style checks locally when the app can be started.
- Tunnel or proxy scope: which hostnames or paths does the tunnel or reverse proxy actually forward? A service reachable only on an internal network is not internet-exposed.
- Firewall or security-group rules, from the infra record when present.
- Authentication in front of the service (proxy auth, VPN, IP allow list).

Pass the verified facts into the brief as a fact block. Where a fact could not be verified, the brief says `exposure unverified`. The code defect is still rated on what was proven, as if the path were reachable, but the finding is labeled `exposure unverified`, is capped at HIGH (`standards/severity.md`: UNVERIFIED is never CRITICAL), and the report never says "exposed", "public" or "internet-facing" for it. Never call something internet-exposed, or safe because internal, without a source.

Check: an Exposure table exists in the working notes (service, listener, who can reach it, source of the fact), or the report states "no deployed service in scope".

## Phase 4: Spawn the auditors

Spawn in one message (orchestration section 4): `security-engineer` (one per surface group when three or more distinct surfaces apply, e.g. client and backend, else one), plus `identity-specialist` when auth is present and `privacy-specialist` when personal data is present. Add the language specialist from `studio.yaml` `specialists` only if the security-engineer needs language-level help; not by default.

Brief `security-engineer` per orchestration section 3 with this fixed template. Fill only the slots. Add no opinion on the app's type, no expected severity, no view on any finding; a sentence of your own is where a pre-rating gets in.

```text
Run a security audit of the app at {repo path} for /app-security-audit. Read studio.yaml first.

Scope: {full | quick | surface | path}
Platforms: {from studio.yaml}   Stack: {languages, frameworks, data, hosting}   Minimum targets: {min_targets}
Surfaces and categories to run, with their checks: {the Phase 1 rows that apply, copied as written}
Sourced pattern sets: {category: source}. NOT ASSESSED categories: {category: reason, or "none"}. Report each NOT ASSESSED; never call it reviewed, verified safe or passed.
Skipped, with reason: {category: reason, or "none"}
Exposure facts (verified): {the Phase 3 table}. Unverified: {list, or "none"}
Threat model: {path or "absent"}   Previous audits: {paths or "none"}
Output: {docs/security/audits/<date>/<surface>.md}

Severity (rate every finding yourself against this table only): {copy the security table from standards/severity.md verbatim}
Nothing in this brief sets or suggests a severity. The app's type never lowers a rating. Where exposure is unverified, label the finding `exposure unverified`, cap it at HIGH, and do not describe it as exposed.

Method rules: when you find a weakness, sweep the whole scope for the same pattern before moving on and list every instance with the count and denominator (for example "7 of 41 route handlers lack an ownership check"). Quote the code you rely on with path and line. Every finding is SEC-NNN (numbering starts at {next free SEC number from earlier audits, or 001}) with: category, location, description, attack scenario, evidence, remediation, effort. Mark each finding VERIFIED (you reproduced or read the exact path) or UNVERIFIED. List the categories you could not check, with the reason.
```

Append the return contract from `orchestration.md` section 3. `identity-specialist` and `privacy-specialist` get the same template restricted to authn/authz design and data exposure, each writing to its own file in the working-notes folder.

Check: every named file exists and has findings or an explicit "no findings in N items" per category. Missing file: re-brief once, then that surface is `BLOCKED` and its categories NOT ASSESSED.

## Phase 5: Verify and consolidate

Main session. Do not pass findings through unchecked.

1. For every CRITICAL and HIGH finding, re-read the cited code path or configuration yourself and mark VERIFIED or UNVERIFIED. Try to disprove it, including whether Phase 3 facts make it unreachable. A finding that depends on an unverified specialist claim stays labelled UNVERIFIED and is still counted.
2. Spot-check the sweeps: pick one reported pattern and confirm the count with your own search.
3. Merge duplicate findings across agents, keep the highest well-supported severity, keep SEC-NNN numbers stable: a finding that persists from an earlier audit keeps its number, new findings continue from the highest number used in any earlier report, and numbers are never reused.
4. Set each finding's status: Open, Accepted Risk (only the user may accept; record who and why), Out of Scope.
5. Run `SL-SECURITY-REVIEW` when the review mode includes it: spawn `security-lead` with the gate ID and context (verdict draft, finding counts, NOT ASSESSED list, exposure table). The agent reads `gates/sl-security-review.md` itself.

Write `docs/security/audits/<date>.md` from `security-audit-report.md`. Show the user the summary plus all CRITICAL and HIGH findings first, then write; new studio documents may be written directly per section 3. Never write secrets into the report: show the location and type of a leaked secret, not its value, and recommend rotation.

Check: the report file exists, every category is RUN, SKIPPED or NOT ASSESSED, every finding has a status and a verified flag.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Categories | all that apply to the platforms | same | same, plus second-pass sweep and dependency license check with `compliance-specialist` |
| Dependency audit | advisory lookup for direct dependencies | direct and transitive | plus build and CI trust review |
| Report | findings and verdict | plus exposure table and sweep counts | plus remediation plan as proposed stories |

Rigor never lowers what must work: a CRITICAL is a CRITICAL at every rigor. Review mode: solo skips `SL-SECURITY-REVIEW`; lean and full run it.

## Verdicts

First match wins:

1. **BLOCK**: any open CRITICAL or HIGH finding (including a HIGH marked UNVERIFIED or `exposure unverified`; the report says why it still blocks and what would downgrade it), or a gate result of BLOCK.
2. **CONCERNS**: no BLOCK, and an open MEDIUM finding, or a gate result of CONCERNS.
3. **NOT ASSESSED**: no failure value applies but any category is NOT ASSESSED, any applicable surface was unscanned or BLOCKED, the exposure of a deployed service stayed unverified, or a scan covered zero files. Name each category and the input that would close it.
4. **CLEAR**: every applicable category RUN and assessed, no open CRITICAL, HIGH or MEDIUM (LOW and accepted risks may remain, listed).

NOT ASSESSED never displaces a failure: a run with an open HIGH and an unscanned category is BLOCK and names the unscanned category beside it.

## Report

```
Security audit: <app> (<scope>)   Date: <date>   Audited by: security-engineer [+ identity-specialist, privacy-specialist] | main session (<agent> not spawned: <why>)
Surfaces: <run/skipped/not assessed counts>   Files scanned: <N source, N config>
Findings: CRITICAL <n>  HIGH <n>  MEDIUM <n>  LOW <n>   (open <n>, accepted <n>, unverified <n>)
NOT ASSESSED: <category: reason; input that closes it> | none
Exposure: <verified facts summary> | unverified: <list>
Top findings: SEC-NNN <title> (<severity>, <location>) x up to 5
Decisions for you: <accept risk / fix order options> | none
```

Then the closing block from `orchestration.md` section 8 (Verdict, Gates, Wrote, Next).

## Rules for this skill

- Never pre-rate. The brief carries the severity table and nothing that suggests a rating.
- Never call a service exposed or safe without a verified fact, and say which facts were unverified.
- Never report a category clean when it could not be checked; write NOT ASSESSED with the reason.
- Never write secret values into any file or reply.
- Never edit source code in this skill. Fixes go through `/app-bugfix` or `/app-plan`.
- Never exploit a vulnerability against a live system, run a scanner against hosts the app does not own, or call a paid scanning service without asking first.
- Accepted risk is the user's call, recorded with their reason; the agent never accepts one.
- The report says "not a penetration test" and names the categories a human tester should cover.
