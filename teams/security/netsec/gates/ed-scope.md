# ED-SCOPE

**Trigger:** the start of every engagement, before any recon, scan, or probe
runs; and again whenever a new target is proposed mid-engagement.

**Owner:** engagement-director.

**Inputs:** `scope.yaml`; the operator's stated goal; the `infra_source` record.

**Checks:**

1. `scope.yaml` exists and is readable at the engagement's path.
2. It carries an `engagement.authorization` statement and an `owner`, and the
   owner is the operator running the engagement.
3. Every entry under `in_scope` is a concrete, resolvable asset (a domain, URL,
   address, or CIDR), not a placeholder.
4. `default_intensity` is one of the three allowed values, and any per-target
   override is within the forbidden-list limits.
5. The requested work resolves entirely to `in_scope` assets, with nothing in
   `out_of_scope` and nothing unresolvable.
6. For any internet-facing target, ownership is confirmable (the operator owns the
   domain / public hostname).

**Verdicts:** `CLEAR`, `BLOCK`, `NOT ASSESSED`.

- `CLEAR`: scope is present, authorized, concrete, and the requested work fits
  inside it. Work may proceed at the stated intensity.
- `BLOCK`: scope is missing, unauthorized, placeholder, or the requested work
  would touch something out of scope or unresolvable. Nothing active runs. Say
  exactly what must be added or fixed.
- `NOT ASSESSED`: `scope.yaml` could not be read at all (distinct from a scope
  that is present but invalid, which is `BLOCK`).

A `BLOCK` here is absolute: no other agent runs an active step until it is
resolved by the operator editing `scope.yaml`.
