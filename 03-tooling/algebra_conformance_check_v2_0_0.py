#!/usr/bin/env python3
"""
PIB Algebra Conformance Check v2.0.0 — against the algebra's ONTOLOGY rules
==========================================================================
Checks every admissibility verdict PIB reaches against the variant algebra's own **ontology rules**, the
ones PIB already vendors, run by a SHACL engine. No Python enumerator is consulted.

Why v1.0.0 was replaced rather than kept: it used the algebra's Python enumerator as the oracle. The
calculus is implemented as ontology rules, and a second implementation — even the owner's own Python one —
is a second source of truth. Checking against it proves agreement with a program, not with the calculus
that other domains will consume.

What is compared, per candidate and not in aggregate: PIB enumerates candidates and marks each admissible
or not. For each candidate the same selection is expressed in the algebra's own vocabulary — members
lists, dependent and prerequisite sets, contributes-to groups, selection markers — and the algebra's
shipped rules are run over it. The algebra's `isViolated` verdict must equal PIB's `isInadmissible`
verdict. A capacity that matched with different candidates admitted would be a false pass.

Semantics are taken from the rules themselves, not assumed:
  exclusive            violated when two members are selected — at most one
  exclusive, unwrapped additionally violated when none is selected — exactly one, unless an optional
                       wraps it via hasInnerOperator, which is how at-most-one is expressed
  or                   violated when none is selected
  dependency           violated when a dependent is selected without its prerequisite
  repetition           violated when selections contributing to a group exceed the budget

**Mandatory has no rule in the algebra's shipped set.** It is a notation convention there — a bare,
undecorated name. So mandatory verdicts cannot be cross-checked against the algebra, and this tool says so
rather than quietly counting them as agreements.

Usage: python3 03-tooling/algebra_conformance_check_v2_0_0.py [spaces.ttl ...]
"""
import os, sys, glob, importlib.util
import rdflib
from rdflib import Literal
from rdflib.collection import Collection
from pyshacl import validate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
VA = rdflib.Namespace("http://example.org/variant-algebra#")
VENDORED = os.path.join(ROOT, "11-vendored-operator-rules")
DEFAULT = [os.path.join(ROOT, "12-operator-fixtures", "profile_variation_spaces_v1_0_0.ttl"),
           os.path.join(ROOT, "12-operator-fixtures", "enumeration_conformance_spaces_v1_0_0.ttl")]

_spec = importlib.util.spec_from_file_location("tx", os.path.join(HERE, "profile_taxonomy_v1_0_0.py"))
tx = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(tx)


def _algebra_rules():
    g = rdflib.Graph()
    for f in sorted(glob.glob(os.path.join(VENDORED, "*.ttl"))):
        g.parse(f, format="turtle")
    return g


def algebra_verdict(graph, space, selected, rules):
    """Express one candidate in the algebra's vocabulary and let ITS rules decide. Returns
    (violated, checked_kinds, unmatched_kinds)."""
    g = rdflib.Graph()
    checked, unmatched = set(), set()
    for f in graph.objects(space, PIBE.hasFeature):
        if f in selected:
            g.add((f, VA.isSelected, Literal(True)))
    for c in graph.subjects(PIBE.inSpace, space):
        kinds = set(graph.objects(c, rdflib.RDF.type))
        if PIBE.ExclusiveConstraint in kinds:
            ms = list(graph.objects(c, PIBE.groupMember))
            node = rdflib.BNode(); Collection(g, node, ms)
            g.add((c, rdflib.RDF.type, VA.ExclusiveOperator)); g.add((c, VA.members, node))
            # PIB's exclusive is AT MOST ONE: expressed here as the algebra expresses it — wrapped by an
            # optional, which its own at-least-one rule tests for via hasInnerOperator.
            wrap = rdflib.BNode()
            g.add((wrap, rdflib.RDF.type, VA.OptionalOperator)); g.add((wrap, VA.hasInnerOperator, c))
            checked.add("exclusive")
        elif PIBE.OrConstraint in kinds:
            ms = list(graph.objects(c, PIBE.groupMember))
            node = rdflib.BNode(); Collection(g, node, ms)
            g.add((c, rdflib.RDF.type, VA.OrOperator)); g.add((c, VA.members, node))
            checked.add("or")
        elif PIBE.DependencyConstraint in kinds:
            dep, pre = graph.value(c, PIBE.dependent), graph.value(c, PIBE.prerequisite)
            dn, pn = rdflib.BNode(), rdflib.BNode()
            Collection(g, dn, [dep]); Collection(g, pn, [pre])
            g.add((c, rdflib.RDF.type, VA.DependencyOperator))
            g.add((c, VA.dependentSet, dn)); g.add((c, VA.prerequisiteSet, pn))
            checked.add("dependency")
        elif PIBE.RepetitionConstraint in kinds:
            grp, mx = graph.value(c, PIBE.budgetGroup), graph.value(c, PIBE.maxSelected)
            g.add((c, rdflib.RDF.type, VA.RepetitionOperator))
            g.add((c, VA.appliesTo, grp)); g.add((c, VA.hasMaxRepetitions, mx))
            for f in graph.subjects(PIBE.contributesToGroup, grp):
                g.add((f, VA.contributesTo, grp))
            checked.add("repetition")
        elif PIBE.MandatoryConstraint in kinds:
            unmatched.add("mandatory")   # the algebra ships no rule for it: convention, not a rule
    validate(g, shacl_graph=rules, advanced=True, inplace=True, inference="none")
    violated = any(True for _ in g.subjects(VA.isViolated, Literal(True)))
    return violated, checked, unmatched


