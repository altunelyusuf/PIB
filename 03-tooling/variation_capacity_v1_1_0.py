#!/usr/bin/env python3
"""
PIB Variation Capacity — ontology-native v1.1.0
===============================================
v1.1.0 (MINOR): runs the rules in two phases, read from each shape's declared phase in the rules file
(generation to a fixpoint, then the checks once) rather than every rule on every pass. Paired with
enumeration rules v2.0.0, which prune as they generate. Same answers; median 21.5 s -> 4.7 s on the
real profile spaces. The self-test additionally plants one inadmissible candidate, because with exact
pruning the checks never reject anything in a normal run — so a normal run cannot show they still work.

v1.0.0.1 (PATCH): the per-profile variation spaces now live in ONE consolidated file, so the
self-test checks every space BY NAME. v1.0.0 took whichever result came first, which was correct
only while each file held a single space — with several spaces in one graph it could silently
compare the wrong space against the expected number. No change to the rules or the calculation.

Computes a wiring space's Variation Capacity entirely in the ontology.

What is NOT here, deliberately: no enumeration, no constraint evaluation, no admissibility
logic, no counting logic. Every one of those lives in SHACL rules and SPARQL. This file is a
harness in the ordinary programming sense — it loads graphs, re-invokes the rule engine until
the graph stops growing, runs one counting query, and prints. If a constraint's meaning ever
needs changing, it is changed in `02-shacl-safeguards/pib_enumeration_rules_v2_0_0.ttl`, not
here.

Why the loop: generation branches one feature at a time, so a space of n features needs n
passes to reach complete candidates. The rule engine available here executes each rule once
per invocation and exposes no fixpoint option, so the harness supplies the iteration. The loop
carries no algebra — it stops when the rules stop producing triples.

Usage:
    python3 03-tooling/variation_capacity_v1_1_0.py <space.ttl> [...]
    python3 03-tooling/variation_capacity_v1_1_0.py --self-test
"""
import sys, os

RULES = os.path.join(os.path.dirname(__file__), "..", "02-shacl-safeguards",
                     "pib_enumeration_rules_v2_0_0.ttl")
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


def phased_shapes():
    """Split the rules file into its generation and check shapes, by each shape's declared phase."""
    import rdflib
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    PHASE = rdflib.URIRef("http://purl.org/pib/enumeration#phase")
    rules = rdflib.Graph(); rules.parse(RULES, format="turtle")
    out = {"generation": rdflib.Graph(), "check": rdflib.Graph()}
    for shape in rules.subjects(rdflib.RDF.type, SH.NodeShape):
        phase = str(rules.value(shape, PHASE) or "")
        if phase not in out:
            raise ValueError(f"rule shape {shape} declares no known phase")
        stack, seen = [shape], set()
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x)
            for pr, o in rules.predicate_objects(x):
                out[phase].add((x, pr, o))
                if isinstance(o, rdflib.BNode): stack.append(o)
    return out["generation"], out["check"]


def compute(space_paths, max_passes=64, verbose=True):
    import rdflib
    from pyshacl import validate

    data = rdflib.Graph()
    for p in space_paths:
        data.parse(p, format="turtle")
    generation, checks = phased_shapes()

    passes, previous = 0, -1
    while len(data) != previous and passes < max_passes:
        previous = len(data)
        validate(data, shacl_graph=generation, advanced=True, inplace=True, inference="none")
        passes += 1
    validate(data, shacl_graph=checks, advanced=True, inplace=True, inference="none")

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
#
# v1.1.0: only the CAPACITY is a reference answer. v1.0.0 also pinned the number of complete candidates
# (64 and 8), but that was a by-product of generating every 2^n selection, not an answer — with pruning it
# legitimately falls to the admissible count. It is replaced by a stronger check: every complete candidate
# must be admissible, which holds only if pruning is exact.
EXPECTED = {
    EX + "CapstoneSpace":             9,
    EX + "OntologyDevelopmentSpace":  1,
}


def check_net_has_teeth():
    """Plant one complete candidate that breaks the capstone's exclusive constraint; the checks must reject it."""
    import rdflib
    from pyshacl import validate
    g = rdflib.Graph(); g.parse(SPACES, format="turtle")
    PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
    c = rdflib.URIRef(EX + "PlantedInadmissible")
    g.add((c, rdflib.RDF.type, PIBE.Candidate)); g.add((c, rdflib.RDF.type, PIBE.CompleteCandidate))
    g.add((c, PIBE.inSpace, rdflib.URIRef(EX + "CapstoneSpace")))
    for f in ("f1_o4sdlc_produces_ad", "f2_radar_consumes_ad", "f3_radar_measures", "f4_pamg_measures", "f5_o4ucm_analysis"):
        g.add((c, PIBE.includes, rdflib.URIRef(EX + f)))          # two measurers at once: must be rejected
    _, checks = phased_shapes()
    validate(g, shacl_graph=checks, advanced=True, inplace=True, inference="none")
    return (c, PIBE.isInadmissible, rdflib.Literal(True)) in g


def self_test():
    """Every declared space must reproduce its reference answer, looked up by the space's name.

    A space missing from the results is a failure, not a pass: silence cannot count as agreement.
    """
    results, totals = compute([SPACES], verbose=True)
    ok = True
    for space, exp_cap in EXPECTED.items():
        name = space.split("#")[-1]
        got_total, got_cap = totals.get(space), results.get(space)
        exact = got_total == got_cap
        match = (got_cap == exp_cap) and exact
        ok &= match
        print(f"  {name}: expected capacity {exp_cap}; got {got_cap}, from {got_total} complete candidates "
              f"({'pruning exact' if exact else 'INADMISSIBLE CANDIDATES SURVIVED PRUNING'})  -> "
              f"{'match' if match else 'MISMATCH'}")
    unexpected = sorted(set(totals) - set(EXPECTED))
    if unexpected:
        print(f"  note: spaces without a reference answer, reported but not checked: "
              f"{[u.split('#')[-1] for u in unexpected]}")
    print(f"  every space reproduces its reference answer: {ok}")
    net = check_net_has_teeth()
    print(f"  safety-net checks reject a planted inadmissible candidate: {net}")
    ok = ok and net
    return 0 if ok else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    print("PIB variation capacity — computed in the ontology, v1.1.0")
    if "--self-test" in sys.argv or not args:
        return self_test()
    compute(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
