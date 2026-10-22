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
