# REFERENCE_ONLY — NOT_A_RELEASE — variant-calculus experiment findings v1.0.0

**Question from the owner:** reconsider adopting the variant-algebra engine's full twelve operators
and its variant calculus. The previous justification for importing only six — that the engine's own
definitions group them into variability, algebraic and structural families — was judged not a strong
enough reason to include some and exclude others.

**That judgement is upheld by this experiment.** The categorisation argument was weak, and worse, it
was a *stipulation enforced as if derived*: the honest answer to "why these six and not the other
six?" was the engine's taxonomy plus my own reading of it, not a measurement. What follows replaces
it with measurements. The governed vocabulary is **unchanged** pending the owner's ruling.

## What the pinned engine can and cannot do (measured, not assumed)

The pinned engine's grammar file parses exactly **six statement kinds** — mandatory, optional,
exclusive, or, repetition, dependency. There is no syntax for addition, subtraction, cartesian
product, division, inverse, intersection or composition, and the enumerator and backends expose no
set-algebra functions; they return variant **sets**.

This is the real distinction, and it is not the taxonomy one:

- the six PIB imports are **enumeration-time constraints** — they shape which variants exist;
- the others are **set-level operations over enumeration results** — they combine variant sets that
  already exist.

So the engine cannot be asked to *enumerate with* an intersection. It can only produce sets that a
calculus layer then combines. Adopting the remaining operators therefore means **adding a calculus
layer on top of enumeration**, not extending the DSL. That is a design decision with a real cost,
and it is the owner's to make.

## Do the extra operators produce anything PIB cannot produce today?

Round 1 tested each operator against a real PIB question. Round 2 corrected a genuine defect in
round 1: the first intersection test used two profiles whose feature vocabularies are disjoint, so
its empty result measured the test's shape, not the operator. Both rounds are kept — the mistaken
one is not deleted, because the record should show what was checked and what changed the answer.

Measured over a shared feature universe:

| Operation | Real PIB question | Result |
|---|---|---|
| **Intersection** | Which wirings suit an artifact that is *both* an ontology deliverable *and* a gamification project? | ontology-based space 6, gamification space 12, **intersection 4** — strictly smaller than either, and a real answer PIB currently cannot give |
| **Subtraction** | Which core-development wirings do *not* depend on the grader measuring source fidelity itself — the open caveat already recorded in this package? | **2 → 1**; the caveat is material, not cosmetic |
| **Cartesian** | What is the joint space across two genuinely independent dimensions (measurement source × grading mode)? | 3 × 3 = **9**, product confirmed |
| Addition / division / inverse | union, symmetric difference, complement within a universe | all non-trivial on real inputs |

## The finding that actually decides it

Re-modelling reproduces the intersection exactly: expressing both profiles' constraints as **one**
component and enumerating gives the identical 4 wirings. So on its own, intersection is *redundant* —
whenever a session can see and rewrite both feature models, the six existing operators suffice.

**But PIB is normally not in that position.** Profiles are composed from interfaces contributed by
separate sessions, and a contributing session's model is not PIB's to rewrite — that is the
cross-session ownership boundary this package is built around. When only enumerated *results* cross
the boundary, re-modelling is unavailable and set-level composition is the only move. The probe
demonstrates this concretely: given two peers' result sets alone (6 and 12 wirings, models never
shared), the intersection is computable and yields 4; re-modelling is simply impossible, because the
statements never crossed.

So the case for the full set is not "the engine defines twelve, so import twelve." It is: **the
algebraic operators are exactly what lets PIB compose wiring spaces across an ownership boundary it
cannot cross by re-modelling.** That is a genuine capability gap, and the owner's instinct that
something was being missed is correct.

## What this does not settle

Three questions remain genuine stipulations — no file, measurement or rule decides them, so they are
the owner's to rule on rather than mine to enforce:

1. **Where the calculus lives.** A layer inside PIB, or a request to the engine's own session to
   provide set operations over its enumeration results? The second keeps the algebra with the
   algebra's owner; the first keeps PIB self-contained.
2. **How far to go.** Intersection, subtraction and cartesian have demonstrated PIB use cases here.
   Division, inverse and composition are implementable and non-trivial but had no PIB question
   driving them in this experiment — adopting them now would be symmetry, not need.
3. **What the operators attach to.** Today PIB's operator individuals annotate *edges within* one
   wiring. Set-level operators act on *whole wiring spaces*, which is a different arity and would
   need its own vocabulary rather than reusing the existing operator property.

## Reproducing

```bash
export PIB_VAF_SRC=/path/to/variant_algebra_framework_v1_0_0/src
python3 10-experiments/probe_round1_operator_use_cases_v1_0_0.py
python3 10-experiments/probe_round2_intersection_and_necessity_v1_0_0.py
```

Both probes compute every number from live enumeration against the pinned engine; none is asserted.

---

## Correction appended (round 3) — do not rewrite the text above

The analysis above is **wrong on its central claim** and is corrected here rather than replaced, so the
record shows what was checked, when, and what changed the answer.

It states that the framework's enumerator "ships no set algebra," that the remaining operators are
therefore set-level operations over results, and that adopting them would mean PIB building a calculus
layer. That conclusion came from reading a single Sprint-2 parser grammar and generalising to the whole
framework.

In fact the framework ships a tested, ontology-native implementation of the full operator specification
as twelve SHACL-AF rule shapes, with generic scaffold classes explicitly intended for a consumer to
instantiate. The operators execute on PIB-shaped data today, using those rules unmodified — including a
k-of-n bound that the six variability operators provably cannot express, obtained by composing
operators rather than by adding a primitive.

The reason PIB carries six is neither the operator categorisation (round 1's answer) nor a
calculus-layer cost (round 2's answer): it is that PIB pins an older generation of the engine, whose
runtime ontology declares only those six.

See `FINDINGS_round3_algebra_is_an_expression_language_v1_0_0.md`.
