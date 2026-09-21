# Retired: the Python wiring validator

`wiring_validator_v1_0_0.py` is **removed as of v2.0.0**. It computed Variation Capacity by calling
the pinned Python enumeration engine through `PIB_VAF_SRC`. PIB's calculation path is now entirely
in the ontology: generation, admissibility and counting are SHACL rules and SPARQL, run by
`variation_capacity_v1_0_0.py`, which contains no algebra.

## Why it was removed rather than kept as a second opinion

Keeping it would have meant keeping the Python engine dependency alive on the calculation path,
which is exactly what this change removes. A tool that is "available but not used" drifts: it is
not re-run, so nobody notices when its answer stops matching.

## The equivalence was measured before removal, not assumed

Both reference cases were computed by the engine first, then independently by the ontology path:

| Space | Engine | Ontology path | Complete candidates |
|---|---|---|---|
| Worked capstone | 9 | **9** | 64 (= 2⁶) |
| Ontology-development profile | 1 | **1** | 8 (= 2³) |

The capstone case is retained as the self-test of `variation_capacity_v1_0_0.py`, so the number the
engine used to produce stays pinned as the answer the ontology must keep reproducing. It is checked
on every run, not recorded once and trusted.

## What still uses Python, and why that is not the same thing

- `variation_capacity_v1_0_0.py` — loads graphs, re-invokes the rule engine until the graph stops
  growing, runs one counting query, prints. No algebra.
- `operator_rule_runner_v1_0_0.py` — same shape, for the operator expression gate.
- `self_coverage_checker_v1_1_0_1.py` — parsing, SHACL and a reasoner harness.

These are ordinary programming: file handling, control flow and reporting. The distinction that
matters is whether the *meaning* of a constraint lives in code or in the ontology. It now lives in
`02-shacl-safeguards/pib_enumeration_rules_v1_0_0.ttl`.

## The engine pin is not deleted

`06-vaf-engine-pin/` is kept. The pin records which engine generation produced the numbers PIB
published historically, which is provenance worth keeping, and it remains the reference if anyone
wants to re-derive the equivalence above. It is no longer required to compute anything here.

---

## Note appended in PIB v2.0.2 — do not rewrite the text above

The text above names `variation_capacity_v1_0_0.py` and the per-case space files as they stood at
retirement. Since v2.0.2 the harness is `variation_capacity_v1_0_0_1.py`, and the two spaces live in
one consolidated file, `12-operator-fixtures/profile_variation_spaces_v1_0_0.ttl`. The equivalence
table is unchanged: the self-test now checks both spaces by name and still reproduces 9 and 1.
