# Handover: the structure unit is now the package (to `pib-hub`)

**From:** OEE governance session, 2026-10-06. **To:** the session that owns `pib-hub`.
**Relation to the earlier handover on file structure and naming:** this changes the UNIT of that rule; everything else in it stands (no file mixes roles, names follow BP-D6, one current file per identity, no patch files, the register ratchet, clear your own lines, touch no other package).

## 1. The owner's ruling (2026-10-06)

"No, not per subject. All subjects should be consolidated in one file per concept and at the end we will have just 1 file for A-Box, 1 file for T-Box, and 1 file for SHACL." Settled in the governance session: the unit is the **package**; former subjects stay inside as modules; the archive of retired history is one triad per package. The rule is BP-D54 in the knowledge base and "Ontology file structure" in discipline v2.15.0.

## 2. The rule in short

- Your package ships ONE T-Box file, ONE A-Box file, ONE SHACL file, each with ONE `owl:Ontology` header and ONE version.
- A former subject becomes a module: its terms keep their IRIs; the module is an UNTYPED resource at the former subject's IRI with `dcterms:isPartOf` (your package's ontology IRI), `dcterms:identifier`, `rdfs:label` and its own `owl:versionInfo`. Never type it `owl:Ontology` or with a domain class.
- Any other package that `owl:imports` a former subject's IRI repoints to your package ontology IRI (tell its owner through that package's inbox, naming only your own file).
- Retired history: your folder named `archive` holds one T-Box, one A-Box, one SHACL file with the retired terms and the version chain. Limit: one graph cannot hold two definitions of one IRI, so a retired term still in use keeps its last retired definition there; every complete retired state remains in git history and release tags.

## 3. Measured in your package today (checker v1.1.0, register v1.5.0)

- Active files per role: A-Box 8 files, T-Box 7 files. Archive files per role: none counted.
- Other recorded lines by rule: N1 2, R1 5.
- The register records the file counts; the check fails if a count grows, and reports a line CLEARED when it is fixed.

## 4. What to do

1. Keep clearing your role-mixing, side-by-side-version and name lines: they stay violations under the new rule, and fixing them is not wasted.
2. Plan the consolidation as its own lineage-governed piece of work: measure first (files, ontology IRIs, imports, what cites each file or version IRI), keep every term IRI, prove the combined graph before and after is identical (one declared exception per deliberate content change), and do one role at a time.
3. When a role is down to one file, delete its U1 line from the register through the next register version (report it in your handover to the OEE inbox).

## 5. What to send back

A short note in the OEE inbox: the plan and its measured size, any point this rule does not settle for your package (state it as a question; do not decide it), and which lines you have cleared.
