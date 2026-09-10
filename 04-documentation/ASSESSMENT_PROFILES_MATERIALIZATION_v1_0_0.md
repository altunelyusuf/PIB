# HUB materialization — assessment profiles v1.0.0

**What this is:** the HUB's Phase-3 materialization of the assessment profiles requested by the PAMG/OBAF
session, after the OBAF resolution. **"OBAF" is retired** — there is no OBAF interface or framework. Assessment
is *PAMG made ontology-native and profile-driven, riding on OEE's measurement facets*; **ontology-development
assessment belongs to OEE**. Published as canonical `pib:Profile` individuals in the HUB namespace
`asmt: <http://purl.org/pib/assessment#>`.

**Scope (B1):** the HUB publishes the profiles, composes the wirings, attests G3 on the real on-disk
interfaces, and runs the gates. The *PAMG-ontology-native grading implementation* (GamOnt-pattern in-ontology
scoring on OEE facets) is **PAMG's own evolution — not done here**; PAMG is represented by its interface.

## Profiles published (4 of 5 — ZeroTime deferred)
| Profile (asmt:) | Category | Measurement basis → grader | VariationCapacity | Publish |
|---|---|---|---|---|
| Profile_CoreSoftwareDevelopment | core software dev | O4SDLC→RADAR→PAMG | 1 | ✅ |
| Profile_OntologyBased | ontology-based system | O4SDLC→RADAR + OEE-quality → PAMG | 1 | ✅ |
| Profile_OntologyDevelopment | ontology deliverable | **OEE-based**: A&D + OEE-quality → PAMG | 1 | ✅ |
| Profile_Gamification | gamification (GamOnt-owned) | GamOnt model+fidelity → PAMG | 1 | ✅ |

VariationCapacity = 1 per profile is the correct `pib:Profile` semantics: each profile pins exactly one
reproducible wiring. Collision guards demonstrably hold (two-graders rejected; no-measurement-source rejected),
computed via the pinned VAF (`Variant_Algebra_Framework_v1_0_0`).

## Gate results (both required to publish)
- **Wiring validity:** all 4 admissible (VC=1), guards hold. ✅
- **Self-coverage (G3) — real on-disk artifacts, not fabricated:**
  - O4SDLC `c2d4ce934d86…` self_covered=True
  - RADAR `c226b671eb85…` self_covered=True
  - PAMG `8f1e2bc1302c…` self_covered=True
  - GamOnt `9996f9077c8e…` (gamont_tbox_v1_1_0.ttl) self_covered=True
  - OEE `1069f7c2f389…` (measurement_tbox_v2_8_0.ttl, the OEE measurement facet) self_covered=True
- **pib_invariants G1–G5** over the composed graph: **conforms, 0 violations.** ✅

## Deferred
- **Profile_ZeroTime** — postponed by owner decision. Independently, its ZT4SWE conformance leg is blocked: the
  ZT4SWE ecosystem ships no designated PIB interface ontology, and `zrcm_v2_5.ttl` is **DL-inconsistent as shipped**
  (verified genuine, not a measurement artifact; likely a datatype/lang-tag axiom clash). That is a finding for the
  ZT4SWE owner (B1 — not edited here). ZeroTime publishes once the ZT4SWE interface is designated and made consistent.

## Propagation (Phase 2 re-declare-against-published)
Spokes bind to the canonical `asmt:Profile_*` IRIs: O4SDLC, RADAR, PAMG, GamOnt, and the OEE measurement facet
each attach to the shared Profile IRI for the project types they serve. Each assessed artifact then carries exactly
one canonical Profile IRI (G1 collision-avoidance); system-specific behaviour stays in each system, keyed to the
shared IRI (no L-64 scope-foreign bloat). `Profile_Gamification` is composed by reference from GamOnt's delivered
interface — ownership stays with GamOnt.

## Honest caveats
- The published file's DL leg shows "not-run" via the owlready2→HermiT bridge (the BP-D3 Java-bridge limitation,
  treated as not-run, not inconsistent); parse + SHACL are clean and G1–G5 conform.
- The OEE self-coverage is attested on `measurement_tbox` as the representative OEE measurement-facet artifact
  (the full facet was verified clean — 0 SHACL violations, DL-consistent — in the v20.23.4 audit).
