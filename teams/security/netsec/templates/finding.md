<!-- One finding. IDs are PREFIX-NNN, numbered per engagement, never reused.
     Prefix by practice: REC (recon), WEB, API, NET, AUTH, VULN, SEC (secrets),
     INFRA, HOST, CLOUD, DET (detection), GRC. -->

### <ID>: <short title>

- **Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO  (or UNVERIFIED)
- **Audience:** internet | LAN | local
- **Framework:** <e.g. ATT&CK T1190, OWASP A01, CWE-89, CIS 4.1, CSF PR.AC>
- **Target:** <hostname / IP / URL / port, resolved and confirmed in scope>
- **Effort to fix:** S | M | L

**What it is.** One or two sentences: the weakness, plainly.

**Attack or failure scenario.** Who the attacker is, what they need to start, the
steps, and what they get. For a misconfiguration, what goes wrong and when.

**Evidence and exposure check.** The command or request and its output (secrets
redacted), the file and lines for a config finding, and exactly what you verified
about exposure (public DNS, bind address, firewall/tunnel scope). State what you
could not verify.

**Remediation.** The specific change, and how to verify the fix is effective
(the retest). Name the fix that kills the whole class if this is one of several.

**Detection note (purple).** Would this attack have been logged? Would it alert?
If unknown, say so and flag for the defensive practice.
