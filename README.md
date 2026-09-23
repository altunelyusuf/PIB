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
   Dependency, Repetition, and the algebraic operators). Admissible wirings are **enumerated by rules in
   the ontology**, not argued for.
3. **A Profile pins one wiring.** A `pib:Profile` binds an artifact category, the criteria shared
   across systems, and exactly one validated `WiringVariant` — so an assessment is reproducible.

## What's here

| Path | Contents |
|---|---|
| `01-ontologies/` | `profile` and `integration-interface` TBoxes, the four canonical **assessment profiles**, the wiring-composition record, and a worked capstone example |
| `02-shacl-safeguards/` | `pib_invariants` — G1 one-wiring-per-profile, G2 profile scoping, G3 self-coverage required before wiring, G4 contract closure, G5 well-formed edges |
| `03-tooling/` | `variation_capacity` and `operator_rule_runner` (harnesses that drive the ontology's rules) and `self_coverage_checker` (parse + SHACL + HermiT) |
| `04-documentation/` | Blueprint, published vocabulary, composition and materialization records |
| `05-prov-records/` | PROV-O provenance |
| `06-vaf-engine-pin/` | SHA-256 pin of the external Variant Algebra Framework engine |
| `07-spoke-contributions/` | Vendored, SHA-pinned, **read-only** interface declarations owned by other systems |
| `08-registration/` | OE ecosystem registration round (submission, contract, closure) |
| `13-consumer-registry/` | Where a consumer ontology registers itself for adaptation — pointers and hashes, never copies |
| `09-handover-inbox/` | Cross-session proposals received by PIB, with dispositions |
| `10-experiments/` | Reference probes and findings (explicitly not releases) |
| `11-vendored-operator-rules/` | Vendored, SHA-pinned, read-only operator rules from the variant algebra |
| `12-operator-fixtures/` | Satisfying and violating candidate selections, proving the operator gate has teeth |

## Wiring expressions

A wiring constraint can be written as a **nested expression** over the variant algebra's operators,
not just a flat list. Operator applications are themselves valid operands, so expressions nest to any
depth, and PIB applies the algebra's **complete set of twelve operators** rather than a subset.

This matters because the operators are constructors, not a fixed menu: composing them expresses
constraints none of them expresses alone. "At most two of four measurement facets may feed the
grader" is not expressible with mandatory, optional, exclusive, or, or dependency — exclusive means
at most *one*, or means at least *one* — but is expressible by composing repetition with a
contributes-to grouping.

```bash
python3 03-tooling/operator_rule_runner_v1_0_0.py              # self-test: proves the rules reject
python3 03-tooling/operator_rule_runner_v1_0_0.py <expr.ttl> <candidate.ttl>
```

The rules are evaluated inside PIB's own gate run, from vendored copies, so the gate needs nothing
outside this package. Evaluation is deliberately run **without inference**, as the rules prescribe;
one consequence is that symmetric predicates must be asserted in both directions rather than relied
on to infer.

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
pip install rdflib pyshacl owlready2 --break-system-packages

# 1. Variation Capacity, computed in the ontology (no engine, no external source needed)
python3 03-tooling/variation_capacity_v1_2_0.py --self-test

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

**The calculation runs in the ontology.** Candidate generation, admissibility against the algebra's
operators, and counting are SHACL rules and SPARQL — see
`02-shacl-safeguards/pib_enumeration_rules_v2_2_0.ttl`. The Python files are harnesses: they load
graphs, drive the rule engine to a fixpoint, run a query and print. No constraint's meaning lives in
code. Spaces are split into independent groups of coupled features, each enumerated on its own, and
the group capacities are multiplied in the ontology — so cost grows with the number of groups, not
exponentially with the number of features. The previously required enumeration engine has been retired from this path; see
`03-tooling/RETIRED_wiring_validator_v1_0_0.md` for the equivalence measured before removing it.

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
- `PROVENANCE.md` — lineage. PIB v1.0.0–v1.4.0 was developed in an internal engineering lineage
  that is now **retired and frozen**; its history is retained and never rewritten. This repository
  is the source of truth from v1.4.1 onward.
- **License: CC BY 4.0** (`LICENSE`), matching the `dcterms:license` declared in every ontology here.

## Citation

> Altunel, Y. (2026). *PIB — Profile + Integration-Interface Blueprint* (Version 1.4.2).
> İstanbul Kültür Üniversitesi, Department of Computer Engineering.
> https://github.com/altunelyusuf/PIB

## Honest scope

PIB is a **validated integration and assessment framework**, not a running assessment service. The
contracts, invariants, profiles and tooling are real and re-runnable; grading itself is PAMG's, and
the systems PIB wires together are developed and owned separately.
