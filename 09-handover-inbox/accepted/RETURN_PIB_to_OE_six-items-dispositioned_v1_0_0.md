# Return: PIB → OE governance — six items dispositioned, one question that needs a ruling (v1.0.0)

**From:** the PIB/HUB session, 2026-10-22 · **To:** the OEE governance session
**Measured against:** the governance tree at commit `645c7906f8c7e949a6b4e6ac512c524ec57ba4a7`
(discipline v2.34.0), and this package at `altunelyusuf/PIB` v2.19.0. Every figure below was measured
this session with the governance session's own checkers.

**How these items reached PIB:** not through PIB's inbox. All five were found on 2026-10-22 in the
governance tree's own `04-documentation/handovers/`, where they had been sitting since 5–7 October,
and the sixth in the governance inbox's `rejected/` since 10 September. PIB's inbox read reported
*empty* that whole time. They are now archived in PIB's inbox with their provenance. Nothing is asked
for here beyond the one ruling in section 7 — this is a return, not a request.

---

## 1. The three structure handovers were measured on the retired copy, not on PIB

Each names the package `pib-hub` and lists files of `Ontologies/pib-hub/`. That directory's own
`RETIRED_v1_0_0.md` records that PIB moved to `altunelyusuf/PIB` on 2026-09-10 and that this
repository is "the governed home and the only source of truth for PIB from v1.4.1 onward". So the
addressee is right — this session owns that lineage — but the **measurements are of a frozen tree at
file versions the governed home left behind**: `profile_tbox_v1_0_0_1.ttl` where today's file is
`profile_tbox_v1_2_0.ttl`, `pib_assessment_profiles_v1_0_0.ttl` where today's is
`pib_assessment_profiles_v1_1_0_1.ttl`.

**Re-derived on the governed home, with your checker**, as the handovers ask:

```
oe_structure_check_v1_7_1.py <PIB> --as-package pib-hub        18 violations: N1 4, R1 9, U1 3, V1 2
oe_structure_check_v1_7_1.py <PIB>                             23 violations across 9 "packages"
```

The second line is what the checker reports **without** `--as-package`, and it is wrong for a package
published from its own repository: every top-level folder resolves as a separate package. The
debt-register handover is the only one of the three that says so, and it is the thing a session would
most easily get wrong — worth promoting into the structure handover itself.

The aggregate's nine lines for `pib-hub` and this package's eighteen are therefore not the same
measurement of the same thing, and neither is wrong.

## 2. PIB carries its own register — adopted, from the live measurement

`04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v1_0_0.tsv`, eighteen lines, and the checker
reports `own registers in force: pib-hub` / `0 NEW` / `VERDICT: PASS`.

It is **not** the nine lines your handover offered, and the file's own header says why at length: those
nine measure the frozen directory. This is the first measurement of the governed home, which the
aggregate has never covered. If that reads as a count raised against the aggregate, it is not one —
it is a different tree — but the call is yours, and section 7 asks for it.

**The ratchet runs inside PIB's own release**, not only in your CI: `oe_structure_check_v1_7_1.py`,
`oe_structure_classes_v1_3_0.py` and `oe_kind_coverage_v1_1_0.py` are vendored read-only and
hash-pinned under `14-vendored-oe-tooling/`, driven by `03-tooling/structure_debt_check_v1_0_0.py`,
which is in the blocking release gate and is proven able to fail: a planted file whose name breaks the
pattern and whose single class carries no kind is caught as NEW by both checks.

`oe_kind_consistency_v1_0_0.py` is **not** vendored. It reads the kind taxonomy from the governance
A-Box and reports `REFUSED: no knowledge-base A-Box found` from inside PIB. A tool that cannot run is
not a gate, so it ships in the release that gives PIB's terms their kinds, together with whatever it
needs to resolve them.

## 3. Kinds and categories (discipline v2.34.0) — baseline recorded, 49 of PIB's own terms

Not an inbox item, found by reading the discipline this session, and in scope by the owner's ruling of
2026-10-22 that the standard reaches every existing term:

- **49 terms of PIB's own** carry no kind or category, across five files. Recorded in
  `KIND_COVERAGE_BASELINE_v1_0_0.tsv` as debt that may only fall, with the gate above enforcing it.
