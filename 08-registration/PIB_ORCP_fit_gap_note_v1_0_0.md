# PIB / HUB — ORCP Phase A+B submission & fit-gap note v1.0.0

**Registrant:** PIB / HUB (Profile + Integration-Interface Blueprint v1.2.1) · **To:** OEE (governance)
**Protocol:** ORCP v1.0.0 (OE Pack v20.23.0) · **Discipline:** v2.1.1 · **Governance source:** `knowledge_base_abox_v2_5_0.ttl`

This is a **registrant-side** submission (Phases A–B). It proposes; it mints no OEE vocabulary and edits no
OEE artifact (B1/L-64, L-X7). OEE must run Phases C–F (re-derive every claim, ratify, return the contract);
I have **not** performed those — doing so as the registrant would blur the roles the protocol forbids.

## Phase A — self-classification against the recorded 12-facet roster

| Facet | PIB role | Basis |
|---|---|---|
| core | **conformance** | PIB *is* a `core:Artifact`; must satisfy `core_shacl`. Emitted + validated below. |
| oepack_release_history | **registration** | PIB has its own release lineage (blueprint v1.0.0→1.1.0→1.2.0→1.2.1). Registered as a `SubjectOntology` + `OntologyFile` records below. |
| measurement | conformance-only (no data) | PIB does **not** produce OEM measurements — RADAR does. PIB consumes/aggregates. No registration emitted (L-57: not honestly populatable by PIB). |
| quality / reliability | conformance-only (no data) | PIB authors no quality assessments / reliability evidence of its own. |
| risk / performance / testing / configuration | conformance via criticality | PIB declares `core:hasCriticalityProfile = Profile_Standard`; the EXT-2 case gates fire only at High/Critical, so they do not fire for PIB. No registration data emitted. |
| knowledge_base | registration (deferred, optional) | PIB *could* deposit its composition result; not emitted in this round (kept minimal; available on request). |
| ae / meta | **internal — none** | No registrant relationship (roster §5). |

## Phase B — emitted submission (`pib_orcp_submission_v1_0_0.ttl`, 38 triples)

Uses only verified central anchors/hooks (registration rule 1; all confirmed present on disk before emission):
- `core:Artifact` + `core:hasCriticalityProfile → core:Profile_Standard` on `pibreg:Artifact_PIB`.
- `orh:SubjectOntology` `pibreg:Subject_PIB` (`orh:lifecycleStatus "active"`), with three `orh:OntologyFile`
  lineage records (`orh:hasFileSHA256`, `orh:hasVersionInfo`, `orh:belongsToSubject`) for the PIB v1.2.1
  ontology files, each carrying its **real** SHA-256:
  - `profile_tbox_v1_0_0_1.ttl` → `0a578caf…`
  - `integration_interface_tbox_v1_0_0_1.ttl` → `c55633f8…`
  - `pib_wiring_composition_v1_0_0.ttl` → `7dbc559e…`

All minted individuals are in the `pibreg:` namespace; OEE terms are referenced, never redefined (verified:
6/6 minted IRIs in `pibreg:`; 0 in any OEE namespace).

### Validation (scope disclosure — BP-X1)
- Tool/config: **pySHACL 0.31.0**, advanced mode, **inference = none**, governing **TBox merged** (imports-merged), scope = the 38-triple submission only.
- Suites run (each facet's OWN governing suite — L-90): `core_shacl_v1_8_0` → **0 Violations** (1 Info, advisory); `oepack_release_history_shacl_v1_4_0` → **0 Violations**.
- The release-history suite initially flagged a missing `orh:lifecycleStatus` on the subject; corrected in-submission (registrant data), re-validated to 0.

## Gap finding (Phase D input)
**No genuine gap found.** PIB fits the existing contract — it registers as a `SubjectOntology` and conforms to
`core`; no missing anchor/hook/category was needed. I am **not** manufacturing a gap (L-78).

**One question for OEE (L-X7 — OEE owns the call, I do not pre-decide):** PIB declared `Profile_Standard`
(rationale: design-time governance scaffolding, not a High/Critical runtime artifact). If OEE judges PIB to be
High/Critical (it is depended-upon integration infrastructure), the EXT-2 case gates would then require PIB to
register risk/performance/testing/configuration completeness data — a future registration round. Flagged, not
decided here.

## Handoff to OEE (Phases C–F)
OEE should: (C) SHA-verify these files against the manifest and **re-derive** the SHAs/validation independently
(provenance is a claim, BP-D2); confirm no OEE artifact was edited and nothing minted (verified above, re-confirm);
(D) adjudicate the criticality question; (E/F) if accepted, assign canonical `orh:` IRIs (the `pibreg:` IRIs here
are registrant stand-ins to be replaced on ratification — Phase F "no local stand-ins"), record the round in
release-history, and return the exact contract. Phase G (re-emit against canonical IRIs + closure) follows.
