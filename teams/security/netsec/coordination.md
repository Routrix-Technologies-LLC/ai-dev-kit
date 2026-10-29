# Coordination

How work flows through the firm without agents tripping over each other or over
the operator's running services.

## Fan-out

- The engagement-director (or a lead) spawns specialists with written briefs. A
  brief names: the exact in-scope target, the intensity ceiling, the method, the
  gate if any, and the deliverable (which template, where to write it).
- **Parallel** when the work is independent and does not contend for the same host
  or the same scanner. **Serial** when two agents would scan or probe the same
  target at once, or when one's output is another's input (recon feeds everyone).
- Recon runs first and its map is shared: every other specialist reads the recon
  output instead of re-scanning.

## Resource discipline

- One heavy scanner per host at a time. Route heavy or long scans through
  `run_locked.sh cpu`. Nothing that opens a window or uses the GPU without
  `run_locked.sh gpu` and a brief that allows it.
- Scans and captures go to `~/AgentScratch/<engagement>/`, named by agent and
  target, so the director can collate without re-running anything.
- Respect quiet hours in `scope.yaml`. Stop heavy work on `run_locked.sh` exit 75.

## Findings flow back

- Each specialist returns findings in `finding.md` format with unique IDs
  (practice prefix, numbered, never reused) plus a coverage note.
- The lead verifies (`FINDING-VERIFIED`) before forwarding. Unverified items are
  labelled, not dropped silently.
- The director collates, dedupes across practices (same root cause = one finding,
  cross-referenced), and hands the set to `report-writer`.

## Purple loop

- The offensive side tells the defensive side which techniques it exercised (by
  ATT&CK ID) and when. The defensive side checks whether each was logged and would
  alert, and files detection gaps as findings.
- Confirmed remediations route to `hardening-engineer`, who implements only on the
  operator's go-ahead and never as a side effect of testing.

## Conflicts

- Two agents disagree on a rating: the owning lead decides; cross-practice
  disagreements go to the director; the severity scale (`standards/severity.md`)
  is the tie-breaker, read literally.
- An agent wants to exceed the intensity ceiling or touch something out of scope:
  it does not; it surfaces the request to the director for the operator.
