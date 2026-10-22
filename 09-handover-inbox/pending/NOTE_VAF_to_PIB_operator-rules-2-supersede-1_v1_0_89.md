# Note: VAF → PIB — operator rules 2.1.0 replace the 1.x file you vendor

**From:** the VAF session (Lineage 5, VAF-WI-111) · **To:** the PIB session · **Date:** 2026-09-28
**Nothing breaks on your side.** Your vendored copy of `variant_algebra_operator_rules_v1_0_0.ttl` (1.2.0) is pinned by hash and still works. This note is about L-121: the generation you pin is now narrower than VAF's.

## What changed

**`02-shacl-safeguards/variant_algebra_operator_rules_v2_1_0.ttl` replaces 1.x in VAF's live tree.** 1.x is quarantined at `_quarantine/2026-09-28-enumeration-engines/`. The 1.x rules checked one candidate, a flat `va:isSelected` state per feature. The 2.1.0 rules evaluate a whole model:
- **Candidates.** They build the variation space and generate the candidates, using your reference kit's branching and carry-over technique.
- **Truth.** They decide whether each feature and each expression node holds or fails in each candidate, with one rule per operator.
- **Special forms.** They apply bodies, removals and conditional substitutions.
- **Variants.** They mark the variants (`va:Variant`) and count them (`va:admissibleVariantCount`, `va:combinatorialUpperBound`).
- **Execution.** The rules run in `sh:order` strata, each to a fixpoint, through `06-runtime/src/variant_rule_executor_v1_0_0.py` on Oxigraph. pySHACL's iteration was too slow: 56 s for eight features, against 0.2 s.
- **Vocabulary.** New terms are in `01-ontologies/variant_algebra_evaluation_vocabulary_v1_1_0.ttl`.

**The meanings are unchanged.** Exclusive is exactly one (at most one inside an optional list), or is at least one, dependency is an implication, intersection is co-selection, and repetition is a bound. On the corpus, 2.x gives the same variants as VAF's former enumerator for every component both evaluate (165 of 165 committed rows).

**Changed for a 1.x reader:**
- **Propagation → partner exclusion.** Propagation is now partner exclusion, scoped to a component. It still reads `va:SetA` / `va:SetB`.
- **Dropped, with no user in VAF:** the Optional marker `va:isAdmissible`, partition (`va:samePartitionAs`), Cartesian pairing (`va:PairGenerator`), and the `va:candidateMember` / `va:hasEmittedMember` form of purge.
- **Carried unchanged:** Division, the Addition closure, the Intersection result members and weak grounding.

## What we ask

Please decide whether PIB moves its pin to 2.1.0 or keeps 1.x as a decided state. If you keep 1.x, record it as such, so the narrower generation is a choice rather than an accident.

## Addendum (VAF-WI-101, same day): extended properties 1.2.0

You also vendor `01-ontologies/variant_algebra_v3_extended_properties_v1_0_80.ttl` by hash. It is now 1.2.0. The file name is unchanged, and so is every other declaration.

**What changed:** `va:calculusImplementationSHA256` for C1–C9 and C22–C29 now gives the hash of the SHACL rule file production runs:
- `variant_algebra_code_analysis_rules_v1_0_0.ttl` for C1–C9;
- `variant_algebra_algebraic_operator_detection_rules_v1_0_80.ttl` for C22–C29.

**Why:** these values held the hashes of Python files. Those hashes were stale, and the Python originals are now removed.

## Addendum 2 (2026-09-28, VAF-WI-113)

The rules file is now `02-shacl-safeguards/variant_algebra_operator_rules_v2_2_0.ttl` (2.2.0), and the vocabulary is `01-ontologies/variant_algebra_evaluation_vocabulary_v1_2_0.ttl` (1.2.0). 2.2.0 adds substitution's model rewrite as rules: the result component, chains in written order, and a classifier replaced wholesale. It also adds the A4 check's variant-level reading. The operator rules of 2.1.0 are unchanged in meaning. A vendored copy of 2.1.0 has no substitution rewrite; its generation is narrower (L-121).

## Addendum 3 (2026-09-28, VAF-WI-114)

`02-shacl-safeguards/variant_algebra_semantic_marker_rules_v2_0_0.ttl` (2.0.0) replaces 1.0.0, which your handover lists among the discovery rules (C10–C13). 1.0.0 was narrower than its calculi:
- **C10** kept four terms and, on Oxigraph, lost the first part at every camel-case boundary (`'$1_$2'` names a group `1_` there).
- **C11** had five of the ten patterns.
- **C12** only confirmed a type name.

2.0.0 is breaking. C10 gives ordered `va:NameTerm` individuals instead of `va:proposesNameTerm` strings, and C12 and C13 read a harvested syntax tree (`01-ontologies/python_syntax_tree_vocabulary_v1_0_2.ttl`). C14–C17 and C32 are new rule files: `variant_artifact_classification_rules_v1_0_0.ttl` and `variant_loop_bound_rules_v1_0_0.ttl`. See `04-documentation/vaf_calculi_on_rules_v1_0_89.md`. A vendored 1.0.0 keeps working with its narrower answers (L-121).

## Addendum 4 (2026-09-28, VAF-WI-117)

`02-shacl-safeguards/variant_algebra_operator_rules_v3_0_0.ttl` (3.0.0, breaking) replaces 2.2.0. The vocabulary is `variant_algebra_evaluation_vocabulary_v1_3_0.ttl`, and the core ontology is `variant_algebra_v3_3_0.ttl`.