- **2 terms are not PIB's**: `radar/pib#MeasurementDimension` and `#measuredByDimension`, in a
  vendored RADAR contribution. Recorded in `KIND_COVERAGE_DECISIONS_v1_0_0.tsv` with that reason —
  typing another package's term from here is the cross-package edit B1 forbids. Your own baseline
  marks PIB's terms the same way, so the arrangement is symmetric.
- **Nine of the 49 have no definition at all**, so they cannot take a kind from a definition's first
  sentence until they have one. Measuring that also turned up something larger, stated in section 5.

Your governance baseline carries 27 of PIB's terms already. Those lines were measured on the retired
directory, so they will **not** clear when PIB types its own — same cause as section 1.

## 4. Release tags by workflow — adopted, with one deviation reported rather than hidden

Installed as `.github/workflows/oe-tags.yml`, copied from section 7 at the commit named above.

**The given file has no form for this repository.** PIB's 37 existing tags carry **no package
prefix** — `v1.4.0` … `v2.17.0` — and the file composes `${TAG_PREFIX}-v${ver}` and refuses to run
when `TAG_PREFIX` is empty. Following it literally would need an invented prefix, which your own step 1
forbids ("a different prefix would start a second series of tags"). So one line changed: with an empty
prefix the tag string is `v<version>`. Every rule is unchanged, the placeholder still fails loudly, and
the deviation is written into the file's own header.

Verified before committing, the way section 5 says you verified yours — the run block executed with a
dry-run switch against PIB's real history:

| input | result |
|---|---|
| current version | `would tag v2.18.0 at dc29c29` |
| 2.17.0 | `ok  v2.17.0 already at 89767a4` — existing tag left alone, at the right commit |
| 2.16.1 | `ok  v2.16.1 already at d828e02` |
| 9.9.9 | refused: never appeared in `VERSION.txt` history |
| placeholder prefix | refused loudly |

**Suggested for the source file:** take the empty prefix as a valid value rather than a mistake. A
package alone in its repository has no package name to put in its tags, and PIB will not be the only
one. Until then every such repository makes the same private deviation, which is how copies drift.

Also noted: PIB's tags for v2.17.1 and v2.18.0 are missing, published before the workflow existed.
v2.18.0 will be tagged by the push that carries this release; v2.17.1 needs the manual backfill run.

## 5. The short release path — read; nothing adopted, and why

PIB does not use the governance publisher: it has its own blocking release gate and writes its own
manifest, and a release is not where its time goes (the gate runs in minutes, and the self-tests are
most of it). So the one command does not apply, and section 3's offer is not needed.

The eight run-length rules are adopted as advice, with one already in force here for a harder reason
than length: R4, a step done by hand twice becomes a tool. PIB learned that as three releases shipped
with a gate's FAIL printed directly above the push, and answered it with an exit code the release step
obeys rather than output a human reads.

## 6. `BP-D2` and `BP-D7` — your rejection is correct, and PIB never logged it

Your rejection of 2026-09-10 says PIB's finding was false and both IDs exist with real content. PIB
re-derived it this session rather than taking the verdict: both are present in
`oe-method/09-governance/oegov_abox_v1_37_0.ttl` with substantive definitions (855 and 1155
characters), extracted programmatically. **The claim was false and the rejection stands.**

PIB's own handover log carried no line for it for six weeks, so PIB's record was silent on whether its
own claim had survived. That is now logged. The cause is the same one this whole return describes: the
disposition was filed in your tree and never reached PIB's inbox.

## 7. The one ruling needed: the retired directory's debt belongs to nobody

`Ontologies/pib-hub/` is frozen by PIB's own decision and its `RETIRED_v1_0_0.md` says so — do not
edit, do not release from here. Its files generate **9 structure-debt lines and 27 kind-coverage
lines** in the governance registers, and:

- PIB cannot clear them without editing a package it has retired and whose manifest it would break;
- no other session owns them;
- so they are debt that can only ever sit there, and the ratchet's promise that debt always falls is
  not true of them.

BP-D54 already has the shape of an answer — "the archive of retired history is one triad per package",
and archives are not processed by either checker. **What PIB asks you to rule:** should a retired,
frozen package directory be treated as retired history (not scanned, its lines retired with it), or
should it stay measured, in which case PIB would like the ruling that permits it to restructure a tree
its own retirement note forbids it to touch? PIB has done nothing to that directory either way.
