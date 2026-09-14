# Proposal to the VAF lineage (altunelyusuf/VAF)

**From:** pib-vaf academic paper session (altunelyusuf/Ontologies-adjacent work, paper "An Algebraic Solution for Variation Management in Ontologies")
**To:** altunelyusuf/VAF — filed in **VAF's own** `07-handover-inbox/pending/`, per the same convention used by the prior `PROPOSAL_vaf-agentic-pipeline_...` handover already in this inbox.
**Date:** 2026-09-14
**Status:** proposal only. Nothing in VAF was modified from this side (cross-session scope, per B1).

---

## Finding 1 — `va:MandatoryOperator`'s type declaration is inconsistent with its own eleven siblings

Checked directly in `01-ontologies/variant_algebra_v3_2_6.ttl`. Eleven of the twelve concrete operator
classes use a consistent multi-type pattern, declaring both `va:Operator` and their family tag
(`va:VariabilityOperator` or `va:AlgebraicOperator`) simultaneously:

```turtle
va:OptionalOperator a va:Operator, va:VariabilityOperator, owl:Class, owl:NamedIndividual ;
va:AdditionOperator a va:AlgebraicOperator, va:Operator, owl:Class, owl:NamedIndividual ;
```

`va:MandatoryOperator` alone breaks this pattern:

```turtle
va:MandatoryOperator a owl:Class ;
    ...
    rdfs:subClassOf va:Operator ;
```

No family tag at all, and `va:Operator` membership expressed via `rdfs:subClassOf` rather than the
multi-type pattern every sibling uses.

**Consequence downstream, disclosed rather than assumed:** any query filtering on
`?x a va:VariabilityOperator` returns five of the six variability operators, silently omitting
Mandatory. A query filtering on `?x a va:Operator` directly still finds all twelve, but only if it
does not also rely on multi-typing to find the family tag. This is a plausible, partial explanation
for count discrepancies observed downstream (Finding 2 below), though not a complete one.

**Proposed:** align `va:MandatoryOperator`'s declaration to the same multi-type pattern as its eleven
siblings — `va:MandatoryOperator a va:Operator, va:VariabilityOperator, owl:Class, owl:NamedIndividual`
— as a PATCH-level fix (no vocabulary change, per BP-D7).

## Finding 2 — An unresolved count discrepancy this session could not reconcile, flagged rather than guessed at

Direct enumeration of `?x a/rdfs:subClassOf va:Operator`-pattern classes across
`variant_algebra_v3_2_6.ttl`, `variant_algebra_v3_extension_v0_3_2.ttl`, and
`variant_algebra_v3_operator_properties_v1_0_0.ttl` (the three files this session could identify as
operator-relevant via the manifest and code search) finds **twelve concrete operator classes**: six
tagged `va:VariabilityOperator` (Mandatory, Optional, Exclusive, Or, Dependency, Repetition) and six
tagged `va:AlgebraicOperator` (Addition, Subtraction, Intersection, Cartesian, Division, Inverse).

This session's own earlier work (the paper under development) had been using only the six
`VariabilityOperator` members, treating them as VAF's complete operator set — an error, corrected
mid-session once the `AlgebraicOperator` family was found.

**However**, this count of twelve does not reconcile with a prior, separate session's own already-filed
proposal in this same inbox (`PROPOSAL_vaf-agentic-pipeline_to_VAF_quality-wiring-and-semantic-calculi_v1_0_0.md`,
Finding 3), which reports a SPARQL query over `operatorSymbol` returning *"17 rows for 16 distinct
operator classes."* This session found zero live `operatorSymbol` value assertions in any of the three
files checked (only the property's own `owl:DatatypeProperty` declaration), and did not load the full
33-file corpus that proposal references.

**This session is not the owner of this artifact and is not positioned to adjudicate which count is
current** — the other proposal may predate a consolidation, or this session's three-file check may be
incomplete relative to the full corpus. Both are real possibilities, and guessing between them would
violate the same evidentiary standard this proposal itself argues for.

**Proposed:** the owning session re-run a full-corpus enumeration (all 33 files, not a sample) of
`?x a va:Operator` (direct and via subclass closure) and separately of every subject carrying
`va:operatorSymbol`, and reconcile the two prior counts (12 here, 16 previously) against that result,
recording whichever count is current in the release history so future sessions do not re-derive it
from scratch.

## Finding 3 — The `AlgebraicOperator` / `VariabilityOperator` split itself is worth a second look, raised by the paper's own author

Raised directly by the person this session is writing the paper for, and independently supported by
what the ontology already asserts: every operator (with the Finding-1 exception) is tagged with
**both** `va:Operator` and its family tag simultaneously, not with the family tag alone. This means
the ontology's own structure already treats `va:Operator` as the one category every operator
unconditionally belongs to, with the family tags functioning as a secondary, descriptive grouping
layered on top — not a partition and not a ranking.

**The risk named, concretely:** a consumer (human or agent) that encounters `va:VariabilityOperator`
before noticing it is one of two co-equal tags, rather than the complete operator category, will
undercount — exactly what happened in this session before Finding 2 above was found. The type-signature
distinction the two families draw (presence-constraints vs. set-transformations) still has real value
for a consumer choosing which operator to use, so this proposal does not suggest removing the family
tags. It suggests that any documentation, README, or query pattern presenting `AlgebraicOperator` or
`VariabilityOperator` should state plainly, in the same sentence, that both are subsets of the one real
category `va:Operator`, to close off the undercounting failure mode at the documentation level rather
than only at the query level.

**Proposed:** no ontology change beyond Finding 1. A documentation note (e.g. in `04-documentation/README.md`
or wherever the operator families are first introduced to a new reader) stating the co-equal,
non-partitioning relationship explicitly.
