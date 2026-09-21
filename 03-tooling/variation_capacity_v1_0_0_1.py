#!/usr/bin/env python3
"""
PIB Variation Capacity — ontology-native v1.0.0.1
=================================================
v1.0.0.1 (PATCH): the per-profile variation spaces now live in ONE consolidated file, so the
self-test checks every space BY NAME. v1.0.0 took whichever result came first, which was correct
only while each file held a single space — with several spaces in one graph it could silently
compare the wrong space against the expected number. No change to the rules or the calculation.

Computes a wiring space's Variation Capacity entirely in the ontology.

What is NOT here, deliberately: no enumeration, no constraint evaluation, no admissibility
logic, no counting logic. Every one of those lives in SHACL rules and SPARQL. This file is a
harness in the ordinary programming sense — it loads graphs, re-invokes the rule engine until
the graph stops growing, runs one counting query, and prints. If a constraint's meaning ever
needs changing, it is changed in `02-shacl-safeguards/pib_enumeration_rules_v1_0_0.ttl`, not
here.

Why the loop: generation branches one feature at a time, so a space of n features needs n
passes to reach complete candidates. The rule engine available here executes each rule once
per invocation and exposes no fixpoint option, so the harness supplies the iteration. The loop
carries no algebra — it stops when the rules stop producing triples.

Usage:
    python3 03-tooling/variation_capacity_v1_0_0_1.py <space.ttl> [...]
    python3 03-tooling/variation_capacity_v1_0_0_1.py --self-test
"""
import sys, os

RULES = os.path.join(os.path.dirname(__file__), "..", "02-shacl-safeguards",
                     "pib_enumeration_rules_v1_0_0.ttl")
FIXTURES = os.path.join(os.path.dirname(__file__), "..", "12-operator-fixtures")

COUNT_QUERY = """
PREFIX pibe: <http://purl.org/pib/enumeration#>
SELECT ?space (COUNT(DISTINCT ?c) AS ?capacity) WHERE {
    ?c a pibe:CompleteCandidate ; pibe:inSpace ?space .
    FILTER NOT EXISTS { ?c pibe:isInadmissible true }
} GROUP BY ?space
"""

TOTAL_QUERY = """
PREFIX pibe: <http://purl.org/pib/enumeration#>
SELECT ?space (COUNT(DISTINCT ?c) AS ?total) WHERE {
    ?c a pibe:CompleteCandidate ; pibe:inSpace ?space .
} GROUP BY ?space
"""


def compute(space_paths, max_passes=64, verbose=True):
    import rdflib
    from pyshacl import validate

    data = rdflib.Graph()
    for p in space_paths:
        data.parse(p, format="turtle")
    shapes = rdflib.Graph()
    shapes.parse(RULES, format="turtle")

    passes, previous = 0, -1
    while len(data) != previous and passes < max_passes:
        previous = len(data)
        validate(data, shacl_graph=shapes, advanced=True, inplace=True, inference="none")
        passes += 1

    results = {}
    for row in data.query(COUNT_QUERY):
        results[str(row[0])] = int(row[1])
    totals = {str(r[0]): int(r[1]) for r in data.query(TOTAL_QUERY)}

    if verbose:
        print(f"  rule passes to fixpoint: {passes}   graph: {len(data)} triples")
        for space, cap in sorted(results.items()):
            name = space.split("#")[-1]
            print(f"  {name}: complete candidates {totals.get(space, 0)}, "
                  f"Variation Capacity (admissible) {cap}")
    return results, totals


SPACES = os.path.join(FIXTURES, "profile_variation_spaces_v1_0_0.ttl")
EX = "http://purl.org/pib/example#"

# Reference answers, checked space by space. The capstone figure is the pinned engine's own answer,
# kept as the number the ontology must keep reproducing.
EXPECTED = {
    EX + "CapstoneSpace":             (64, 9),
    EX + "OntologyDevelopmentSpace":  (8, 1),
}


def self_test():
    """Every declared space must reproduce its reference answer, looked up by the space's name.

    A space missing from the results is a failure, not a pass: silence cannot count as agreement.
    """
    results, totals = compute([SPACES], verbose=True)
    ok = True
    for space, (exp_total, exp_cap) in EXPECTED.items():
        name = space.split("#")[-1]
        got_total, got_cap = totals.get(space), results.get(space)
        match = (got_total == exp_total) and (got_cap == exp_cap)
        ok &= match
        print(f"  {name}: expected {exp_total} complete / capacity {exp_cap}; "
              f"got {got_total} / {got_cap}  -> {'match' if match else 'MISMATCH'}")
    unexpected = sorted(set(totals) - set(EXPECTED))
    if unexpected:
        print(f"  note: spaces without a reference answer, reported but not checked: "
              f"{[u.split('#')[-1] for u in unexpected]}")
    print(f"  every space reproduces its reference answer: {ok}")
    return 0 if ok else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    print("PIB variation capacity — computed in the ontology, v1.0.0.1")
    if "--self-test" in sys.argv or not args:
        return self_test()
    compute(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
