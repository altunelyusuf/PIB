# Safe profile management — the architecture, its rules, and how each is enforced

**Status:** current. **Introduced:** PIB v2.13.0, 2026-09-23.
Derived from the variant algebra's own operator semantics, not from a convention invented here.

## The one definition everything follows from

The algebra defines its mandatory operator as: **the feature must appear in every variant.**

That is the whole architecture in a sentence. A requirement true of *every* variant is a claim about the
**domain**; a requirement true of *one* variant describes that **variant**. Where a rule belongs is not a
matter of taste or of remembering to annotate — it follows from what the rule says.

## Two layers

| Layer | Holds | Operators that belong here | Binds |
|---|---|---|---|
| **Meta** — the domain | what an artifact must satisfy to be an artifact of this domain at all | **mandatory** (and domain invariants) | every variant |
| **Profile** — the variant | what makes this variant the particular thing it is | optional, exclusive, or, dependency, repetition | only artifacts declaring that profile |

The choice operators are meaningless as domain-wide claims: "at most one scoring route" is a statement
about one variant's shape, not about the domain. That asymmetry is why mandatory rises and the rest stay.

## The enforcement rules

**E0 — Scope follows the rule's home.** A rule declared by a profile is local to it, always; a rule owned
by no profile is domain-general. Generality is a property of where a rule lives, never a default that
silence selects. *Enforced by* `profile_scoped_validate_v1_0_0.py`, which evaluates each artifact against
the general rules plus its own profile's, and never another variant's.

**E1 — A meta rule must not reject a legal variant.** Each profile's admissible variants are enumerated
from its own constraints, then again with the meta constraints folded in. If the capacity drops, the
domain layer is rejecting variants a profile declares legal. *Enforced by*
`profile_architecture_check_v1_0_0.py`. This is a failure, not a warning: either the rule is not general
or the profile is not legal, and someone must decide which. Measured on the shipped fixture, a rule true
of one variant and wrongly placed at the meta layer rejected **3 of 6** legal variants of the other.

**E2 — A requirement true of every variant belongs at meta.** A feature every profile mandates, which the
meta layer does not, is the same requirement restated once per profile. Reported as a **lift**, not a
failure: it is correct today and fragile tomorrow, because restated requirements drift — one copy is
updated, the others are not, and a later variant inherits the stale one. That is not hypothetical; it is
what a consuming session reported after a profile-derived expectation propagated into a live lineage.

**E3 — A profile-local rule is never evaluated outside its home.** The complement of E1: E1 stops the
domain over-reaching, E3 stops one variant's rules reaching another. *Enforced by* the scoped validator;
measured, applying every rule to everything invalidated **4** artifacts of which **2 were legal**, while
scoping left exactly the 2 genuinely faulty ones.

**E4 — What a validator applies is exactly: the general rules, plus the artifact's own profile's rules.**
Nothing else is in scope for that artifact, ever.

## What is deliberately not enforced

Whether a rule *should* be general. That is a modelling judgement about meaning, and no tool can make it.
What the tools do is narrower and answerable: report where the **spaces disagree with where the rules
currently live** — a domain rule that rejects legal variants, or a variant requirement that every variant
shares. Both are facts about the graph; the decision they prompt stays with the modeller.

## Running it

```bash
python3 03-tooling/profile_architecture_check_v1_0_0.py [spaces.ttl]   # E1, E2
python3 03-tooling/profile_scoped_validate_v1_0_0.py <data> <shapes>   # E0, E3, E4
```

Both are proven discriminating: each passes a correct fixture and fails a fixture broken in exactly one
way — a mandatory rule misplaced at meta, and a requirement restated by every variant.
