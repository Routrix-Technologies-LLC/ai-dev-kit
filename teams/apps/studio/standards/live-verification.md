# Live verification

Done means it works where it runs. Evidence for any change with runtime behaviour comes from the built artifact, deployed to a real test environment and exercised the way a user or an attacker would. Unit tests, fakes and code review are extra layers. They are never the proof. Rigor (`rigor.md`) never relaxes this.

Why: an agent that writes code and an agent that tests that code are the same model from a different angle, and a mock only proves the mock. A real running system and real tools give independent signal.

## What counts as live

| Change touches | Live proof is |
|---|---|
| A service, API or backend | The built service running on the test environment, hit with real requests over the real network path (`curl`, a client, a load tool). Request, response and the relevant log lines are retained |
| A web UI | A real browser, headless and never stealing focus, driven against the web UI served by the test environment. Screenshots are retained and opened and looked at, with console errors and failed requests counted |
| A desktop app or installer | The real installer or package installed on a real or virtual machine (clean snapshot), launched, used for the story's path, then upgraded and uninstalled where the story touches those |
| A mobile app | The signed or release-configuration build installed on an emulator, simulator or device, and the story's path driven there |
| A CLI or library | The packaged artifact installed the way a user installs it, then run on real input in a clean directory or container |
| Data, config, infra | The change applied to the test environment (migration on a copy of realistic data, config loaded, deploy and rollback run) and the result checked from outside |
| Security | The abuse case attempted against the running deployment, not only argued from the code (see Red team below) |

Not live, so not proof on their own: unit tests, tests against fakes or in-memory stand-ins, a compile or build pass, a dev server on the author's own machine when a test environment exists, reading the code, another agent's opinion of the code.

## Mockups

A mockup, wireframe or static prototype is allowed to show a look and to agree it with the user. It must be labelled `MOCKUP` where it is shown and in its file name. It is never evidence that a feature exists, and a story shown only as a mockup is not done.

## Red team and security testing

Security and red-team work attacks the running deployment with real tools, in addition to agent review, so the evidence does not come only from another model. Pick tools by surface (examples, not a closed list):

| Surface | Tools |
|---|---|
| Web app and API | OWASP ZAP (baseline or full scan), scripted probes in the style of Burp or `curl` loops for auth, authorization, IDOR, injection and rate limits, a fuzzer for inputs and API schemas |
| TLS and HTTP headers | `testssl.sh`, a header scanner |
| Network exposure | `nmap` against the test host: only the intended ports answer |
| SSH and other protocols | `ssh-audit`, protocol-specific testers and fuzzers |
| Containers and images | An image scanner, a check that the container runs unprivileged |
| Desktop | Installer and update-channel tampering, file and registry permission checks, unsigned or modified package behaviour, a sandbox or privilege review of the running process |
| Mobile | Platform-appropriate static and dynamic analysis of the release build, traffic interception on the test device, storage and exported-component checks |
| Dependencies and secrets | Dependency audit and secret scan output |

Rules:

- **Throwaway environments only.** Attack tools run against the test environment from a separate disposable box or container, never on the owner's own machine and never against a production system or third-party service. Scan targets and tools are named in the evidence note.
- **Quiet.** Browsers, scanners and emulators run headless or on the test host, and do not take focus or inject input on a desktop someone is using.
- **Report what ran.** Tool, version, target, command, date, and the raw or trimmed output retained. A finding is rated by `severity.md`; "the scanner found nothing" is a result for that tool only, and says what it did not cover.
- **Agent review stays.** `security-engineer` review and threat-model reasoning decide what to attack and read the results. They do not replace the attack.

## No test environment

If the app has no test environment, creating one is the first story of the project (or of the adoption), ahead of feature work: a place the built artifact can be deployed, reset to a known state and reached by the tools above, recorded in `studio.yaml` `test_environment:`. Until it exists, every story with runtime behaviour keeps its live criterion unmet.

## Verdict words

- A story, gate or audit with no live evidence is **NOT ASSESSED** for that part. It is never PASS, never ADEQUATE, never CLEAR.
- A story stays **not done** (In Review) until its live-verification criterion has evidence on disk, or the user, who owns the decision, records in the story why live proof is impossible for that story (for example no test environment can exist for it yet) and what stands in for it. An agent cannot waive this.
- Evidence note line, added under the `Run result:` line: `Live result: LIVE - <environment, build or commit, what was exercised, evidence path> | NOT LIVE-VERIFIED - <why> | N/A - <why there is no runtime behaviour>`. "It is a small change" and "the unit tests pass" are not N/A reasons.
- The deployed build is the build that will ship (or the same commit built the same way). Evidence from a different build is labelled with the difference.

## Where it lives

`studio.yaml` `test_environment:` says how to reach the environment, deploy to it, reset it and run a browser against it (no credentials in the file, only the names of where they are kept). Live evidence is stored with the other evidence in `docs/qa/evidence/<story-or-change>/`, small files only.
