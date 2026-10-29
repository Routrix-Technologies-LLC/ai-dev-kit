---
name: sec-audit
description: "Configuration-level audit of in-scope hosts, containers, network devices, and cloud: firewall and VLAN segmentation, Proxmox/Docker and host hardening, cloud/edge config, scored against CIS benchmarks. Read-only. Use for 'audit this box', 'is this configured securely', 'check my segmentation', 'is it listening on what it should', 'harden this host'."
argument-hint: "[host / device / cloud scope]"
user-invocable: true
---

# Infrastructure configuration audit

Driven by `infrastructure-lead`. Read-only on devices and hosts; a config change is
a separate, confirmed action for `hardening-engineer`.

## Steps

1. `ED-SCOPE` CLEAR for the target. Pull the live config from the record
   (`infra_source`) and, read-only, from the host or device where allowed.
2. Run the specialists that fit:
   - Firewall / switch / VLAN isolation: `firewall-segmentation-auditor`
     (+ `network-pentester` to prove reachability from the segment).
   - Hypervisor / container / escape surface: `container-host-auditor`.
   - OS hardening on a host: `endpoint-hardening-analyst`.
   - Cloud / edge config the operator owns: `cloud-posture-analyst`.
3. Score against the relevant CIS Benchmark with `cis-benchmark-specialist`.
4. Confirm each listener's real exposure (bind address, firewall) before rating.
   Prove segmentation from both the rules and the wire. Verify MEDIUM+ findings.

## Output

Ranked, benchmark-mapped findings with the exact config lines and remediation,
plus a short "is it listening on what it should" verdict per host.
