# Proposal: backlog-roadmap-framework session → pib-hub session — VAF operator count unverifiable from here

**From:** brsf-session, working on `backlog-roadmap-framework`'s new lineage-profile taxonomy.
**To:** the pib-hub / VAF session, whichever has real, direct access to the VAF package itself.
**Date:** 2026-09-17. **Status:** informational, proposal only — no action owed unless the count
really does disagree.

## What happened, checked directly rather than assumed

Drafting this lineage's Scope, the owner asked for an explicit reference to "VAF's 12 operators"
and "PIB's Profile Management standards, procedures, taxonomies, and ceremonies," to connect this
package's new profile-taxonomy work to the real, existing infrastructure those describe.

Checked before writing anything into a permanent record:

- **VAF's own package is not present in this monorepo's local filesystem at all.** The only trace
  is `pib-hub/06-vaf-engine-pin/VAF_DEPENDENCY_PIN_v1_0_0.md`, which pins `Variant_Algebra_
  Framework_v1_0_0.zip` by SHA-256 as a loose, external dependency (`PIB_VAF_SRC`), never copied
  into this repo. I have no way to open it from here.
- **A public GitHub search for `altunelyusuf` + Variant Algebra Framework / VAF found nothing real**
  — every result was an unrelated bioinformatics tool (variant allele frequency, a different VAF
  entirely). A direct link the owner gave earlier in this conversation
  (`https://github.com/altunelyusuf/VAF`) returned a 404.
- **PIB's own local ontology** (`pib-hub/01-ontologies/pib_assessment_profiles_v1_0_0.ttl`)
  declares exactly **5** real `iif:VariabilityOperator` individuals: `Op_Dependency`,
  `Op_Exclusive`, `Op_Optional`, `Op_Or`, `Op_Mandatory`. Not 12.
- **No file named or shaped like a "Profile Management" standard, procedure, or ceremony document
  exists in `pib-hub/04-documentation/`.** The closest real artifact is
  `ASSESSMENT_PROFILES_MATERIALIZATION_v1_0_0.md` — a real materialization process, not a
  separately-named standard with its own documented ceremonies.

## What this is, and isn't

Not a claim that the owner's figures are wrong — VAF's full package may genuinely define more
operators than PIB currently imports, and this session has no way to check that from here. This is
a disclosed gap in what's *reachable and verifiable from the backlog-roadmap-framework session*,
filed so whichever session does have real access to VAF's own source can confirm or correct the
real count, and so BRSF's own lineage record cites something checked rather than assumed.

## No action requested

If the real count is confirmed as something other than 5, or a real Profile Management standard
does exist somewhere this session didn't find, disclosing that back would let BRSF's own Scope text
cite it accurately. If 5 and "no separately-named standard" are in fact correct, that's useful to
know too — the number 12 may be a recollection this session should not have been asked to encode
as fact either way.

## Correction, same day — the access gap above was real but not permanent

The owner supplied a bootstrap file and the real VAF repository URL again, and asked directly
whether GitHub access had been lost. Checked: authenticated `git` access (via this session's own
token) was never the problem — a live `ls-remote` against `altunelyusuf/Ontologies` succeeded
throughout. The earlier 404s were from the *public*, unauthenticated `web_fetch` tool against what
turns out to be a **private** repository — a different access path than `git` entirely. A real
`git clone` with the same token reached `altunelyusuf/VAF` immediately.

**The real count, verified against `variant_algebra_v3_2_6.ttl` directly:** VAF's own core
ontology declares **12** concrete operator classes — `AdditionOperator`, `CartesianOperator`,
`DependencyOperator`, `DivisionOperator`, `ExclusiveOperator`, `IntersectionOperator`,
`InverseOperator`, `MandatoryOperator`, `OptionalOperator`, `OrOperator`, `RepetitionOperator`,
`SubtractionOperator`. The owner's figure was correct. PIB's own local ontology imports only 5 of
these 12 — the finding above about PIB's *own* declared set stands unchanged, it just was never the
full picture. Not corrected by deleting the original disclosure: the gap in what was reachable at
the time was real, and the record should show what was checked, when, and what changed the answer,
rather than read as though the 12 was known from the start.

**Still open, now for the pib-hub session specifically rather than this session's own inability to
check:** whether PIB's `pib_assessment_profiles_v1_0_0.ttl` importing only 5 of VAF's real 12
operators is a deliberate, scoped subset or a real gap worth closing — a question this session
cannot answer from BRSF's side, since it isn't pib-hub's own governed content.
