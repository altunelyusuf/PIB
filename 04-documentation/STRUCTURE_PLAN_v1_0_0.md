# Structure plan v1.0.0 — what the eighteen debt lines cost to clear, and in what order

**Written 2026-10-22, at PIB v2.19.0.** The debt is recorded and ratcheted
(`04-documentation/structure-debt/`), and the gate that enforces it is in the blocking release gate.
This document says how it gets cleared. It exists because a register with no plan beside it becomes a
permanent exemption with a ratchet drawn around it.

## What the measurement is

Taken with the governance session's own checker, `--as-package pib-hub` (without that flag the
checker resolves every top-level folder as its own package and the counts are wrong):

| rule | count | what it is |
|---|---|---|
| R1 | 9 | one file mixes roles — vocabulary, instance data, shapes |
| N1 | 4 | the file name does not match `name_vMAJOR_MINOR_PATCH.ttl` |
| U1 | 3 | more than one active file of a role: 16 A-Box files, 11 T-Box, 5 SHACL — the package ships one of each |
| V1 | 2 | two versions of the ORCP submission side by side |

Separately, and from the same standard: **49 of PIB's own terms carry no kind or category**, nine of
them with no definition at all.

## What measuring it turned up, which is larger than the debt

PIB's enumeration vocabulary — the terms the calculation rules read and write — **exists almost
entirely inside the rule bodies and nowhere as declarations**. Measured: in the `pibe:` namespace,
**8 classes** used as types with no declaration anywhere (`VariationSpace`, `Candidate`,
`CompleteCandidate` and the five constraint classes), and **18 properties** used with no declaration
(`hasFeature`, `includes`, `inSpace`, `requires`, `groupMember`, `dependent`, `prerequisite`,
`budgetGroup`, `maxSelected`, `contributesToGroup`, `featureIndex`, `featureCount`, `isInadmissible`,
`decidedUpTo`, `violates`, `derivedFrom`, `isMetaSpace`, `refinesMetaSpace`). `GroupSpace` declares
`rdfs:subClassOf pibe:VariationSpace` where the parent is never declared.

The rules work, because SPARQL reads triples and does not need a declaration. But a consumer cannot
read the vocabulary, nothing can carry a kind it has no declaration for, and the connectedness
standard cannot be measured on terms that are not there. This is the real content of the next release,
and it is why the kind coverage is not simply a matter of adding 49 lines.

## The order, and why this order

**Step 1 — declare the vocabulary and type every term (next release, MINOR).**
Declare the 26 missing enumeration terms with definitions, domains and ranges; write definitions for
the nine defined-nowhere terms; then give all of PIB's classes a kind and all of its object properties
a category, and vendor the governance consistency checker so a kind that contradicts a parent's is
caught. Purely additive: no IRI changes, no file moves, nothing a consumer imports changes. Clears the
49-line kind baseline to zero and leaves the structure register untouched.

**Step 2 — one T-Box, one A-Box, one SHACL file (the release after, MAJOR).**
This is what clears R1, U1, N1 and most of the structural debt at once, and it is MAJOR because files
leave the package: 11 T-Box, 16 A-Box and 5 SHACL files become one of each, with each former subject
recorded as a module at its own former IRI, carrying `dcterms:isPartOf`, `dcterms:identifier`,
`rdfs:label` and its own `owl:versionInfo`, as BP-D54 prescribes. Terms keep their IRIs, so a consumer
that imports a term is unaffected; a consumer that imports a *file* is, and PIB's consumer registry is
where those are known. It is deliberately second: merging files that carry undeclared vocabulary would
bury the gap found above inside a bigger file.

**Step 3 — the two V1 lines, and the vendored contributions.**
The ORCP submissions are records of closed registration rounds, and a record of the past is not
rewritten; whether a superseded submission leaves the package or becomes archive is a question for the
registration ceremony, not for the structure rule, and it goes there. The three spoke contributions
under `07-spoke-contributions/` each mix roles, but they are **other packages' vendored declarations**,
read-only here: PIB reports their shape to their sessions rather than splitting files it does not own.

**Not in any step: `Ontologies/pib-hub/`.** The retired directory's own nine lines and 27 kind lines
sit in the governance registers and PIB may not touch that tree — its retirement note forbids it. The
ruling that question needs is asked in
`09-handover-inbox/accepted/RETURN_PIB_to_OE_six-items-dispositioned_v1_0_0.md`, section 7.

## What would make this plan wrong

If step 2's module form turns out not to carry something PIB's rules depend on — the phase ordering
read from the rules file, or the shapes' targets — the merge is the wrong shape and the plan changes
rather than the rules bending to it. That is checked by running PIB's own capacity and conformance
gates against the merged files before the old ones leave, and the release does not ship if they
disagree with today's figures: capstone 9, ontology-development 1, budget 11, later-prerequisite 6,
or-spread 12, combined 3, five independent groups 243, unsatisfiable 0.


---

## Execution record — step 1 done in PIB v2.20.0 (2026-10-22)

