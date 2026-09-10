# PIB — Profile + Integration-Interface Blueprint v1.4.0

**Status:** Phases 1–3 complete (vocabulary published, interfaces composed, per-profile wirings validated);
reproducibility gap closed (vendored spoke pins, `07-`); **ORCP registration round CLOSED** — PIB is an
accepted external registrant of the OEE ecosystem (`08-registration/`). Verified against OE Pack v20.23.4. **v1.4.0:** four canonical assessment profiles materialized & published (`01-ontologies/pib_assessment_profiles`, `04-documentation/ASSESSMENT_PROFILES_MATERIALIZATION`) — OBAF retired; PAMG-as-grader on OEE facets, profile-driven; ZeroTime deferred.

Subject-based package (OE numbered-dash convention) defining how the generic ontology ecosystem
(**RDODI generates, RADAR measures, PAMG grades**) talks via a shared **Profile** vocabulary and a
loose **produces/consumes** integration contract, validated by the pinned **Variant Algebra Framework**.

## Layout
```
01-ontologies/         profile_tbox + integration_interface_tbox + worked-example ABox
02-shacl-safeguards/   pib_invariants (G1 one-wiring-per-profile, G2 profile-scoped, G3 self-coverage
                       required, G4 contract-closure, G5 edge well-formed)
03-tooling/            wiring_validator (wraps pinned VAF) + self_coverage_checker
04-documentation/      BLUEPRINT_v1_0_0.md (the design), this README, BOOTSTRAP_PROMPT
05-prov-records/       PROV-O lineage
06-vaf-engine-pin/     VAF dependency pin (SHA-256 of the verified full framework package + 4 core files)
07-spoke-contributions/ vendored, SHA-pinned, read-only spoke interface TTLs (reproducibility) + pins note
08-registration/       ORCP round (CLOSED): submission + builder + fit-gap note + Phase G closure +
                       OEE return contract (vendored as received) + REGISTRATION_STATUS
VERSION.txt MANIFEST_SHA256.txt
```

## Quick verification (what was proven here)
- `python3 03-tooling/wiring_validator_v1_0_0.py` → Variation Capacity 9; all 4 collision-guard checks PASS
  (requires the pinned VAF at `PIB_VAF_SRC`, default = this session's unpack path).
- SHACL invariants run; G3 correctly refuses the worked example's interfaces until they carry
  self-coverage attestations (the gate has teeth).

## Two gates, both required before adoption
1. **Self-coverage** (per node, profile-independent): `self_coverage_checker` — ontology valid standalone.
2. **Wiring validity** (per profile): `wiring_validator` — operator constraints + contract closure, via VAF.

## Honest status
Scaffold + verified tooling, NOT a populated ecosystem. The parallel session builds out real interface
declarations (validated against actual content — L-58), self-coverage attestations, and per-profile wirings.

---

# BOOTSTRAP_PROMPT (for the dedicated PIB session)

You are building out the Profile + Integration-Interface ecosystem from blueprint v1.0.0, under OE
Operating Discipline v2.1.0. FIRST verify the OE files on disk (SHA), and ask for any missing input rather
than assume. Then:

1. Read `04-documentation/BLUEPRINT_v1_0_0.md` and the two TBoxes in `01-ontologies/`.
2. Pin VAF per `06-vaf-engine-pin/` (the FULL framework package; SHA-verify the 4 core files). Confirm
   `wiring_validator` runs against it. Do NOT pin the sub-kits.
3. For each real participant (O4SDLC, RADAR, PAMG, RDODI): author an `OntologyInterface` with `produces`/
   `consumes` of real capabilities, and run `self_coverage_checker` to attach a `SelfCoverageAttestation`
   (satisfies G3). VALIDATE each `produces` against the producing ontology's actual content (L-58).
4. Author per-profile wiring models (capstone exists; add IEEE paper, courseware, …); run `wiring_validator`
   per profile; record Variation Capacity.
5. Keep B1/L-64: this package does not edit RDODI/RADAR/PAMG/O4SDLC — it declares contracts ABOUT them and
   ships proposals to each owning line. Each system attaches its own profile-specific behaviour to the
   shared Profile IRI; do not pull system-specific vocabulary into the shared ontologies.
6. Forward to the VAF line the fix-forward note (parser eager grammar-load) from `06-vaf-engine-pin/`.
