# Vendored spoke contributions — pinned, read-only (NOT HUB-owned)

The three files in this folder are **verbatim, SHA-256-pinned, read-only copies** of the Phase-2
interface contributions delivered by the spoke sessions. They are vendored here **solely so the
Phase-3 composition conformance verdict re-validates from this package alone** (closing the
reproducibility gap raised in `HUB_PROPOSAL_composed_graph_reproducibility_v1_0_0`).

**Ownership / B1.** These remain **spoke-owned**. Vendoring an unmodified, attributed, pinned copy
for reproducibility neither edits, authors, nor alters spoke content, so B1/L-64 is preserved. The
HUB does not maintain or evolve these files; if a spoke re-issues a contribution, the HUB re-vendors
the new SHA and bumps. Do not edit these in place.

## Pinned inputs
| File (vendored name) | SHA-256 | Origin |
|---|---|---|
| `o4sdlc_interface_contribution_v1_0_0.ttl` | `c2d4ce934d8691fa…` | O4SDLC spoke (Charter 02 source), zip MANIFEST 5/5 OK |
| `radar_interface_contribution_v1_0_0.ttl` | `c226b671eb8570db…` | RADAR spoke (Charter 02), zip MANIFEST 4/4 OK |
| `pamg_interface_contribution_v1_0_0.ttl` | `8f1e2bc1302c8b41…` | PAMG spoke (Charter 03), **loose `ex:PAMG_if` form** (the G3-satisfying RDF form; see Phase-3 record §B4) |

## Reproduction loadset (acceptance gate)
Validate the composed graph **from this package, no external files**:

```
data  = 01-ontologies/example_capstone_profile_abox_v1_0_0.ttl
      + 01-ontologies/profile_tbox_v1_0_0_1.ttl
      + 01-ontologies/integration_interface_tbox_v1_0_0_1.ttl
      + 01-ontologies/pib_wiring_composition_v1_0_0.ttl
      + 07-spoke-contributions/*.ttl          ← supplies the iif:hasSelfCoverage links (G3)
shapes = 02-shacl-safeguards/pib_invariants_v1_0_0.ttl
expect: conforms=True, 0 violations; wiring_validator → VC=9 (both profiles)
```

Without `07-spoke-contributions/`, `01-ontologies/*` alone yields 3 G3 violations (the interfaces
have no attestation link) — the gap this folder closes.
