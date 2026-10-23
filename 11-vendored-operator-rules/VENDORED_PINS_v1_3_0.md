# Vendored algebra files — pinned, read-only (NOT PIB-owned)

The three files here (and the shapes file in `vendored-shapes/`, below) are **verbatim, SHA-256-pinned, read-only copies** of the variant algebra's own
calculus and its runner, vendored so PIB's conformance gate re-runs **from this package alone** — the
same reason the spoke interface declarations are vendored under `07-spoke-contributions/`.

**Ownership.** They remain owned by the algebra's session. PIB does not maintain or evolve them and
must not edit them in place. If that session re-issues them, PIB re-vendors the new hashes and bumps.

| File | SHA-256 | Role |
|---|---|---|
| `variant_algebra_operator_rules_v8_0_0.ttl` | `2b4888ba317b8ff4…` | the calculus: builds the variation space, generates the candidates, decides every statement, marks and counts the variants (854 triples, 129 rules) |
| `vaf_domain_tbox_v1_0_30.ttl` | `71073e7fee66358f…` | the algebra's one T-Box — the classes and properties the rules read and write |
| `variant_rule_executor_v1_0_0.py` | `0035b795c21f530f…` | the algebra's own rule runner: compiles each `sh:SPARQLRule` to an update and runs the `sh:order` strata to a fixpoint |

Vendored from the algebra (repository `altunelyusuf/VAF`) at commit `0fd5539f23dcb29df7bc84c7d438b10e1d6b4b62`
(2026-10-23), package version 2.258.0. The rules file is the module `variant_algebra_operator_rules_v8_0_0.ttl` of the
algebra's one SHACL file `02-shacl-safeguards/variant_algebra_shapes_v1_3_4.ttl`, extracted with the
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

The rules are not to be run by pySHACL. Measured in PIB v3.4.0 on all eight of PIB's variation spaces (rdflib 7.6.0,
pySHACL 0.40.1, advanced mode, in place, no inference, blank and skolemised input alike): it ends **without an error and
with one variant node, whatever the space** — where the algebra's runner gives 9, 1, 11, 3, 243, 6, 12 and 0 variants. That is a
wrong answer and a silent one. The failure PIB reported earlier — an AttributeError raised by rdflib's SPARQL aggregate
implementation on an unbound value inside the counting rules — is **PIB's own earlier observation and was not reproduced** in
that measurement; the algebra's session did not reproduce it either. The algebra ships the
runner these rules need, so PIB vendors **the algebra's runner** rather than writing one — which is
what L-105 asks for. The runner decides nothing about the calculus: it compiles each rule's CONSTRUCT
into an INSERT and runs the strata to a fixpoint.

## Execution configuration is prescribed, not chosen

Blank nodes must be **skolemised** before the rules run. The generation rules build candidate IRIs by
string concatenation on the node they branch from, and a blank node has no such form: left as blank
nodes, an RDF list of operator members silently yields zero candidates and no error. PIB's gate
skolemises, as the algebra's own evaluator does and for the same reason.

## Re-vendored in PIB v3.4.0 — the T-Box moved nineteen generations, the calculus did not

What changed against the pins above: the T-Box went from `vaf_domain_tbox_v1_0_11.ttl` to `vaf_domain_tbox_v1_0_30.ttl`.
It declares exactly the same 388 classes, 677 object properties and 759 datatype properties as before — none dropped, none
added; what changed is the text and the rows around them. The rules module differs from the pinned one only by the paragraph
for consumers that the algebra's note (released in its 2.252.0) put into its header comment: no rule changed (854 triples,
129 rules, as before). The executor is byte-identical (`0035b795c21f530f…`).

Measured before this pin was written, not assumed: PIB's conformance check, run against the new files, gives **sets identical
to PIB's own on all eight variation spaces**, element by element, and its self-test still fails in both directions.

## Added in PIB v3.6.0 — the algebra's own shapes, so PIB's content can be checked against them

| File | SHA-256 | Role |
|---|---|---|
| `vendored-shapes/variant_algebra_shapes_v1_3_4.ttl` | `2fc2883fdeb84c34…` | the algebra's one SHACL file, verbatim, from the same commit as the files above (`0fd5539f…`, package 2.258.0) |

It is used for its constraints only (`03-tooling/borrowed_shapes_check_v1_0_0.py`): the check fails on any
violation whose focus node is one of PIB's, and no rule in it is run. It sits in its own folder because the
conformance check loads every `.ttl` in `vendored/` as rules.
