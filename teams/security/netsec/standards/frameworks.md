# Frameworks

The firm speaks in recognized frameworks so findings map to something the operator
can track over time, and so coverage is a map rather than a hunch. Confirm the
current edition of each in its official source before citing it; versions below
are what was current at authoring and may have moved.

## Offensive and technical

- **MITRE ATT&CK**: the tactic/technique map. Use it as a coverage checklist and
  to label what a finding would let an attacker do next.
- **OWASP Top 10** (web), **OWASP API Security Top 10**, **OWASP ASVS** (as the
  web/app control checklist, by level), **OWASP WSTG** (web testing method),
  **OWASP MASVS/MASTG** (mobile, if in scope).
- **NIST SP 800-115**: technical security testing and assessment method.
- **CWE**: name the weakness class for each finding.

## Defensive and detection

- **MITRE ATT&CK** again, as the detection coverage map: for each technique that
  matters here, is there telemetry, and would it alert.
- **NIST SP 800-92** (log management), **SP 800-61** (incident handling) for the
  IR and SOC practices.
- **The Pyramid of Pain** and detection-engineering practice for rule quality.

## Governance, risk, compliance

- **NIST Cybersecurity Framework (CSF) 2.0**: the six functions (Govern, Identify,
  Protect, Detect, Respond, Recover). The firm's default way to structure a
  posture assessment for this operator.
- **NIST SP 800-53** (control catalog) and **SP 800-171** (protecting controlled
  unclassified info) for control-level mapping when the operator wants depth.
- **CIS Controls v8** (the 18 controls and implementation groups) and **CIS
  Benchmarks** (per-platform hardening: Linux, Windows, Docker, Proxmox/KVM,
  network devices). The benchmark specialist scores against these.
- **ISO/IEC 27001/27002** as a cross-reference when the operator thinks in those
  terms.

## How to use them

- A home or small environment is not held to an enterprise control set as pass/
  fail. Map findings to a framework so they are trackable, and rate them by real
  risk to this operator, not by raw control deviation.
- When you cite a control or a Top 10 item, name the exact identifier (for example
  `CIS 4.1`, `ATT&CK T1190`, `CWE-89`, `CSF PR.AC`), so the operator can look it
  up and so findings dedupe cleanly across agents.
