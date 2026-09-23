#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.  Adaptation plan item 3: can PIB delegate the set-level operators to the
variant algebra now that all twelve are ontology-native upstream, instead of declaring six it never uses?

The question PIB actually has is set-level: which whole wirings are admissible under TWO profiles at once.
The true answer is computed first with PIB's own enumeration (both profiles' constraints in one space), then
the upstream operator rules are given the same data to see how far they reach. Nothing is asserted.
"""
import importlib.util, rdflib, sys
from pyshacl import validate

spec = importlib.util.spec_from_file_location("vc", "03-tooling/variation_capacity_v1_2_0.py")
vc = importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
EX = "http://purl.org/pib/example#"
VA = rdflib.Namespace("http://example.org/variant-algebra#")

HEAD = """@prefix pibe: <http://purl.org/pib/enumeration#> .
@prefix ex: <http://purl.org/pib/example#> .
"""
# One shared universe: analysis-design, adequacy measurement, ontology quality, gamification model, grade.
FEATS = ["ad", "meas", "oq", "gam", "grade"]
def space(name, mandatory, deps=()):
    L = [f"ex:{name} a pibe:VariationSpace ; pibe:featureCount 5 ; pibe:hasFeature " +
         ", ".join(f"ex:{f}" for f in FEATS) + " ."]
    L += [f"ex:{name}_m{i} a pibe:MandatoryConstraint ; pibe:inSpace ex:{name} ; pibe:requires ex:{f} ."
          for i, f in enumerate(mandatory)]
    L += [f"ex:{name}_d{i} a pibe:DependencyConstraint ; pibe:inSpace ex:{name} ; pibe:dependent ex:{a} ; pibe:prerequisite ex:{b} ."
          for i, (a, b) in enumerate(deps)]
    return "\n".join(L) + "\n"

IDX = "\n".join(f"ex:{f} pibe:featureIndex {i+1} ." for i, f in enumerate(FEATS)) + "\n"
ONT  = space("OntologyBased", ["ad", "meas", "grade"], [("grade", "meas")])
GAM  = space("Gamification", ["gam", "grade"], [("grade", "gam")])
BOTH = space("BothAtOnce", ["ad", "meas", "grade", "gam"], [("grade", "meas"), ("grade", "gam")])

def cap(ttl, name):
    open(f"/tmp/d_{name}.ttl", "w").write(HEAD + IDX + ttl)
    r, t, _ = vc.compute([f"/tmp/d_{name}.ttl"], verbose=False)
    return r.get(EX + name), t.get(EX + name)

print("=== the true answers, from PIB's own enumeration ===")
for ttl, n in ((ONT, "OntologyBased"), (GAM, "Gamification"), (BOTH, "BothAtOnce")):
    c, t = cap(ttl, n)
    print(f"  {n:14s} capacity {c}   (from {t} candidates across its groups)")

print("\n=== what upstream's intersection rule does with the same subject matter ===")
data = rdflib.Graph()
data.parse(data=f"""@prefix va: <http://example.org/variant-algebra#> .
@prefix ex: <http://purl.org/pib/example#> .
# v1.1.0 of the rule requires each operand to be typed as one side of the intersection (SetA / SetB);
# the version PIB previously vendored matched any operands. Typed accordingly.
ex:ProfileOverlap a va:IntersectionOperator ; va:hasOperand ex:ad , ex:meas , ex:grade , ex:gam .
ex:ad a va:SetA . ex:meas a va:SetB . ex:grade a va:SetB . ex:gam a va:SetA .
ex:ad va:coOccursWith ex:meas . ex:meas va:coOccursWith ex:ad .
ex:meas va:coOccursWith ex:grade . ex:grade va:coOccursWith ex:meas .
""", format="turtle")
shapes = rdflib.Graph()
for f in ("11-vendored-operator-rules/variant_algebra_operator_rules_v1_0_0.ttl",
          "11-vendored-operator-rules/variant_algebra_v3_extended_properties_v1_0_0.ttl"):
    shapes.parse(f, format="turtle")
validate(data, shacl_graph=shapes, advanced=True, inplace=True, inference="none")
members = sorted(str(o).split("#")[-1] for o in data.objects(rdflib.URIRef(EX + "ProfileOverlap"), VA.hasResultMember))
print(f"  intersection result members (ELEMENTS, not wirings): {members}")
print("""
=== reading ===
The upstream operators work on ELEMENTS that co-occur. PIB's question is about WHOLE WIRINGS admissible
under two profiles at once, which is answered above by enumerating both profiles' constraints in one space.
These are different arities: one intersects features, the other intersects sets of selections. Delegating
the first does not answer the second.""")
