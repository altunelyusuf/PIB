# REFERENCE_ONLY — NOT_A_RELEASE — variant-calculus findings, round 3 (corrects rounds 1–2)

**Owner's challenge:** the algebra provides a rich set of operators for *expression construction* and
expands expressive capacity; the operators are generic rather than specific to limited types; and the
analysis was short-cut by keyword and regex reading rather than a comprehensive one.

**All three points are upheld. Rounds 1–2 reached a wrong conclusion, and this document records what
changed the answer rather than quietly replacing it.**

## What rounds 1–2 got wrong, and why

Round 2 concluded: *"the pinned engine's grammar parses exactly six statement kinds and its enumerator
ships no set algebra, therefore the remaining operators are set-level operations over results, and
adopting them means PIB building a calculus layer."*

That was derived from **one surface** — a Sprint-2 parser grammar file — and generalised to the whole
framework. It is exactly the failure the discipline names: a narrow check mistaken for a sufficient
one, and a non-existence claim ("the engine cannot do X") resting on a single narrow probe.

Read comprehensively, the framework ships:

- an **operator implementation properties** file, and
- **twelve SHACL-AF rule shapes** implementing the full operator specification — optional, exclusive,
  or, dependency, **addition, division, intersection, repetition, cartesian (three layers), and the
  subtraction/inverse purge** — described in the file itself as "real implementation ... not a
  proposal, ships alongside tested SHACL-AF rules," with a named test suite.

So the operators are **already executable**, ontology-natively. PIB is already an RDF/SHACL package
running pySHACL. **No calculus layer needed to be built: it already exists and PIB can run it today.**

## Proven by running the framework's own rules, unmodified, on PIB data

Round 3's probe loads the shipped rules and properties files as-is and runs them over PIB-shaped data
with `advanced=True, inplace=True, inference="none"` — the exact configuration the rules file
prescribes. Every result below is computed:

| Test | Result |
|---|---|
| **k-of-n**: at most two of four measurement facets may feed the grader | three selected → violated **True**; two selected → violated **False** |
| **Intersection**: capabilities jointly present across two profiles | result members computed correctly; a non-co-occurring capability correctly excluded |
| **Subtraction / inverse**: exclude grader self-measurement before emission | inverse-marked member **purged**, remaining three emitted |
| **Cartesian with pruning**: pair measurement sources with grading modes | the source excluding every partner **pruned**; survivors passed into pairing |

## The point that actually answers the challenge: expression construction

The k-of-n test is the one that matters. **The six variability operators cannot express "at most two of
four"**: exclusive means at most *one*, or means at least *one*, and mandatory, optional and dependency
say nothing about a count. The framework expresses it anyway — by **composing** the repetition operator
with a contributes-to grouping, which its own definition describes as "real composition ... not new
algebra."

That is the owner's point demonstrated rather than conceded: the operators are **constructors in an
expression language**, not a menu of fixed features. The framework carries the machinery for this
directly — operand and inner-operator links for nesting, operator precedence and symbols for concrete
syntax, arity, and algebraic laws (commutativity, associativity, identity elements) that license
rewriting and simplification. Its cartesian scaffolding classes say so explicitly: "generic by design,
matching the operator's own domain-agnostic thesis definition, **not tied to one use case**." They were
built for a consumer such as PIB to instantiate.

## Why PIB ended up with six — the real reason, and it is not a principled one

Comparing the two ontology copies the framework ships, operator class by operator class:

- the **core** ontology declares seventeen operator classes (twelve concrete);
- the **runtime** ontology declares seven — the six variability operators plus their superclass.

Every operator class diverges between them. The runtime copy is the **older generation**, and it is the
generation the pinned Python engine implements — which is why its grammar parses exactly six statement
kinds.

**PIB's six operators are an artifact of pinning that older engine generation, not a scope decision at
all.** Neither the categorisation argument of two rounds ago nor the calculus-layer argument of one
round ago was the real explanation.

## Correction owed on an earlier finding of mine

An earlier note from this session told the framework's own session that the
variability/algebraic/structural grouping "is asserted nowhere — all three grouping classes have zero
subclasses." **That overstated the case and is corrected.** The grouping *is* asserted — in the runtime
ontology, where the six variability operators do declare their superclass. The finding I should have
filed is the sharper one: the two copies share one namespace and diverge systematically, so which
axioms hold depends on which file a consumer loads. A correction has been filed to that session's inbox.

That is the same multi-source failure twice in one line of work, found by re-checking rather than by any
gate. Recorded plainly, not filed away.

## Recommendation, and what remains the owner's to rule

The evidence now supports **adopting the full operator set** and running the framework's shipped rules
directly, rather than importing six. Two consequences are derivable rather than matters of taste:

- the engine pin needs revisiting — PIB pins the older generation by hash, and the operators live in the
  newer one plus its rules files;
- adopting costs PIB no new algebra implementation, only vocabulary and a rule-execution step.

Still genuine stipulations, so still the owner's call and not enforced here:

1. Whether PIB models operator **expressions** (nested operand trees) or only flat operator applications.
2. Whether the rules are executed inside PIB's gate run or requested from the framework's session.
3. Whether adoption is staged (intersection, subtraction, cartesian, k-of-n first) or complete.

The governed vocabulary in this package is therefore **unchanged** pending that ruling.

## Reproducing

```bash
python3 10-experiments/probe_round3_shipped_operator_rules_v1_0_0.py
```
