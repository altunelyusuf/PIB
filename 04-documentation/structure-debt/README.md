# This package's own debt registers

Three files, and one rule they share: **a count may fall and may never rise.** They record what does
not yet meet a governance standard, so that the gap is measured rather than discovered, and so that a
release cannot quietly add to it. `03-tooling/structure_debt_check_v1_0_0.py` enforces them in PIB's
blocking release gate, with the governance session's own checkers vendored under
`14-vendored-oe-tooling/`.

| File | What it holds | State at PIB v2.20.0 |
|---|---|---|
| `STRUCTURE_DEBT_REGISTER_v1_1_0.tsv` | files that break a structure rule: names, mixed roles, versions side by side, more than one file per role | **14 lines** (was 18) |
| `KIND_COVERAGE_BASELINE_v1_1_0.tsv` | this package's classes and object properties carrying no kind or category | **empty** (was 49) |
| `KIND_COVERAGE_DECISIONS_v1_0_0.tsv` | terms this package does not type, each with its reason | 2 — a vendored RADAR contribution, its own session's to type |

## Why the comments live here and not in the registers

The kind registers are read by a parser that **drops exactly the first line and treats every other
line as data**. A comment block inside them would be parsed as rows: the column header became a row
when it was tried, and the checker duly reported a term called `iri` as cleared. So those two files
carry the column header on line 1 and nothing else but data, and their explanation is here. The
structure register's checker does skip `#` comments, and that file keeps its own history in its header.

## What may be done here without asking anyone

Remove a line whose files are fixed, and lower a count that really fell. Both are debt shrinking.

## What may not

Raise a count, add a line the governance aggregate does not carry, or mark a line as an exception. The
checker fails the run and the aggregate generator refuses the change, keeping the previous ceiling.
Those need the owner's ruling, recorded in the aggregate line.

## One thing these registers cannot measure

The retired `Ontologies/pib-hub/` directory — PIB's own frozen lineage in the monorepo — generates 9
structure-debt and 27 kind-coverage lines in the **governance** registers. PIB may not edit a tree its
own retirement note freezes, and no other session owns it, so that debt can only sit there. The ruling
is asked for in `09-handover-inbox/accepted/RETURN_PIB_to_OE_six-items-dispositioned_v1_0_0.md`,
section 7, and nothing here can close it.
