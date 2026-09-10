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
- SHACL invariants (`pib_invariants_v1_0_0.ttl`) across all 5 real ontology files: G3
  (self-coverage required before wiring) correctly refuses the 3 worked-example interfaces
  (PAMG, RADAR, O4SDLC) for lacking `SelfCoverageAttestation` — matching the package's own
  documented claim that "the gate has teeth," not a defect.

## Honest status carried forward from the source package

Scaffold + verified tooling, NOT a populated ecosystem. Real interface declarations for the
ecosystem's actual participants (O4SDLC, RADAR, PAMG), self-coverage attestations, and
per-profile wiring models beyond the one worked capstone example remain open work — see this
package's own `README.md` and `BLUEPRINT_v1_0_0.md` for the complete, honest scope.

## Session attribution

Transferred under `OE_SESSION=pib-publish-session`, a new session distinct from the original
`pib-hub-session` that built and first published this content to Ontologies (see
`https://claude.ai/chat/deecfc96-1250-4967-a407-8500247813fd`).
