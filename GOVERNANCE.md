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

The **VAF engine is not vendored** — it is pinned by SHA-256 in `06-vaf-engine-pin/` and loaded at
run time via `PIB_VAF_SRC`. Pinning, not copying, is deliberate: it keeps VAF's lineage with its owner.

## Registration status

PIB is a **registered, accepted external registrant** of the OEE ecosystem (ORCP round CLOSED;
criticality `core:Profile_Standard`; `pibreg:` instance IRIs accepted as-is). It is **not** a governed
member of the OEE 12-facet roster — promotion would be a separate governor decision. Evidence and the
returned contract are in `08-registration/`.

## Release procedure

1. Re-run the gates: `03-tooling/wiring_validator` against the pinned VAF, `self_coverage_checker`,
   and `pib_invariants` over `01-ontologies/` **plus** `07-spoke-contributions/` (validating
   `01-ontologies/` alone produces the known G3 standalone-vs-merged artifact, not a real failure).
2. Bump `VERSION.txt` per BP-D7 and regenerate `MANIFEST_SHA256.txt`; confirm it self-verifies.
3. Commit with a `Session:` trailer naming the session, push, and tag `vX.Y.Z`.
