#!/usr/bin/env python3
"""
PIB Rule Scope Check v1.0.0
===========================
Finds validation rules whose scope is real but undeclared: a shape whose own query tests a profile
property, while nothing on the shape says it is profile-specific.

Why this matters more than it looks. A rule that binds only some profiles is not wrong — it is often
exactly right. The danger is that the dependency lives inside the query, where a reader sees it only by
reading SPARQL, and a tool cannot see it at all. Then a requirement can quietly stop applying to a whole
class of artifacts with nobody deciding to drop it. That is not hypothetical: a consuming session reported
precisely this after a profile-scoped expectation propagated into a live lineage, and measuring this
ecosystem on 2026-09-23 found four shipped shapes conditioning on a profile and none declaring it.

The rule this enforces, from PIB's shared vocabulary: **absence of a scope means general.** A rule binds
everyone unless it says otherwise. So the check never asks "is this rule general?" — it asks the narrower,
answerable question: does any rule *behave* as profile-specific while *declaring* nothing?

Usage:
    python3 03-tooling/rule_scope_check_v1_0_0.py [shapes-dir-or-file ...]
    python3 03-tooling/rule_scope_check_v1_0_0.py --self-test
"""
import os, sys, glob
import rdflib
from rdflib.namespace import RDF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
PIB = rdflib.Namespace("http://purl.org/pib/profile#")
# Profile properties whose appearance in a query means the rule is profile-conditioned.
PROFILE_PROPS = ("hasCriticalityProfile", "hasProfile", "declaresProfile", "selectsWiring",
                 "requiresObligationSetAdoption", "requiresEpicDecomposition", "forDepthLevel",
                 "forArtifactDomain", "hasRuleScope")


def scan(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(os.path.join(p, "*.ttl"))) if os.path.isdir(p) else [p]
    undeclared, declared, checked = [], 0, 0
    for f in files:
        try:
            g = rdflib.Graph(); g.parse(f, format="turtle")
        except Exception:
            continue
        for s in g.subjects(RDF.type, SH.NodeShape):
            checked += 1
            q = ""
            for c in g.objects(s, SH.sparql):
                q += str(g.value(c, SH.select) or "")
            for c in g.objects(s, SH.rule):
                q += str(g.value(c, SH.construct) or "")
            conditions = [p for p in PROFILE_PROPS if p != "hasRuleScope" and p in q]
            if not conditions:
                continue
            if (s, PIB.hasRuleScope, None) in g:
                declared += 1
            else:
                undeclared.append((os.path.basename(f), str(s).split("#")[-1], conditions))
    return checked, declared, undeclared


def main(paths=None, verbose=True):
    paths = paths or [os.path.join(ROOT, "02-shacl-safeguards")]
    checked, declared, undeclared = scan(paths)
    if verbose:
        print(f"PIB rule scope check v1.0.0 — {checked} shape(s) examined")
        print(f"  profile-conditioned and declared: {declared}")
        for f, shape, props in undeclared:
            print(f"  UNDECLARED: {f} :: {shape} tests {', '.join(props)} but declares no rule scope")
        print("  PASS — no rule is profile-specific without saying so" if not undeclared
              else f"  FAIL — {len(undeclared)} rule(s) scoped in the query but not in the declaration")
    return len(undeclared)


def self_test():
    import tempfile
    tmp = tempfile.mkdtemp()
    common = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix pib: <http://purl.org/pib/profile#> .
@prefix ex: <http://example.org/t#> .
"""
    # general rule: no profile property in its query -> not flagged
    open(os.path.join(tmp, "general.ttl"), "w").write(common + """
ex:GeneralShape a sh:NodeShape ; sh:sparql [ a sh:SPARQLConstraint ;
    sh:select \"\"\"SELECT $this WHERE { $this ex:anything ?x }\"\"\" ] .
""")
    # profile-conditioned but undeclared -> must be flagged
    open(os.path.join(tmp, "hidden.ttl"), "w").write(common + """
ex:HiddenShape a sh:NodeShape ; sh:sparql [ a sh:SPARQLConstraint ;
    sh:select \"\"\"SELECT $this WHERE { $this <http://example.org/core#hasCriticalityProfile> ?p }\"\"\" ] .
""")
    # profile-conditioned and declared -> must NOT be flagged
    open(os.path.join(tmp, "declared.ttl"), "w").write(common + """
ex:DeclaredShape a sh:NodeShape ; pib:hasRuleScope ex:OnlyHigh ; sh:sparql [ a sh:SPARQLConstraint ;
    sh:select \"\"\"SELECT $this WHERE { $this <http://example.org/core#hasCriticalityProfile> ?p }\"\"\" ] .
ex:OnlyHigh a pib:ProfileSpecific .
""")
    print("PIB rule scope check — self-test")
    n_general = main([os.path.join(tmp, "general.ttl")], verbose=False)
    n_hidden = main([os.path.join(tmp, "hidden.ttl")], verbose=False)
    n_declared = main([os.path.join(tmp, "declared.ttl")], verbose=False)
    print(f"  a general rule                      -> {n_general} flagged (expected 0)")
    print(f"  a rule scoped only inside its query -> {n_hidden} flagged (expected 1)")
    print(f"  the same rule, scope declared       -> {n_declared} flagged (expected 0)")
    ok = (n_general, n_hidden, n_declared) == (0, 1, 0)
    print(f"  the check discriminates: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raise SystemExit(1 if main(args or None) else 0)
