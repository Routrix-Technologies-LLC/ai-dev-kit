---
name: app-threat-model
description: "Build a STRIDE threat model over the app's data-flow diagram and trust boundaries, with platform-specific threats, ranked risks, and mitigations turned into proposed stories. Use when the user starts or changes anything touching auth, money, personal data, IPC, updates, deep links, the network or extensions, before architecture is accepted, or asks 'what could go wrong security-wise'."
argument-hint: "[app] [full | <scope or feature>] [--review solo|lean|full]"
user-invocable: true
---

# App Threat Model

Finds what can go wrong before it is built, in a form the team can act on. It draws the data flows and trust boundaries, applies STRIDE to every element that crosses or sits at a boundary, adds the threats specific to the app's platforms, rates and ranks the risks, and converts each accepted mitigation into a proposed story. It is a design-time model; checking the built code against it is `/app-security-audit`.

Writes: `docs/security/threat-model.md` (template `threat-model.md`).
Next: `/app-plan` (the proposed stories), `/app-architecture` (boundary changes), `/app-security-audit` (verify the build against this model), `/app-privacy-review` (personal data flows).

## When to use and when not to

- Use at architecture stage for the whole app, and again whenever a new boundary appears: a new integration, a new IPC surface, auth changes, a new data class, an updater, a plugin or extension point.
- Auditing existing code for vulnerabilities is `/app-security-audit`. A single endpoint's contract is `/app-api`. Data inventory and consent are `/app-privacy-review`.

## Inputs

- Required: `studio.yaml`, and the architecture doc (`docs/architecture/architecture.md`) or enough description of components and data flows to draw them. No architecture yet: offer `/app-architecture`, or draw a first diagram with the user in Phase 2 and label it PROVISIONAL.
- Optional: existing threat model (update it; never overwrite sections the user has edited without showing the diff), API contracts, the privacy record, incident history, the brief's user and data descriptions.
- Unknown facts (what data is stored, who can call this) are asked or recorded as UNKNOWN. An UNKNOWN on a trust boundary is a risk item, not a skip.

## Platform routing

| Platform in `studio.yaml` | Specialists | Platform threats that must be walked (Phase 4) |
|---|---|---|
| web | `web-lead`, `frontend-engineer` | XSS (stored, reflected, DOM), CSRF, clickjacking, CORS and CSP misconfiguration, session cookie flags, open redirects, third-party script supply chain, subresource integrity, service worker scope |
| backend | `backend-lead`, `identity-specialist` | Injection, broken authentication and authorization (object and function level), SSRF, mass assignment, rate limiting and abuse, secrets handling, multi-tenant isolation, webhook spoofing, deserialization |
| windows, macos, linux | `desktop-lead`, `hybrid-desktop-engineer`, the OS engineer | Local IPC callers and identity checks, webview bridge exposure and capability scope, auto-updater integrity (signed, pinned channel, downgrade protection), installer and DLL or library search path hijack, privilege elevation, custom URL scheme handlers, files written to user-writable locations later executed, local data at rest, crash dumps leaking data |
| ios, android | `mobile-lead`, `ios-engineer`, `android-engineer`, `cross-platform-mobile-engineer` | Local storage and keychain or keystore use, backups and screenshots leaking data, deep links and universal or app links (hijack, parameter injection), exported components and intents, WebView settings, certificate validation and pinning, jailbreak or root assumptions, push payload content, clipboard, extension and widget data sharing, debug builds shipped |
| extension | `web-platform-engineer` | Permission breadth (host, tabs, storage, native messaging), content script to page trust, message origin checks, remote code, update channel, data exfiltration through granted permissions |
| cli | `principal-engineer`, language specialist | Argument and environment injection, config and credential files and their modes, temp file races, update and install scripts, piped input, plugin loading |
| library | `principal-engineer` | Misuse-resistant defaults, input handling in public functions, dependency chain, unsafe code and FFI boundaries |

Always: `security-lead` (owns the model and its gate), `security-engineer` (STRIDE pass, mitigations), `privacy-specialist` (personal data flows, linkability, disclosure threats). Add `identity-specialist` when sign-in or sessions exist, `integrations-engineer` for third-party services, `ai-features-engineer` when a model receives untrusted input or can take actions (prompt injection, data leakage through context, tool authority).

## Phase 1: Resolve and announce

Per `orchestration.md` sections 1 and 2. Decide the scope: `full` (the whole app) or a named feature or boundary. Check for an existing `docs/security/threat-model.md` and decide update versus create.

Check: announce block printed, scope stated, existing model noted.

## Phase 2: Data-flow diagram and trust boundaries

