# Rules of engagement

These are the firm's standing limits. `scope.yaml` can tighten them per
engagement; it cannot loosen the forbidden list.

## Always forbidden, at every intensity

- **Denial of service.** No stress, flood, amplification, or resource-exhaustion
  testing. No deliberately crashing a service to prove it can crash.
- **Destruction or modification.** No deleting, corrupting, encrypting, or
  changing data or configuration. Auditors read; they do not write. A config
  change the operator asked for is a separate, confirmed action, done by the
  hardening practice, not a side effect of testing.
- **Real-data exfiltration.** Never copy real user data off a host to prove access.
  Prove access with a benign marker (a record count, a non-sensitive field, a file
  listing), not by taking the data.
- **Off-property testing.** Nothing outside `in_scope`. No pivoting onto a
  third-party service, an upstream provider, the ISP, or another person's device,
  even if a path exists.
- **Secret disclosure.** No recording a secret's value anywhere. No posting the WAN
  public IP.

## By intensity

- **passive**: observe only. Public records, certificates, version banners, infra
  docs, config review. No probing beyond a normal client request.
- **active-nondestructive** (default): scanning, safe probes, version and header
  checks, auth-surface mapping, segmentation reachability tests, benchmark review.
  Must change no state.
- **exploit-opt-in**: proof-of-concept against `exploit_safe` targets only, only to
  the point of confirming the weakness.

## Needs explicit go-ahead (ask first)

- Credential brute-force or password spraying (lockout risk).
- Anything that could trip an account lockout, rate limit, or alerting that pages
  the operator, unless the engagement is also testing that alerting on purpose.
- Any config or device change, even a reversible one.
- Testing during a window `scope.yaml` marks as quiet hours.

## Stop and escalate

- A sign of real compromise that is not the team's testing.
- Any instability or outage caused by testing: stop, help restore, report.
- The operator needs the machine back: pause heavy or GPU work.
- Scope ambiguity that would require touching something not clearly in scope.
