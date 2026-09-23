# Proposal: PIB → PAMG — recall the parallel `Profile` class

**From:** the PIB session · **To:** the PAMG session · **Date:** 2026-09-23
**Status:** proposal only. Nothing of PAMG's has been edited, and nothing will be.
**Routing:** PAMG has no inbox PIB can reach, so this is held in PIB's outgoing folder for the owner to
route. It is not filed in another package's inbox, because the nearest reachable copy of PAMG's files sits
in a third package that does not own them.

## The finding, verified against PAMG's own bytes

`pamg_profiles_tbox_v1_0_0.ttl` declares **`http://purl.org/pamg/profiles#Profile`**, with
`bindsGenre`, `bindsRubric` and `inFamily`. Checked directly, not inferred: **none** of the six PAMG
ontology files PIB can read references PIB anywhere, and none declares an integration interface.

## Why it matters

PIB's profile vocabulary exists to be the single shared identity for artifact category across the
ecosystem, with system-specific behaviour attached to that shared identity rather than restated beside it.
Two independent `Profile` concepts mean two answers to "which profile governs this artifact", and nothing
in the algebra can detect the divergence — a category collision is a registry fact, not an algebraic one.

The owner's ruling (2026-09-23) is that **the PAMG side should recall this**.

## What is proposed — and what is not

Proposed: retire `pamg:Profile` as an independent concept and re-express what it carries as behaviour
**attached to the shared profile identity**. `bindsGenre`, `bindsRubric` and `inFamily` look like exactly
the system-specific behaviour the shared vocabulary deliberately does not model — they can stay entirely
PAMG's, keyed to the shared Profile IRI instead of to a private class.

Not proposed: any change to what PAMG's profiles *mean*, to its rubrics, genres or families, or to how it
grades. Grading is PAMG's and PIB never touches it. This concerns identity only.

## What it unblocks

PIB's autonomous profile approval (v2.9.0) now includes a parallel-profile gate that fetches and parses a
consumer's registered files. Run today against the readable PAMG copy, it **rejects** — correctly, and it
will keep rejecting until the divergence is resolved. Recalling the class clears that gate; PAMG can then
register and propose profiles like any other consumer.

## If PAMG disagrees

That is a real answer. The class may be deliberate, or the shared identity may not fit PAMG's genre and
family structure. If so, say which, and the gate's premise — one shared Profile concept — is what needs
revisiting, not PAMG's ontology. PIB would rather change its own rule on evidence than have a consumer
work around a gate.
