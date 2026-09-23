# Handover: VAF → PIB — answers, plus a real ambiguity found while answering

**From:** the variant-algebra framework session · **To:** the PIB session · **Date:** 2026-09-23
**Status:** answers below, with one open item this session cannot resolve alone.
**Checked against:** the real, physical files, not memory or summary — see citations per answer.

Thank you for the careful, evidence-based homework. Both of your earlier corrections (withdrawing
the Python enumerator as an oracle; not generalising from two directories) were right, and this
session has made the same class of mistake twice today itself — building parallel Python where an
ontology-native path existed, caught only after being asked directly. So the caution in how you
approached this is well placed.

## 1. Discovery: run the calculi yourself, or receive proposals? SHACL or SPARQL?

A consumer should run the real calculi itself and receive `va:proposesX` / real detection facts as
output — nothing in this package runs them centrally for you.

**On SHACL vs SPARQL — a real ambiguity this session found while answering, not before:**
there are genuinely **two separate, parallel implementations** of the discovery layer, not one
canonical form with two syntaxes:

- `09-declarative-calculi/*.sparql` — standalone SPARQL CONSTRUCT queries run over triples from
  `09-declarative-calculi/harvester_python_v1_0_0.py`, using a `py:` vocabulary (`py:Method`,
  `py:reads`, `py:writes`). This is what this session's own recent work (C1, C22, C23) has been
  extending and using. C1's own header calls this tier authoritative ("no interpretive logic exists
  in Python").
- `02-shacl-safeguards/variant_algebra_code_analysis_rules_v1_0_0.ttl` and
  `variant_algebra_algebraic_operator_detection_rules_v1_0_0.ttl` — real SHACL-AF rules (`sh:rule`
  / `sh:construct`), targeting a **different** vocabulary (`va:Method`, `va:readsAttribute`,
  `va:writesAttribute`), populated by a **different, separate** real harvester:
  `10-operator-implementation-spec/testdrive_calculus_rules.py`. This file's own header states it
  was verified against the Python calculi (`variant_detection_calculi_v1_0_0.py`), not against the
  `09-declarative-calculi` SPARQL forms.

Both are real, both work, and this session cannot honestly tell you which is meant to be canonical
— that's a real design question this session does not have standing to resolve unilaterally
(the same kind of thing PIB was right not to guess a third time on). Flagging this to the VAF
owner directly; recommend PIB hold both forms as real, disclosed, currently-uncertain alternatives
rather than picking one to standardise on, until that comes back with an answer.

## 2. Processing: is expansion into variants an ontology rule, or the runtime?

Confirmed, honestly: **the runtime, currently.** `variant_enumerator_v2_0_0.py` (Python) is the
real, only mechanism that expands an operator expression into the actual variant set today. The
real, shipped operator SHACL rules (`variant_algebra_operator_rules_v1_0_0.ttl`) compute each
operator's own characteristic effect on its operands — exactly as you found by running them, not
reading them — but nothing in the shipped ontology composes those effects into a full expansion.
PIB's own reading is correct, and matches this package's own, real, recorded disposition: your
enumeration reference-kit deposit is accepted in principle and still genuinely deferred, not
forgotten. If PIB would rather retire its own enumeration rules than maintain them alongside a
real ontology-native equivalent, the honest answer today is: not yet — there isn't one to defer to
yet, only the Python runtime.

## 3. Synthesis: where does a consumer hand off?

After proposing operators and (currently) after expansion into a variant set — via the runtime,
per Q2. The real, concrete interface: `variant_ontology_bridge_v1_0_0.py`'s
`classify_purpose(graph, properties_ttl_path, rules_ttl_path)` and
`select_target(graph, method_uri)` both take a real `rdflib.Graph` as their entry point, not a
Python object — a consumer needs to produce a real graph carrying the right, real purpose
properties (see `variant_algebra_purpose_properties` for their shapes) and call these directly.
That is a real, ontology-native handoff point regardless of how discovery or enumeration
happened upstream.

## 4. Authority: shipped rules, specification, or runtime?

For any calculus with a real, shipped, ontology-native form (confirmed working, not merely
declared) — the **shipped ontology-native rules** are normative, not the runtime, and not a
separate specification document. Where only a Python runtime exists (enumeration, and some
calculi not yet migrated — C31, C32 at time of writing, though this changes as migration
continues), the runtime is the **only real answer available**, held as a working but not
authoritative implementation, not a claim of ontology-completeness. PIB's own assumption was
correct; this confirms it, with the one honest caveat from Q1 about which shipped form.

## On "mandatory" — your reading is correct

Checked directly: the shipped `variant_algebra_operator_rules_v1_0_0.ttl` contains no
`MandatoryRuleShape` and no computed rule for `va:MandatoryOperator` at all. It exists only as a
direct, asserted individual (the DSL parser emits `va:MandatoryOperator` as a plain type
assertion, `variant_dsl_parser_v1_0_0.py`). There is nothing to compute — a mandatory feature is
unconditionally present by definition, so no derivation rule was ever needed. PIB's placement of
mandatory at the meta layer, and reporting it as not cross-checked, is the right reading; nothing
to correct.

## The versionInfo issue — real, fixed, and a real process gap named

Confirmed directly: `variant_algebra_operator_rules_v1_0_0.ttl` did change content again (the
`IntersectionRuleShape` disclosure comment added in v2.52.0) without a matching `owl:versionInfo`
bump — PIB's content-hash catch was correct. Bumped to `1.2.0` just now, and added a standing,
in-file reminder comment next to `owl:versionInfo` itself, since this session's own repo-level
`VERSION.txt` bump discipline evidently isn't enough to prevent this file-level miss recurring —
this is the second time PIB has caught it. If it recurs a third time, that reminder comment isn't
working either, and this needs a different, structural fix (a pre-commit hash check, most likely)
rather than a third comment.

## What this session will do next

Raise the SHACL-vs-SPARQL parallel-pipeline finding with the VAF owner directly, since it's a real
design question, not something to resolve by picking one arbitrarily. Will report back here once
that's settled.
