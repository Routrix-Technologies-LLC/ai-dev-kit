# FINDING-VERIFIED

**Trigger:** before any finding rated MEDIUM or above enters the report; run by a
lead or a reviewer who did not produce the finding.

**Owner:** the relevant practice lead (or report-writer as a backstop).

**Inputs:** the finding in `finding.md` format, with its evidence.

**Checks (adversarial: try to disprove it):**

1. **Real?** Re-read or re-run the evidence. Does the claimed cause actually
   produce the claimed effect on this target, this version?
2. **Reachable?** Is the exposure proven for the stated audience (internet / LAN /
   local), or inferred from config? Re-run the exposure check.
3. **Rated right?** Does the severity match impact-and-reachability per
   `standards/severity.md`, not a textbook CVSS score?
4. **Not a duplicate?** Is it the same root cause as another finding?

**Verdicts:** `CONFIRMED`, `PLAUSIBLE`, `REFUTED`.

- `CONFIRMED`: reproduced, exposure proven, rating fits. It enters the report as
  stated.
- `PLAUSIBLE`: likely real but exposure or reproduction could not be fully proven.
  It enters the report labelled `UNVERIFIED` with what would confirm it, and is
  never rated CRITICAL.
- `REFUTED`: could not be reproduced, or exposure is proven absent. It does not
  enter the report as a finding; note it as checked-and-cleared if useful.
