# PIB — Profile + Integration-Interface Blueprint

Formal, machine-checked integration contracts between independent ontology-engineering systems.

PIB answers a specific problem: when several ontology systems must work together — one *generates*
analysis-and-design artifacts, another *measures* their adequacy, another *grades* them — how do you
let them integrate **without** `owl:imports` welding them into one brittle graph, and how do you
*prove* a given wiring is valid rather than asserting it?

PIB's answer has three parts:

1. **Declared interfaces, not imports.** Each system declares what it *produces* (public exports)
   and what it *consumes* (required inputs). Integration becomes a declared, validated **contract**;
   every ontology keeps its standalone self-coverage.
2. **The wiring space is a variability model.** The set of possible produces→consumes bindings is a
   variation space governed by variant-algebra operators (Mandatory, Optional, Exclusive, Or,
   Dependency, Repetition). Admissible wirings are **enumerated by a pinned engine**, not argued for.
3. **A Profile pins one wiring.** A `pib:Profile` binds an artifact category, the criteria shared
   across systems, and exactly one validated `WiringVariant` — so an assessment is reproducible.

## What's here

| Path | Contents |
|---|---|
| `01-ontologies/` | `profile` and `integration-interface` TBoxes, the four canonical **assessment profiles**, the wiring-composition record, and a worked capstone example |
| `02-shacl-safeguards/` | `pib_invariants` — G1 one-wiring-per-profile, G2 profile scoping, G3 self-coverage required before wiring, G4 contract closure, G5 well-formed edges |
| `03-tooling/` | `wiring_validator` (wraps the pinned variant-algebra engine) and `self_coverage_checker` (parse + SHACL + HermiT) |
| `04-documentation/` | Blueprint, published vocabulary, composition and materialization records |
| `05-prov-records/` | PROV-O provenance |
| `06-vaf-engine-pin/` | SHA-256 pin of the external Variant Algebra Framework engine |
| `07-spoke-contributions/` | Vendored, SHA-pinned, **read-only** interface declarations owned by other systems |
| `08-registration/` | OE ecosystem registration round (submission, contract, closure) |

## Assessment profiles

Four canonical profiles are published, each pinning one validated wiring, with grading performed by
PAMG over measurement facets rather than by a separate framework:

| Profile | Measurement basis → grader |
|---|---|
| Core software development | O4SDLC → RADAR → PAMG |
| Ontology-based system | O4SDLC → RADAR + OEE ontology-quality → PAMG |
| Ontology development | **OEE-based**: A&D model + OEE ontology-quality → PAMG |
| Gamification | GamOnt model + fidelity → PAMG |

A fifth, **ZeroTime**, is deliberately **not** published: it is deferred, and its ZT4SWE leg is
independently blocked because `zrcm_v2_5.ttl` is DL-inconsistent as shipped. That is recorded rather
than papered over — see `04-documentation/ASSESSMENT_PROFILES_MATERIALIZATION_v1_0_0.md`.

## Reproducing the checks

```bash
pip install rdflib pyshacl lark owlready2 --break-system-packages

# 1. wiring validity against the pinned engine (requires the VAF source; see 06-vaf-engine-pin/)
export PIB_VAF_SRC=/path/to/variant_algebra_framework_v1_0_0/src
python3 03-tooling/wiring_validator_v1_0_0.py

# 2. invariants over the FULL package — 01-ontologies/ plus 07-spoke-contributions/
python3 - <<'PY'
import rdflib, glob
from pyshacl import validate
g = rdflib.Graph()
for f in glob.glob('01-ontologies/*.ttl') + glob.glob('07-spoke-contributions/*.ttl'):
    g.parse(f, format='turtle')
s = rdflib.Graph().parse('02-shacl-safeguards/pib_invariants_v1_0_0.ttl', format='turtle')
print(validate(g, shacl_graph=s, advanced=True)[0])   # -> True, 0 violations
PY
```

**Validate the whole package, not `01-ontologies/` alone.** Alone, it yields 3 G3 self-coverage
refusals — a known standalone-vs-merged measurement artifact, not a defect: the attestation links
live in `07-spoke-contributions/`, which is precisely why they are vendored.

## Integrity

Every file is SHA-256 pinned in `MANIFEST_SHA256.txt`, which self-verifies:

```bash
grep -v '^#' MANIFEST_SHA256.txt | grep . \
  | sed -E 's/[[:space:]]+\([0-9]+b\)[[:space:]]*$//' | sha256sum -c
```

The variant-algebra engine is **pinned by hash, not vendored** — its lineage stays with its owner.

## Governance, provenance, license

- `GOVERNANCE.md` — how PIB inherits the OE Operating Discipline by highest-SemVer resolution, and
  the boundaries that apply (ownership of vendored artifacts; historical records are never rewritten).
- `PROVENANCE.md` — lineage. PIB was developed inside the `altunelyusuf/Ontologies` monorepo as
  `pib-hub`; that directory is now **retired and frozen**, with its history preserved at tag
  `pib-hub-v1.4.0`. This repository is the source of truth from v1.4.1 onward.
- **License: CC BY 4.0** (`LICENSE`), matching the `dcterms:license` declared in every ontology here.

## Citation

> Altunel, Y. (2026). *PIB — Profile + Integration-Interface Blueprint* (Version 1.4.2).
> İstanbul Kültür Üniversitesi, Department of Computer Engineering.
> https://github.com/altunelyusuf/PIB

## Honest scope

PIB is a **validated integration and assessment framework**, not a running assessment service. The
contracts, invariants, profiles and tooling are real and re-runnable; grading itself is PAMG's, and
the systems PIB wires together are developed and owned separately.
