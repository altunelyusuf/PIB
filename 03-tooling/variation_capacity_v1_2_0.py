#!/usr/bin/env python3
"""
PIB Variation Capacity — ontology-native v1.2.0
===============================================
v1.2.0 (MINOR): runs the rules in the phases the rules file declares — partition, generation, check,
combine — in their declared order, each to a fixpoint. The capacity is no longer computed here: the
combine phase multiplies the group capacities in the ontology and this harness only reads the result.

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
needs changing, it is changed in `02-shacl-safeguards/pib_enumeration_rules_v2_1_0.ttl`, not
here.

Why the loop: generation branches one feature at a time, so a space of n features needs n
passes to reach complete candidates. The rule engine available here executes each rule once
per invocation and exposes no fixpoint option, so the harness supplies the iteration. The loop
carries no algebra — it stops when the rules stop producing triples.

Usage:
    python3 03-tooling/variation_capacity_v1_2_0.py <space.ttl> [...]
    python3 03-tooling/variation_capacity_v1_2_0.py --self-test
"""
import sys, os

RULES = os.path.join(os.path.dirname(__file__), "..", "02-shacl-safeguards",
                     "pib_enumeration_rules_v2_1_0.ttl")
FIXTURES = os.path.join(os.path.dirname(__file__), "..", "12-operator-fixtures")

CAPACITY_QUERY = """
PREFIX pibe: <http://purl.org/pib/enumeration#>
SELECT ?space ?cap WHERE { ?space pibe:variationCapacity ?cap . FILTER NOT EXISTS { ?space a pibe:GroupSpace } }
"""

COMPLETE_QUERY = """
PREFIX pibe: <http://purl.org/pib/enumeration#>
SELECT ?space (COUNT(DISTINCT ?c) AS ?n) WHERE {
    ?g pibe:groupOf ?space . ?c a pibe:CompleteCandidate ; pibe:inSpace ?g } GROUP BY ?space
"""

REJECTED_QUERY = """
PREFIX pibe: <http://purl.org/pib/enumeration#>
SELECT ?space (COUNT(DISTINCT ?c) AS ?n) WHERE {
    ?g pibe:groupOf ?space . ?c a pibe:CompleteCandidate ; pibe:inSpace ?g ; pibe:isInadmissible true } GROUP BY ?space
"""


def phased_shapes():
    """Split the rules file into one shapes graph per phase, in the order the rules file declares."""
    import rdflib
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    P = rdflib.Namespace("http://purl.org/pib/enumeration#")
    rules = rdflib.Graph(); rules.parse(RULES, format="turtle")
    order = [str(rules.value(ph, P.phaseName))
             for ph in sorted(rules.subjects(rdflib.RDF.type, P.Phase), key=lambda ph: int(rules.value(ph, P.phaseOrder)))]
    graphs = {name: rdflib.Graph() for name in order}
    for shape in rules.subjects(rdflib.RDF.type, SH.NodeShape):
        phase = str(rules.value(shape, P.phase) or "")
        if phase not in graphs:
            raise ValueError(f"rule shape {shape} declares no known phase")
        stack, seen = [shape], set()
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x)
            for pr, o in rules.predicate_objects(x):
                graphs[phase].add((x, pr, o))
                if isinstance(o, rdflib.BNode): stack.append(o)
    return [(name, graphs[name]) for name in order]


def compute(space_paths, max_passes=64, verbose=True):
    import rdflib
    from pyshacl import validate

    data = rdflib.Graph()
    for p in space_paths:
        data.parse(p, format="turtle")
    passes = 0
    for name, shapes in phased_shapes():
        previous = -1
        while len(data) != previous and passes < max_passes:
            previous = len(data)
            validate(data, shacl_graph=shapes, advanced=True, inplace=True, inference="none")
            passes += 1

    results = {str(r[0]): int(r[1]) for r in data.query(CAPACITY_QUERY)}
    totals = {str(r[0]): int(r[1]) for r in data.query(COMPLETE_QUERY)}
    rejected = {str(r[0]): int(r[1]) for r in data.query(REJECTED_QUERY)}

    if verbose:
        print(f"  rule passes to fixpoint: {passes}   graph: {len(data)} triples")
        for space, cap in sorted(results.items()):
            name = space.split("#")[-1]
            print(f"  {name}: complete candidates across its groups {totals.get(space, 0)}, "
                  f"rejected {rejected.get(space, 0)}, Variation Capacity {cap}")
    return results, totals, rejected


