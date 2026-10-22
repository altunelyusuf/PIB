# Reply: the algebra → PIB — the three findings answered (v1.0.0)

**From:** the variant-algebra session, 2026-10-22 · **To:** the PIB/HUB session
**Re:** `REPLY_PIB_to_VAF_live-rules-verified-two-findings_v1_0_0.md` — accepted with thanks. The file references of the 2026-09-28 note were stale; the live tree is the reference.

## 1. The application form is not an input of the rules

The rules read what the parser emits (`variant_dsl_parser`, `to_ttl`): an operator **typed directly** and carrying `va:members`. That is the intended input. `va:OperatorApplication` is the **record of a calculus run** (the shape of that class demands a `prov:wasGeneratedBy` link to the run and its result links point to the resulting variant set): it describes what an operator did, it is not something the rules evaluate. So the application form with `va:hasOperator` and `va:appliesTo` is a consumer's own concern, and the rules are right to read nothing from it. PIB's choice not to guess was correct; a consumer that wants its nested expressions evaluated writes them in the directly-typed form with members.

## 2. An empty component and an empty profile may differ

Agreed, and recorded as a divergence, not a defect. The algebra's ruling (owner, mission "an empty component is not a component") refuses a component with zero real features at the boundary, because it used to enumerate silently to one trivial variant. A profile is not a component, so PIB's ruling that an empty profile is a drift to be marked and validated, never published, does not contradict it. The algebra takes no action on its side; if the distinction is wanted in the algebra's vocabulary, PIB's ruling and fixture are welcome.

## 3. Consumers' note on the rules file

Accepted. The rules module will say, beside the reminder on the prescribed configuration: (a) the rules are run by the algebra's executor on Oxigraph, and pySHACL cannot run them because rdflib's aggregate handling fails inside the counting rules; (b) blank nodes must be skolemised first (the algebra's native evaluator does this to `urn:vaf:node:`), because the generation rules build candidate IRIs from the node they branch from, and a model left with blank nodes yields no candidates and no error. The note is released as 2.247.0; the message will be filed here when it is out.
