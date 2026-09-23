# PIB consumer registry — register your ontology for adaptation

A consumer ontology registers itself here. PIB then verifies what you declared, against your bytes, and
adapts on that basis.

**Why this exists.** PIB previously located consumers by hand — searching repositories, comparing snapshots,
asking where things lived. That does not scale, and worse, it is not verifiable: a snapshot someone pasted
months ago cannot be checked against anything. A registration is a **pointer plus hashes**, so any claim PIB
later makes about your ontology can be re-derived by anyone from your own repository.

**Why a new folder rather than an existing one.** The closest existing areas were checked first, as this
package's discipline requires. `09-handover-inbox/` carries one-off proposals that get dispositioned and
closed; a registry is durable state that stays true between rounds. `07-spoke-contributions/` holds
verbatim *copies* of other packages' bytes; a registration holds **no copies at all**. Either name would
have to describe two different things, so this area is its own.

**Why pointers and not copies.** This follows the convention the OE ecosystem already settled: a registrant
keeps its own bundle in its own repository, and the registry keeps the pointer, the hash and the result.
Copies rot silently; a hash tells you the moment they do.

## What to file

One Turtle file in `pending/`, named `registration_<your-package>_v<major>_<minor>_<patch>.ttl`. Start from
`TEMPLATE_consumer_registration_v1_0_0.ttl` in this folder. It declares:

| You declare | Why PIB needs it |
|---|---|
| your package name and repository URL | so PIB reads your bytes, not a snapshot of them |
| a commit SHA or tag | so the reading is reproducible and cannot move under either of us |
| each ontology file you want adapted, with its SHA-256 | so PIB can prove it read exactly what you published |
| your interface: what you **produce** and **consume** | this is the contract PIB composes wirings from |
| a self-coverage attestation | PIB's invariants require it before any wiring is published |
| whether your repository is reachable with the credentials PIB is given | so an unreachable pointer is stated, not discovered later |

Nothing else is required, and nothing about your internal design is wanted here. What your ontology means
is yours; what it exchanges is the contract.

## What PIB does with it

1. `03-tooling/consumer_registration_check_v1_0_0.py` validates your record against
   `02-shacl-safeguards/pib_consumer_registration_shacl_v1_1_0.ttl` — a malformed record is rejected with a
   reason, never half-adapted.
2. Where your repository is reachable, the same tool **fetches your files and compares hashes**. A mismatch
   is reported, never silently accepted: it means your registration and your repository disagree.
3. If both pass, the record moves to `registered/`, a line is added to `REGISTRY.tsv` stating what was
   actually verified, and your interface becomes eligible for wiring composition.
4. If your repository is not reachable, the record is still recorded — marked unreachable, with its hashes
   kept — and PIB will say so plainly rather than pretending to have checked.

## Proposing a profile

A registered consumer may also propose a **profile**, in `profiles/pending/`. Approval is **autonomous**
(owner's ruling, 2026-09-23): the gates decide, nothing waits for a signature, and the decision plus what
was verified is appended to `PROFILE_REGISTRY.tsv`.

A proposal declares its proposer, one artifact category, any criteria it claims are **shared**, and its
variation space in the algebra's DSL. `03-tooling/profile_approval_v1_0_0.py` then decides:

| Gate | Rejects |
|---|---|
| shape | a record missing proposer, category, or variation space |
| identity | a "new" category whose name collides with one already in `CATEGORIES.tsv` — bind to that identity instead of minting a second for the same thing |
| shared criteria | a criterion naming fewer than two systems: the vocabulary defines shared as meaningful to more than one system, so a criterion only its proposer uses is system-specific behaviour |
| variation | a space with no admissible wiring — a profile must pin exactly one |
| parallel profile | a consumer declaring its own `Profile` class, fetched and parsed from its registered files |

**A consumer may introduce a new category** (owner's ruling). The identity gate therefore looks for a
*collision*, not for novelty. Names collide on meaning, not punctuation: `capstone_report` collides with
`Capstone report`.

Where a consumer's files cannot be read, the parallel-profile result is **UNCHECKED**, never "clean".

## What PIB will never do

- **Author or edit your ontology.** Findings about your package are filed to *you* as proposals; PIB does
  not change another package's content, and a registration is not permission to.
- **Adapt against a snapshot you did not register.** PIB currently pins June interface declarations for
  three consumers; those stay frozen and clearly marked until their owners register something current.
- **Claim a check it did not run.** An unreachable repository yields "unreachable", not "verified".

## Known candidates, deliberately not pre-registered

PIB's published profiles reference interfaces for O4SDLC, RADAR, PAMG, GamOnt, a ZT4SWE conformance
reference, and the OE measurement facet. They are **not** listed here as registered, because registering on
another package's behalf would assert something it has not said. When each registers, it appears here.

One finding already worth your attention if you are PAMG: the PAMG ontologies PIB can currently read
declare their own `Profile` class and reference PIB nowhere. That is a divergence to resolve in your
registration, not something PIB will paper over.
