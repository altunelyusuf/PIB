# Vendored governance checkers — pinned, read-only (NOT PIB-owned)

**Verbatim, SHA-256-pinned, read-only copies** of the governance session's structure and kind
checkers, vendored so PIB's ratchet runs **from this package alone**. Same arrangement as the
algebra's rules under `11-vendored-operator-rules/`, and for the same reason: PIB's release must not
depend on another tree being checked out beside it.

**Ownership.** They remain the governance session's. PIB does not maintain or evolve them and must
not edit them in place. When that session re-issues them, PIB re-vendors the new hashes and bumps.

| File | SHA-256 | Role |
|---|---|---|
| `oe_structure_check_v1_7_1.py` | `b3a8cda70d8660d6…` | names, mixed roles, versions side by side, one file per role |
| `oe_structure_classes_v1_3_0.py` | `8cd0d299ba24dcb6…` | the class table the structure checker reads; it refuses to run without it |
| `oe_kind_coverage_v1_1_0.py` | `b2bb2498a90bcb80…` | every named class carries a kind, every object property a category |

Vendored from the governance tree at commit `645c7906f8c7e949a6b4e6ac512c524ec57ba4a7` (2026-10-22),
discipline v2.34.0.

## What is deliberately not vendored yet

`oe_kind_consistency_v1_0_0.py` — a class's kind must agree with its named parents'. It reads the kind
taxonomy from the governance A-Box (`oe-method/09-governance/oegov_abox_v*.ttl`) and refuses to run
without it, so from inside PIB it reports `REFUSED: no knowledge-base A-Box found`. A tool that cannot
run is not a gate, so it is not shipped here. It is vendored in the release that gives PIB's terms
their kinds, together with whatever the checker needs to resolve them — which is when its answer first
means anything, since a class with no kind is not measured by it.

## How the checkers are driven

`03-tooling/structure_debt_check_v1_0_0.py` runs both with PIB's own registers and passes
`--as-package pib-hub`. That flag is not optional: pointed at a repository root without it, the
checker resolves every top-level folder as its own package and reports 23 violations across 9
"packages" instead of 18 across one. The wrapper passes it so the measurement cannot be taken the
wrong way by accident.
