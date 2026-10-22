# RETIRED — `operator_rule_runner_v1_0_0.py`, and the adaptation it leaves open

**Retired in PIB v2.18.0 (2026-10-22). Removed. It passed on the day it was retired; that is not why it went.**

## Why it went

The runner executed the algebra's **1.x** operator rules over PIB's wiring-expression ontology and
reported which constraints each decided. Those rules were quarantined by their owner on 2026-09-28.
The runner could only keep reporting by keeping a retired generation pinned — a gate that still
prints `rules have teeth: True` while speaking for semantics its owner has withdrawn.

Re-pointing it at the algebra's current rules was tried first, not assumed impossible. It does not
work as PIB's expressions stand, and the reason is specific rather than general:

- The current rules evaluate a whole model rooted at a `va:Component`. PIB's expression ontology
  declares no component, so with the rules run over it unchanged, nothing targets anything: 111
  triples in, 8 added, no candidate and no truth value.
- Adding a component carrier that declares the features and the operator applications is not enough
  either — still zero variants. The current rules read an operator **typed directly** and carrying
  `va:members` (measured: a component with one such repetition and one exclusive yields three
  variants). PIB's applications instead carry `va:OperatorApplication` with `va:hasOperator` pointing
  at an operator individual, and the repetition application uses `va:appliesTo` on a group feature
  rather than `va:members`. The current rules give that form no reading.

## What covers the loss

`algebra_conformance_check_v3_0_0.py` exercises every operator PIB uses — mandatory, exclusive, or,
dependency and repetition — across eight variation spaces, comparing variant sets against the
algebra's current rules. That is more coverage than the runner's single wiring fixture, not less.
PIB's expression ontology keeps its own invariant gates (`pib_invariants_v1_0_0.ttl`, G1–G5).

## What stays open, stated rather than quietly dropped

PIB's wiring expressions are **not consumable by the algebra's current rules** in the form PIB
publishes them. Closing that means either giving the expressions the directly-typed, `va:members`
form the rules read, or asking the algebra whether the application form should be readable. The
measurement above is the evidence either conversation needs; it is filed to the algebra in
`09-handover-inbox/accepted/REPLY_PIB_to_VAF_live-rules-verified-two-findings_v1_0_0.md`, and it is
not treated as settled here.
