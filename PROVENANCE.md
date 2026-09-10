# PIB — provenance and lineage note

This repository is the standalone home for PIB (Profile + Integration-Interface Blueprint),
created 2026-09-10.

## Governed lineage (not rewritten — L-112)

PIB v1.0.0–v1.4.0 was developed and released in an internal engineering lineage before this
repository existed: the Phase 1–3 build, ORCP registration and Phase-G closure with the OEE
ecosystem, per-profile wiring validation, reproducibility vendoring, and the four canonical
assessment profiles materialized with OBAF retired. That lineage is retained in full and is
never rewritten or deleted; releases from v1.4.1 onward are made here.

This repository does not duplicate the OE Pack. Governance is inherited by reference from the
OE Operating Discipline (see `GOVERNANCE.md`), which is maintained separately and versioned
independently of this package.

## What's here

The verified content of the final internal release (27 files, manifest self-verified clean 27/27)
promoted to repository root. `PUBLISH_RECORD.ttl` is carried over **unedited** as the honest
historical record of how that content was originally published — it describes the publish ceremony
that produced it, not this repository's own releases, and is deliberately left that way rather than
rewritten to look native here (L-112).

## Real, verified before transfer, not asserted (2026-09-10)

Independently re-run this session, against the pinned VAF engine (exact SHA-256 match confirmed
for all 4 pinned core files):
- `wiring_validator_v1_0_0.py`: Variation Capacity 9, all 4 collision-guard checks PASS, exit 0.
- SHACL invariants (`pib_invariants_v1_0_0.ttl`): validating `01-ontologies/` ALONE yields 3 G3
  refusals (PAMG, RADAR, O4SDLC lack `SelfCoverageAttestation`) — this is the known
  standalone-vs-merged measurement artifact documented in this package since v1.2.1, NOT the gate
  refusing real content. The attestation links live in `07-spoke-contributions/`, which is exactly
  why they are vendored. Validated over the full package (`01-ontologies/` + `07-spoke-contributions/`):
  **conforms=True, 0 violations** (pySHACL, advanced mode, merged graph, 589 triples).

## Honest status (corrected v1.4.1 — the statement below replaced a stale one)

The transferred v1.4.0 text described this package as a scaffold whose real interface
declarations, self-coverage attestations, and per-profile wiring models "remain open work."
That was **false for v1.4.0** and is corrected here per B3, having been re-derived directly from
the shipped bytes rather than carried forward on report. The v1.4.0 content actually carries:

- **8 `iif:OntologyInterface`** individuals, **8/8 with `iif:hasSelfCoverage`** attestations
  (real O4SDLC / RADAR / PAMG declarations vendored in `07-spoke-contributions/`, plus the
  assessment-layer interfaces including the OEE measurement facet and GamOnt).
- **6 `pib:Profile`** and **6 `iif:WiringVariant`** — the worked capstone + IEEE-paper examples
  and the four canonical assessment profiles (Core software development, Ontology-based,
  Ontology-development on OEE, Gamification), each pinning one validated wiring.
- Full package conforms to `pib_invariants` with **0 violations**.

What genuinely remains open: **`Profile_ZeroTime`** (deferred by owner decision; its ZT4SWE leg is
additionally blocked because `zrcm_v2_5.ttl` is DL-inconsistent as shipped — a finding for the
ZT4SWE owner, not edited here per B1), and the PAMG-ontology-native grading implementation, which
is PAMG's own evolution and not this package's to build.

## Session attribution

Promoted under `OE_SESSION=pib-publish-session`, a session distinct from the `pib-hub-session`
that built and first released this content. Session attribution for every release is recorded in
`PUBLISH_RECORD.ttl` (`reliability:authoringSession`) and in the `Session:` trailer of each commit.
Working-session URLs and internal repository paths are deliberately not cited here: they resolve
for no external reader and are not part of this package's verifiable record.
