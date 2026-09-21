# REFERENCE_ONLY — NOT_A_RELEASE — criticality test-drive for PIB: standard versus high

**Question from the owner:** is there a methodology for deciding PIB's criticality level for its fresh
registration round, and if not, a test-drive analysis to decide it.

## Is there a methodology? No criteria exist; a method for forks does

Checked across the prose documents, the vocabulary and shapes, and the tooling — not one query:

- **No criteria for choosing a level exist anywhere in OE.** The core vocabulary defines criticality as
  "how much process rigor its context demands" and gives four levels with one-line descriptions —
  low, standard ("default rigor for ordinary components"), high ("elevated rigor; substantial process
  evidence required"), critical ("maximal rigor … safety/business critical") — with no threshold
  between them. The shapes only *consume* the declared level; the registration protocol only says the
  registrant *declares* it. **No registrant has ever declared high or critical** outside test fixtures.
- **A method for this kind of fork does exist, but only as a named practice.** The registration protocol
  says to "test-drive alternatives where it settles the choice (the A/B method)," and the four
  criticality gates were themselves built with a three-case pattern. OE deliberately never recorded it
  as a separate rule, judging it an application of existing ones.

This analysis applies that method.

## What the level actually controls

Four gates, one per facet, each silent below high and identical at high and critical:

| Facet | At high or critical, every registered … must … |
|---|---|
| Risk | identified risk — carry a mitigation or a risk treatment |
| Performance | performance test of the artifact — carry a measured result |
| Testing | test of the artifact — carry a result |
| Configuration | change to the artifact — satisfy an acceptance criterion |

They check the completeness of what is **registered**, not whether any process happened. Critical adds
nothing over high for these gates.

## PIB's real evidence — re-derived this session, nothing invented

- **Tests:** four, all re-run and passing — capacity self-test, operator expression gate self-test,
  invariants over the full package, manifest self-verification.
- **Performance:** capacity computation over the consolidated profile spaces, median **20,508 ms** over
  three timed runs (spread under 100 ms).
- **Changes:** all **twelve** tagged releases record a passing gate result in their own manifest. Checked
  by reading each one — a pattern check first misreported v1.4.0, which abbreviates its result.
- **Risks:** five, with only the treatments actually recorded in the repository:

| Risk | Treatment on record |
|---|---|
| The ZeroTime profile is blocked by an upstream library that is logically inconsistent as shipped | deferred by owner decision |
| Vendored operator rules can drift from the algebra's own current files | hash-pinned copies, verified re-vendor procedure |
| The fixpoint iteration lives in the harness, not the ontology | **none** — accepted by the owner in conversation, never written down |
| The registration record no longer matches the files PIB ships | fresh registration round |
| Capacity computation cost grows with the candidate count, which doubles per feature | **none** — the loop bound in the harness guarantees termination, not cost |

## Results — OE's own shipped shapes, unmodified

pySHACL, advanced mode, no inference; each facet's full suite over the registration data plus the core
and facet vocabularies.

| Scenario | Standard | High |
|---|---|---|
| Nothing registered but the level | PASS | PASS |
| **PIB's real evidence, as documented today** | **PASS** | **FAIL — risk gate** |
| Real evidence + the two missing treatments | PASS | PASS |
| Teeth check: real evidence + one test with no result | — | FAIL — risk and testing gates |

## What the test-drive settles

1. **The level on its own proves nothing.** Declaring high while registering nothing passes every gate.
   High is worth only as much as the evidence registered under it.
2. **PIB already meets high on three of four facets.** Its tests, performance measurement and every
   release are complete as they stand.
3. **The entire cost of high, today, is two risk treatments.** One is already decided and only needs
   writing down — your acceptance of the harness loop. The other is a genuine new decision: what to do
   about the growth of capacity-computation cost.
4. **The analysis surfaced a real risk nobody had measured.** Twenty seconds for two small spaces, with
   candidates doubling per feature, means the ontology-native calculation will not stay practical as
   profiles grow. Standard would never have asked about it.

## What it does not settle — still the owner's decision

The definitions give no threshold, so whether PIB's context now demands elevated rigor is a
stipulation. What is fact: the stated reason PIB chose standard — design-time scaffolding rather than a
component that computes — is no longer true; PIB now computes, and it is public for external academic
and industrial projects to consume.

**Recommendation, offered as a proposal:** high. The cost is measured and small, three facets already
comply, and the one remaining obligation forces a decision PIB needs anyway. High turns completeness into
a standing obligation for every future risk, test, measurement and release — which is what a publicly
consumed, computing component should carry.

## Two findings about the gates themselves, filed to OE

- The gates check completeness of registered items only, so high with nothing registered passes — OE
  had already noted this from PIB's first round; the test-drive reproduces it.
- The gates report **once per artifact, naming only the artifact**. One untreated risk and five produce
  the identical report, so neither the registrant nor the reviewer can see which item failed or whether
  a fix made progress.

## Reproducing

```bash
python3 10-experiments/probe_criticality_ab_test_drive_v1_0_0.py <path-to-oe-pack> <median-ms>
```
