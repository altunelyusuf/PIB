# REFERENCE_ONLY — findings: reducing the cost of PIB's ontology-native capacity computation

**Question from the owner:** is there any way to reduce the cost of computing Variation Capacity, which
the criticality test-drive measured at a median 20.5 s for two small spaces?

**Short answer: yes — two ways, one adopted, one proven but not yet built in the ontology.**

## Where the time went (measured, not guessed)

- The **final pass cost the most (8.6 s) and changed nothing** — it only confirmed the graph had stopped
  growing.
- **Branching dominated** each pass (4.0 s over the final graph): it re-fired on every candidate, every
  pass, including ones already branched.
- The five admissibility checks ran on **every** pass, though they only matter once candidates are complete.
- **Nothing was pruned**, so candidates grew to 2ⁿ.

## Each technique measured on its own — every variant required to reproduce 9 and 1

| Variant | Time | Candidates | Same answers |
|---|---|---|---|
| Current rules — everything, every pass | 21.5 s | 142 | yes |
| + checks run once, after generation | 17.3 s | 142 | yes |
| + branch once, inherit atomically | **34.3 s — slower** | 142 | yes |
| + prune branches that already break a constraint | 10.8 s | 27 | yes |
| + engine visits only the frontier | **4.7 s** | 27 | yes |

One hypothesis was wrong and is kept on record: "branch once" made things slower, because the rule engine
still runs every rule's query for every candidate before the skip condition is reached. The saving came
only once the engine was told to visit the frontier and nothing else.

## Scaling — the question that actually matters

Built from independent groups whose true capacity is exactly 3ᵏ:

| Features | True capacity | Current rules | Pruning + frontier | **Partitioned** |
|---|---|---|---|---|
| 4 | 9 | 4.1 s | 2.7 s | 1.4 s |
| 6 | 27 | 16.4 s | 8.5 s | 1.9 s |
| 8 | 81 | — | 27.9 s | 2.5 s |
| 10 | 243 | — | over 70 s | 3.0 s |
| 20 | 59,049 | — | — | **5.7 s** |

- The current rules grow about **fourfold per group**; pruning brings it to about **threefold** — tracking the
  true admissible count. Pruning lowers the base; growth stays exponential whenever admissible wirings
  multiply across independent groups.
- **Partitioning changes the curve to linear**: enumerate each independent group on its own, then combine the
  counts. Twenty features and 59,049 admissible wirings, from 60 candidates in under six seconds.

## Correctness of pruning — checked beyond the two real spaces

Pruning is dangerous if wrong: it can discard valid wirings silently. Every constraint path was tested
against the unpruned rules as reference, and against hand combinatorics:

| Targeted space | Unpruned reference | Pruned | By hand |
|---|---|---|---|
| At most 2 of 4 (budget) | 11 | 11 | 1 + 4 + 6 = 11 |
| Dependency with a later prerequisite | 6 | 6 | 8 − 2 = 6 |
| Or-group with spread members | 12 | 12 | 16 − 4 = 12 |
| All constraint kinds combined | 3 | 3 | — |

No inadmissible candidate survived pruning in any space.

## What was adopted — PIB v2.1.0

Pruning, atomic inheritance and frontier targeting are now the governed enumeration rules (v2.0.0), and the
harness runs them in two phases that each rule shape declares itself. Same answers; 21.5 s → 4.7 s.

Two design points, because they are correctness matters rather than speed:
- **Inheritance is atomic** — a successor is created together with all its parent's selections. Pruning reads
  those selections; reading them before they are complete would discard valid wirings without any error.
- **Frontier tests are per branch** — if both branches shared one test, the first to run would hide the
  candidate from the second.

With pruning exact, the admissibility checks never reject anything in a normal run, so a normal run can no
longer show they still work. The self-test therefore plants one inadmissible candidate and requires the
checks to reject it.

## What is not built yet — partitioning in the ontology

The partitioned figures above required declaring the groups by hand and multiplying the counts in the
harness. A fully ontology-native version needs two things the rules don't yet do: **find the independent
groups** from which features share a constraint (the algebra's own backend does exactly this), and
**combine their counts** — SPARQL has no product aggregate, so that would be a running-product rule.

## Consequence for the open criticality decision

The unrecorded cost risk now has a real treatment available rather than only a feature limit: pruning is
adopted, and partitioning would make cost grow with the number of independent groups rather than
exponentially with features. Exponential growth would then remain only inside a single tightly-coupled group.

---

## Appended 2026-09-21 (PIB v2.2.0) — partitioning built into the ontology

Built as proposed above, and adopted. Enumeration rules v2.1.0 add two phases around generation and checking:
**partition** (couple features that share a constraint; group each feature under the lowest index it reaches
through couplings; scope each constraint to its group) and **combine** (count each group's admissible
selections, zero included; multiply along the group order with a running product; record the space's
capacity). The harness now only reads the capacity from the graph.

**Fully ontology-native scaling** — groups found and counts multiplied by the rules, nothing declared by hand:

| Features | True capacity | Before partitioning | Now | Candidates |
|---|---|---|---|---|
| 4 | 9 | 2.7 s | 2.6 s | 6 |
| 10 | 243 | over 70 s | 6.2 s | 15 |
| 20 | 59,049 | impractical | 15.5 s | 30 |
| 40 | 3,486,784,401 | impractical | 58.0 s | 60 |

Growth is now roughly **quadratic in the number of independent groups**, not exponential in features: the
running product needs one pass per group and each pass revisits every group. Building the product as a tree
rather than a chain would reduce that further; it is not needed at current profile sizes.

**PIB's one deliberate difference from the algebra's decomposition, and proof it matters.** The algebra treats
repetition as binding a single feature and adds no coupling for it. PIB's repetition is a budget shared by
several contributors, so here those contributors are coupled. With that coupling removed — following the
algebra's rule literally — the budget case "at most 2 of 4" returns **16 instead of 11, with no error**. It is
now a permanent case in the capacity self-test.

**Two defects in my own build were caught before release:**
- The group rule excluded group spaces with a filter placed inside an aggregate subquery, where the current
  node is not bound — so the exclusion did nothing, every group was marked partitioned, and nothing was
  generated. The result was a capacity of **0 with no error**. Fixed by excluding groups at the rule's target.
- The self-test's exactness check assumed complete candidates equal the capacity, true only while every
  candidate was a whole wiring. With partitioning they legitimately differ (the capstone needs 7 candidates
  for a capacity of 9). Replaced by checking the property that actually matters — no inadmissible candidate
  survives — measured directly as the rejected count.

**Self-test now covers eight spaces**, all reproducing their known capacities: the two profile spaces, plus
six conformance cases — budget, later prerequisite, spread or-group, all constraints combined, five
independent groups (243), and an unsatisfiable group whose zero must make the whole product zero rather than
be skipped. It demonstrably fails when the budget case expects the wrong answer.
