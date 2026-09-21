# PIB Handover Inbox Log

Plain text, not RDF — deliberately. This tracks "has this been looked at, and with what outcome,"
which is bookkeeping, not domain knowledge. One line of history per item is enough to stop a future
session re-reading something already decided.

**How this works.** `pending/` holds anything not yet reviewed, and is checked at PIB session start
as a standing ceremony step. On review the file moves to `accepted/`, `rejected/` or `deferred/`,
and a line is added below. Nothing arrives automatically — an item is placed here by the owner, or
archived here by a session that received it elsewhere.

**Direction.** A proposal arriving *at* PIB belongs here. A proposal PIB sends *to* another package
goes into that package's own inbox, where one exists, not only into PIB's documentation for the
other session to find by chance.

**Every disposition line states the verification actually performed** — the disposition is itself an
externally-verifiable claim, not a summary of how persuasive the proposal read.

| Item | Source | Disposition | Release | Verification actually performed |
|---|---|---|---|---|
| `PROPOSAL_backlog-roadmap-framework_to_pib-hub_vaf-operator-count-unverifiable_v1_0_0.md` | backlog & roadmap framework session, 2026-09-17 | **accepted** | PIB v1.5.0 | Asked whether PIB declaring five variability operators against the variant-algebra engine's twelve was a deliberate subset or a gap. Both figures re-derived directly this session, not taken on report: cloned the engine's repository with authenticated git access and parsed its core ontology (`variant_algebra_v3_2_6.ttl`) — twelve concrete operator classes confirmed, matching the proposal's corrected count. The engine's own class definitions partition those twelve by role, scoping its variability family to exactly Mandatory, Optional, Exclusive, Or, Dependency and Repetition; PIB's subset is therefore principled and evidence-backed, not a preference. The proposal's count of five was correct and exposed a real defect: PIB's integration-interface vocabulary has always stated it governs those six, but only five individuals were declared — **Repetition was missing**. Added in v1.5.0; declared set now six, matching both PIB's own prose and the engine's family. Classified a genuine gap, not a safeguard working: no PIB gate checks operator individuals against the vocabulary's prose, so it would have persisted undetected. Findings on the engine's own ontology (prose-only grouping; one operator with no superclass) were filed to that package's inbox rather than fixed here, since PIB does not own it. |
| `HANDOVER_OE_to_PIB_dependency-shape-changed-since-registration_v1_0_0.md` | OEE governance session, 2026-09-21 | **accepted** | PIB v2.0.3 | Each factual claim checked against the bytes before disposition. (1) The engine environment variable has no references in any tooling script or top-level document — true as scoped; the remaining mentions are historical records, the pin file, and reference probes. (2) The two-step shift — vendored rules first, then calculation moved into the ontology at v2.0.0 — is recorded in both addenda of the pin file. (3) The registration closed at pack v20.23.4 with standard criticality and no gateable items — confirmed from PIB's own registration status. (4) The pack version stated was accurate when filed; it has since moved to v20.74.0. Beyond the handover: comparing the registered file records with today's files shows one of three registered files superseded and two governed ontologies shipped since that were never registered. Answer to the question asked: the stated basis for standard criticality — design-time scaffolding rather than a component that computes — no longer holds, since PIB now performs its own calculations and is publicly consumed; the choice of level is a stipulation, taken to the owner rather than decided here. A fresh registration round is warranted by OE's own maintenance threshold, a major version change since registration. Correction filed to OE: its registry records PIB as unversioned at closure, but the registered submission itself states v1.2.1. Separately, while answering the handover's third point, found the algebra had retired the properties file PIB vendors by consolidating it; re-vendored after verifying the replacement is a strict superset. |

