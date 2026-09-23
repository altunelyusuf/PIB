# Vendored operator rules — pinned, read-only (NOT PIB-owned)

The two files here are **verbatim, SHA-256-pinned, read-only copies** of the variant algebra's own
operator implementation, vendored so PIB's operator gate re-runs **from this package alone** — the
same reason the spoke interface declarations are vendored under `07-spoke-contributions/`.

**Ownership.** These remain owned by the algebra's session. PIB does not maintain or evolve them and
must not edit them in place. If that session re-issues them, PIB re-vendors the new hashes and bumps.

| File | SHA-256 | Role |
|---|---|---|
| `variant_algebra_v3_extended_properties_v1_0_0.ttl` | `a42a48e4d2aac9d7…` | the properties the rules read and write (upstream's consolidated properties file) |
| `variant_algebra_operator_rules_v1_0_0.ttl` | `02276cfc6f312e5d…` | twelve rule shapes implementing the full operator set |

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

## Re-vendored in PIB v2.0.3 — the properties file changed upstream

The algebra's own v2.18.0 merged eight separate property files into one. The file PIB originally
vendored, `variant_algebra_v3_operator_properties_v1_0_0.ttl`, no longer exists at its origin.

Replaced with the consolidated `variant_algebra_v3_extended_properties_v1_0_0.ttl`, after checking
it is a strict superset for everything the rules use: all 21 terms the old file declared are still
declared, and none of their type, domain or range axioms changed or disappeared. The operator gate's
self-test was run against the new file **alone** before the old copy was removed — satisfying
candidate clean, violating candidate rejected on both constraints.

The rules file itself is unchanged upstream and still byte-identical to PIB's copy.

## Re-vendored in PIB v2.5.0 — upstream gave the changed content a version

Both files had changed upstream **in place, still declaring version 1.0.0**. PIB held its pin and asked for a
distinct version rather than adopt content it could not name; the algebra's session accepted that and bumped
both to **1.1.0**.

Adopted after measuring what the discipline requires before taking a higher version — that it supersedes
rather than diverges: all 30 algebra terms PIB binds to are covered exactly as before, and the new files
**drop nothing** the pinned copies declared. The operator gate was then run against the new files before the
old copies were replaced: identical results, violating fixture still rejected on both constraints.

One mismatch remains upstream and is reported, not worked around: the files declare `owl:versionInfo "1.1.0"`
while their **filenames still read `v1_0_0`**. PIB pins by hash, so it is unaffected; a consumer pinning by
filename still cannot tell the two apart.
