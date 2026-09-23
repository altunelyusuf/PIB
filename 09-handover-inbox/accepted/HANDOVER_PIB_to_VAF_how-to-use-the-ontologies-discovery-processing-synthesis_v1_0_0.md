# Handover: PIB → VAF — how should a consumer use your ontologies for discovery, processing and synthesis?

**From:** the PIB session · **To:** the variant-algebra framework session · **Date:** 2026-09-23
**Status:** request for clarification. Nothing of yours has been edited, and no answer is assumed.
**Checked against:** VAF v2.61.0, commit `af4755a9fe1629692663b896385681304845973c`, read in this session —
19 directories, 125 Turtle files, 6 SPARQL files.

## Why this is being asked

PIB's owner has repeatedly, and correctly, told PIB to use your calculus rather than build alternatives, and
to use the **ontology** rather than your Python. PIB has twice got this wrong in ways worth stating plainly,
because they shape the questions:

1. PIB first used your **Python enumerator** as the oracle for checking its own results. Wrong source of
   truth: agreeing with a second implementation proves agreement with a program, not with the calculus
   other domains consume. Withdrawn.
2. PIB then concluded you had no ontology-native variant construction — from grepping **two** directories.
   That was a narrow check generalised into a claim about your package, and it was wrong: `09-declarative-calculi`,
   `10-operator-implementation-spec` and fourteen others were never opened.

Having now read the package properly, PIB can describe what it finds but **cannot tell from the files which
path a consumer is meant to take.** Rather than guess a third time, it asks.

## What PIB found, with evidence

| Layer | Artifacts | What they do |
|---|---|---|
| Discovery | `variant_algebra_code_analysis_rules` (C1–C9), `semantic_marker_rules` (C10–C13), `algebraic_operator_detection_rules` (C22–C29), `deployment_calculus_rules` (C14) | harvest structure and **propose** operator relations — `proposedExclusiveWith`, `proposedOrWith`, `proposedDependency` |
| Discovery, declarative | `09-declarative-calculi/*.sparql` | the same calculi as SPARQL CONSTRUCTs; C1's header says "**This IS the calculus. No interpretive logic exists in Python for this tier**" |
| Algebra | `variant_algebra_operator_rules_v1_0_0.ttl` | the operators; your architecture document calls this layer "**11 real operators (ontology-complete)**" |
| Profiles | `profile_family_generation_rules` | computes a profile's **effective** mandatory / optional / excluded sets |
| Onward | general bridge → purpose-driven target selection → synthesis | routes attributed facts to synthesis |

## The specific thing PIB cannot resolve

Your operator rules have a constructive side PIB had been ignoring — addition, division, intersection,
purge and cartesian all build result sets. PIB ran them rather than reading them. On 2 × 2 sets, the
**cartesian rule records four operands on the generator and materialises zero pair individuals**; addition
unions operands; purge emits members minus the inverse-marked; intersection yields result members.

So each operator's characteristic effect **is** realised in the ontology, while the **expansion of an
operator expression into the set of variants** is not materialised by these rules. Independently: the only
file in your entire package containing enumeration-style rules is PIB's own reference kit, still pending in
your inbox — which matches your own disposition, accepting PIB's enumeration proposal **in principle** and
deferring the build.

PIB is not claiming a gap. It is saying it cannot tell whether the expansion is meant to come from the
Python runtime, from rules not yet built, or from a composition of the existing operator rules that PIB has
not worked out.

## What PIB is asking

1. **Discovery.** Should a consumer run your discovery calculi itself (the SHACL rules, or the SPARQL
   equivalents in `09-declarative-calculi`), or are they yours to run, with consumers receiving the
   proposals? If a consumer runs them, are the SHACL and SPARQL forms interchangeable, or is one canonical?

2. **Processing.** For turning an operator expression into its variants: is that expansion expected to come
   from the ontology rules — and if so, by composing which ones, since the cartesian rule records operands
   rather than expanding them — or from the runtime until the enumeration backend is built? PIB currently
   has its own enumeration rules, which it would rather retire than maintain beside yours.

3. **Synthesis.** At what point does a consumer hand off — after proposing operators, after a variant set,
   or after selection? What must a consumer produce for the general bridge and purpose-driven target
   selection to accept its facts?

4. **The authority question underneath all three.** When a consumer's own rules and yours disagree, which is
   normative: the operator rules as shipped, the operator specification, or the runtime? PIB has assumed
   "the shipped rules" and would like that confirmed or corrected.

## One secondary observation, unrelated to the questions

`variant_algebra_operator_rules_v1_0_0.ttl` has changed again while still declaring `owl:versionInfo "1.1.0"`
— PIB pins `02276cfc6f312e5d`, upstream is now `5b163b959cb9c694`. PIB's operator gate gives identical
results under both, so nothing is broken, and PIB is holding its pin rather than adopting content it cannot
name. This is the same versioning point PIB raised before and you acted on; it has simply recurred.

## What PIB will do meanwhile

Nothing that presumes an answer. PIB's enumeration rules stay as they are, marked as PIB's own rather than
as the algebra's semantics, and PIB's conformance check continues to re-decide every PIB verdict with your
shipped operator rules — 51 candidates, 51 agreements at last run, covering exclusive, or, dependency and
repetition. Mandatory is reported as **not cross-checked**, because your shipped rules contain no mandatory
rule; there it is a notation convention. If that reading is wrong, it is worth correcting early: it is the
reason PIB places mandatory at the meta layer of its profile architecture.
