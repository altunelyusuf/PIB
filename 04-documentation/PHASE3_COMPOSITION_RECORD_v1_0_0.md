# PIB HUB — Phase 3 Wiring Composition Record v1.0.0

Session 00 (HUB) composed the per-profile integration wirings from the Phase-2 spoke interface
contributions, against the published HUB vocabulary v1.1.0. No spoke file was edited (B1).

## Inputs consumed (Phase-2 contributions, SHA-256 verified, referenced not copied)
| Spoke | File consumed | SHA-256 (head) | Internal MANIFEST |
|---|---|---|---|
| O4SDLC | `o4sdlc_interface_contribution_v1_0_0.ttl` | `c2d4ce93…` | 5/5 OK |
| RADAR | `radar_interface_contribution_v1_0_0.ttl` | `c226b671…` | 4/4 OK |
| PAMG | `pamg_interface_contribution_v1_0_0.ttl` (loose, `ex:PAMG_if` form) | `8f1e2bc1…` | n/a (loose file) |

## Contributed contract (closes)
O4SDLC **produces** `ex:AnalysisDesignVocabulary` → RADAR **consumes** it, **produces**
`ex:AdequacyMeasurement` → PAMG **consumes** it, **produces** `ex:InstitutionalGrade` (terminal).
Every consumed capability has a producer; no dangling consume (G4 closes).

## Invariants on the composed graph (HUB example + 3 contributions)
`pib_invariants_v1_0_0.ttl` via pyshacl 0.31.0 (advanced, allow_warnings/infos): **conforms=True, 0
violations.** G3 now satisfied for all three interfaces (each carries a `hasSelfCoverage` attestation),
G1/G2 hold for both profiles, G4 closes.

## Per-profile Variation Capacity (pinned VAF engine)
| Profile | Variation Capacity | Wiring valid | Publishable |
|---|---|---|---|
| `ex:CapstoneProfile` | **9** | yes | yes |
| `ex:IEEEPaperProfile` | **9** | yes | yes |

Engine: `Variant_Algebra_Framework_v1_0_0` (pkg SHA `7858339e…`, shipped BruteForceBackend) via
`wiring_validator_v1_0_0.py`. 4/4 collision guards reject as expected (two-measurers /
consume-without-produce / no-A&D-source). Both profiles share VC=9: RADAR reused the same
`HasAnalysisDesignModel` criterion over the same chain, so the contributed edge set — hence the
variation space and its capacity — is identical; each profile selects a different point in it.

## Publishability verdict
Charter rule: a wiring is publishable iff wiring-valid AND every participating interface self-covers.
- **Wiring validity:** both profiles VC=9>0, guards correct → PASS.
- **Self-coverage (HUB-checkable):** all 3 interfaces carry G3 attestations; composed graph conforms;
  each interface *contribution TTL* re-verified by the HUB as parse + DL-consistent standalone
  (`self_coverage_checker_v1_1_0_1 --hermit`, owl:imports stripped).
- **Self-coverage (spoke module-level):** accepted as DECLARED claims — the spokes' underlying modules
  (o4ucm/o4df/o4se/radar_tbox/pamg ontologies) were NOT contributed, so the HUB cannot re-run them.
  O4SDLC attests canonical OWLAPI/HermiT PASS on all 5 modules; RADAR and PAMG attest SHACL-standalone
  PASS with the DL leg explicitly DEFERRED. Residual to close on the spoke lines: RADAR + PAMG module
  DL-consistency.

**Verdict: both wirings PUBLISHABLE on all HUB-checkable gates.** The only unverified residual is
RADAR/PAMG module-level DL-consistency (their attestation to complete; not HUB-blocking).

## Findings returned to spokes (B1 proposals — not edits)

1. **HUB tool defect, ACCEPTED + FIXED (own tool).** O4SDLC and PAMG independently reported that
   `self_coverage_checker_v1_1_0 --hermit` gave false negatives: the owlready2→HermiT bridge
   network-dereferenced `owl:imports` / ontology IRIs and folded the errors into `self_covered=False`.
   Verified on the HUB side with a constructed probe (a DL-consistent ontology importing a
   non-resolvable IRI → `self_covered=False`). Fixed in **`self_coverage_checker_v1_1_0_1`** (PATCH):
   `owl:imports` stripped before reasoning (true standalone), and a reasoner that cannot run is
   recorded "not-run" rather than counted INCONSISTENT — only a real `OwlReadyInconsistentOntologyError`
   now fails the verdict. The spokes' canonical-OWLAPI/HermiT attestations are therefore accepted.

2. **PAMG contribution — two divergent forms (to PAMG owner).** Two distinct PAMG artifacts were
   delivered: the packaged `pamg_pib_interface_v1_0_0.ttl` declares `pamg:PAMG_Interface` with its
   self-coverage in a **separate JSON file** (no `iif:hasSelfCoverage` RDF link → would FAIL G3), while
   the loose `pamg_interface_contribution_v1_0_0.ttl` declares `ex:PAMG_if` **with** the G3 attestation
   as an RDF individual and matches the O4SDLC/RADAR sibling form + the worked example. The HUB composed
   against the **loose `ex:PAMG_if`** form (the only one satisfying G3 and matching the ecosystem
   naming). Recommend PAMG reconcile to the single `ex:PAMG_if` RDF form and retire the JSON-only variant.

3. **PAMG reduction caveat (already flagged by PAMG, noted here).** PAMG's plan to consume RADAR's
   `ex:AdequacyMeasurement` and retire its own measurement engine carries an open item: confirm RADAR
   covers source-fidelity before retiring `pamg:SourceFidelityMetric`. This is a Charter-02/03 seam, not
   a HUB-composition blocker.
