# REFERENCE_ONLY — NOT_A_RELEASE — findings: approving profiles, and what the algebra can and cannot police

**Owner's question:** if each ontology declares its own profile, how are standards kept? Would a registration
system that controls and approves profile descriptions, using the variant algebra as the main mechanism, work?

## First, a correction to the premise

The model does **not** let each ontology declare its own profile. The shared profile identity — artifact
category, criteria meaningful to more than one system, the single pinned wiring — belongs to this package;
a consuming system attaches its own behaviour *to* that shared identity. PAMG declaring its own `Profile`
class is the **divergence the model forbids**, not an example of how the model works. So the standard is
already defined; what is missing is an **enforcement path** at the moment a profile is proposed.

## Measured: what the algebra can decide

Using only shipped pieces — the converter, the enumeration rules, the capacity harness — a profile proposed
by a consumer in the algebra's own notation is approvable or rejectable today:

| Proposal | Capacity | Verdict |
|---|---|---|
| A coherent coursework profile | **9** admissible wirings | approve — it can pin exactly one |
| A proposal whose own constraints contradict | **0** | reject — no admissible wiring exists |

That is a real gate, not a formality: it rejects on the proposal's own arithmetic.

## Measured: what the algebra cannot decide

Two proposals that are algebraically impeccable but break the shared standard:

- Two consumers claiming **the same artifact category** under different profile names — capacities 3 and 3.
  **The algebra approves both.** Nothing in it knows a category is meant to be one shared identity.
- A criterion declared "shared" but used by only **one** system — the vocabulary's own definition says a
  shared criterion is "meaningful to MORE THAN ONE system", yet no algebraic property expresses that.

These are **registry facts, not algebraic ones**: they are about who else claims the same thing, which is
knowable only from the registry, never from one proposal's own equations.

## Recommendation

**Yes to the registration-and-approval system — and no to making the algebra its main mechanism.** Two
layers, each policed by the mechanism that can actually see the failure:

| Layer | Mechanism | Catches |
|---|---|---|
| **Identity** — category, shared criteria, one shared Profile concept | the consumer **registry** (v2.7.0) plus this package's invariants | two consumers claiming one category; a "shared" criterion only one system uses; a parallel Profile class |
| **Variation** — which wirings are admissible, which one is pinned | the **variant algebra**, through this package's rules and capacity computation | contradictory constraints, unsatisfiable proposals, more than one pinned wiring |
| **Contract** — can it be wired at all | the existing invariants | missing self-coverage, unmatched consumes |

The algebra also supplies the **interchange notation**: a consumer proposes in the algebra's DSL, and the
converter (v2.6.0) turns it into a space this package can compute. That is the right and sufficient role for
it — necessary for the variation layer, blind to the identity layer.

**Build it as an extension of the consumer registry, not beside it.** The registry already carries pointer,
hash, interface and disposition; a profile proposal is another record type in the same pipeline, with the
same three-state disposition. A second parallel registry would duplicate an implementation that exists.

## What only the owner can decide

Three stipulations, which no evidence settles:

1. **Approval strictness** — do the gates approve automatically when they pass, or is a human sign-off
   required for a new shared category?
2. **New categories** — may a consumer introduce one, or only bind to categories this package already
   publishes?
3. **The PAMG divergence** — is PAMG's `Profile` retired in favour of the shared identity, re-expressed as
   behaviour attached to it, or ratified as a legitimate exception? This is PAMG's to decide; the registry
   can only make the divergence visible, never resolve it.
