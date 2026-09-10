# PIB — provenance and lineage note

This repository is the standalone home for PIB (Profile + Integration-Interface Blueprint),
created 2026-09-10.

## Governed lineage (not rewritten — L-112)

Full prior history — the PIB Phase 1-3 build, ORCP registration and Phase-G closure with the
OEE ecosystem, the v1.0.0-v1.4.0 lineage (vocabulary publication, per-profile wiring validation,
reproducibility vendoring, four canonical assessment profiles materialized with OBAF retired) —
remains on record at:

`https://github.com/altunelyusuf/Ontologies/tree/pib-hub-v1.4.0/pib-hub`

That history is never rewritten or deleted. This repository does not duplicate the Ontologies
discipline/OE Pack — governance is inherited from `altunelyusuf/Ontologies`, per the same pattern
already used for `altunelyusuf/VAF` and `altunelyusuf/RDODI-Research`.

## What's here

The verified content of `pib-hub-v1.4.0` (27 files, manifest self-verifies clean 27/27), copied
out of the `pib-hub/` subdirectory of the Ontologies monorepo to repository root.
`PUBLISH_RECORD.ttl` is carried over unedited as the honest historical record of how this content
was originally published (it references the Ontologies publish ceremony that produced it, not
this repository).

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

Transferred under `OE_SESSION=pib-publish-session`, a new session distinct from the original
`pib-hub-session` that built and first published this content to Ontologies. Session attribution
for every release is recorded in `PUBLISH_RECORD.ttl` (`reliability:authoringSession`) and in the
`Session:` trailer of each commit; the private working-session URL previously cited here was
removed when this repository was made public, as it is not resolvable to anyone but its owner.
