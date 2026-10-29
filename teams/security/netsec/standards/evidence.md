# Evidence

A finding without evidence is a rumour. The firm's credibility is that every claim
can be reproduced by the operator. Hold this bar on everything that reaches the
report.

## What counts as evidence

- The exact target (hostname, IP, URL, port), resolved and confirmed in scope.
- The command or request you ran, verbatim, and its output (redacted of secrets).
- The date and the source for any version, CVE, or framework claim.
- A measurement where the finding is quantitative (timing, count, size).
- For a config finding: the file path and the exact lines, read from the live
  system or the infra record, not remembered.

## The exposure check, always

Before "exposed", "public", or "at risk", prove it:

- Public DNS: `nslookup <name> 1.1.1.1` (does it resolve publicly, and to what).
- Bind address: `127.0.0.1`/private vs `0.0.0.0`/`::`; confirm what is listening
  with `ss -ltnp`, `netstat -ano`, or `lsof -iTCP -sTCP:LISTEN` and match the
  process.
- Firewall, port-forward, and tunnel or reverse-proxy scope: which names and paths
  are actually published.
- Whether the service is in use at all.

State the audience (internet / LAN / local). If you cannot check, write `exposure
unverified` and rate on what you proved.

## Redaction

- Never record a secret's value. Report its location and kind.
- Keep the WAN public IP out of every artifact.
- When a tool can redact (for example gitleaks `--redact`), turn it on so values
  never reach your output or the report.

## Honesty about coverage

- A category you did not assess is "not assessed", never "clean".
- A tool that found nothing is a result only if you confirmed the technique
  applies to this target and version. Say which tool, which version, what date.
- Report what you could not reach and why, next to what you did.
- Never report a scan, check, or exploit as done or passing that you did not run
  and see.
