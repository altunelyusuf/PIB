# Vendored operator rules — pinned, read-only (NOT PIB-owned)

The two files here are **verbatim, SHA-256-pinned, read-only copies** of the variant algebra's own
operator implementation, vendored so PIB's operator gate re-runs **from this package alone** — the
same reason the spoke interface declarations are vendored under `07-spoke-contributions/`.

**Ownership.** These remain owned by the algebra's session. PIB does not maintain or evolve them and
must not edit them in place. If that session re-issues them, PIB re-vendors the new hashes and bumps.

| File | SHA-256 | Role |
|---|---|---|
| `variant_algebra_v3_operator_properties_v1_0_0.ttl` | `6300bd7157b0fa8a…` | the properties the rules read and write |
| `variant_algebra_operator_rules_v1_0_0.ttl` | `b9e4cd27d884a83b…` | twelve rule shapes implementing the full operator set |

## Execution configuration is prescribed, not chosen

The rules file states it: **advanced mode, in place, and no inference**. PIB's runner uses exactly
that. One consequence is worth repeating because it changes results silently rather than erroring:

> Symmetric predicates are **not** inferred in both directions. The intersection operator's
> co-occurrence link is declared symmetric, but with inference off, asserting only one direction
> yields a half-populated result and no warning. Assert both directions.

## Why the rules, not the engine binary

The previously pinned Python engine implements an **older generation** of the algebra whose runtime
ontology carries only the six variability operators. The full twelve, and the machinery for composing
them, live in the current core ontology plus these rules. Adopting the rules is what gave PIB the
complete operator set; see `06-vaf-engine-pin/` for the pin's current standing.
