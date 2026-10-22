# This package's own debt registers

Three files, and one rule they share: **a count may fall and may never rise.** They record what does
not yet meet a governance standard, so that the gap is measured rather than discovered, and so that a
release cannot quietly add to it. `03-tooling/structure_debt_check_v1_1_0.py` enforces them in PIB's
blocking release gate, with the governance session's own checkers vendored under
`14-vendored-oe-tooling/`.

Since v3.1.0 that gate runs a **third** check with no register of its own: kind **consistency**, a
class's kind against its named parents'. It has nothing to record because it finds nothing — 11
subclass links between two typed classes, no contradiction — which is what makes PIB's earlier claim
that child and parent agree by construction a measurement rather than an argument. It could not run
here until the governance session added `--abox FILE` in answer to PIB's report, since it refuses
without the taxonomy of kinds.

| File | What it holds | State at PIB v3.3.0 |
|---|---|---|
| `STRUCTURE_DEBT_REGISTER_v3_0_0.tsv` | files that break a structure rule | **empty — the checker reports CLEAN** (18 at v2.19.0, 14 at v2.20.0, 9 at v2.21.0, 1 at v3.0.0) |
| `KIND_COVERAGE_BASELINE_v1_1_0.tsv` | this package's classes and object properties carrying no kind or category | **empty** (was 49) |
| `KIND_COVERAGE_DECISIONS_v1_0_0.tsv` | terms this package does not type, each with its reason | 2 — a vendored RADAR contribution, its own session's to type. Since v2.21.0 those files sit under a `vendored/` folder, which the checker does not read at all, so the two entries hold nothing the scan would otherwise raise; they are kept as the record of **why** PIB does not type another package's terms, which is the question a future session will ask. |

## Why the comments live here and not in the registers

The kind registers are read by a parser that **drops exactly the first line and treats every other
line as data**. A comment block inside them would be parsed as rows: the column header became a row
when it was tried, and the checker duly reported a term called `iri` as cleared. So those two files
carry the column header on line 1 and nothing else but data, and their explanation is here. The
structure register's checker does skip `#` comments, and that file keeps its own history in its header.

## How the last line closed, and why it took three exchanges

The package ships one T-Box, one A-Box and one SHACL file. The last line said there were **two** A-role
files, the second being the registration submission — a **unit of its own** by the governance owner's
ruling of 2026-10-07. Folding it into the domain A-Box would have satisfied the count by breaking that
ruling, so PIB did not: it asked for a row in the governance units table instead, which is that
session's file to edit.

The row came back carrying the wording PIB had asked for, `unit=PIB/08-registration`, and matched
nothing: PIB's gate resolves every path under the staged slug. PIB measured which form works rather
than guessing — `PIB/08-registration` → X1, `08-registration` → X1, `pib-hub/08-registration` → clean —
and that session corrected the one token. The unit now carries its own `VERSION.txt`, and PIB carries
its own copy of the two governance tables in `04-documentation/`, which is where their reader looks for
a package that holds one. **Zero violations.**

The register file stays, empty. It is the ratchet's floor, and an absent register is indistinguishable
from one nobody wrote.

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
