# Proposal disposition — composed-graph reproducibility (v1.2.0 → v1.2.1)

**Proposal:** `hub_proposal_composed_graph_reproducibility_v1_0_0` (from PAMG/Charter-03 spoke).
**Disposition:** **ACCEPTED — PRIMARY remediation (vendor pinned spoke contributions).** Applied in v1.2.1.

## Independent verification (HUB, this session — L-65: verify before applying)
Reproduced the proposal's evidence exactly with pyshacl 0.31.0:
- `01-ontologies/*` alone → **209 triples, 3 G3 violations** (O4SDLC_if, RADAR_if, PAMG_if).
- `01-ontologies/*` + the 3 spoke contributions → **337 triples, 0 violations.**

The proposal's SHA pins match the contributions the HUB consumed in Phase 3 (`c2d4ce93…`,
`c226b671…`, `8f1e2bc1…`). Finding confirmed: correctness was never in doubt (VC=9, guards, G1/G2/G4
re-confirmed), but the Phase-3 conformance verdict was not reproducible from the package alone.

## Why PRIMARY over the alternative
The lockfile alternative documents reproducibility but still requires the verifier to independently
obtain the spoke files — the gap stays open. Inlining the attestation triples into HUB-owned files
would duplicate spoke claims as HUB content (worse for B1 + staleness). Vendoring verbatim,
SHA-pinned, read-only, attributed copies makes the package self-validating while preserving B1
(no edit/authoring of spoke content). See `07-spoke-contributions/VENDORED_PINS_v1_0_0.md`.

## Changes applied (v1.2.1, PATCH)
- ADD `07-spoke-contributions/` — 3 vendored pinned TTLs + provenance/loadset note.
- VERSION 1.2.0 → 1.2.1; unpacked folder renamed `…_v1_0_0` → `…_v1_2_1` (reconciled per the gate).
- MANIFEST regenerated; composed graph now re-validates **conforms=True from the package as shipped**.
- No HUB ontology vocabulary changed; no spoke file edited.
