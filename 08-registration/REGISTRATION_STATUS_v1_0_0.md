# PIB/HUB — Registration status (ORCP round, CLOSED)

**Status: REGISTERED — accepted external registrant. Round CLOSED.**

PIB/HUB completed a full Ontology Registration & Conformance Protocol (ORCP) round with OEE governance.

| Item | Value |
|---|---|
| Protocol | ORCP v1.0.0 |
| OEE verdict | COMPLIANT — ACCEPTED |
| Criticality (D.1) | `core:Profile_Standard` (accepted; revisable if gateable items are later registered) |
| IRI/roster (D.2) | `pibreg:` instances correct as-is; **accepted external registrant**, NOT a governed roster subject |
| Recorded by OEE | `orh:ReleaseEvent_OEPack_v20_23_3` (processed) + `…_v20_23_4` (closed) |
| Closed against pack | OE Pack v20.23.4 |

## What this folder contains
- `pib_orcp_submission_v1_0_0.ttl` — the emitted registration instances (Phase B). Registers PIB as a
  `core:Artifact` (conformance, `Profile_Standard`) and as an `orh:SubjectOntology` with `orh:OntologyFile`
  lineage records for the three PIB ontology files. Uses only central `core:`/`orh:` hooks; all minted
  individuals are in `pibreg:` (no OEE vocabulary minted — B1/L-64).
- `build_pib_orcp_submission_v1_0_0.py` — the builder that emits the submission (recomputes file SHAs live).
- `PIB_ORCP_fit_gap_note_v1_0_0.md` — Phase A self-classification + Phase B claims + scope disclosure (BP-X1).
- `PIB_ORCP_Phase_G_closure_note_v1_0_0.md` — PIB's closure confirming the contract and re-derivation.
- `OEE_to_PIB_registration_contract_v1_0_0.md` — **vendored read-only, exactly as OEE returned it** (Phase F).
  This is OEE's artifact, included for provenance; not edited here.

## Re-validation (this package build)
The submission re-validates **0 violations** against the current OE Pack (v20.23.4) — `core_shacl` +
`oepack_release_history_shacl`, pySHACL 0.31.0, inference=none, governing TBox merged (L-90, BP-X1).

## Open only as future choices (not pending)
Roster promotion (PIB → governed subject) and registering gateable items (risk/performance/testing/
configuration) or a knowledge_base deposit — each would open a new A–G round and re-assess criticality.