By the owner's decision, every expression now has one meaning, the sets it generates. A statement holds where the variant restricted to its names is one of them:
- `a < b` is a with b;
- in `a | b` and `a $ b`, the names of the part not chosen are absent;
- `a - b` is a and not b, also as a statement.

The keyword forms (`requires`, `exclusive`, `or`) and the order edges keep their meaning as shorthands. See `04-documentation/vaf_native_evaluator_v1_3_0.md`. A vendored 2.x copy gives the old answers for expression statements (L-121).

## Addendum 5 (2026-09-28, VAF-WI-112)

`02-shacl-safeguards/variant_algebra_operator_rules_v3_1_0.ttl` (3.1.0) replaces 3.0.0. The vocabulary is `variant_algebra_evaluation_vocabulary_v1_4_0.ttl`.
- **Classifier bodies left the language** (the owner's decision of 2026-09-28): the carrier rules and a substitution's blocks inside a component are gone, and the body terms (`va:inBodyOf` and the rest) are deprecated. A model with a body is refused by the parser.
- **Presence apart from truth:** a feature's presence is `va:presentIn` / `va:absentIn`. It differs from its truth only for a variable whose definition generates the empty set.
- **A repeated group inside an expression** is decided by the group rule.
- **Definitions** are expanded to terminals by a new file, `02-shacl-safeguards/variant_definitions_expansion_rules_v1_0_0.ttl`.

For models without bodies and without a repeated group inside an expression, a vendored 3.0.0 gives the same variants (L-121). See `04-documentation/vaf_native_evaluator_v1_4_0.md`.

## Addendum 6 (2026-09-28, VAF-WI-118)

`02-shacl-safeguards/variant_algebra_operator_rules_v4_0_0.ttl` (4.0.0, breaking) replaces 3.1.0. The vocabulary is `variant_algebra_evaluation_vocabulary_v1_5_0.ttl`, and the core ontology is `variant_algebra_v3_4_0.ttl`.
- **The rules generate each expression's sets.** A node holds in a candidate when the candidate's counts on its features are one of those sets, so one truth rule replaces the per-operator truth rules of 3.x.
- **`+` is additive** (the owner's ruling of 2026-09-28): a name on both sides is one feature, so `(p $ q) + p` gives {p} and {p, q}. 3.x gave {p}.
- **Definitions** are generated by the same rules, and the 3.1.0 expansion rules file is retired.
- **Core ontology 3.4.0** tags `+` as "product" and `$` as "union".

For expressions whose operands share no name, a vendored 3.1.0 gives the same variants (L-121). See `04-documentation/vaf_native_evaluator_v1_5_0.md`.

## Addendum 7 (2026-09-28, VAF-WI-119)

`02-shacl-safeguards/variant_algebra_operator_rules_v5_0_0.ttl` (5.0.0, breaking) replaces 4.0.0. The vocabulary is `variant_algebra_evaluation_vocabulary_v1_6_0.ttl`, and the core ontology is `variant_algebra_v3_4_37.ttl`.
- **Exclusion and dependency hold for the whole variant** (the owner's rulings of 2026-09-28). The sets are generated as in 4.0.0; then a variant that has both sides of an `X $ Y`, or X of an `X < Y` without Y, is dropped wherever the relation is written. `(a $ b) + (a $ c)` gives {a} {b, c}; `[a] + [b] + [a < b]` gives {} {b} {a, b}; `(p $ q) + p` gives {p}.
- A variable's variants are its consistent sets (`va:ConsistentSet`); a component's candidate that breaks a relation is not admissible.
- **Core ontology 3.4.1** returns the tag of `$` to "restriction".

A vendored 4.0.0 gives the same variants for a component whose exclusions and dependencies are each a statement of their own (not inside `+`, a list or an optional item); the 131-model corpus is unchanged (L-121). See `04-documentation/vaf_native_evaluator_v1_6_0.md`.

## Addendum 8 (2026-09-28, VAF-WI-121)

`02-shacl-safeguards/variant_algebra_operator_rules_v6_0_0.ttl` (6.0.0) replaces 5.0.0; the vocabulary is `variant_algebra_evaluation_vocabulary_v1_7_0.ttl`. The variants are unchanged. What changed is how they are reached:
- a variable's definition is split into independent groups, counted by the product of their counts, its own sets generated only when asked for;
- a component's candidates are built after the sets, and a branch that already breaks a statement is not extended (your kit's pruning technique, now in VAF's rules);
- the orders of the candidate rules moved (20-23 to 25.1-25.4).

A vendored 5.0.0 gives the same variants, more slowly (L-121). See `04-documentation/vaf_native_evaluator_v1_7_0.md`.

## Addendum 9 (2026-09-28, VAF-WI-122)

`02-shacl-safeguards/variant_algebra_operator_rules_v7_0_0.ttl` (7.0.0, breaking) replaces 6.0.0; the vocabulary is `variant_algebra_evaluation_vocabulary_v1_8_0.ttl`. Recursive definitions are allowed and evaluated to their least closed set. A join's result is now raw (`va:rawSetOf`, `va:rawPartialOf`, `va:rawKey`), and one representative per node, stage and key carries `va:setOf` / `va:partialOf`: a consumer reading join results directly must read the representatives. Component variants are unchanged. See `04-documentation/vaf_native_evaluator_v1_8_44.md`.
