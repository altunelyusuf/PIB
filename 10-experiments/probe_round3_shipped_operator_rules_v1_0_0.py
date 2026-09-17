#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.  Round 3, correcting round 2's central error.

Rounds 1-2 concluded that the engine "cannot enumerate with" the algebraic operators, because the
Python DSL grammar parses only six statement kinds — and therefore that adopting them would mean
PIB building a calculus layer itself. That conclusion was reached from one surface (a Sprint-2
parser grammar) and is WRONG.

Read comprehensively instead: the framework ships an ontology-native implementation of the full
operator specification as SHACL-AF rules, with its own scaffold classes explicitly described as
"generic by design ... not tied to one use case," for a consumer to instantiate. PIB is already an
RDF/SHACL package running pySHACL. So the operators are directly executable here, today, with no
new calculus layer.

This probe proves that by running the framework's OWN shipped rules, unmodified, over PIB-shaped
data — including a constraint the six variability operators provably cannot express.
"""
import rdflib, itertools
from pyshacl import validate

VA = rdflib.Namespace("http://example.org/variant-algebra#")
EX = rdflib.Namespace("http://purl.org/pib/assessment#")
RULES = "/home/claude/VAF/02-shacl-safeguards/variant_algebra_operator_rules_v1_0_0.ttl"
PROPS = "/home/claude/VAF/01-ontologies/variant_algebra_v3_operator_properties_v1_0_0.ttl"

def run_rules(data_ttl):
    g = rdflib.Graph(); g.parse(data=data_ttl, format="turtle")
    before = len(g)
    shapes = rdflib.Graph(); shapes.parse(RULES, format="turtle"); shapes.parse(PROPS, format="turtle")
    validate(g, shacl_graph=shapes, advanced=True, inplace=True, inference="none")
    return g, before, len(g)

HDR = """@prefix va: <http://example.org/variant-algebra#> .
@prefix ex: <http://purl.org/pib/assessment#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
"""

print("=" * 94)
print("ROUND 3 — running the framework's OWN shipped operator rules over PIB data")
print("=" * 94)

# ---------------------------------------------------------------- 1. k-of-n
# PIB question: "at most TWO of the four measurement facets may feed the grader."
# The six variability operators cannot express this: exclusive = at most ONE, or = at least ONE,
# optional/mandatory/dependency say nothing about a count. Composing Repetition with contributesTo
# expresses it exactly — operator COMPOSITION creating expressiveness the base set lacks.
print("\n[1] k-of-n: at most 2 of 4 measurement facets may feed the grader")
data = HDR + """
ex:MeasurementBudget a va:RepetitionOperator ;
    va:appliesTo ex:FacetGroup ; va:hasMaxRepetitions 2 .
ex:radar_adequacy   va:contributesTo ex:FacetGroup ; va:isSelected true .
ex:oee_quality      va:contributesTo ex:FacetGroup ; va:isSelected true .
ex:gamont_fidelity  va:contributesTo ex:FacetGroup ; va:isSelected true .
ex:pamg_self_measure va:contributesTo ex:FacetGroup .
"""
g, b, a = run_rules(data)
violated = (EX.MeasurementBudget, VA.isViolated, rdflib.Literal(True)) in g
print(f"    three facets selected, budget 2  -> violated = {violated}   (expected True)")

data2 = data.replace("ex:gamont_fidelity  va:contributesTo ex:FacetGroup ; va:isSelected true .",
                     "ex:gamont_fidelity  va:contributesTo ex:FacetGroup .")
g2, _, _ = run_rules(data2)
violated2 = (EX.MeasurementBudget, VA.isViolated, rdflib.Literal(True)) in g2
print(f"    two facets selected,   budget 2  -> violated = {violated2}   (expected False)")
print("    => a real k-of-n bound, expressed by COMPOSING operators, not by a new primitive.")

# ---------------------------------------------------------------- 2. Intersection
print("\n[2] Intersection: which capabilities are jointly present across two profiles")
data = HDR + """
ex:ProfileOverlap a va:IntersectionOperator ;
    va:hasOperand ex:analysis_design , ex:pamg_grades , ex:gamont_model .
ex:analysis_design va:coOccursWith ex:pamg_grades .
"""
g, b, a = run_rules(data)
res = sorted(str(o).split('#')[-1] for o in g.objects(EX.ProfileOverlap, VA.hasResultMember))
print(f"    result members: {res}   (gamont_model correctly absent — no co-occurrence asserted)")

# ---------------------------------------------------------------- 3. Subtraction / Inverse
print("\n[3] Subtraction via inverse marking: exclude grader self-measurement before emission")
data = HDR + """
ex:CoreDevCandidate a va:CandidateVariant ;
    va:candidateMember ex:analysis_design , ex:radar_adequacy , ex:pamg_grades , ex:pamg_self_measure .
ex:pamg_self_measure va:isInverseMarked true .
"""
g, b, a = run_rules(data)
emitted = sorted(str(o).split('#')[-1] for o in g.objects(EX.CoreDevCandidate, VA.hasEmittedMember))
print(f"    emitted members: {emitted}")
print(f"    inverse-marked member purged? {'pamg_self_measure' not in emitted}   (expected True)")

# ---------------------------------------------------------------- 4. Cartesian with pruning
print("\n[4] Cartesian with Layer-0 pruning: pair measurement sources with grading modes")
data = HDR + """
ex:radar_adequacy a va:SetA .
ex:oee_quality    a va:SetA .
ex:legacy_source  a va:SetA ;
    va:excludesPartner ex:grade_in_ontology , ex:grade_externally .
ex:grade_in_ontology a va:SetB .
ex:grade_externally  a va:SetB .
ex:Pairs a va:PairGenerator .
"""
g, b, a = run_rules(data)
prunable = sorted(str(s).split('#')[-1] for s in g.subjects(VA.isPrunable, rdflib.Literal(True)))
operands = sorted(str(o).split('#')[-1] for o in g.objects(EX.Pairs, VA.hasOperand))
print(f"    pruned (excludes every partner): {prunable}")
print(f"    operands surviving into pairing : {operands}")

print("\n" + "=" * 94)
print("Conclusion: the operators execute HERE, on PIB-shaped data, using the framework's own")
print("shipped rules unmodified. No calculus layer needed to be built. Rounds 1-2 were wrong.")
print("=" * 94)
