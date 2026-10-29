# Severity and priority

Three scales, kept apart on purpose. Use the words exactly.

- **Severity** is how bad the defect is: its impact if it happens. It is a fact about the defect.
- **Priority** is how soon it is fixed: a scheduling decision that weighs severity, how many users hit it, workarounds, risk of the fix and the release calendar.
- **Finding severity** (CRITICAL to LOW) rates security issues and review findings.

A high-severity bug may be low priority (a crash in a feature nobody can reach yet), and a low-severity bug may be high priority (a typo in the store listing the day before launch). Never raise severity to get something scheduled; change the priority and say why.

## Bug severity

| Level | Definition | Examples by platform |
|---|---|---|
| **S1 Critical** | Data loss or corruption, security breach, the app or service unusable for most users, or a failure that blocks release of a core promise. No acceptable workaround | Web: checkout or login fails for all users; one user sees another's data. Windows, macOS, Linux: the app crashes on launch; saved documents are overwritten or lost; an update leaves the app unstartable. iOS, Android: crash on launch after the new OS version; purchases are charged but not delivered; the local database is wiped on upgrade. Backend: writes are silently dropped; a migration corrupts rows; an auth bypass. CLI: the command deletes or truncates the wrong files |
| **S2 High** | A major feature is broken or unusable for many users, or a significant degradation; a workaround exists but is hard or unreasonable | Web: search returns nothing in one browser; the form cannot be submitted on mobile width. Desktop: the tray icon never appears; file association opens the wrong app; sync stalls until restart. Mobile: push notifications do not arrive on one OS version; rotation loses typed input; the app is unusable with a screen reader on the main flow. Backend: p95 latency five times the budget; one endpoint returns 500 for valid input. CLI: a documented flag is ignored |
| **S3 Medium** | A feature misbehaves in a limited case or for few users; an easy workaround exists; no data at risk | Web: a filter resets on refresh; the layout breaks between two breakpoints. Desktop: the window forgets its position; a dialog is mispositioned on a second monitor at high DPI. Mobile: a list jumps on refresh; a screen is slightly clipped on small phones. Backend: a log line lacks a correlation ID; pagination is off by one at an edge. CLI: an error message is unhelpful |
| **S4 Low** | Cosmetic or minor; no functional impact | A typo; a misaligned icon by a few pixels; an inconsistent capitalization; a tooltip missing; a rarely seen console warning |

When unsure between two levels, take the higher and note the doubt; `qa-lead` resolves it. Any bug that loses user data is at least S2, and S1 if it is not recoverable.

## Priority

| Level | Meaning | Typical rule |
|---|---|---|
| **P0** | Fix now, drop other work | Active data loss or security exposure; production down; blocks a release or hotfix |
| **P1** | Fix before the next release | Blocks the current milestone; S1 and S2 default here |
| **P2** | Schedule normally | Fix in a coming batch; S3 defaults here |
| **P3** | When convenient, or never | Backlog; S4 defaults here; may be closed as won't fix with a reason |

`qa-lead` triages severity; `product-manager` sets priority with the user; `program-director` resolves schedule conflicts. Record both on the bug report (`bug-report.md`).

## Usability and accessibility findings

Usability and accessibility findings are rated on the bug scale (S1 to S4) when they are filed as defects, so agents do not invent a mapping. Rate by the effect on a user trying to complete a main flow, in the worst realistic case (screen reader, keyboard only, text scaled to 200 percent, small screen).

| Level | Usability or accessibility meaning |
|---|---|
| **S1** | A user cannot complete a core flow at all and has no workaround (for example, sign-in is impossible with a screen reader), or the defect blocks a legal or store requirement for release (a required accessibility, consent or disclosure obligation) |
| **S2** | A main flow is unusable or only completable with great difficulty by a group of users: not operable by keyboard, not announced by a screen reader, fails WCAG 2.2 AA on a main flow, unreadable at the supported text sizes. A main flow unusable with a screen reader or keyboard is S2 unless it also meets the S1 test |
| **S3** | A secondary flow is affected, a workaround is easy, or an AA failure sits off the main flow (a missing label on a rarely used control, a focus order oddity) |
| **S4** | Polish: best-practice gaps, wording, spacing that does not hinder use |

The assessing agent proposes the level and labels it "proposed"; `qa-lead` confirms S1 and S2. A usability study's task-failure counts (`usability-test-plan.md`) and an accessibility audit's Blocker, Major and Minor classes (`accessibility-audit.md`) are evidence for the level, not substitutes for it; the audit report shows both the class and the severity word.

## Security and review findings

Used by `security-engineer`, `code-reviewer`, audits and gate reviews.

| Level | Definition | Default response |
|---|---|---|
| **CRITICAL** | Exploitable now with serious impact: remote code execution, authentication or authorization bypass, exposure or loss of user data, exposed secrets in production, destructive data bug on a common path | Stop-ship. Fix before release; hotfix if released. `security-lead` decides risk acceptance with the user |
| **HIGH** | A real defect with significant impact or a likely path to one: injection needing a precondition, missing authorization on a sensitive action, weak or missing crypto on sensitive data, broken update verification, a crash or data-loss bug on an uncommon path | Fix before release. Accepting it needs a written reason |
| **MEDIUM** | Weakens defenses or has limited impact: missing hardening, verbose errors, an overly broad permission, a correctness bug with a workaround, notable maintainability risk | Fix in the current or next batch; track in the tech debt or risk register |
| **LOW** | Minor or theoretical: style, naming, small clarity issues, defense-in-depth ideas | Fix opportunistically. Style findings are labelled as style |

Every finding names a file and line (or a specific place), a concrete failure scenario, and the smallest fix. A finding that could not be verified is labelled `UNVERIFIED` and never rated CRITICAL. Rate by what you proved, not by what could be imagined; "might be insecure" is not a finding.

The scales map loosely: S1 corresponds to CRITICAL, S2 to HIGH, S3 to MEDIUM, S4 to LOW, but a review finding is about code or design and a bug is about observed behavior. Use each in its own place and do not translate one into the other in a report.

## Deviation levels

Used when comparing a change with its spec, ADR, design or standard.

| Level | Meaning | Effect |
|---|---|---|
| **BLOCKING** | Contradicts a requirement, an accepted ADR, a security or data-safety rule, or an acceptance criterion | The work is not done; fix or get a recorded exception from the owner |
| **ADVISORY** | Departs from a preference, convention or non-critical guidance; the result still works and is safe | Note it, fix if cheap, track otherwise |
| **OUT OF SCOPE** | Noticed but not part of this change or its brief | Report as a follow-up with a suggested owner; do not fix in this change |

## Who may set S1 or CRITICAL

- **S1** is set by `qa-lead` (or by the user). Any agent may propose S1 with evidence, but must label it "proposed S1" until `qa-lead` confirms.
- **CRITICAL** is set by `security-engineer` for security findings and by `code-reviewer` or `principal-engineer` for correctness and data-loss findings, always with a reproduced or traced failure scenario. A CRITICAL finding is escalated to `security-lead` (security) or `technical-director` (other) in the same report.
- Accepting or downgrading an S1 or CRITICAL is never done by the agent who wrote the code. Risk acceptance and stop-ship belong to `security-lead` and, for release, `release-manager`, with the user's final word.
