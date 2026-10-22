# Your package now holds its own structure-debt register (v1.0.0)

**From:** the OE governance session, 2026-10-07. **To:** the session that owns `pib-hub`.
**What changed for you:** you can now clear your own structure-debt lines in your own release, without asking anyone.
**What you must do:** nothing today, if you would rather not. Your lines keep working exactly as they do now until you
adopt the file below.

## Why

The rule has always said that the owning session clears its own register lines. Until now every package's lines lived
in one file inside the governance package, so clearing one meant editing a package you do not own — which the operating
discipline forbids — and the only path was to file a handover and wait for the governance session. The owner ruled on
2026-10-07 that each package carries its own register.

## Your file, ready to save

Save this as `pib-hub/04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v1_0_0.tsv` in your next release. It is
your 9 lines from the aggregate, unchanged, with the rules in its header:

```
# STRUCTURE DEBT REGISTER (this package's own) v1.0.0 -- the lines of pib-hub, and of no other package.
# The owner ruled on 2026-10-07 that a package carries its own register and clears its own lines in its own release, which is
# what BP-D54 always said; the governance aggregate carries the ceilings and the ecosystem-wide view.
# A line may be removed here, and a count lowered here, with nobody else involved: debt may always shrink. A count may NOT be
# raised here, a line the aggregate does not carry may NOT be added, and a status may NOT be raised to `exception`: the checker
# fails the run and the aggregate generator refuses it, keeping the previous ceiling. Those go through the owner's ruling,
# recorded in the aggregate line as `ruling: ...`.
# rule	path	status	note
N1	pib-hub/01-ontologies/integration_interface_tbox_v1_0_0_1.ttl	debt	name does not match <name>_v<MAJOR>_<MINOR>_<PATCH>.ttl
R1	pib-hub/01-ontologies/pib_assessment_profiles_v1_0_0.ttl	debt	holds roles T+A (T 2, A 47, S 0)
R1	pib-hub/01-ontologies/pib_wiring_composition_v1_0_0.ttl	debt	holds roles T+A (T 4, A 3, S 0)
N1	pib-hub/01-ontologies/profile_tbox_v1_0_0_1.ttl	debt	name does not match <name>_v<MAJOR>_<MINOR>_<PATCH>.ttl
R1	pib-hub/07-spoke-contributions/o4sdlc_interface_contribution_v1_0_0.ttl	debt	holds roles T+A (T 5, A 4, S 0)
R1	pib-hub/07-spoke-contributions/pamg_interface_contribution_v1_0_0.ttl	debt	holds roles T+A (T 5, A 4, S 0)
R1	pib-hub/07-spoke-contributions/radar_interface_contribution_v1_0_0.ttl	debt	holds roles T+A (T 7, A 8, S 0)
U1	pib-hub/A	debt	files=8: 8 active A files; the package ships one
U1	pib-hub/T	debt	files=7: 7 active T files; the package ships one
```

## What you may do in it, and what you may not

- **Remove a line** when you have fixed the files it records, and **lower a `files=` or `missing=` count** when the
  number really fell. Both are debt shrinking, and neither needs anyone's permission or any handover.
- **You may not** raise a count, add a line the aggregate does not carry, or change a status to `exception`. The
  checker fails the run and names the line; the aggregate generator refuses the change and keeps the previous ceiling.
  Those need the owner's ruling, which is recorded in the aggregate line as `ruling: ...`. This is what keeps the
  ratchet from certifying itself, and it is the reason the arrangement can be trusted at all.

## How to check it before you publish

With a current tooling checkout (v1.34.0 or later):

```
python3 oe_structure_check_v1_4_0.py <the tree> --register <the governance aggregate>
```

It reports `own registers in force: pib-hub` once your file is in place, and your lines are then read from your file. If
your package is published from its own repository rather than from the governance tree, add
`--as-package <the slug your publisher uses>`: a repository checked at its own root resolves every top-level folder as
a separate package, while your publisher stages the whole repository under its slug, and only the second view matches
what the register carries.

If you do nothing, the aggregate governs your lines exactly as before, so nothing of yours breaks.

## Where things live now

| | |
|---|---|
| your own register | `pib-hub/04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v*.tsv` |
| the governance aggregate (ceilings, ecosystem view) | `oe-pack/04-documentation/structure-debt/STRUCTURE_DEBT_AGGREGATE_v*.tsv`, generated |
| the rules | unchanged: BP-D53 and BP-D54 in the knowledge base |

The aggregate is regenerated from the packages' own registers, so once you adopt, a line you clear leaves the
ecosystem view by itself. Nothing in this notice asks you to change an ontology file.
