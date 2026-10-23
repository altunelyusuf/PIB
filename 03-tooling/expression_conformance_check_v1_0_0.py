#!/usr/bin/env python3
"""
PIB Expression Conformance Check v1.0.0 — wiring expressions, evaluated by the algebra's own rules
==================================================================================================
A wiring expression is written in the form the algebra's rules read, so the algebra can say what it
admits. Two rules in PIB's SHACL (`pibx:ExpressionComponentRuleShape`, `pibx:ExpressionFeatureRuleShape`)
gather the expressions that govern one wiring into one component; the algebra's vendored rules and
runner do the rest. Nothing here decides what an expression means: this file loads, runs, reads back,
and compares.

What it compares against, and why that is not circular: the two candidate files in
`12-operator-fixtures/fixtures/` are written by hand, one that satisfies the capstone constraints and one
that breaks two of them. The positive candidate's selection must be one of the variants the rules
produce, and the negative one's must not.

Usage:
    python3 03-tooling/expression_conformance_check_v1_0_0.py
    python3 03-tooling/expression_conformance_check_v1_0_0.py --self-test
"""
import os, sys, glob, importlib.util
import rdflib
import pyoxigraph as ox

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VENDORED = os.path.join(ROOT, "11-vendored-operator-rules", "vendored")
ABOX = os.path.join(ROOT, "01-ontologies", "pib_abox_v1_0_0.ttl")
SHACL = os.path.join(ROOT, "02-shacl-safeguards", "pib_shacl_v1_0_0.ttl")
FIX = os.path.join(ROOT, "12-operator-fixtures", "fixtures")
POSITIVE = os.path.join(FIX, "candidate_positive_v1_0_0.ttl")
NEGATIVE = os.path.join(FIX, "candidate_negative_v1_0_0.ttl")
PIBX = "http://purl.org/pib/wiring-expression#"
VA = "http://example.org/variant-algebra#"
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def _executor():
    spec = importlib.util.spec_from_file_location("vaf_rule_executor", os.path.join(VENDORED, "variant_rule_executor_v1_0_0.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def _rules_graph():
    """The algebra's vendored rules plus PIB's own expression shapes (the shapes in the wiring-expression namespace only)."""
    g = rdflib.Graph()
    for f in sorted(glob.glob(os.path.join(VENDORED, "*.ttl"))):
        g.parse(f, format="turtle")
    own = rdflib.Graph().parse(SHACL, format="turtle")
    for shape in set(own.subjects(SH.rule, None)):
        if str(shape).startswith(PIBX):
            stack = [shape]
            while stack:
                n = stack.pop()
                for p, o in own.predicate_objects(n):
                    g.add((n, p, o))
                    if isinstance(o, rdflib.BNode):
                        stack.append(o)
    return g


def variants(abox_graph):
    """Run the rules over the expressions in the graph; return ({component: [set of feature local names]}, raw count)."""
    ex = _executor()
    rules = ex.compile_rules(_rules_graph())
    staging = ox.Store(); staging.load(abox_graph.serialize(format="turtle").encode("utf-8"), format=ox.RdfFormat.TURTLE)
    sk = lambda t: ox.NamedNode("urn:pib:node:" + t.value) if isinstance(t, ox.BlankNode) else t
    store = ox.Store(); store.extend(ox.Quad(sk(q.subject), q.predicate, sk(q.object)) for q in staging)
    ex.run(store, rules)
    pfx = "PREFIX va: <" + VA + ">\n"
    sets = set()
    rows = store.query(pfx + """
        SELECT ?v (GROUP_CONCAT(?f; separator=",") AS ?fs) WHERE {
            ?v a va:Variant ; va:hasAssignment ?a .
            ?a va:assignedFeature ?x ; va:assignedCount ?k . FILTER(?k > 0)
            BIND(REPLACE(STR(?x), "^.*#", "") AS ?f) } GROUP BY ?v""")
    for r in rows:
        sets.add(frozenset(r["fs"].value.split(",")) if r["fs"].value else frozenset())
    total = int(list(store.query(pfx + "SELECT (COUNT(?v) AS ?n) WHERE { ?v a va:Variant }"))[0]["n"].value)
    if total == len(sets) + 1:
        sets.add(frozenset())
    return sets, total, store


def selection(path):
    """The names a candidate file selects (va:isSelected true)."""
    g = rdflib.Graph().parse(path, format="turtle")
    return frozenset(str(s).split("#")[-1] for s in g.subjects(rdflib.URIRef(VA + "isSelected"), rdflib.Literal(True)))


def run(abox=None, verbose=True, mutate=None, positive=None, negative=None):
    g = abox if abox is not None else rdflib.Graph().parse(ABOX, format="turtle")
    if mutate:
        mutate(g)
    sets, total, _ = variants(g)
    pos, neg = selection(positive or POSITIVE), selection(negative or NEGATIVE)
    bad = 0
    if verbose:
        print("PIB expression conformance check v1.0.0 — wiring expressions evaluated by the algebra's rules")
        print(f"  the capstone wiring admits {total} variants")
    for label, sel, want in (("positive candidate", pos, True), ("negative candidate", neg, False)):
        got = sel in sets
        ok = got == want
        bad += 0 if ok else 1
        if verbose:
            print(f"  {label:20} {'admitted' if got else 'refused':9} expected {'admitted' if want else 'refused':9} {'ok' if ok else 'DISAGREE'}")
    if total == 0:
        bad += 1
        if verbose: print("  no variants at all — the expressions were not read")
    return bad


NESTED = """@prefix va: <http://example.org/variant-algebra#> . @prefix pibx: <http://purl.org/pib/wiring-expression#> . @prefix t: <urn:t#> .
t:E a pibx:WiringExpression ; pibx:governsWiring t:W ; pibx:hasRootApplication t:Root .
t:Root a pibx:OperatorApplication, va:AdditionOperator ; va:hasLeftOperand t:Ex ; va:hasRightOperand t:x .
t:Ex a pibx:OperatorApplication, va:ExclusiveOperator ; va:hasLeftOperand t:p ; va:hasRightOperand t:a .
"""


def _refuses(ttl):
    """Does PIB's operand-form shape report the graph? (The shape is validated alone, over just this graph.)"""
    import pyshacl
    shapes = rdflib.Graph().parse(SHACL, format="turtle")
    only = rdflib.Graph()
    stack = [rdflib.URIRef(PIBX + "OperandFormShape")]
    while stack:
        n = stack.pop()
        for p, o in shapes.predicate_objects(n):
            only.add((n, p, o))
            if isinstance(o, rdflib.BNode): stack.append(o)
    conforms, _, _ = pyshacl.validate(rdflib.Graph().parse(data=ttl, format="turtle"), shacl_graph=only, inference="none")
    return not conforms


def self_test():
    """The check must be able to fail, in both directions."""
    print("PIB expression conformance check v1.0.0 — self-test")
    base = run(verbose=False)
    print(f"  as published: {base} disagreement(s)   (expected 0)")

    def tighten(g):   # a budget of one: the positive candidate (two facets) is no longer admissible
        VAN = rdflib.URIRef(VA + "hasMaxRepetitions")
        node = rdflib.URIRef(PIBX + "MeasurementBudgetApp")
        g.remove((node, VAN, None)); g.add((node, VAN, rdflib.Literal(1)))
    t = run(verbose=False, mutate=tighten)
    print(f"  budget tightened to one: {t} disagreement(s)   (expected >0)")

    def loosen(g):    # a budget of three: the negative candidate (three facets and two graders) still breaks the grader rule
        VAN = rdflib.URIRef(VA + "hasMaxRepetitions")
        node = rdflib.URIRef(PIBX + "MeasurementBudgetApp")
        g.remove((node, VAN, None)); g.add((node, VAN, rdflib.Literal(3)))
    l = run(verbose=False, mutate=loosen)
    print(f"  budget loosened to three: {l} disagreement(s)   (expected 0, the grader rule still refuses the negative)")

    def drop_grader(g):   # without the grading expression the negative candidate's three facets are still refused, but two graders would be admitted
        g.remove((rdflib.URIRef(PIBX + "CapstoneGraderExpression"), rdflib.URIRef(PIBX + "governsWiring"), None))
    d = run(verbose=False, mutate=drop_grader)
    print(f"  grading expression unbound: {d} disagreement(s)   (expected >0)")

    def unread(g):    # an expression whose root is gone: nothing is read, and the check must say so
        g.remove((None, rdflib.URIRef(PIBX + "hasRootApplication"), None))
    u = run(verbose=False, mutate=unread)
    print(f"  no root applications: {u} disagreement(s)   (expected >0)")
    # a nested expression, in the binary form the rules read: an addition of an exclusive and a feature means
    # one of the two exclusive features together with the third (the algebra's own wording: addition inside an
    # expression is co-inclusion, both operands present), so exactly two variants: {p, x} and {a, x}
    nested = rdflib.Graph().parse(data=NESTED, format="turtle")
    ns, nt, _ = variants(nested)
    nest_ok = ns == {frozenset({"p", "x"}), frozenset({"a", "x"})} and nt == 2
    print(f"  nested addition of an exclusive and a feature: {sorted(map(sorted, ns))}   (expected [['a','x'],['p','x']]) {'ok' if nest_ok else 'WRONG'}")
    # an expression node given with the unordered operand predicate is refused by the shape, not half-read
    refused = _refuses(NESTED.replace("va:hasLeftOperand t:Ex ; va:hasRightOperand t:x", "va:hasOperand t:Ex, t:x"))
    print(f"  the same node with unordered operands is refused by the operand-form shape: {refused}   (expected True)")
    accepted = not _refuses(NESTED)
    print(f"  the published form is not refused: {accepted}   (expected True)")
    ok = base == 0 and t > 0 and l == 0 and d > 0 and u > 0 and nest_ok and refused and accepted
    print(f"  the check can fail in both directions: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(1 if run() else 0)
