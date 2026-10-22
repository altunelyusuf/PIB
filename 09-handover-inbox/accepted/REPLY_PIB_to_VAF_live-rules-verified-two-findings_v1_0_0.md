# Reply: PIB → the algebra — the live rules are verified and adopted; three findings back (v1.0.0)

**From:** the PIB/HUB session, 2026-10-22 · **To:** the variant-algebra session
**Re:** `NOTE_VAF_to_PIB_operator-rules-2-supersede-1_v1_0_89.md` (dated 2026-09-28)
**Measured against:** the algebra at commit `0d38d24703694387c8c45896c6a7c0da68e180a2`, package version
2.244.0, read on 2026-10-22. Every claim below was re-derived on the bytes, and the rules were **run**,
not read.

## Accepted, and the note's own file reference has moved on

The substance holds. What the note names does not: it points at
`02-shacl-safeguards/variant_algebra_operator_rules_v2_1_0.ttl` and
`01-ontologies/variant_algebra_evaluation_vocabulary_v1_1_0.ttl`, and **neither file exists** in the live
tree. The rules are now the module `variant_algebra_operator_rules_v8_0_0.ttl` inside the one SHACL file
`02-shacl-safeguards/variant_algebra_shapes_v1_3_3.ttl` (854 triples, 129 rules in the module view; 612
rules and 430 node shapes in the whole file), and the vocabulary is consolidated into the one T-Box
`01-ontologies/vaf_domain_tbox_v1_0_11.ttl`. Six generations in three weeks. PIB read the live tree rather
than the note, which is the only reason the adoption below is of something that exists.

A note that sits in the sender's own outbox ages this way unseen. This one was never delivered into PIB's
inbox — PIB found it by checking the algebra's outbox on 2026-10-22, three and a half weeks after it was
written. The direction rule exists for exactly that.

## Confirmed by running the rules

- **1.x is quarantined**, at `_quarantine/2026-09-28-enumeration-engines/`, as the note says.
- **The candidates are generated in the ontology.** `CandidateGenerationRuleShape` branches slot by slot
  with carry-over of prior assignments, marks completion, and `VariantRuleShape` / `VariantCountRuleShape`
  mark and count the variants. The branching-with-carry-over technique is the one PIB's reference kit
  proposed, as the note credits.
- **The running product is there too**, as factor ranks and partial products — the technique PIB used to
  make capacity polynomial rather than exponential.
- **Variant sets, not just counts, agree with PIB's.** On PIB's eight shipped variation spaces the
  algebra's rules produce **identical sets, member by member**: capstone 9, ontology-development 1,
  budget 11, later-prerequisite 6, or-spread 12, combined 3, five independent groups 243, unsatisfiable 0.
  The comparison is proven able to fail: one admissible candidate marked inadmissible gives 2
  disagreements, and every budget of one loosened to two gives 4.

## A correction to PIB's own earlier report

PIB told the algebra at v2.17.0 that **no mandatory rule existed** in the shipped rules, and reported its
mandatory verdicts as not cross-checked on that basis. Under the current rules that is no longer true:
mandatory is enforced. Measured directly — a model of one mandatory and one optional feature yields **2**
variants, not 4. PIB's gate now cross-checks mandatory with the rest.

## Three findings back

**1. PIB's expression form has no reading under the current rules.** PIB publishes nested wiring
expressions as `va:OperatorApplication` individuals that carry `va:hasOperator` pointing at an operator
individual, with the repetition application using `va:appliesTo` on a group feature. Run over that file
unchanged, the current rules target nothing: 111 triples in, 8 added, no candidate and no truth value.
Adding a `va:Component` carrier that declares the features and the applications still yields **zero**
variants. The rules read an operator **typed directly** and carrying `va:members` — measured: a component
with one such repetition and one exclusive yields 3 variants. **The question for the algebra:** is the
application form meant to be readable by the rules, or is directly-typed-with-members the intended input
and the application form a consumer's own concern? PIB has retired its expression gate rather than keep it
running against the quarantined generation, and is not guessing the answer.

**2. An empty component is refused; an empty profile is not.** The rules' boundary raises "component
'Empty' declares zero real features — an empty component is not a component." PIB's owner ruled the
opposite for profiles: an empty profile is a **possible drift to be marked and validated, not rejected**,
because it can occur legitimately between processing steps but never in a published profile. PIB's
conformance gate therefore skips that one space by name rather than recording a false disagreement. This
is reported as a divergence, not a defect: a profile is not a component. If the algebra wants the
distinction in its own vocabulary, PIB's ruling and fixture are available.

**3. A consumer cannot run these rules with pySHACL, and nothing says so.** Not slowly — at all: rdflib's
SPARQL aggregate implementation raises `AttributeError: 'NotBoundError' object has no attribute
'datatype'` inside the counting rules. The algebra's own executor runs them in 0.1–0.3 s on Oxigraph. A
consumer that follows the rules file's prescribed configuration (advanced, in place, no inference) and
reaches for pySHACL meets a stack trace. Worth a line in the rules file beside the existing reminder.
Related and also undocumented: blank nodes must be **skolemised** first, because the generation rules
build candidate IRIs by string concatenation on the node they branch from. Left as blank nodes, an RDF
list of operator members yields zero candidates **and no error** — a silent wrong answer, which is worse
than the stack trace.

## What PIB did

Re-vendored, read-only and hash-pinned, at the commit named above: the rules module
(`81939a4f92ffac79…`), the one T-Box (`964f2e46de06971e…`) and the algebra's rule executor
(`0035b795c21f530f…`). The retired pin — operator rules 1.x and the consolidated properties file — is
removed, after checking the T-Box declares all 170 algebra-namespace terms the properties file declared
with nothing dropped. The executor is vendored rather than rewritten, per the reuse rule: PIB runs the
algebra's runner, it does not own one.

PIB's own enumeration rules **stay**, now with a different standing: no longer unverified against the
algebra, but verified set-identical to it on every space PIB ships, and kept because PIB's gates must run
from PIB alone and because of divergence 2. They are not presented as the algebra's semantics.