Spawn `security-lead` (or draft in the main session and have `security-lead` review) with the architecture doc excerpt. Output goes into section 2 of the model.

1. List **assets** worth protecting: credentials and tokens, personal data by class, payment data, user content, signing keys, the update channel, the integrity of the app's code and config, availability.
2. List **actors**: anonymous user, signed-in user, administrator, another tenant, a malicious local process or user on the same machine, a malicious web page, a compromised dependency, a third-party service, the operator, an insider.
3. Draw the diagram as text (a Mermaid diagram or an indented list; the file must be readable without a renderer). Elements: external entities, processes, data stores, data flows. Number every element and every flow (`E1`, `P1`, `D1`, `F1`) so threats can cite them.
4. Mark **trust boundaries** on the diagram: client to server, process to process, app to OS service, web page to native bridge, app to third party, user device to cloud, tenant to tenant, build pipeline to release.
5. List **entry points**: every place data or control enters (endpoints, IPC commands, deep links, file open handlers, push messages, clipboard, command line, environment, update feed).

Decision point: show the diagram and boundary list; ask the user to confirm or correct (AskUserQuestion). A diagram the user has not seen is not the model.

Check: the model file has numbered elements and flows, at least one trust boundary, and an entry point list; or a stated reason there is no boundary (a stand-alone offline tool with no input from others still has a file input boundary).

## Phase 3: STRIDE over the diagram

Spawn in parallel, one file each under `~/AgentScratch/app-threat-model/<run>/`: `security-engineer` (all elements, STRIDE), `privacy-specialist` (information disclosure and linkability on every flow carrying personal data), plus the platform specialists from the routing table, each for the elements in their platform.

Brief each with the numbered diagram and this method:

| Letter | Threat | Question per element | Applies to |
|---|---|---|---|
| S | Spoofing | Can something pretend to be this user, process, device or server? How is identity proven at this boundary? | entities, processes, flows |
| T | Tampering | Can data in the store or in transit, or the code itself, be altered? Who can write it? | stores, flows, processes |
| R | Repudiation | Could an actor deny an action? Is there a log that survives and cannot be edited by that actor? | processes, entities |
| I | Information disclosure | Can data be read by someone who should not? In transit, at rest, in logs, in crash reports, in error messages, through side channels? | stores, flows, processes |
| D | Denial of service | Can it be made unavailable or exhausted: resource, rate, size, lock, update that bricks? | processes, stores, flows |
| E | Elevation of privilege | Can someone gain rights they were not given: a lower-privilege caller invoking a higher-privilege command, escaping a sandbox? | processes |

Each agent returns threats as rows: id (`T-NNN`), element or flow id, STRIDE letter, the threat in one sentence naming an actor and an action, the existing control (or none), likelihood and impact (low, medium, high with a one-line reason), and a proposed mitigation. A threat that cannot be traced to an element is rejected as speculation.

Check: every file exists; every element and flow in the diagram has at least one STRIDE row or an explicit "none applies: <reason>". The main session counts the coverage (elements covered of elements listed) and prints it with the denominator.

## Phase 4: Platform threats

Using the routing table, require each platform specialist to walk their list and mark each item: threat found (row added), not applicable (reason), or NOT ASSESSED (missing information). A platform in `studio.yaml` with no specialist file returned is a named gap; its threat list shows as NOT ASSESSED in the model.

Also cover, for every platform, the supply chain (dependencies, build pipeline, signing keys, update delivery) and the secrets in play (where each lives, who can read it, how it rotates).

Check: each in-scope platform has a completed checklist table in the model with no blank rows.

## Phase 5: Rate, rank and decide

Main session merges the rows, removes duplicates (keep both ids cited), and rates each risk using `standards/severity.md` words: CRITICAL, HIGH, MEDIUM, LOW from likelihood and impact. Verify the CRITICAL and HIGH threats yourself: re-read the cited element and flow, and confirm the actor can really reach the entry point. Mark any not re-checked `UNVERIFIED`.

For each threat, the response is one of: mitigate (with the control), accept (with owner and reason), transfer (to a platform or provider, stating what they guarantee, sourced), avoid (remove the feature). Accepting a CRITICAL or HIGH risk needs the user's explicit word.

Decision point: present the ranked top risks and the proposed responses; ask the user to approve the set, or choose per item (AskUserQuestion, grouped; ask once for the set). The response to a CRITICAL or HIGH risk is never chosen for the user.

## Phase 6: Mitigations become proposed stories

For every mitigate response, add a row to the model's "Proposed stories" table: title, threat ids addressed, change type (Security, Config, Infra, Logic), acceptance criterion in binary form ("the IPC command `X` rejects callers other than the app's own signed process, shown by test `Y`"), owner role from the roster, and priority (P0 to P3 by risk). Do not write story files; `/app-plan` creates them from this table and the threat ids stay as the traceability link.

