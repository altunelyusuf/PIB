# Handover: OE to PIB — dependency shape has changed since registration; is the criticality profile still right?

**From:** OEE governance session **To:** PIB/HUB
**Per:** `B1` (a proposal, not an edit — PIB's own registration decision to make)

## The finding

PIB's ORCP registration closed at `oe-pack v20.23.4` (`COMPLIANT — ACCEPTED`), with criticality
`core:Profile_Standard`, no gateable facets registered. `oe-pack` is now at `v20.71.0`. PIB's own
`VERSION.txt` moved twice during this session's investigation alone, most recently to `2.0.2`.

Checked directly before writing this, not carried forward from PIB's own dependency-pin notes
alone:

- `PIB_VAF_SRC` — the loose, external VAF engine dependency the registered submission was built
  against — has **zero remaining references** anywhere in PIB's current top-level docs or
  `03-tooling/` scripts. Confirmed by direct search, not assumed from the pin file's own claim.
- Per PIB's own `06-vaf-engine-pin/VAF_DEPENDENCY_PIN_v1_0_0.md`, this happened in two real steps:
  first the vendored operator rules (`11-vendored-operator-rules/`) took over evaluation from the
  pinned Python engine, then, as of PIB `v2.0.0`, Variation Capacity computation moved entirely
  into SHACL rules and SPARQL inside PIB's own ontology — a genuine architectural shift, not a
  version bump alone.
- The registered submission's own criticality assessment (`Profile_Standard`) was made against the
  *earlier* dependency shape. Nothing in the registered record reflects that PIB's calculation path
  no longer touches an external runtime dependency at all.

## What's being asked

Not a ruling — that's OE's to make once PIB's own session decides to act, per `Ontology_Registration_Conformance_Protocol`
Phase A onward. This handover only asks PIB's own session to consider:

1. Given the dependency shape has genuinely changed twice since the registered assessment, does
   `Profile_Standard` still fit, or does moving calculation on-ontology change what criticality
   profile is appropriate?
2. If PIB's own session judges the profile still correct, that's a real answer — OE has no standing
   basis to require reassessment on a version gap alone (`B1`); this is offered as an observation
   flagged from the registered record's own age, not a demand.
3. A related, parallel handover went to VAF itself this session, naming its own `F-0` operator-scope
   divergence (15 operators in the current ontology vs 6 in the older runtime-scope file it shares
   an IRI with) as worth carrying into any fresh submission either package makes — relevant here
   too, since PIB's own vendored operator rules sit downstream of whichever generation VAF settles on.

---
Filed by the OEE governance session, prompted by a direct request to assess how VAF's variant
concepts (and PIB's consumption of them) affect OE, OEE, the operating discipline, and the
registration protocol.
