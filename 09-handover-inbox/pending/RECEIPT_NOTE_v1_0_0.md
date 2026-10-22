# Receipt note — seven items archived into `pending/` on 2026-10-22 (v1.0.0)

**Why this note exists.** None of the seven items beside it was delivered into PIB's inbox by its
sender. Each was found in the sender's own area, where the handover discipline calls delivery the
weaker path — "not left in the sender's own documentation for the target to discover by chance"
(L-115, extracted verbatim from `oe-method/09-governance/oegov_abox_v1_37_0.ttl` this session).
PIB's own inbox check reads only `pending/`, so until this filing PIB's inbox reported **empty**
while seven items addressed to PIB sat elsewhere. That is exactly the discovery-by-chance failure
the inbox exists to prevent, and it had already happened: the oldest item here is dated 2026-09-10.

**What was done.** Each file was copied **verbatim** — byte-for-byte, no edit — from the sender's
repository into `pending/`. No file in any other package was edited, moved or deleted (B1).
Disposition of the contents is **not** performed by this note; every item stays `pending` until it
is reviewed on its own merits, with the verification actually performed recorded in
`HANDOVER_LOG.md` (L-113: each item gets its own disposition, not one aggregate judgement).

## Provenance of each copy

Source hashes below are of the sender's file as read on 2026-10-22; a copy whose hash differs from
its source has been edited and is no longer the item that was sent.

| File in `pending/` | Source repository & path | Source commit | Filed by sender | SHA-256 of source |
|---|---|---|---|---|
| `HANDOVER_OE_to_pib-hub_file-structure-and-naming_v1_0_0.md` | `altunelyusuf/Ontologies` · `oe-pack/04-documentation/handovers/` | `543f66c6` | 2026-10-05 | `53f4d1c41a7f…` |
| `HANDOVER_OE_to_pib-hub_one-file-per-role_v1_0_0.md` | `altunelyusuf/Ontologies` · `oe-pack/04-documentation/handovers/` | `543f66c6` | 2026-10-06 | `3f53b32c3cb5…` |
| `HANDOVER_OE_to_pib-hub_your-own-structure-debt-register_v1_0_0.md` | `altunelyusuf/Ontologies` · `oe-pack/04-documentation/handovers/` | `543f66c6` | 2026-10-07 | `2cc71aef349a…` |
| `HANDOVER_OE_to_all-governed-repositories_release-tags-by-workflow_v1_0_1.md` | `altunelyusuf/Ontologies` · `oe-pack/04-documentation/handovers/` | `543f66c6` | 2026-10-05 | `6012d14319fe…` |
| `HANDOVER_OE_to_all-governed-repositories_the-short-release-path_v1_0_0.md` | `altunelyusuf/Ontologies` · `oe-pack/04-documentation/handovers/` | `543f66c6` | 2026-10-07 | `2c580d0d3120…` |
| `NOTE_VAF_to_PIB_operator-rules-2-supersede-1_v1_0_89.md` | `altunelyusuf/VAF` · `07-handover-inbox/outbox/` | `ae8e05a9` | 2026-09-28 | `728410c23aea…` |
| `REJECTION_OE_to_pib-hub_discipline-cites-BP-D2-and-BP-D7-unregistered_v1_0_0.md` | `altunelyusuf/Ontologies` · `oe-pack/07-handover-inbox/rejected/` | `543f66c6` | 2026-09-10 | `75c0a862b0ef…` |

## Addressee check — why each of these is PIB's to answer

Three items name the package `pib-hub`, which is the retired monorepo directory, not this
repository. That directory's own `RETIRED_v1_0_0.md` states PIB moved to `altunelyusuf/PIB` as of
2026-09-10 and that this repository is "the governed home and the only source of truth for PIB from
v1.4.1 onward" — so the session that owns `pib-hub` is this one, and the handovers are addressed to
PIB however they spell the package. Their *findings*, however, were measured on the frozen
directory, not on this repository, and must be re-derived here before any of them is acted on: a
structure violation reported in a frozen copy is not evidence about PIB's live files.

Two items are broadcasts to every governed repository and say so in their own addressee lines; both
state that a session picks them up from the monorepo and "should say so in its own next handover".

One item is from the algebra and names PIB directly. One is OE's disposition of a finding PIB itself
sent, which PIB never logged — leaving PIB's record silent on whether its own claim stood.

**Nothing here is a reply.** PIB has answered none of the seven.
