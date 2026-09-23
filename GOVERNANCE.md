# PIB — governance

**This repository is the governed home of PIB as of 2026-09-10 (v1.4.1).** All further PIB releases
are made here. The internal engineering lineage in which PIB v1.0.0–v1.4.0 was developed is
**retired** — frozen at its final release, retained as the historical record, and no longer the
source of truth.

## Discipline

PIB is an OE-compliant package. It does not carry its own copy of the discipline or the OE Pack —
governance is **inherited by reference**, resolved **by highest SemVer at use time, never by a
remembered path or pinned filename** (a pinned filename goes stale on the next bump):

| Governing artifact | Resolution rule | State applied at v1.4.1 |
|---|---|---|
| Operating discipline | highest `OE_Operating_Discipline_v*.md` in the OE Pack | **v2.6.0** |
| Governance source (ABox) | highest `knowledge_base_abox_v*.ttl` in the OE Pack | **v2.23.0** |
| Lineage discipline | highest `LINEAGE_OPERATING_DISCIPLINE_v*.md` | **v60.0.0** |

A detached copy of the discipline is non-authoritative the moment it diverges from the in-pack copy.
Sessions working on PIB run the three-step ceremony against the **live** OE Pack, including the
standing session-start step of reviewing the OE handover inbox.

These governing artifacts are maintained and versioned outside this package. Readers without access
to them can still verify everything this repository asserts about *itself*: the manifest, the SHACL
invariants, the wiring enumeration, and the profile set are all re-runnable from the files here.

## What HUB and PIB are — and why they are not two things

**HUB is a role; PIB is the package that role maintains.** They are not two systems working differently,
and the apparent difference is a naming artifact worth stating plainly, because it recurs: this repository
is `PIB`, the OE registry entry is `pib-hub`, and the retired monorepo directory was `pib-hub/`.

- **PIB** — the *Profile + Integration-Interface Blueprint*: the shipped ontologies, shapes, rules and tools
  in this repository.
- **HUB** — the *role in the ecosystem's architecture*, defined by this package's founding charter: the owner
  of "the shared infrastructure that belongs to no single system — the Profile and Integration-Interface
  ontologies, the invariants, the validators, the engine pin, and the per-profile wiring composition."

The role has exactly two modes, and it never has a third:

1. **Publisher (first phase).** It publishes the shared vocabulary that consuming systems declare *against*.
   Nothing can be composed until this exists; that is why the charter made it phase one.
2. **Composer (third phase).** It takes the interfaces those systems declare, composes each profile's wiring
   from them, validates it, and publishes only what passes both gates — wiring validity and self-coverage.

What the role explicitly excludes: **it never authors a consuming system's content.** The charter states the
boundary directly — it "declares the shared LANGUAGE and composes wirings from interfaces the spokes deliver;
it does not author the spokes' interfaces or touch their content."

## Who is authorized for profile management

Authority is split **by layer, not by system**. This is the whole reason the package exists, and it is stated
in the profile vocabulary itself:

| Layer | Authorized party | Examples |
|---|---|---|
| The shared profile — category identity, the criteria meaningful to **more than one** system, and the single selected wiring | **The HUB role, through this package** | `ArtifactCategory`, `SharedCriterion`, which wiring a profile pins |
| System-specific behaviour **attached to** the shared profile identity | **Each consuming system, for itself** | grading weights → PAMG; measurement dimensions → RADAR; generation templates → RDODI |
| Whether a profile may be *published* | **Both**, and both must pass | the HUB runs the gates; the system must have declared an interface that self-covers |

The vocabulary puts it this way: system-specific behaviour "is NOT modelled here — it is attached by each
system to the shared Profile IRI." So a consuming system is fully sovereign over what a profile *means for it*,
and has no authority over the shared identity; the HUB is the reverse. Neither can act for the other.

Two consequences that decide real cases:

- **Nobody may mint a second Profile concept.** A parallel profile vocabulary defeats the single shared
  identity this package exists to provide, and duplicates an authoritative implementation that already exists.
  *Open case:* the PAMG ontologies currently readable declare their own `Profile` class and reference this
  package nowhere. That is a genuine divergence, and resolving it is **PAMG's** decision to make in its own
  registration — not something this package may patch, because patching it would breach the same boundary
  that protects PAMG's authority over its own content.
- **The HUB cannot rescue an unwilling consumer.** If a system does not declare an interface, its profile
  simply cannot be composed. The gate is not a formality that the HUB can waive for convenience.

## Boundaries that apply here specifically

- **B1 / L-64 — ownership.** `07-spoke-contributions/` holds **vendored, SHA-pinned, read-only**
  copies of artifacts owned by other sessions (O4SDLC, RADAR, PAMG). They are pinned dependencies,
  not PIB content: never edited here. `08-registration/OEE_to_PIB_registration_contract_v1_0_0.md`
  is the OEE governance artifact, carried verbatim as received. A defect found in any of them is a
  **proposal to its owner**, filed to that package's handover inbox where one exists (L-115).
- **L-112 — records of past state are not rewritten.** `PUBLISH_RECORD.ttl` describes the original
  publish ceremony that produced this content and is carried **unedited**. Corrections to
  historical statements are made by appended note, never by rewriting what was true at the time.
  Files that describe *current* state (this file, `PROVENANCE.md`, `MANIFEST_SHA256.txt`) are updated
  normally.
- **BP-D7 — versioning.** Every changed file gets a new version; a version is never reused for
  changed content. PATCH for fix/doc-only, MINOR for backwards-compatible additions.

## External dependency

PIB's calculation runs **in the ontology**: candidate generation, admissibility and counting are SHACL
rules and SPARQL (`02-shacl-safeguards/pib_enumeration_rules_v2_2_0.ttl`). The Python files are
harnesses — they drive the rule engine and report; no constraint's meaning lives in code.

The variant-algebra **engine is no longer a runtime dependency**: as of v2.0.0 nothing in this package
requires it, and the tool that called it was removed. Its pin in `06-vaf-engine-pin/` is retained as
**provenance** for the capacities published in earlier releases. The algebra's **operator rules** are
vendored read-only and SHA-pinned under `11-vendored-operator-rules/` so the gates re-run from this
package alone; pinning rather than absorbing keeps that lineage with its owner.

## Registration status

PIB is a **registered, accepted external registrant** of the OEE ecosystem. Round one closed at
criticality standard; **round two was ratified at criticality high** (owner's decision, 2026-09-21;
OE Pack v20.78.0). High criticality makes completeness a standing obligation: every risk, test,
performance measurement and release PIB registers must carry its treatment, result, measurement or
acceptance criterion. `pibreg:` instance IRIs were accepted as-is in round one. It is **not** a governed
member of the OEE 12-facet roster — promotion would be a separate governor decision. Evidence and the
returned contract are in `08-registration/`.

## Release procedure

1. Re-run the gates: `03-tooling/wiring_validator` against the pinned VAF, `self_coverage_checker`,
   Run `03-tooling/reference_check_v1_0_0.py` first: it fails the release if a current document cites a
   file the package no longer ships. It exists because two releases in one day went out citing renamed
   files after that warning was printed and stepped over — a warning nobody stops for is not a safeguard.
   and `pib_invariants` over `01-ontologies/` **plus** `07-spoke-contributions/` (validating
   `01-ontologies/` alone produces the known G3 standalone-vs-merged artifact, not a real failure).
2. Bump `VERSION.txt` per BP-D7 and regenerate `MANIFEST_SHA256.txt`; confirm it self-verifies.
3. Commit with a `Session:` trailer naming the session, push, and tag `vX.Y.Z`.
