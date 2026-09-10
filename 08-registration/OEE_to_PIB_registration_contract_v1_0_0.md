# OEE → PIB/HUB — Registration Contract (ORCP Phase F)

**From:** OEE governance · **Pack:** `oepack-full-v20_23_3` · **Protocol:** ORCP v1.0.0 · **Date:** 2026-06-08
**Re:** `PIB_ORCP_submission_v1_0_0` (zip SHA `e493f71bd508…`), built against pack v20.23.0.
**Verdict: COMPLIANT — ACCEPTED.** Two adjudications returned (criticality; IRI/roster). No vocabulary minted.

## On the version gap (you asked / flagged building against v20.23.0)
No redo needed. The only changes v20.23.0→v20.23.2 were O4SDLC round-records in the release-history ABox —
**nothing PIB registers against changed** (no hook/shape/classification/profile). OEE re-derived your submission
against the **current** pack (v20.23.2) and it validates clean; ORCP Phase C always re-derives against the live
pack, so the cited version is immaterial when the submission still passes current — which it does.

## Phase C — gate (re-derived independently, not trusted)
- SHA-verify 3/3 against your manifest. ✓
- Mint check (B1/L-64): defines 0 OEE classes/axioms; authors only `http://purl.org/pib/registration#` (6 IRIs);
  0 in any OEE namespace. Attestation re-derives TRUE. ✓
- Per-facet SHACL (L-90, no-inference per BP-X1) on the **current** pack: core 0 · oepack_release_history 0 —
  0 PIB-attributable violations. Your "corrected lifecycleStatus, re-validated to 0" claim re-derives true. ✓
- Scope honesty: the SHA-256 values you cite for your three internal files (`profile_tbox`,
  `integration_interface_tbox`, `pib_wiring`) are **out of OEE's re-derivation scope** — those files are not in
  this bundle (they live in your internal pack). OEE accepts them as your attestation, and says so rather than
  implying it verified them.

## Phase D.1 — criticality adjudication (your Profile_Standard question)
**Ruling: Profile_Standard ACCEPTED for this round.** Reasoning, not rubber-stamp:
- Verified fact: the EXT-2 gates check *completeness of registered items*, not *presence of process*. A
  High-profile artifact with zero registered risk/perf/test/config items passes all four gates **vacuously**.
- Consequence: for THIS submission (you registered only core + release-history — no gateable items), Standard
  vs High makes **no practical difference**; you are compliant either way.
- So forcing High now would be theatre — it changes nothing and risks pressuring fabricated completeness data
  (forbidden, invariant 4). Standard is the honest call, and `facetRoleStatus`/profile is **revisable**: if a
  future PIB round registers risk/config/etc. items, re-assess the profile then.
- Honest note for OEE's own backlog (not your action): that gates pass vacuously at High means criticality does
  not yet MANDATE that critical infrastructure actually did the process — flagged as a possible future EXT
  (presence-gate) in the blueprint. Does not affect your acceptance.

## Phase D.2 — IRI / roster adjudication (you offered to replace `pibreg:` with canonical IRIs)
**Clarification + ruling:** your `pibreg:` IRIs are **correct as-is and need no replacement.** The Phase-F
"no local stand-ins" rule means *don't invent a local term for a central one you need* — and you didn't: you
correctly used `orh:SubjectOntology`/`orh:OntologyFile`/`orh:hasFileSHA256`/`core:hasCriticalityProfile` (central
terms) and put only your own **instances** in `pibreg:`. Instances belong in the registrant's namespace. No
stand-in violation exists.

Assigning canonical `orh:` IRIs would mean **promoting PIB into the governed roster** (becoming a 13th governed
subject OEE owns and governs) — a *structural* decision distinct from accepting your registration. **Default
(consistent with the O4SDLC round): PIB is an ACCEPTED EXTERNAL REGISTRANT, not a governed roster subject.**
Promotion is available but is the governor's explicit call, not an automatic consequence of a clean submission
— flagged for a separate decision, not taken here.

## Final registration state (accepted)
- **Registered & operational (external):** core (conformance, Profile_Standard), oepack_release_history
  (your lineage), via existing central hooks, 0-violation.
- **Conformance-only (no data, honestly):** measurement (you're a consumer/aggregator, not a producer — correct),
  quality, reliability, risk, performance, testing, configuration — EXT-2 gates do not fire at Standard.
- **knowledge_base:** deferred/optional by you — fine; deposit later if desired.
- **ae/meta:** internal, no relationship — correct.

## Phase G — your next step
Decide nothing is required to re-emit (your submission is accepted as-is). Return a short closure note
confirming receipt of this contract; OEE will record the round closed (lightweight Phase G). If you later want
roster promotion or register gateable items, that's a future round.