Also list **residual risks** (accepted or unmitigated) and **assumptions** the model rests on (for example "the OS keychain protects secrets from other apps"), each with how it would be checked.

## Phase 7: Write, gate, checkpoint

Ask once for the file, then write `docs/security/threat-model.md` from the template, using its numbered headings (1 Scope, 2 Data-flow diagram, 3 Trust boundaries, 4 Assets, 5 Threats by STRIDE (with the platform checklists as subsections), 6 Mitigations (`M-NNN`, each addressing `T-NNN` ids), 7 Residual risk, 8 Stories raised (the proposed stories table, status `Proposed`), 9 Review triggers, Change log), with the Last reviewed date, the scope, the diagram, the boundary and entry point lists, the STRIDE table with coverage counts, platform checklists, the ranked risks, responses, proposed stories, residual risks and assumptions. Existing model: update in place, keeping ids stable (never renumber `T-NNN`); mark removed threats `Closed` with the reason.

Gate `SL-THREAT-MODEL` (owner `security-lead`) is this skill's own single-purpose gate, so it runs in `lean` and `full` and is skipped in `solo` (`gates/README.md`). Spawn it with the model path and its diagram, the architecture document path, the privacy record path if any, the proposed stories, the platforms and the coverage count; it reads its own gate file. Its words are APPROVE, CONCERNS, REJECT or NOT ASSESSED. Record the result directly under the title as `> **Security Lead review (SL-THREAT-MODEL)**: <VERDICT> <date>` (no line when skipped). CONCERNS: ask to revise, accept (recorded in Residual risk) or discuss. Overwrite the checkpoint.

Map each mitigation to a verifiable requirement in the standard that fits the platform (OWASP ASVS for web and backend, OWASP MASVS for mobile; look up the current version and requirement ids from the official source rather than from memory, or write the mapping as NOT ASSESSED) so `/app-security-audit` can check it later.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Scope | boundary list, entry points, top 10 threats | full diagram, STRIDE on every element, platform checklists | plus abuse cases, supply chain section, residual risk sign-off by `security-lead` |
| Agents | `security-engineer` plus the platform specialist | plus `privacy-specialist` | plus identity, integrations and AI specialists where they apply |
| Re-run trigger | new boundary | new boundary or quarterly review | each release that changes a boundary |

Rigor changes how deep, never whether CRITICAL and HIGH threats are verified.

| Review mode | Gates |
|---|---|
| solo | `SL-THREAT-MODEL skipped: solo mode` |
| lean | SL-THREAT-MODEL runs (the own gate of a single-purpose review skill, always-on in lean) |
| full | SL-THREAT-MODEL runs |

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

1. `BLOCKED`: the architecture or diagram cannot be established, a required agent returned nothing after one re-brief, or the gate returned REJECT. The skill says what is missing and writes only a partial model labelled so.
2. `NOT ASSESSED`: the model is written, but a platform checklist, a trust boundary or an element could not be assessed (missing specialist file, UNKNOWN boundary the user could not resolve), or `SL-THREAT-MODEL` returned NOT ASSESSED. The verdict line lists each area; the model marks them NOT ASSESSED, and a clean gate is not claimed.
3. `COMPLETE`: the model is written, STRIDE coverage is stated with its denominator, platform checklists are filled, every CRITICAL and HIGH threat has a user-approved response, and nothing above applied.

## Report

```
Threat model: <scope>   Platforms: <list>
Diagram: <N entities, N processes, N stores, N flows, N trust boundaries, N entry points>
STRIDE coverage: <elements covered of elements listed>   Platform checklists: <N of N complete>
Threats: CRITICAL <N>, HIGH <N>, MEDIUM <N>, LOW <N>   UNVERIFIED <N>   NOT ASSESSED areas: <list or none>
Responses: mitigate <N>, accept <N>, transfer <N>, avoid <N>
Proposed stories: <N> (P0 <N>, P1 <N>, ...)
Skipped: <agent or step and why>

Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: SL-THREAT-MODEL: <verdict> | none run (<mode> mode)
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Every threat cites a numbered element or flow. No generic checklist dumps.
- Never mark an element "no threats" without a reason, and never treat an UNKNOWN trust boundary as safe.
- Never choose the response to a CRITICAL or HIGH risk for the user, and never accept one silently.
- Never write story files or change code; the model produces a table for `/app-plan`.
- Never state that a platform mechanism protects something unless that is sourced or checked; otherwise list it as an assumption.
- Never renumber threat ids or delete a closed threat.
- Never put real secrets, keys or personal data in the model.
