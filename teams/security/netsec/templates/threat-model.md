# Threat model: <asset or environment>

A lightweight model to focus the assessment on what actually matters here.

## Scope and assets

- What is modeled (one asset, or the whole environment).
- What is worth protecting (the data, the services, the uptime, the reputation),
  ranked. What would actually hurt if lost or exposed.

## Actors

Who might attack, and what they start with: anonymous internet user, a malicious
authenticated user, a compromised internal device or IoT thing, a malicious
dependency or container image, someone on the LAN (guest Wi-Fi, a visitor),
someone with physical access.

## Data-flow and trust boundaries

Processes, stores, external entities, and the flows between them. Mark every trust
boundary: internet to edge, edge to LAN, VLAN to VLAN, host to container, user to
admin, your config to a third party (Cloudflare, cloud, upstream DNS). Each arrow
crossing a boundary is a candidate threat site.

## Threats (STRIDE at each boundary)

| # | Element / boundary | STRIDE | Threat | Likelihood | Impact | Rating | Mitigation / finding |
|---|---|---|---|---|---|---|---|
| | | S/T/R/I/D/E | | | | | |

## Decisions

For each threat: mitigate (preferred), eliminate (remove the feature or exposure),
transfer (a vetted service), or accept (the operator's call, recorded with the
reason). A mitigation with no verification is a wish: link it to a finding and a
retest.
