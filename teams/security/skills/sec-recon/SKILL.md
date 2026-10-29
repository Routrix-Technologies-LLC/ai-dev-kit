---
name: sec-recon
description: "Reconnaissance pass over in-scope assets: discovery, port and service and version mapping, the internet-vs-LAN exposure line, DNS and email posture, and TLS. Produces the shared attack-surface map. Use for 'what's exposed', 'what's listening', 'map my attack surface', or before deeper testing."
argument-hint: "[asset or scope]"
user-invocable: true
---

# Reconnaissance pass

Driven by `offensive-lead` with the recon specialists. Non-destructive. The map it
produces feeds every other practice.

## Steps

1. Confirm `ED-SCOPE` is CLEAR for the assets in question (`/sec-engage` if not).
2. Launch in parallel against in-scope assets:
   - `attack-surface-analyst`: discovery, ports, services, versions, and the hard
     internet / LAN / local exposure line (proven, not inferred).
   - `dns-email-security-analyst`: DNS hygiene, SPF/DKIM/DMARC, subdomain takeover.
   - `tls-crypto-analyst`: TLS and certificate posture, every hop.
   - `osint-analyst`: public footprint and leaked-credential presence (passive).
3. Consolidate into one shared map in `~/AgentScratch/<engagement>/` and summarize:
   what resolves where, what is listening, which audience can reach it, notable
   endpoints, and any surprises (a stale public record, a service bound wide).

## Output

The shared attack-surface map plus any recon-level findings (unexpected exposure,
stale records, weak TLS), ready for the offensive and infrastructure practices.
