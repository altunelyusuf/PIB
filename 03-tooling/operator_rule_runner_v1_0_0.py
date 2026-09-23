#!/usr/bin/env python3
"""
PIB Operator Rule Runner v1.0.0
===============================
Executes the variant algebra's operator rules INSIDE PIB's own gate run, over PIB's wiring
expressions, and reports what each operator decided.

Why the rules are vendored rather than loaded from the engine: PIB's gates must re-run from this
package alone (the same reason the spoke interface declarations are vendored). The two files under
11-vendored-operator-rules/ are verbatim, SHA-pinned, read-only copies owned by the algebra's own
session; they are never edited here.

Execution configuration is not a choice made here — the rules file prescribes it: advanced mode,
in-place, and NO inference. That last point has a consequence worth stating, because it silently
changes results: symmetric predicates such as the intersection operator's co-occurrence link are
NOT inferred in both directions. A consumer asserting only one direction gets a half-populated
result and no error. PIB asserts both directions explicitly.

Usage:
    python3 03-tooling/operator_rule_runner_v1_0_0.py [data.ttl ...]
Defaults to PIB's own wiring-expression ontology when no argument is given.
"""
import sys, os, glob

RULES_DIR = os.path.join(os.path.dirname(__file__), "..", "11-vendored-operator-rules")
DEFAULT_DATA = [os.path.join(os.path.dirname(__file__), "..", "01-ontologies",
                             "pib_wiring_expressions_v1_0_0_1.ttl")]

VA = "http://example.org/variant-algebra#"


def run(data_paths, verbose=True):
    import rdflib
    from pyshacl import validate

    va = rdflib.Namespace(VA)
    data = rdflib.Graph()
    for p in data_paths:
        data.parse(p, format="turtle")
    before = len(data)

    shapes = rdflib.Graph()
    for p in sorted(glob.glob(os.path.join(RULES_DIR, "*.ttl"))):
        shapes.parse(p, format="turtle")

    # Exactly the configuration the rules file prescribes.
    validate(data, shacl_graph=shapes, advanced=True, inplace=True, inference="none")

    result = {
        "triples_before": before,
        "triples_after": len(data),
        "inferred": len(data) - before,
        "violated": sorted(str(s).split("#")[-1] for s in data.subjects(va.isViolated, rdflib.Literal(True))),
        "admissible": sorted(str(s).split("#")[-1] for s in data.subjects(va.isAdmissible, rdflib.Literal(True))),
        "prunable": sorted(str(s).split("#")[-1] for s in data.subjects(va.isPrunable, rdflib.Literal(True))),
        "result_members": sorted(f"{str(s).split('#')[-1]}->{str(o).split('#')[-1]}"
                                 for s, o in data.subject_objects(va.hasResultMember)),
        "emitted_members": sorted(f"{str(s).split('#')[-1]}->{str(o).split('#')[-1]}"
                                  for s, o in data.subject_objects(va.hasEmittedMember)),
    }

    if verbose:
        print(f"  operator rules: 12 shapes, advanced=True inplace=True inference=none")
        print(f"  data: {before} triples in, {len(data)} out ({result['inferred']} inferred)")
        print(f"  violated constraints : {result['violated'] or 'none'}")
        print(f"  structurally sound   : {result['admissible'] or 'none'}")
        if result["result_members"]:
            print(f"  operator results     : {result['result_members']}")
        if result["emitted_members"]:
            print(f"  emitted after purge  : {result['emitted_members']}")
        if result["prunable"]:
            print(f"  pruned candidates    : {result['prunable']}")
    return result


FIXTURES = os.path.join(os.path.dirname(__file__), "..", "12-operator-fixtures")


def self_test():
    """Prove the rules have teeth, the same way the wiring validator's self-test does.

    A satisfying candidate legitimately infers NOTHING — these rules construct a violation
    marker and stay silent otherwise. So "nothing was inferred" cannot be read as a failure;
    only the negative fixture can show the rules actually fire.
    """
    expr = DEFAULT_DATA[0]
    pos = os.path.join(FIXTURES, "candidate_positive_v1_0_0.ttl")
    neg = os.path.join(FIXTURES, "candidate_negative_v1_0_0.ttl")
    print("  self-test: satisfying candidate")
    rp = run([expr, pos], verbose=False)
    print(f"    violations: {rp['violated'] or 'none'}   (expected none)")
    print("  self-test: violating candidate (three facets against a budget of two, two graders)")
    rn = run([expr, neg], verbose=False)
    print(f"    violations: {rn['violated'] or 'none'}   (expected both constraints)")
    ok = (not rp["violated"]) and len(rn["violated"]) >= 2
    print(f"  rules have teeth: {ok}")
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv or len(sys.argv) == 1:
        print("PIB operator rule runner v1.0.0")
        return self_test()
    print("PIB operator rule runner v1.0.0")
    r = run([a for a in sys.argv[1:] if not a.startswith("--")])
    if r["violated"]:
        print("  GATE: FAIL — a wiring expression is violated")
        return 1
    print("  GATE: PASS — no wiring expression violated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
