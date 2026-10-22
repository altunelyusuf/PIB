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

---

## The taxonomy — how taxonomic entries arise from the relationships (added v2.14.0)

The profile taxonomy is **not authored and not generated a second time**. The enumeration already builds
the branch tree: every candidate records the parent it came from and the feature it decided. The taxonomy
phase reads that structure and expresses it taxonomically — interior nodes are partial commitments (a
genus), leaves are complete variants (a species).

### What each relationship contributes

| Relationship | Taxonomic effect | Why |
|---|---|---|
| **Mandatory, at meta** | **no entry** | the feature is in every variant, so it characterises the *root* and distinguishes nothing below it — the structural reason mandatory belongs at the meta layer |
| **Mandatory, inside a profile** | **no branch; a forced decision** | the "leaves it" side is pruned, leaving one child taxonomically identical to its parent |
| **Optional** | **two entries** — takes / leaves | disjoint and jointly covering the parent |
| **Exclusive {a, b}** (PIB: *at most one*) | **three entries** — a, b, neither | at most one may be taken, so two members yield three mutually disjoint leaves |
| **Exclusive, the algebra's own** (*exactly one*) | **two entries** — a, b | the algebra's `exclusive { a \| b }` requires one member, so the "neither" branch does not exist |
| **Or {a, b}** | **three entries** — a, b, both | at least one must be taken, so the "neither" branch is pruned |
| **Dependency a → b** | **no entry of its own** | it *prunes* branches that take a without b |
| **Repetition (k-of-n)** | **no entry of its own** | it prunes branches exceeding the budget |
| **Independent groups** | **separate dimensions**, not one tree | groups combine by product; presenting them as a single tree would misstate the space |

Two structural facts follow, and both are materialised:

- **Siblings are disjoint by construction** — one takes the feature the other leaves. Nothing needs to
  assert it; it is what branching *is*.
- **A single surviving child is recorded as a forced decision, not drawn as a fork.** A taxonomy that
  shows a choice where none exists misleads a reader about the space, which is the whole point of having
  one.

### Worked: the capstone

Three independent dimensions, whose product is the capacity:

```
dimension 1 (two mandatory edges)   takes f1 [forced] → takes f2 [forced]              → 1 variant
dimension 2 (exclusive measurer)    takes f3 → leaves f4 [forced]                      → 3 variants
                                    leaves f3 → takes f4 | leaves f4
dimension 3 (or: analysis/design)   takes f5 → takes f6 | leaves f6                    → 3 variants
                                    leaves f5 → takes f6 [forced]
```

1 × 3 × 3 = **9**, the capstone's published capacity, reached independently of the counting path. The
mandatory pair contributes **no branches at all** — it is domain structure, not variation, which is
exactly what the architecture predicts.

### Running it

```bash
python3 03-tooling/profile_taxonomy_v1_0_0.py <spaces.ttl> [space-name]
```

Proven per operator: optional yields 2 leaves, mandatory 1 with a forced decision, exclusive 3, or 3, and
dependency adds no branch while pruning to 3.

### Checked against the algebra, not against PIB's own expectations (v2.15.0)

The branch shapes above were first verified against expectations PIB wrote for itself, which proves
self-consistency and nothing about meaning. They are now checked against the **algebra's own enumerator**:
the same expression is enumerated by the algebra and by PIB, and the two sets of selections — not their
counts — must be equal. A count match with different members would otherwise pass falsely.

That check found a real defect the self-consistent tests could not. PIB's converter wrote PIB's
*at-most-one* exclusive as the algebra's `exclusive { a | b }`, which means *exactly one*: the outward
direction silently dropped the "neither" variant, and the inward direction silently added it. The faithful
forms are `atmost 1 of { … }` outward, and at-most-one plus at-least-one inward. Corrected, all seven
operator cases agree as sets, and every shipped space agrees on capacity with the algebra — capstone 9,
budget 11, five independent groups 243, unsatisfiable 0.

Run the converter's round trip with `VAF_SRC` set to the algebra's runtime; the conformance gate below
needs nothing outside this package.

### Conformance is checked against the algebra's LIVE ontology rules (v2.18.0)

The first conformance check used the algebra's **Python enumerator** as its oracle. That was the wrong
source of truth and was withdrawn: the calculus is implemented as ontology rules, and agreeing with a
second implementation proves agreement with a program rather than with the calculus other domains
consume. The second check used the algebra's **rules**, but the 1.x generation of them — which the
algebra quarantined on 2026-09-28. A pinned generation is invisible from inside the consumer, so the
check kept printing agreement for semantics its owner had withdrawn.

`03-tooling/algebra_conformance_check_v3_0_0.py` runs the algebra's **current** rules, vendored from its
live tree together with the algebra's own rule executor, and compares **variant sets element by element**
rather than per-candidate verdicts. The current rules do the whole job in the ontology: they build the
variation space, generate the candidates by branching with carry-over, decide every statement in each
candidate, and mark and count the variants.

Result across the shipped spaces: **eight spaces, eight sets identical, zero disagreements** — capstone
9, ontology-development 1, budget 11, later prerequisite 6, or-spread 12, combined 3, five independent
groups 243, unsatisfiable 0. Not merely equal counts: the same variants, member by member.

What changed in what this makes visible:

- **Mandatory is cross-checked at last.** The 1.x rules shipped no mandatory rule, so the previous check
  had to report mandatory as not cross-checked. The current rules enforce it — measured directly: one
  mandatory and one optional feature yield 2 variants, not 4. Every operator PIB uses is now decided by
  the algebra. Mandatory still sits at the meta layer here, for the reason that has not changed: it is a
  statement about every variant, not a choice within one.
- **At-most-one stays a budget of one.** PIB's exclusive means at most one and the algebra's exclusive
  operator means exactly one, so the exclusive is handed over as a budget of one — the same mapping the
  converter uses, and not a preference: written as the algebra's exclusive it drops the "neither" variant.
- **One divergence is deliberate on both sides.** The algebra refuses a component with no features; PIB
  marks an empty profile as possible drift and validates it rather than rejecting it, on the owner's
  ruling. The gate skips that space by name instead of recording a false disagreement.

The check is proven to discriminate in both directions on real data: one admissible candidate marked
inadmissible is caught (2 disagreements), and every budget of one loosened to two is caught (4). The first
draft of that self-test mutated the other way — unmarking an inadmissible candidate — and reported no
disagreement at all, because exact pruning means no complete candidate is ever marked inadmissible. A
mutation that cannot fire proves nothing, so the direction that exercises the filter is the one used.
