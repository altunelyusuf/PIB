# Handover — OE governance → the pib-hub session: file structure and file naming (v1.0.0)

Addressee: the session that owns the package `pib-hub`. This handover covers only that package. Date: 2026-10-05.

## 1. What changed in the method

The owner asked why new ontologies are loose single files and why older files drift from the naming and version conventions. Checked against the files: the rule existed only as comments, and no automated check covered most packages. It is now recorded and enforced.

- **The rule (knowledge base BP-D53, discipline v2.14):** an ontology subject ships as at most one T-Box file (classes and properties), one A-Box file (individuals) and one SHACL file (shapes), all declaring the same ontology IRI. No file mixes roles. No extension, follow-up, addition or patch file sits beside the three; a change goes into the canonical file as a new version, and the old version leaves the package. File names follow `name_vMAJOR_MINOR_PATCH.ttl`.
- **The check:** `repo-tooling/oe_structure_check_v1_0_0.py` reads each Turtle file's parsed content, not its name. It runs in CI on every push to every package (until now CI ran only for one package's folder), and your ceremony (`oe_ceremony_v1_0_2.sh`, stage 6) reports your package's state.
- **The ratchet:** violations that existed on 2026-10-05 are recorded in `oe-pack/04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v1_0_0.tsv`. CI fails on any violation that is not in the register, so the debt can only shrink. You do not edit the register: a fixed violation is detected and reported as CLEARED, and the OE session prunes the lines.

## 2. What the check found in your package

7 recorded violation(s): N1 2, R1 5.

**N1 — The file name does not follow the pattern name_vMAJOR_MINOR_PATCH.ttl.** (2)
What to do: Rename to the pattern in a new version (a change of identity is a new version; the old name leaves the package with a release-history record). Do not rename in place.
- `pib-hub/01-ontologies/integration_interface_tbox_v1_0_0_1.ttl` — name does not match <name>_v<MAJOR>_<MINOR>_<PATCH>.ttl
- `pib-hub/01-ontologies/profile_tbox_v1_0_0_1.ttl` — name does not match <name>_v<MAJOR>_<MINOR>_<PATCH>.ttl

**R1 — One file mixes roles: vocabulary (classes and properties), instance data, and rules (shapes).** (5)
What to do: Split the file by role: classes and properties to the T-Box, individuals to the A-Box, shapes to the SHACL file, all declaring the same ontology IRI. Each resulting file is a new version; the combined file is retired.
- `pib-hub/01-ontologies/pib_assessment_profiles_v1_0_0.ttl` — holds roles T+A (T 2, A 47, S 0)
- `pib-hub/01-ontologies/pib_wiring_composition_v1_0_0.ttl` — holds roles T+A (T 4, A 3, S 0)
- `pib-hub/07-spoke-contributions/o4sdlc_interface_contribution_v1_0_0.ttl` — holds roles T+A (T 5, A 4, S 0)
- `pib-hub/07-spoke-contributions/pamg_interface_contribution_v1_0_0.ttl` — holds roles T+A (T 5, A 4, S 0)
- `pib-hub/07-spoke-contributions/radar_interface_contribution_v1_0_0.ttl` — holds roles T+A (T 7, A 8, S 0)

## 3. What to do

1. Run the ceremony first, as always. Then list your lines with `awk -F'\t' '$2 ~ /^pib-hub\//' oe-pack/04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v1_0_0.tsv`, and check the state with `python3 repo-tooling/oe_structure_check_v1_0_0.py . --package pib-hub --register oe-pack/04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v1_0_0.tsv`.
2. Clear the violations above in your own package, one rule at a time, each as a proper new version (a changed file gets a new version and the old one leaves; nothing is edited in place; historical records are corrected by an appended note). Do not touch any other package (B1).
3. Before each push, re-run the command: it must print `0 NEW`, and it prints `CLEARED` for what you fixed.
4. Any structure decision the rule does not settle (for example a file you believe is an exception) is a question for the owner, stated with the file and the reason. An exception is recorded only with the owner's ruling.
5. When your list is clear, say so in a return to the OE inbox (`oe-pack/07-handover-inbox/pending/`), one short note with the commit.

## 4. Read before acting

The rule is knowledge-base entry BP-D53 (and L-125 for why it drifted); the discipline section is "Ontology file structure". Read them from the repository, not from this note.
