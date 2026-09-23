> **Delivery cover (2026-09-23, `brsf-session`).** Addressed to: PIB. Originally filed to
> `oe-pack/07-handover-inbox/pending/` in the `altunelyusuf/Ontologies` monorepo as a documented
> fallback (per `OE_Operating_Discipline` L-113), since neither `pib-hub` nor any known PIB
> location had a real handover inbox at that time. Redirected here, to PIB's own real
> `09-handover-inbox/pending/` at `altunelyusuf/PIB` (a separate repository from the `Ontologies`
> monorepo, confirmed via its own README's stated filing convention), on the owner's own direct
> instruction that PIB is now ready to receive handovers directly. The fallback copy is being
> removed from oe-pack's own inbox as part of this same redirection, matching PIB's own README:
> "it is routed as soon as a real inbox exists... not a parking place." Verification the
> addressee can run is stated in this handover's own last section.

# Handover (v1.0.0): general/meta rules versus profile-specific rules is not a BRSF-local concern — it belongs in PIB's own shared Profile vocabulary

**From:** backlog-roadmap-framework (registrant session) **To:** PIB (Profile + Integration-Interface Blueprint)
**Date:** 2026-09-23.

## The real, concrete problem this session just found in its own package

BRSF built a real `LineageProfile` mechanism (`v1.98.0`): a profile configures what a given
`(LineageDepthLevel, LineageArtifactDomain)` combination actually requires — whether it needs
Epic decomposition, whether it needs `adoptsObligationSet`. Two real profiles exist, each derived
from one real, closed lineage's own complete history.

**Checked directly, not assumed:** zero of this package's 321 real SHACL shapes reference any
`LineageProfile` property. The mechanism exists as description; nothing reads it. Every current
rule binds every lineage unconditionally, regardless of which profile it declares.

**A real, active consequence of this gap, found while investigating a direct owner challenge**
(historic lineages may be non-conformant to current standards; deriving a new profile from one
risks quietly codifying a weaker requirement into what future lineages inherit): a real rule
added after this package's first profile was derived (`L3`, a Done item needs a test harness
whose completeness was *derived*, not merely asserted) was never satisfied by the *second*
profile's own source lineage. That gap has since propagated into a currently-active lineage that
declared the same profile as its template — a real, live consequence, not a hypothetical one,
confirmed by re-validating both lineages' own real content against this package's current, live
shapes rather than the standard in force when each closed.

## Why this is PIB's concern, not only BRSF's

PIB is the shared Profile vocabulary this ecosystem already uses across RDODI, RADAR, PAMG, and
VAF's own domain-profile mechanism. Every one of those consumers faces the identical structural
question BRSF just found the hard way: when a profile mechanism exists, how does a rule declare
whether it is a *general* rule (binds every profile, always) or a *profile-specific* rule (binds
only under a stated profile condition) — and how does a validator know which is which, rather
than discovering the answer by manual inspection after something has already gone wrong? This is
a property of the *profile pattern itself*, not of BRSF's own vocabulary; every consumer of PIB's
shared Profile concept will hit the same gap independently unless the distinction is established
once, centrally, and reused.

## What is proposed, for PIB to adjudicate, not implement here

1. **A real, general/profile-specific distinction in PIB's own shared vocabulary** — something in
   the shape of an explicit gate a rule can declare (e.g., "this rule applies only when profile
   property X holds"), with a stated, safe default for any rule that declares no gate: general,
   binding everyone, unconditionally. The safe default matters as much as the mechanism — a rule
   that could silently become profile-scoped by omission is exactly the risk this handover exists
   to prevent, not create.
2. **A supporting, real verification mechanism**, not just vocabulary: something equivalent to
   what this session just built and proved in its own package
   (`backlog_validate_v1_9_0.py`'s own `validate_lineage()` / `--validate-lineage`, reusing
   `pyshacl`'s own `--focus`) — a way to check a given lineage's real content against the general
   rules a profile mechanism defines as universal, independent of which profile that lineage
   declares. BRSF's own version is offered for reuse or as a reference implementation if useful;
   this handover does not assume PIB's own consumers share BRSF's own tooling stack.
3. **Whether existing PIB-governed profile mechanisms** (VAF's own domain-profile system,
   RDODI's profile-and-integration usage) already have real answers to this that BRSF should have
   found and reused instead of nearly building ad hoc — checked here only as far as BRSF's own
   direct investigation reached, not comprehensively surveyed across the ecosystem.

## What BRSF will do meanwhile

Not blocked on this ruling. Per the owner's own direct instruction, BRSF is not building its own,
local, ad hoc version of this distinction while this handover is open — the intent is to adopt
PIB's own eventual standard rather than have two, divergent answers to the same real problem
across the ecosystem. In the meantime, BRSF's own default stays exactly what it already,
accidentally is: every current shape binds unconditionally, the safe direction to stay on while
this is unresolved.

## Verification method for PIB

1. Confirm directly, the same way this handover did: in BRSF's own `02-shacl-safeguards/
   backlog_shacl_v1_131_0.ttl`, no shape currently references any `LineageProfile` property
   (`grep -c "requiresObligationSetAdoption\|requiresEpicDecomposition\|forDepthLevel\|
   forArtifactDomain"` returns zero).
2. The real, propagated consequence is reproducible directly: `backlog_validate_v1_9_0.py
   <register> --validate-lineage L_GovernanceMitigations` (the currently-active lineage) shows 4
   real Violations against the `L3` rule described above, on BRSF's own live register at
   `v1.306.0` or later.
3. If PIB builds a real distinction mechanism, BRSF's own `LineageProfile` class and its two real
   profiles are offered as a real, already-evidenced test case to validate the mechanism against
   before it ships more broadly.
