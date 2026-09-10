# Profile + Integration-Interface Blueprint (PIB) v1.0.0

**Status:** BLUEPRINT for a dedicated parallel session to build out. Authored in the PAMG session
under OE Operating Discipline v2.1.0 (OE Pack v20.11.0, ABox SHA `c0db3c13…`). Per L-64/B1 this is a
self-contained design package, not edits to RDODI / RADAR / PAMG / O4SDLC.

## 1. Problem this solves
The ecosystem has three generic, loosely-coupled systems — **RDODI generates, RADAR measures,
PAMG grades** — that all operate *per category of artifact*. Without a shared notion of category and
a declared way for ontologies to connect, two failures occur:
- **Category collisions:** one system treats an artifact as category A while another treats it as B.
- **Brittle integration:** `owl:imports` chains couple ontologies tightly and break self-coverage
  (observed: O4DF's broken `example.org/core` import; an O4SE module reported inconsistent standalone).

## 2. The two coupled concepts

### Profile (shared category + variant configuration)
A `Profile` binds: one `ArtifactCategory`, the `SharedCriteria` for that category (only criteria
meaningful to MORE THAN ONE system), and exactly one validated `WiringVariant`. A Profile is the
**variant configuration** in the variant-algebra sense — it resolves the integration variation space
to one reproducible point. Every artifact carries exactly one canonical Profile IRI (collision-avoidance).
This **consolidates** existing fragments — PAMG's `Profile` (Rubric+DocumentGenre+MetricSet) and RDODI's
profile registry — rather than inventing a fourth; RADAR (which had none) gains the concept here.
System-specific behaviour (grading weights, generation templates, measurement dimensions) is **NOT**
modelled here — it stays in each system, attached to the shared Profile IRI (avoids L-64 scope-foreign bloat).

### Integration-Interface (produces/consumes contract + variation space)
Each ontology DECLARES its interface — `produces` (public exports) and `consumes` (required inputs) —
**without `owl:imports`**. Integration is a **declared, validated contract**, not a hard import. The set
of candidate produces→consumes bindings is a **variation space** whose features (`IntegrationEdge`) are
governed by variant-algebra operators (Mandatory/Optional/Exclusive/Or/Dependency/Repetition). A Profile
selects one valid `WiringVariant`; edges are scoped `forProfile`, so the same edge can be active under one
profile and not another. Distinct from PROV-O: this is **design-time capability**, PROV-O is **runtime
history** — they compose, never conflated.

## 3. The two gates (kept separate on purpose)

| Gate | Scope | Tool | What it checks |
|---|---|---|---|
| **Self-coverage** | per node, profile-INDEPENDENT | `self_coverage_checker_v1_0_0.py` | each ontology parses, is SHACL-conformant (and optionally DL-consistent) **standalone**, no consumed ontology merged |
| **Wiring validity** | per profile | `wiring_validator_v1_0_0.py` (wraps VAF) | operator constraints hold + every active `consumes` matched by an active `produces`; reports Variation Capacity |

A wiring is adoptable **only if BOTH gates pass.** Self-coverage has teeth: the SHACL invariant G3 refuses
any interface lacking a `SelfCoverageAttestation` (demonstrated — the worked example's three interfaces all
fail G3 until attested).

## 4. VAF as the formal engine (verified, pinned)
The wiring validity engine is the **Variant Algebra Framework**, pinned to
`Variant_Algebra_Framework_v1_0_0` (package SHA-256 `7858339ee554f330…`). Verified working THIS session:
the shipped `BruteForceBackend.enumerate()` + `is_admissible()` (core files SHA-pinned in
`06-vaf-engine-pin/`) correctly enumerated 9 admissible variants of the worked capstone wiring and rejected
two-measurers / consume-without-produce / no-A&D-source. **Loose dependency:** the validator loads VAF from
a path (`PIB_VAF_SRC`), never copies it — mirroring how RADAR loads RDODI's enforcement. **Pin the FULL
framework package, not the sub-kits** — `vaf-workbench-kit` and `Vaf_package` ship the backend without the
enumerator/grammar and cannot run the validity path.

## 5. The variant connection (why this is your variant algebra)
The integration space **is** a variation space: edges = features; operators = your six VAF operators;
a profile = a configuration/binding; Variation Capacity = count of valid wirings. Profile-driven wiring is
a direct application of VAF to ecosystem integration — not a metaphor.

## 6. What the parallel session must build out (scope)
1. **Self-coverage attestations** for each real participant (O4SDLC, RADAR, PAMG interfaces) — run the
   checker, attach attestations, satisfy G3.
2. **Real interface declarations** for RDODI/RADAR/PAMG/O4SDLC (produces/consumes of actual capabilities),
   each validated against actual ontology content (L-58 — a declaration blind to content is documentation
   that lies; the contract validator MUST confirm the producing ontology truly defines the capability).
3. **Per-profile wiring models** beyond the capstone example (IEEE paper, courseware, …); compute Variation
   Capacity per profile.
4. **Lazy-load fix for VAF's parser** (eager `_load_grammar()` at import) + ship the `.lark` — record as a
   fix-forward note to the VAF line (sub-kit packaging defect).
5. **Decide where the shared ontologies live** — recommended: standalone pinned ontology (this package),
   not folded into OE (keeps category vocabulary out of the governance core).

## 7. Honest limits of this blueprint
- The TBoxes + SHACL + tooling are authored and parse/run here; they are a SCAFFOLD, not a populated,
  fully-validated ecosystem integration. Populating real interfaces is the parallel session's job.
- Wiring validity is verified against the pinned VAF engine; **Variation Capacity is reported as
  admissible-variant count** by the engine — VAF's own dedicated metric module was not separately confirmed.
- DL-consistency in the self-coverage checker is a hook (caller wires the HermiT harness), not run here.