**The vocabulary is declared.** The 26 terms that existed only inside rule bodies now have
declarations, definitions written from what the rules actually do with them, kinds and categories, and
domains and ranges where the rules fix them: `VariationSpace`, `Candidate`, `CompleteCandidate`,
`Constraint` and its five kinds, and the eighteen properties. `GroupSpace` no longer names a parent
that does not exist. Purely additive, and measured as such — PIB's capacity figures are unchanged
(capstone 9, ontology-development 1, budget 11, later-prerequisite 6, or-spread 12, combined 3, five
independent groups 243, unsatisfiable 0), and the algebra's own rules still produce identical variant
sets on all eight spaces.

**Every term is typed.** All 49 untyped terms carry a kind or a category, so the kind-coverage baseline
is empty. The assignments follow the ecosystem's own precedents rather than being invented here, read
from the governance vocabulary: a constraint is a specification, a criterion and a candidate are
information artifacts, a closed list of category values is a value domain, a phase is a process. Where
a class has a parent, child and parent carry the same kind by construction, so the consistency check
has nothing to contradict when it is vendored.

**Nine terms that had no definition at all now have one** — among them `conditionProperty`, which named
a property with no statement of what it was for, and the four consumer-registry properties the
approval gate reads.

**Four N1 lines are gone.** Every file whose name broke the version pattern was reissued under a
conforming name and version, with the old one leaving the package: the integration-interface T-Box at
1.1.0, the profile T-Box at 1.3.0, the wiring expressions at 1.1.0, the assessment profiles at 1.2.0,
the consumer-registration shapes at 1.2.0, the enumeration rules at 2.4.0, and the consumer
registration template renamed out of its `TEMPLATE_` prefix. Structure debt fell from 18 lines to 14;
nothing was raised.

**What step 2 still has to do:** the 9 R1 lines (files mixing roles), the 3 U1 lines (11 T-Box, 16
A-Box and 5 SHACL files where the package ships one of each) and the 2 V1 lines. That is the MAJOR
release this plan describes, and the plan above stands unchanged.


---

## Execution record — step 2 done in PIB v3.0.0 (2026-10-22), and one line that is not PIB's to close

**Authorized.** The owner authorized this work on 2026-10-22, in answer to the ruling asked for in the
return to the governance session.

**Before the merge, three reclassifications** — read from the governance session's own class table
rather than guessed, and each one a statement about what the files are rather than where they sit:
the three spoke contributions are copies of other packages (`vendored/`), the five operator fixtures
are deliberate test inputs (`fixtures/`), the superseded ORCP submission is retired history
(`archive/`). Two further sets the same reading caught, which the plan had not: PIB's **vendored
algebra files** were being counted as PIB's own, because `11-vendored-operator-rules` does not begin
with `vendored`, and the **experiment probe** in `10-experiments` was counted as a live shapes file.
Both moved to the class that describes them. Eighteen lines fell to nine without a file being edited.

**The merge.** Eleven files became three: `01-ontologies/pib_tbox_v1_0_0.ttl` (105 classes and
properties), `01-ontologies/pib_abox_v1_0_0.ttl` (97 individuals and all instance data), and
`02-shacl-safeguards/pib_shacl_v1_0_0.ttl` (31 shapes — the five invariants, the twenty rule shapes of
the calculation, the registration shapes). Seven former subjects are recorded as modules at their own
IRIs, carrying the metadata their file headers carried. **Every term keeps the IRI it always had**, so
a consumer that names a term is unaffected; a consumer that named a *file* reads one of these three.

**The split was made with the checker's own role definitions**, imported from the vendored copy rather
than reimplemented, so the measurement afterwards cannot disagree with the intent. Verified as a move:
1270 source triples, 1270 accounted for, all 305 typed named subjects present, and each new file holds
exactly one role and one ontology header.

**What the plan said would make it wrong, and what actually bit.** The plan said: *if the module form
turns out not to carry something PIB's rules depend on, the merge is the wrong shape and the plan
changes rather than the rules bending to it.* It happened, in the smallest possible way. The five
**phases** of the calculation are instance data — a name and an order each — so one file per role put
them in the A-Box while their rule shapes stayed in the SHACL file, and the harness raised
`rule shape CompleteRuleShape declares no known phase` on the first run. Nothing bent: the phase order
is still declared in the ontology and not in the harness, which is the whole point of declaring it; the
harness now reads the phases from the A-Box and the shapes from the SHACL file. The capacity figures
came out identical.

**Unchanged, and checked rather than asserted:** capstone 9, ontology-development 1, budget 11,
later-prerequisite 6, or-spread 12, combined 3, five independent groups 243, unsatisfiable 0 — and the
algebra's own rules still produce identical variant sets on all eight spaces.

**One guard was added rather than lost.** With one SHACL file, the calculation's rule shapes sit beside
shapes that are not part of it. The harness selects the phased ones, and a shape that carries
`sh:rule` with no phase is now an **error** rather than a shape quietly skipped: a rule dropped from
every phase would never run and the capacity would simply come out wrong. Measured on the merged file:
exactly the 20 rule shapes carry phases, and the 11 plain constraint shapes carry neither.

**The one line left is not PIB's to close.** The registration submission is an A-role file, and the
governance owner ruled that a registration is a unit of its own obeying the three-file rule separately.
Merging it into the domain A-Box would break that ruling to satisfy a count. Naming it as a unit needs
a row in the governance session's units table, which is that session's file; it is asked for, with its
reason, in `09-handover-inbox/accepted/HANDOVER_PIB_to_OE_archive-report-and-two-asks_v1_0_0.md`.
