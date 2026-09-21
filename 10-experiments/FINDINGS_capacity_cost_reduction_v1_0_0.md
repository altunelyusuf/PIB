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
