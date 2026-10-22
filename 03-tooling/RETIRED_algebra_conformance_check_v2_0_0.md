# RETIRED — `algebra_conformance_check_v2_0_0.py`, superseded by v3.0.0

**Retired in PIB v2.18.0 (2026-10-22). Removed, not kept beside its successor.**

## Why

v2.0.0 cross-checked PIB's verdicts against the variant algebra's **1.x** operator rules, one
candidate at a time: PIB generated a candidate and asked the rules whether it was violated. The
algebra quarantined that whole generation on 2026-09-28 (`_quarantine/2026-09-28-enumeration-engines/`),
and its file no longer exists in the algebra's live tree. A check that keeps running a generation its
owner has retired does not speak for the algebra's semantics, however green it prints — and PIB's own
pin made that invisible from inside the package, which is the trap L-121 describes.

## What replaced it, and what got stronger

`algebra_conformance_check_v3_0_0.py` runs the algebra's **current** rules, vendored from the live
tree with the algebra's own executor, and compares **variant sets element by element** rather than
per-candidate verdicts. Two gains, both measured:

- A capacity that matched while admitting different variants used to pass; now it cannot.
- **Mandatory is cross-checked.** v2.0.0 had to report mandatory as not cross-checked, because the
  1.x rules shipped no mandatory rule. The current rules enforce it, so every operator PIB uses is
  decided by the algebra.

## What was not carried over

Nothing. v2.0.0's reporting of "operator kinds the algebra ships no rule for" is empty under the
current rules, so the field itself is gone rather than printed as always-none.