def run(paths=None, verbose=True, graphs=None):
    paths = paths or DEFAULT
    rules = _algebra_rules()
    agree = disagree = 0
    kinds_checked, kinds_unmatched = set(), set()
    if verbose:
        print("PIB algebra conformance check v2.0.0 — verdicts from the algebra's OWN ontology rules")
    for graph in (graphs if graphs is not None else [tx.build(p) for p in paths]):
        groups = [g for g in graph.subjects(PIBE.groupOf, None)]
        for grp in sorted(groups, key=str):
            cands = [c for c in graph.subjects(rdflib.RDF.type, PIBE.CompleteCandidate)
                     if (c, PIBE.inSpace, grp) in graph]
            for c in cands:
                sel = set(graph.objects(c, PIBE.includes))
                pib_bad = (c, PIBE.isInadmissible, Literal(True)) in graph
                alg_bad, ck, un = algebra_verdict(graph, grp, sel, rules)
                kinds_checked |= ck; kinds_unmatched |= un
                if un and not ck:
                    continue          # nothing the algebra can rule on; not counted either way
                if pib_bad == alg_bad:
                    agree += 1
                else:
                    disagree += 1
                    if verbose:
                        names = sorted(str(s).split("#")[-1] for s in sel)
                        print(f"  DISAGREE {str(grp).split('#')[-1]} :: {{{', '.join(names)}}} — "
                              f"PIB says {'inadmissible' if pib_bad else 'admissible'}, "
                              f"the algebra says {'violated' if alg_bad else 'not violated'}")
    if verbose:
        print(f"  candidates ruled on by the algebra's rules: {agree + disagree}")
        print(f"  operator kinds cross-checked: {sorted(kinds_checked)}")
        print(f"  operator kinds the algebra ships NO rule for, so not cross-checked: "
              f"{sorted(kinds_unmatched) or 'none'}")
        print(f"  agree {agree}, disagree {disagree}")
    return disagree


def self_test():
    """The check must report a disagreement when a verdict is actually wrong in the graph.

    Not a comparison of two constants: a real candidate's verdict is mutated — an inadmissible one is
    made to look admissible, and vice versa — and the check is re-run over the mutated graph.
    """
    import tempfile
    d = tempfile.mkdtemp()
    base = """@prefix pibe: <http://purl.org/pib/enumeration#> .
@prefix ex: <http://purl.org/pib/example#> .
ex:S a pibe:VariationSpace ; pibe:featureCount 2 ; pibe:hasFeature ex:a , ex:b .
ex:a pibe:featureIndex 1 . ex:b pibe:featureIndex 2 .
ex:x a pibe:ExclusiveConstraint ; pibe:inSpace ex:S ; pibe:groupMember ex:a , ex:b .
"""
    path = os.path.join(d, "s.ttl"); open(path, "w").write(base)
    print("PIB algebra conformance check — self-test")
    clean = run([path], verbose=False)
    print(f"  honest verdicts                                  -> {clean} disagreement(s) (expected 0)")

    # 1. PIB admits something the algebra rejects.
    #    Hiding an existing rejection is not possible here and saying so matters: exact pruning means no
    #    complete candidate is ever marked inadmissible — they are removed before completion. So the case
    #    is created the way the data allows, by making an ADMITTED candidate violate the constraint.
    g1 = tx.build(path)
    grp = next(iter(g1.subjects(PIBE.groupOf, None)))
    members = [m for c in g1.subjects(PIBE.inSpace, grp)
               if (c, rdflib.RDF.type, PIBE.ExclusiveConstraint) in g1
               for m in g1.objects(c, PIBE.groupMember)]
    corrupted = 0
    for c in list(g1.subjects(rdflib.RDF.type, PIBE.CompleteCandidate)):
        if (c, PIBE.inSpace, grp) not in g1:
            continue
        have = set(g1.objects(c, PIBE.includes))
        missing = [m for m in members if m not in have]
        if have & set(members) and missing:
            g1.add((c, PIBE.includes, missing[0])); corrupted += 1   # now two exclusive members selected
    d1 = run(graphs=[g1], verbose=False)
    print(f"  {corrupted} admitted candidate(s) made to violate the rule -> {d1} disagreement(s) (expected >0)")

    # 2. invent a rejection: PIB now claims a clean selection is inadmissible
    g2 = tx.build(path)
    invented = 0
    for c in list(g2.subjects(rdflib.RDF.type, PIBE.CompleteCandidate)):
        if (c, PIBE.isInadmissible, Literal(True)) not in g2:
            g2.add((c, PIBE.isInadmissible, Literal(True))); invented += 1
    d2 = run(graphs=[g2], verbose=False)
    print(f"  {invented} rejection(s) invented                          -> {d2} disagreement(s) (expected >0)")

    ok = clean == 0 and d1 > 0 and d2 > 0
    print(f"  the check discriminates in both directions: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raise SystemExit(1 if run(args or None) else 0)
