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
| `oe_kind_consistency_v1_1_0.py` | `06c09a2690bfcf58…` | a class's kind agrees with its named parents' |
| `vendored/oegov_abox_v1_37_0.ttl` | `53f3c2d1025afcdf…` | the governance A-Box, read by the consistency check for the taxonomy of kinds |

The first three files were vendored from the governance tree at commit
`645c7906f8c7e949a6b4e6ac512c524ec57ba4a7` (2026-10-22, discipline v2.34.0); the consistency check and
the A-Box copy at commit `54a4ea4d` the same day (discipline v2.36.0).

## The consistency check, and why it is here now

At v2.19.0 this file said `oe_kind_consistency` was **deliberately not vendored**: it read the kind
taxonomy from the governance A-Box, refused to run without one, and a tool that cannot run is not a
gate. PIB reported that, and the governance session added `--abox FILE` on 2026-10-22.

So it is vendored here now, with a verbatim, hash-pinned copy of the governance A-Box beside it under
`vendored/` — a folder name no scanning tool reads, which is accurate: it is another package's file,
not PIB's. The check runs from this package alone and is in the blocking gate.

What it found is nothing, and that is the point: **11 subclass links between two classes that both
carry a kind, no contradiction**. PIB's claim at v2.20.0 that child and parent carry the same kind by
construction is from v3.1.0 measured rather than argued. It is proven able to fail on PIB's own files:
`CompleteCandidate` given the kind Process under an InformationArtifact parent is reported as the
contradiction it is.

**The A-Box copy is a snapshot and will age.** It is pinned by hash, so a change upstream is visible
rather than silent; what it is read for — the `skos:broader` tree of the kinds — moves slowly, and PIB
re-vendors when the governance session re-issues it.

## How the checkers are driven

`03-tooling/structure_debt_check_v1_0_0.py` runs both with PIB's own registers and passes
`--as-package pib-hub`. That flag is not optional: pointed at a repository root without it, the
checker resolves every top-level folder as its own package and reports 23 violations across 9
"packages" instead of 18 across one. The wrapper passes it so the measurement cannot be taken the
wrong way by accident.
