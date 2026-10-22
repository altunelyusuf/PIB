# Vendored algebra files — pinned, read-only (NOT PIB-owned)

The three files here are **verbatim, SHA-256-pinned, read-only copies** of the variant algebra's own
calculus and its runner, vendored so PIB's conformance gate re-runs **from this package alone** — the
same reason the spoke interface declarations are vendored under `07-spoke-contributions/`.

**Ownership.** They remain owned by the algebra's session. PIB does not maintain or evolve them and
must not edit them in place. If that session re-issues them, PIB re-vendors the new hashes and bumps.

| File | SHA-256 | Role |
|---|---|---|
| `variant_algebra_operator_rules_v8_0_0.ttl` | `81939a4f92ffac79…` | the calculus: builds the variation space, generates the candidates, decides every statement, marks and counts the variants (854 triples, 129 rules) |
| `vaf_domain_tbox_v1_0_11.ttl` | `964f2e46de06971e…` | the algebra's one T-Box — the classes and properties the rules read and write |
| `variant_rule_executor_v1_0_0.py` | `0035b795c21f530f…` | the algebra's own rule runner: compiles each `sh:SPARQLRule` to an update and runs the `sh:order` strata to a fixpoint |

Vendored from the algebra at commit `0d38d24703694387c8c45896c6a7c0da68e180a2` (2026-10-22), package
version 2.244.0. The rules file is the module `variant_algebra_operator_rules_v8_0_0.ttl` of the
algebra's one SHACL file `02-shacl-safeguards/variant_algebra_shapes_v1_3_3.ttl`, extracted with the
algebra's own module-view loader so that what PIB vendors is byte-identical to what the algebra runs.

## Re-vendored in PIB v2.18.0 — the pinned generation had been retired upstream

What PIB pinned before: `variant_algebra_operator_rules_v1_0_0.ttl` (content 1.2.0) and
`variant_algebra_v3_extended_properties_v1_0_0.ttl`. Neither exists in the algebra's live tree any
more. The rules were quarantined on 2026-09-28; the properties file was consolidated into the one
T-Box above, which declares all 170 of its algebra-namespace terms with nothing dropped (checked
before the old copy was removed).

The old generation checked **one candidate at a time** — PIB generated candidates and the rules said
whether each was violated. The current generation does the whole job in the ontology: it generates the
candidates by branching with carry-over, decides each statement per candidate, and marks and counts
the variants. On PIB's eight variation spaces it produces **variant sets identical to PIB's own**,
element by element, not merely equal counts.

## Why the executor is vendored too, and why that is not a parallel implementation

The rules cannot be run by pySHACL. Tried, and it fails rather than running slowly: rdflib's SPARQL
aggregate implementation raises on an unbound value inside the counting rules. The algebra ships the
runner these rules need, so PIB vendors **the algebra's runner** rather than writing one — which is
what L-105 asks for. The runner decides nothing about the calculus: it compiles each rule's CONSTRUCT
into an INSERT and runs the strata to a fixpoint.

## Execution configuration is prescribed, not chosen

Blank nodes must be **skolemised** before the rules run. The generation rules build candidate IRIs by
string concatenation on the node they branch from, and a blank node has no such form: left as blank
nodes, an RDF list of operator members silently yields zero candidates and no error. PIB's gate
skolemises, as the algebra's own evaluator does and for the same reason.
