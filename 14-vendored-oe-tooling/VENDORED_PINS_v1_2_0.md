# Vendored governance checkers — pinned, read-only (NOT PIB-owned)

**Verbatim, SHA-256-pinned, read-only copies** of the governance session's structure and kind
checkers, vendored so PIB's ratchet runs **from this package alone**. Same arrangement as the
algebra's rules under `11-vendored-operator-rules/`, and for the same reason: PIB's release must not
depend on another tree being checked out beside it.

**Ownership.** They remain the governance session's. PIB does not maintain or evolve them and must
not edit them in place. When that session re-issues them, PIB re-vendors the new hashes and bumps.

| File | SHA-256 | Role |
|---|---|---|
| `oe_structure_check_v1_9_0.py` | `7dda3eb7e8c48dd7…` | names, mixed roles, versions side by side, one file per role |
| `oe_structure_classes_v1_3_0.py` | `8cd0d299ba24dcb6…` | the class table the structure checker reads; it refuses to run without it |
| `oe_kind_coverage_v1_2_0.py` | `5b1f092182edbda8…` | every named class carries a kind, every object property a category |
| `oe_kind_consistency_v1_1_0.py` | `06c09a2690bfcf58…` | a class's kind agrees with its named parents' |
| `vendored/oegov_abox_v1_38_0.ttl` | `ab91c660f8a18a34…` | the governance A-Box, read by the consistency check for the taxonomy of kinds |

**Sources, as last re-vendored (2026-10-24, discipline v2.37.0), each verified byte-equal to the governance tree.**
Structure checker v1_9_0: `oe-method/03-tooling/`, commit `3c8cd36f`. Kind coverage v1_2_0:
`repo-tooling/`, commit `ff398ec3`. A-Box v1_38_0: `oe-method/09-governance/`, commit `13252de8`. The class
table (v1_3_0, commit `da2ebf8a`) and the consistency check (v1_1_0, commit `ff398ec3`) are unchanged and
were re-confirmed byte-equal. Earlier pins (v1_7_1, v1_1_0, v1_37_0) are in git history under the release tags.

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


## The two governance tables, carried in `04-documentation/`

`OE_STRUCTURE_CLASSES_v1_7_0.tsv` (the folder and file classes) and `OE_STRUCTURE_UNITS_v1_4_0.tsv`
(the named units, including PIB's registration unit) are **copies of the governance session's files**,
read-only here and never edited. They do not sit in this folder because their reader looks for them in
`<root>/04-documentation` for "a package that carries its own copy", which is exactly what PIB is: a
package published from its own repository, where the governance tree is not beside it.

Without the units table PIB's own gate cannot see the row that names its registration unit, and the
unit's version file would be reported as a folder whose class is unknown — worse than the line it
closes. With both tables, PIB measures **zero structure violations**.

They are `.tsv`, so no scanning tool reads them as ontology content. PIB re-copies them when that
session re-issues them; a change there that PIB has not copied shows up as a measurement that differs
from the governance tree's, which is the visible failure rather than a silent one.
