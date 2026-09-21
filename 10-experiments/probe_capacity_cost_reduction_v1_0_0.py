#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.  Can PIB's ontology-native capacity computation be made cheaper?

Profiling showed where the ~20 s goes: the final pass costs the most while changing nothing; the
branching rule re-fires on every candidate every pass; the admissibility checks run on every pass;
and nothing is pruned, so candidates grow to 2^n. Each technique below targets one of those, and is
measured on its own so its contribution is visible.

A technique only counts if it reproduces the SAME answers: capstone 9, ontology development 1.
Faster-but-different is a bug, not an optimisation. This file is a harness; all logic is in rules.
"""
import time, re, statistics, rdflib, sys
from pyshacl import validate

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
GOVERNED = "02-shacl-safeguards/pib_enumeration_rules_v1_0_0.ttl"
OPTIMIZED = "10-experiments/pib_enumeration_generation_optimized_v1_0_0.ttl"
SPACES = "12-operator-fixtures/profile_variation_spaces_v1_0_0.ttl"
EXPECTED = {"CapstoneSpace": 9, "OntologyDevelopmentSpace": 1}
GEN_NAMES = {"SeedRuleShape", "BranchRuleShape", "InheritRuleShape", "CompleteRuleShape"}

COUNT = """PREFIX pibe: <http://purl.org/pib/enumeration#>
SELECT ?space (COUNT(DISTINCT ?c) AS ?n) (COUNT(DISTINCT ?b) AS ?bad)
WHERE { ?c a pibe:CompleteCandidate ; pibe:inSpace ?space .
        OPTIONAL { ?c pibe:isInadmissible true . BIND(?c AS ?b) } } GROUP BY ?space"""


def subgraph(shapes, keep):
    """Copy the named shapes (and their blank-node bodies) into a new shapes graph."""
    out = rdflib.Graph()
    for s in shapes.subjects(rdflib.RDF.type, SH.NodeShape):
        if str(s).split("#")[-1] not in keep:
            continue
        stack, seen = [s], set()
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x)
            for p, o in shapes.predicate_objects(x):
                out.add((x, p, o))
                if isinstance(o, rdflib.BNode): stack.append(o)
    return out


def fixpoint(data, shapes):
    prev, passes = -1, 0
    while len(data) != prev:
        prev = len(data)
        validate(data, shacl_graph=shapes, advanced=True, inplace=True, inference="none")
        passes += 1
    return passes


def run(variant, spaces=SPACES):
    gov = rdflib.Graph(); gov.parse(GOVERNED, format="turtle")
    names = {str(s).split("#")[-1] for s in gov.subjects(rdflib.RDF.type, SH.NodeShape)}
    checks = subgraph(gov, names - GEN_NAMES)
    data = rdflib.Graph(); data.parse(spaces, format="turtle")
    t = time.perf_counter()
    if variant == "V0":
        passes = fixpoint(data, gov)                       # current: everything, every pass
    else:
        if variant == "V1":
            gen = subgraph(gov, GEN_NAMES)                 # current generation, checks once after
        else:
            txt = open(OPTIMIZED).read()                  # V4: the file as written
            if variant in ("V2", "V3"):                    # without frontier targeting: visit every candidate
                txt = re.sub(r'sh:target \[ a sh:SPARQLTarget ; sh:select """.*?""" \] ;',
                             "sh:targetClass pibe:Candidate ;", txt, flags=re.S)
            if variant == "V2":                            # and without pruning
                txt = re.sub(r"\n\s+# (exclusive|mandatory):.*?(?=\n\s+OPTIONAL)", "", txt, flags=re.S)
            gen = rdflib.Graph(); gen.parse(data=txt, format="turtle")
        passes = fixpoint(data, gen)
        validate(data, shacl_graph=checks, advanced=True, inplace=True, inference="none")
    ms = (time.perf_counter() - t) * 1000
    res = {str(r[0]).split("#")[-1]: (int(r[1]), int(r[2])) for r in data.query(COUNT)}
    cands = len(set(data.subjects(rdflib.RDF.type, rdflib.URIRef("http://purl.org/pib/enumeration#Candidate"))))
    return ms, passes, cands, res


if __name__ == "__main__":
    label = {"V0": "current rules, everything every pass",
             "V1": "+ checks run once, after generation",
             "V2": "+ branch once, inherit atomically",
             "V3": "+ prune branches that already break a constraint",
             "V4": "+ engine visits only the frontier"}
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"{'variant':52s} {'ms':>8s} {'passes':>6s} {'cands':>6s}  capacity (complete / rejected)    same answer?")
    for v in ["V0", "V1", "V2", "V3", "V4"]:
        times = []
        for _ in range(reps if v != "V0" else 1):
            ms, passes, cands, res = run(v); times.append(ms)
        cap = {k: n - bad for k, (n, bad) in res.items()}
        same = cap == EXPECTED
        detail = "  ".join(f"{k[:9]} {n - bad} ({n}/{bad})" for k, (n, bad) in sorted(res.items()))
        print(f"{v} {label[v]:49s} {statistics.median(times):8.0f} {passes:6d} {cands:6d}  {detail:34s} {same}")


# ---------------------------------------------------------------------------------------------------
# Scaling. A constant-factor saving is not the question; growth is. Spaces are built from k independent
# groups of two features under an exclusive constraint: each group admits exactly 3 choices (neither,
# one, the other), so the true capacity is 3^k and the unpruned candidate count is 2^(2k).
# ---------------------------------------------------------------------------------------------------

def synthetic_space(k, name="Scale"):
    lines = ["@prefix pibe: <http://purl.org/pib/enumeration#> .",
             "@prefix ex: <http://purl.org/pib/example#> ."]
    feats = [f"ex:{name}{k}_f{i}" for i in range(1, 2 * k + 1)]
    lines.append(f"ex:{name}{k} a pibe:VariationSpace ; pibe:featureCount {2*k} ; pibe:hasFeature {', '.join(feats)} .")
    for i, f in enumerate(feats, 1):
        lines.append(f"{f} pibe:featureIndex {i} .")
    for g in range(k):
        a, b = feats[2 * g], feats[2 * g + 1]
        lines.append(f"ex:{name}{k}_x{g} a pibe:ExclusiveConstraint ; pibe:inSpace ex:{name}{k} ; pibe:groupMember {a}, {b} .")
    path = f"/tmp/scale_{name}{k}.ttl"
    open(path, "w").write("\n".join(lines) + "\n")
    return path


def scaling(ks, variants, budget_s=240):
    import signal
    print(f"\n{'k groups':>8s} {'features':>8s} {'true cap':>8s} " + " ".join(f"{v+' ms':>10s} {v+' cands':>9s}" for v in variants))
    for k in ks:
        path = synthetic_space(k)
        row = f"{k:8d} {2*k:8d} {3**k:8d} "
        for v in variants:
            def _timeout(*_): raise TimeoutError
            signal.signal(signal.SIGALRM, _timeout); signal.alarm(budget_s)
            try:
                ms, passes, cands, res = run(v, spaces=path)
                cap = sum(n - bad for n, bad in res.values())
                ok = "" if cap == 3 ** k else f"!{cap}"
                row += f"{ms:10.0f} {cands:9d}{ok} "
            except TimeoutError:
                row += f"{'>'+str(budget_s)+'s':>10s} {'-':>9s} "
            finally:
                signal.alarm(0)
        print(row)
