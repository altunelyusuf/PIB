# PIB — adaptation plan for the variant algebra's advancements (v2.26.0 → v2.50.0)

**Prepared:** 2026-09-22 · **Against:** algebra v2.50.0 (`5827c02`) · **PIB at:** v2.3.1
**Method:** every claim below was checked against the algebra's shipped bytes in this session, not taken
from its changelog. Where a difference changes PIB's numbers, the difference was computed.

## What changed upstream that bears on PIB

| Advancement | Bearing on PIB |
|---|---|
| **All twelve operators now genuinely ontology-native** (v2.42–2.44: division, cartesian, then intersection) | The set-level operators PIB deferred in earlier rounds now exist as rules upstream. PIB need never build them. |
| **Exclusive redefined as "exactly one"** (thesis eq. 2.35), plus a new at-least-one rule shape | **Direct semantic conflict with PIB's "at most one".** Material: the capstone is 9 under PIB's reading, 6 under the algebra's. |
| **Parenthesizable, precedence-climbing expression grammar** (v2.34) | A concrete syntax PIB's nested wiring expressions could serialise to and parse from. |
| **Owner-directed standing rule: Python → ontology-native** (v2.39) | PIB already converted (v2.0.0). No new obligation; confirms direction. |
| **Minimum-feature validation — "an empty component is not a component"** (v2.47) | A validity condition PIB does not currently check for variation spaces. |
| **Both files PIB vendors changed in place, still labelled v1.0.0** | Pin drift PIB's hashes caught; the version number hides it. |
| PIB's enumeration proposal **accepted in principle, build deferred** | The blocker is that PIB's reference files were unreachable from that session — fixable by PIB today. |

## Items, in priority order

### 1. Exclusive semantics — fix a misstatement PIB publishes (do now, patch)

PIB's wiring-expression vocabulary types its exclusive operator as the algebra's `ExclusiveOperator`
while labelling it "at most one of the operands may be selected". Upstream now defines that class as
**exactly one**; the at-most-one reading is the *optional-wrapped* form. PIB's own intent is at most one
("at most one system may measure"), so **PIB's published capacities do not change** — 9 stays 9. What is
wrong is the claim, not the number.

Measured, so the stakes are explicit: capstone capacity is **9** under at-most-one and **6** under
exactly-one. A reader who takes PIB's operator typing at face value would compute 6.

**Action:** state the mapping explicitly in the wiring-expression vocabulary — PIB's exclusive means the
optional-wrapped form — and keep PIB's own enumeration vocabulary (`pibe:ExclusiveConstraint`) as the
at-most-one constraint it already is.

### 2. Vendored-file drift — hold the pin, ask for a version (do now, report)

Both vendored files differ from upstream while carrying the same version:

| File | PIB's pin | Upstream now |
|---|---|---|
| operator rules | `b9e4cd27…` | `7a3569…` (+84 lines: three new rule shapes) |
| extended properties | `225e1de2…` | `cc8670…` (implementation hashes updated) |

Behaviourally, PIB's operator gate gives **identical results** under both — checked by running the gate
against upstream's current files. So this is not urgent, and re-vendoring is safe.

It is nonetheless **held, not adopted**: adopting content that changed under an unchanged version number
means PIB could not later tell which bytes it pinned, and the same-version change is itself a versioning
defect to report. **Action:** report to the algebra's session and re-vendor once a distinct version exists.

### 3. Unblock the deferred enumeration build (do now)

The algebra accepted PIB's ontology-native enumeration proposal **in principle** and deferred the build
for one stated reason: PIB's reference files were "NOT accessible anywhere in this session's filesystem",
and it declined to build from prose alone rather than risk an unverified correctness gap — the right call.

**Action:** deposit the three reference files directly into the algebra's inbox, read-only and hash-pinned,
so the build can be differentially verified against a real implementation rather than a description.

### 4. Delegate the set-level operators instead of carrying them unused (later, needs a test-drive)

PIB names all twelve operators but only six take part in enumeration; intersection, cartesian, division,
addition, subtraction and inverse are declared and unused. Upstream now implements all of them as rules.
Before adopting, measure on PIB's real questions — "which wirings suit an artifact under two profiles at
once" was the case that motivated them in the first place. **Not** a rewrite of PIB's enumeration: those
operators act on whole wiring spaces, which is a different arity from the constraints inside one space.

### 5. Adopt the minimum-feature validity condition (later, cheap)

The algebra now rejects a component with no features. PIB has no equivalent check: a variation space with
no features currently yields a capacity of 1 (the empty selection) rather than being rejected as ill-formed.
**Action:** add it as a conformance case and decide whether PIB treats such a space as invalid or as
capacity 1 — a semantic choice, so the owner's to make, not to be settled by this plan.

### 6. Expression grammar as concrete syntax (later, optional)

PIB's nested expressions exist only as graph structure. The algebra's new grammar would give them a
readable, parenthesised written form. Worth doing only if PIB gains a reason to exchange expressions as
text; nothing today needs it.

## What explicitly does not change

- **The harness loop stays.** The algebra converted Python to ontology-native but still has no rule-iteration
  mechanism, so PIB's fixpoint loop remains the accepted, recorded risk it already is.
- **PIB's enumeration rules stay PIB's.** Upstream's operator rules evaluate one candidate at a time; PIB's
  are candidate-scoped so a whole space can be evaluated at once. That distinction is the reason PIB's rules
  exist and is unaffected by any of the above.
- **Published capacities stay.** 9 and 1 are unchanged by every item here.

---

## Execution record (appended 2026-09-22, PIB v2.5.0) — do not rewrite the plan above

**Item 1 — exclusive semantics: DONE** in v2.4.0. The mapping is recorded in the wiring-expression
vocabulary; published capacities unchanged.

**Item 2 — vendored drift: DONE.** The algebra's session accepted PIB's finding and gave both files a
distinct version (`1.1.0`). PIB adopted them after measuring what the discipline requires before taking a
higher version: all 30 algebra terms PIB binds to are covered, and the new files drop nothing. The operator
gate was run against them before replacing the old copies — identical results.

*Reported back, not worked around:* the files declare version 1.1.0 while their **filenames still read
`v1_0_0`**, so a consumer pinning by filename still cannot distinguish them.

**Item 3 — delegate the set-level operators: RESOLVED, no build needed.** Measured rather than assumed. The
algebra's operators — including the newly ontology-native ones — work at **element level**: the intersection
rule intersects operands that co-occur. PIB's question is **set-level**: which whole wirings are admissible
under two profiles at once. On the same subject matter the algebra's rule returns one element while PIB's
enumeration returns a capacity of 2. Different arities; delegating the first does not answer the second.

**Decision:** keep PIB's six declared-but-unused operators as what they are — expression constructors at
element level — with the arity now stated in the vocabulary, and keep PIB's enumeration for set-level
questions. Nothing is duplicated: PIB does not implement the element-level operators, it uses the algebra's.

*Found while testing, reported to the algebra:* v1.1.0's intersection rule now requires each operand to be
typed as one side of the intersection (`SetA`/`SetB`); the version PIB previously vendored matched any
operands. A prior consumer's data silently returns nothing under the new rule. PIB's own gate did not catch
it because the gate exercises repetition and exclusion, not intersection.

**Items 4, 5 — awaiting the owner's decision**, as agreed: whether a featureless space is invalid or has
capacity 1, and whether PIB needs a written concrete syntax for its expressions.
