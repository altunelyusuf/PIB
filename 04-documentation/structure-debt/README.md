# This package's own debt registers

Three files, and one rule they share: **a count may fall and may never rise.** They record what does
not yet meet a governance standard, so that the gap is measured rather than discovered, and so that a
release cannot quietly add to it. `03-tooling/structure_debt_check_v1_0_0.py` enforces them in PIB's
blocking release gate, with the governance session's own checkers vendored under
`14-vendored-oe-tooling/`.

| File | What it holds | State at PIB v3.0.0 |
|---|---|---|
| `STRUCTURE_DEBT_REGISTER_v2_0_0.tsv` | files that break a structure rule | **1 line** (18 at v2.19.0, 14 at v2.20.0, 9 at v2.21.0) |
| `KIND_COVERAGE_BASELINE_v1_1_0.tsv` | this package's classes and object properties carrying no kind or category | **empty** (was 49) |
| `KIND_COVERAGE_DECISIONS_v1_0_0.tsv` | terms this package does not type, each with its reason | 2 — a vendored RADAR contribution, its own session's to type. Since v2.21.0 those files sit under a `vendored/` folder, which the checker does not read at all, so the two entries hold nothing the scan would otherwise raise; they are kept as the record of **why** PIB does not type another package's terms, which is the question a future session will ask. |

## Why the comments live here and not in the registers

The kind registers are read by a parser that **drops exactly the first line and treats every other
line as data**. A comment block inside them would be parsed as rows: the column header became a row
when it was tried, and the checker duly reported a term called `iri` as cleared. So those two files
carry the column header on line 1 and nothing else but data, and their explanation is here. The
structure register's checker does skip `#` comments, and that file keeps its own history in its header.

## The one line left, and why PIB cannot close it

The package now ships one T-Box, one A-Box and one SHACL file. The remaining line says there are
**two** A-role files, and the second is the registration submission — which the governance owner ruled
on 2026-10-07 is a **unit of its own**, obeying the three-file rule separately. Merging it into the
domain A-Box would break that ruling in order to satisfy a count; naming it as a unit needs a row in
the governance session's units table, which is that session's file to edit. Asked for, with its
reason, in `../../09-handover-inbox/accepted/HANDOVER_PIB_to_OE_archive-report-and-two-asks_v1_0_0.md`
section 2. Until the row exists this line stays, and lowering it would be the wrong kind of green.

## What may be done here without asking anyone

Remove a line whose files are fixed, and lower a count that really fell. Both are debt shrinking.

## What may not

Raise a count, add a line the governance aggregate does not carry, or mark a line as an exception. The
checker fails the run and the aggregate generator refuses the change, keeping the previous ceiling.
Those need the owner's ruling, recorded in the aggregate line.

## The one thing these registers could not measure — now settled

The retired `Ontologies/pib-hub/` directory, PIB's own frozen lineage in the monorepo, generated 9
structure-debt and 27 kind-coverage lines in the **governance** registers that no session could clear.
The owner authorized the fix on 2026-10-22: that directory's retired content is now held as its
archive (one T-Box, one A-Box, one SHACL file, every former subject a module at its own IRI) and its
three spoke contributions sit under `vendored/`, both being folder classes the checkers do not read.

Measured with the governance session's own checkers afterwards: the **27 kind-coverage lines are
CLEARED** and that run passes. The 9 structure lines are reported **NOT MEASURED** rather than cleared
— a package with no active Turtle file drops out of the scan, so the checker cannot see that the files
are gone. They name files that no longer exist and are the governance session's to remove.
