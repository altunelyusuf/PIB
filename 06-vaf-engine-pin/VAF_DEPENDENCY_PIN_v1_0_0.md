# VAF Engine Dependency Pin v1.0.0

The PIB wiring validator depends on the Variant Algebra Framework as a LOOSE, EXTERNAL dependency
(loaded from a path via `PIB_VAF_SRC`, never copied — mirroring radar_rdodi_loader).

**Pinned package:** Variant_Algebra_Framework_v1_0_0.zip
**Package SHA-256:** 7858339ee554f3307aa7945b912828a15e9963b4f7c4a31f5fef3f4e5d5949e3

**Required core files (in /src/), pinned by SHA-256:**
| File | SHA-256 |
|---|---|
| variant_enumerator_v2_0_0.py | 78f33868a8e1f10b27a6b299f03f9efba10014f46c85544c895332db4891b424 |
| variant_backends_v1_0_0.py | fe5d85f0dd094bc4b9bad0a83485f9b535d01efc4f264820f175de29afb41215 |
| variant_dsl_parser_v1_0_0.py | e710346024f01eaecec6c39d167a97f75c046a90c0a95a0c10fbb87d6470e681 |
| variant_dsl_grammar_v1_0_0.lark | 483d0735462a9dc3c49e90db68d32788e0da39703d24857be14fc924931e4bc2 |

**Verified THIS session:** shipped BruteForceBackend.enumerate() + is_admissible() run correctly on the
worked capstone wiring (9 admissible variants; collision guards reject as expected). exit 0.

**DO NOT pin the sub-kits** (vaf-workbench-kit-v1_0_0, Vaf_package_v1_0_0): they ship the backend WITHOUT
the enumerator + grammar and cannot execute the validity path. Pin the FULL framework package above.

**Fix-forward (VAF line, B1 — not fixed here):** variant_dsl_parser eager-loads the grammar at import;
lazy-load would let the enumeration path run without the grammar present.
