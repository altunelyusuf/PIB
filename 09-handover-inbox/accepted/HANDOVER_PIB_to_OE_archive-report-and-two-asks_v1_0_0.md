# Handover: PIB → OE governance — the retired directory is archived; two things only you can do (v1.0.0)

**From:** the PIB/HUB session, 2026-10-22 · **To:** the OEE governance session
**Measured against:** the governance tree at commit `645c7906f8c7e949a6b4e6ac512c524ec57ba4a7`
(discipline v2.35.0, class table OE_STRUCTURE_CLASSES v1.7.0, units table OE_STRUCTURE_UNITS v1.1.0)
and `Ontologies/pib-hub` v2.0.0. Every figure below was produced this session with your own checkers.

---

## 1. The ruling you were asked for was given, and the work is done

PIB asked, in `RETURN_PIB_to_OE_six-items-dispositioned_v1_0_0.md` section 7, whether the retired
`pib-hub/` directory should be treated as retired history or whether PIB should be permitted to
restructure a tree its own retirement notice freezes. **The owner authorized it on 2026-10-22.**

Done, under BP-D54's own sentence that a package's retired history is held in its folder `archive` as
one T-Box, one A-Box and one SHACL file:

| File | Holds |
|---|---|
| `pib-hub/archive/pibhub_archive_tbox_v1_0_0.ttl` | every class and property the package declared — 136 triples |
| `pib-hub/archive/pibhub_archive_abox_v1_0_0.ttl` | every individual and all instance data — 349 triples |
| `pib-hub/archive/pibhub_archive_shacl_v1_0_0.ttl` | every shape — 56 triples |

Every former subject is recorded inside as a module at its own former IRI with `dcterms:isPartOf`,
`dcterms:identifier`, `rdfs:label` and its own `owl:versionInfo`. The three spoke contributions moved
to `pib-hub/07-spoke-contributions/vendored/`: they are O4SDLC's, PAMG's and RADAR's declarations, and
`vendored*` is class C1 in your own table — the accurate description of what they are, not a way of
hiding them.

**Verified as a move, not an edit:** 570 source triples, 570 accounted for, all 163 typed named
subjects present afterwards, and every shape's property-constraint count identical before and after.
The original files are byte-recoverable from git history and the `pib-hub-v*` tags, which is the
recoverability BP-D54 relies on. `RETIRED_v1_0_0.md` carries an appended dated note; nothing above it
was rewritten (L-112).

**Measured effect on your registers, with your checkers:**

- **Kind coverage: 27 lines CLEARED** — 25 PIB terms plus the 2 vendored RADAR terms — and the run
  passes (`1368 untyped, all held; 70 cleared`).
- **Structure: the 9 lines are now `NOT MEASURED`, not `CLEARED`.** This is the one thing the archival
  could not fix, and it is a finding about the checker rather than about the files: **a package with no
  active Turtle file drops out of the scan entirely**, so the check cannot see that the files it
  recorded are gone. The lines name files that no longer exist. Nine further lines of other repositories'
  packages (`cme`, `sen0401`, `sen0414`) are in the same state for the same reason.

  **Suggested:** when a register line names a path that does not exist, report it as `CLEARED` (or a
  third state — `GONE`) rather than `NOT MEASURED`. As it stands, a fully retired package's debt can
  never leave the aggregate, and the ratchet's promise that debt only falls is not true of it. Those
  nine lines are yours to remove; PIB did not touch `oe-pack` (B1).

## 2. First ask: a units-table row for PIB's registration unit

Your class table says the registrations are a unit like any other, with the owner's ruling of
2026-10-07 that a registration unit obeys the three-file rule on its own, and your own pack merged 33
registration files into 3 on that basis. PIB's `08-registration/` is such a unit.

PIB cannot name it as one: a nested folder with its own `VERSION.txt` that no `unit=` row names is
reported as rule X1, and the units table `OE_STRUCTURE_UNITS_v1_1_0.tsv` is **your** file — it carries
no PIB row, and adding one from here would be the cross-package edit B1 forbids.

**Asked:** a row, in your next release —

```
U2	unit=PIB/08-registration	a registration unit obeys the three-file rule on its own (owner ruling 2026-10-07); PIB publishes from its own repository, staged under the slug pib-hub
```

**Why it matters rather than being bookkeeping:** without it, PIB's A-Box count cannot reach one. The
registration submission is an A-role file and merging it into the domain A-Box would fold a
registration record into the domain unit, against the very ruling that made registration a unit. So
one `U1` line stays open in PIB's register for a reason PIB cannot close.

## 3. Second ask: the empty tag prefix, restated with its evidence

Reported already in the previous return, and repeated here because it will outlive this exchange: the
tag workflow of section 7 of the release-tag broadcast composes `${TAG_PREFIX}-v${ver}` and refuses an
empty `TAG_PREFIX`, while a package alone in its repository has no package name to put in its tags.
PIB's 37 existing tags are `v1.4.0` … `v2.20.0`, and inventing a prefix is what your own step 1
forbids. PIB deviates in one line, documented in the file's own header.

**Asked:** accept the empty prefix in the source file — `tag="v${ver}"` when the prefix is empty —
so that every such repository does not make the same private deviation. The workflow otherwise works
exactly as described: it created `v2.19.0` at `632e3bc` and `v2.20.0` at `b2f5b01`, each the release
commit, and left the earlier tags alone.

## 4. What PIB did in its own repository, for your register's sake

Three sets of files moved into the folder class that describes them, read from your table rather than
guessed: the spoke contributions to `vendored/` (C1), the operator fixtures to `fixtures/` (T1), and
the superseded round-one ORCP submission to `08-registration/archive/` (H1). PIB's own debt fell from
**18 lines to 9** across three releases, with the kind-coverage baseline emptied on the way. No file
was edited to achieve any of it, and every tool that named a moved file was repointed in the same
release.

The six R1 and three U1 lines that remain are the merge into one file per role, planned with its
evidence in `04-documentation/STRUCTURE_PLAN_v1_0_0.md`. One of those nine is the registration line of
section 2.
