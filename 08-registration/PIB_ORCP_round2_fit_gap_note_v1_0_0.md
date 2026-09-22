# PIB — ORCP round two: submission and fit-gap note v1.0.0

**Registrant:** PIB (public, `https://github.com/altunelyusuf/PIB`) · **To:** OEE governance
**Protocol:** ORCP v1.0.0 · **Discipline:** OE Operating Discipline v2.11.1 · **Governance source:**
`knowledge_base_abox_v2_30_0.ttl` · **Round-one baseline:** v1.2.1 (files kept unchanged in this folder)
· **Package at submission:** PIB v2.3.0

**Why this round:** OE's registration-maintenance check flags PIB (1.2.1 → 2.2.0, a major change); OE
accepted PIB's reply confirming a fresh round was warranted. The owner has since ruled on criticality.

## The criticality decision

**Declared: high.** Owner's decision, 2026-09-21. The round-one basis for standard — design-time
scaffolding rather than a component that computes — no longer holds: PIB now computes variation capacity
entirely in the ontology and is public for external academic and industrial use. The choice was informed
by an A/B test-drive against OE's own gates (`10-experiments/FINDINGS_criticality_ab_test_drive_v1_0_0.md`),
which showed high would cost exactly two recorded risk treatments; both are recorded in this round.

## Phase A — classification against the recorded roster (strategy v1.2.0, 12 live facets)

| Facet | PIB's relationship this round | Basis |
|---|---|---|
| core | conformance | PIB is a core artifact, declared at high criticality |
| release history | registration + conformance | the PIB subject and its five current governed ontology files |
| risk | registration + conformance | one risk assessment, six identified risks, each with a recorded mitigation or treatment |
| testing | registration + conformance | four tests, each with a result |
| performance | registration + conformance | one performance test with a measured median |
| configuration | registration + conformance | sixteen releases, each satisfying a recorded acceptance criterion |
| measurement | deferred | no metric exists for variation capacity; minting one would breach "propose, don't mint" |
| quality | deferred | grading is PAMG's, not PIB's; PIB holds no quality assessments of itself |
| reliability | deferred | PIB holds no reliability evidence of its own |
| knowledge base | none this round | PIB's one lesson already went through OE's inbox and was accepted |
| ae, meta | none | internal facets |

## Phase B — what is emitted (`pib_orcp_submission_v2_0_0.ttl`, 178 triples)

Built by `build_pib_orcp_submission_v2_0_0.py` from PIB's own files and git tags. Every anchor and hook is
central; all 47 minted individuals are in PIB's registrant namespace, as OE accepted in round one.

- **Release history.** Five current files with their SHA-256: the profile vocabulary (1.0.0.1), the
  integration-interface vocabulary (1.0.0.2), the wiring composition (1.0.0), the assessment profiles
  (1.1.0.1) and the wiring expressions (1.0.0). The integration-interface vocabulary superseded the file
  registered in round one; that round-one record is restated with its **registered** hash and linked as the
  prior version of its successor. The worked capstone example is illustrative and, as in round one, not
  registered.
- **Risk.** Six identified risks — the blocked ZeroTime profile (deferred by owner decision), drift of the
  vendored operator rules (hash pins plus a verified re-vendor procedure, already exercised once), the
  fixpoint loop living in the harness (**accepted by the owner on 2026-09-17 — first recorded here**), the
  stale registration record (treated by this round), capacity-computation cost (pruning, frontier targeting
  and partitioning; median 20.5 s → 4.5 s on the profile spaces), and dependence on engine-specific SHACL
  evaluation behaviour, which produced a silent zero during development (an eight-space known-answer
  self-test plus a planted inadmissible candidate, run before every release).
- **Testing.** Four tests, re-run on 2026-09-21 and passing: the capacity self-test, the operator expression
  gate self-test, the invariants over the full package, and manifest self-verification.
- **Performance.** Capacity computation over the profile spaces: median **4,466 ms** of three timed runs.
- **Configuration.** One change operation per tagged release, v1.4.0 through v2.2.1. Each satisfies the
  criterion "release gates re-run and passing, recorded in the release's own manifest" — derived by the
  builder reading each tag. All sixteen qualify; two whose first pattern match was descriptive were checked
  by reading their manifests directly. Version 1.3.0 existed only as a file delivered during a session and
  never reached a remote OE could check, so it is not registered.

## Validation — scope disclosure

pySHACL 0.40.1, advanced mode, **inference off**, each facet's **full** governing suite (not only its gate),
over the submission merged with the core vocabulary and ABox and that facet's own vocabulary:

| Suite | Violations |
|---|---|
| core 1.8.0 | 0 (1 advisory Info) |
| release history 1.4.0 | 0 |
| risk 3.3.0 | 0 |
| performance 1.5.0 | 0 |
| testing 1.1.0 | 0 |
| configuration 1.1.0 | 0 |

**The high-criticality gates were shown to engage, not pass vacuously.** Removing the owner's acceptance of
the harness loop fails the risk gate; removing the cost mitigation fails the risk gate; removing one test
result fails the testing gate. The unmodified submission passes all three.

## Gaps found

**None new this round.** Two findings from the test-drive — no criteria exist for choosing a criticality
level, and the criticality gates report once per artifact rather than per failing item — are already
pending in OE's inbox and are not repeated here.

## For OE (Phases C–F)

Re-derive rather than trust: the file hashes against PIB's public repository, the six suite runs, and the
release list from the public tags. The bundle stays in PIB's own repository, per OE's current guidance to
registrants; `BUNDLE_MANIFEST_round2_v1_0_0.txt` pins the three bundle files.
