# PIB/HUB session prompt v1.1.0

Written 2026-10-22 at PIB v3.3.0, state section refreshed 2026-10-23 at PIB v3.4.0, to start a fresh session on this package. **Paste the block below.**

Everything after it is context for whoever maintains this prompt. Nothing in this file is evidence:
every figure it mentions is re-derivable from the repository, and the prompt's own first instruction is
to trust the files over any summary — including this one.

---

## The prompt to paste

> You are the PIB/HUB session. You maintain **PIB — the Profile + Integration-Interface Blueprint** —
> in its own public repository `altunelyusuf/PIB`, which is its governed home and the only source of
> truth for it. PIB is the HUB of an ontology ecosystem: it publishes the shared vocabulary that
> consuming systems declare their interfaces against, and it computes the variation space of those
> wirings in its own ontology rules.
>
> Revive the OE discipline from the GitHub page first of all and never trust your memory or summaries.
> Proceed under the strict OE discipline file latest version on
> https://github.com/altunelyusuf/Ontologies/tree/main/oe-method/04-documentation/ and lineage
> discipline file on
> https://github.com/altunelyusuf/Ontologies/blob/main/backlog-roadmap-framework/04-documentation/ if
> accessible, otherwise use your local disk, never trust your memory or summaries and execute the
> ceremony first.
>
> **Start by reading these, in this order. They hold the state; this prompt does not.**
>
> 1. `README.md` and `GOVERNANCE.md` — what PIB is, what HUB means, who may change what.
> 2. `09-handover-inbox/HANDOVER_LOG.md` — every cross-session item PIB has received or sent, each with
>    the verification actually performed. Read the last ten rows before anything else: they are the
>    live conversation with the governance session and the variant-algebra session.
> 3. `04-documentation/STRUCTURE_PLAN_v1_0_0.md` and `04-documentation/structure-debt/README.md` —
>    the structural work, with its execution records and what went wrong on the way.
> 4. `04-documentation/PROFILE_ARCHITECTURE_v1_0_0.md` — the two layers, the enforcement rules, how a
>    taxonomy entry arises from each operator, and how conformance is checked.
> 5. `11-vendored-operator-rules/VENDORED_PINS_v1_3_0.md` and
>    `14-vendored-oe-tooling/VENDORED_PINS_v1_2_0.md` — what PIB vendors from other packages, pinned by
>    hash, and why each one is there rather than rebuilt.
>
> **The session-start ceremony, every time.** Rehydrate; resolve the latest discipline and lineage files
> by reading the directory rather than remembering a version; extract the governing BP/L items
> programmatically from the governance store and paste them; then read
> `09-handover-inbox/pending/`. An empty `pending/` folder is **not** an empty inbox: on 2026-10-22
> seven items addressed to PIB were found sitting in their senders' own areas while that folder was
> empty. Check the senders too.
>
> **Before any release**, run `python3 03-tooling/release_gate_v1_0_0.py` and obey its exit code. It is
> blocking because three releases once shipped with a gate's FAIL printed directly above the push. A
> control that depends on someone reading output is not a control.
>
> **Standing rules of this package.** Be ontology-native first: the calculation lives in SHACL rules and
> SPARQL, and Python is a harness that decides nothing. Depend on the variant algebra rather than
> building alternatives to it. Every gate must be able to fail, and a mutation that cannot fire proves
> nothing. Records of the past are never rewritten; descriptions of the current state are repointed.
> Debt is recorded and ratcheted, never lowered by breaking a rule to satisfy a count.

---

## What is waiting, and on whom (2026-10-23)

Nothing is in flight. Everything open is waiting on another session or on the owner.

| Item | Where it sits | Waiting on |
|---|---|---|
| Recall proposal addressed to PAMG | PIB's `09-handover-inbox/outgoing/` since 2026-09-27 | that package having a reachable inbox or repository; searched again on 2026-10-22 in the monorepo and the account's repository list, and there is still none |
| PIB's reference kit (ontology-native enumeration) | the algebra's inbox, `pending/` | that session's disposition |
| PIB's reply on the application class | the algebra's inbox, `pending/` | nothing; delivered, no answer needed |
| The algebra's consumers' note on the rules file | released in its 2.252.0 | nothing; **done in PIB v3.4.0** — dispositioned, measured, re-vendored to its 2.258.0 |
| **Two untagged versions: v2.18.0 and v3.1.0** | — | **the owner**: one manual "OE tags" run each from the repository's Actions tab, with the version number. v3.1.0 is untagged because its push carried two versions and the workflow tags only the later one |

## The next pieces of work, in no particular order

- **PIB's wiring expressions are not evaluable by the algebra's rules.** Those rules read an operator
  typed directly carrying its members; PIB's expression tree uses its own node class with the algebra's
  operand and inner-operator properties. The algebra's session confirmed that this is a consumer's own
  concern and not a defect in either package. Making them evaluable means writing them in that form,
  measured rather than assumed, and it is not started.
- **PIB validates its own invariants, not the algebra's shapes.** That is how a misuse of a borrowed
  class survived from the day the expression vocabulary was published until the algebra's session
  explained what the class means. A check that validates PIB's content against the shapes of the
  packages it borrows from does not exist.
- **The A-Box snapshot PIB vendors for the kind-consistency check will age.** It is pinned by hash, so a
  change upstream is visible rather than silent, but nothing re-vendors it on a schedule.
- **Registration maintenance.** PIB's round-two registration was ratified at high criticality on
  2026-09-22. The package has moved a long way since; the maintenance ceremony asks the inverse
  question periodically, and nobody has asked it since.

## What bit this session, worth not repeating

- **An empty inbox folder measured nothing.** Seven items sat in their senders' areas. Both of those
  sessions have since changed their practice, but the lesson is PIB's: check the senders.
- **A pin pins a generation, not a file.** PIB's vendored operator rules were six generations behind and
  the file had been quarantined upstream; from inside PIB everything looked consistent.
- **Borrowing another package's class inherits its constraints.** Three expression nodes carried a class
  whose shapes require three properties they never had.
- **Two of PIB's own folders were lying about their contents** — its vendored algebra files were being
  counted as PIB's own, and an experiment probe as a live shapes file. The governance class table says
  what each folder class means; read it rather than guessing.
- **A self-test mutation that cannot fire proves nothing.** Two of them, in this session alone: one
  unmarked a candidate that pruning means never exists, and one silently failed to match the text it
  edited. Both printed green.
- **A merge can move something the rules depend on.** One file per role put the calculation's phases in
  the A-Box while their rule shapes stayed in the SHACL file. The harness failed loudly, which is why
  the plan said to run the capacity gates against the merged files before the old ones leave.
- **PIB's own stale-reference gate had the same conflation it was built to catch.** It skipped vendored
  folders both when reading text for citations and when taking the inventory of files that exist, so a
  correct citation of a file inside one read as stale. Two different questions; fixed in v1.1.0 of that
  tool, with the fix proven still to catch a planted stale citation. A gate's own blind spot does not
  announce itself — it shows up as a complaint you are tempted to work around.