SPACES = os.path.join(FIXTURES, "profile_variation_spaces_v1_0_0.ttl")
EX = "http://purl.org/pib/example#"

# Reference answers, checked space by space. The capstone figure is the pinned engine's own answer,
# kept as the number the ontology must keep reproducing.
#
# v1.1.0: only the CAPACITY is a reference answer. v1.0.0 also pinned the number of complete candidates
# (64 and 8), but that was a by-product of generating every 2^n selection, not an answer — with pruning it
# legitimately falls to the admissible count. It is replaced by a stronger check: every complete candidate
# must be admissible, which holds only if pruning is exact. v1.2.0: with partitioning, complete candidates
# are counted per group while the capacity is their product, so exactness is checked directly as "no
# complete candidate was rejected" rather than as "complete candidates equal the capacity".
EXPECTED = {
    EX + "CapstoneSpace":             9,
    EX + "OntologyDevelopmentSpace":  1,
}

# Conformance cases with independently known capacities (see the fixture's header for derivations).
# Budget2of4 guards PIB's one deliberate difference from the algebra's decomposition: budget contributors
# are coupled. Following the algebra's rule literally gives 16 here, with no error — measured, v1.2.0.
CONFORMANCE = os.path.join(FIXTURES, "enumeration_conformance_spaces_v1_0_0.ttl")
CONFORMANCE_EXPECTED = {
    EX + "Budget2of4": 11, EX + "LaterPrereq": 6, EX + "OrSpread": 12,
    EX + "Combined": 3, EX + "Independent5": 243, EX + "Unsatisfiable": 0,
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
    checks = dict(phased_shapes())["check"]
    validate(g, shacl_graph=checks, advanced=True, inplace=True, inference="none")
    return (c, PIBE.isInadmissible, rdflib.Literal(True)) in g


def _check(label, path, expected):
    results, totals, rejected = compute([path], verbose=False)
    ok = True
    print(f"  {label}:")
    for space, exp_cap in expected.items():
        name = space.split("#")[-1]
        got_cap, n_complete, n_rejected = results.get(space), totals.get(space), rejected.get(space, 0)
        # With partitioning, complete candidates are per group and the capacity is their PRODUCT, so the
        # two counts legitimately differ. What must hold is that pruning is exact: no complete candidate in
        # any group is inadmissible — measured directly as the rejected count. A space that generated no
        # candidates at all is a failure, never a pass.
        exact = n_complete is not None and n_rejected == 0
        match = (got_cap == exp_cap) and exact
        ok &= match
        state = ("NO CANDIDATES GENERATED" if n_complete is None else
                 f"{n_rejected} INADMISSIBLE SURVIVED PRUNING" if n_rejected else "pruning exact")
        print(f"    {name:26s} expected {exp_cap:>4}  got {str(got_cap):>4}  from {n_complete} candidates "
              f"({state})  -> {'match' if match else 'MISMATCH'}")
    return ok


def self_test():
    """Every declared space must reproduce its known capacity, looked up by name."""
    ok = _check("profile spaces", SPACES, EXPECTED)
    ok = _check("conformance spaces", CONFORMANCE, CONFORMANCE_EXPECTED) and ok
    net = check_net_has_teeth()
    print(f"  safety-net checks reject a planted inadmissible candidate: {net}")
    ok = ok and net
    print(f"  every space reproduces its known capacity: {ok}")
    return 0 if ok else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    print("PIB variation capacity — computed in the ontology, v1.2.0")
    if "--self-test" in sys.argv or not args:
        return self_test()
    compute(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
