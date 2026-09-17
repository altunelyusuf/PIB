#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.  Round 2, correcting round 1's badly-shaped intersection test.

Round 1 intersected two profiles whose feature vocabularies are disjoint, so the empty result
measured my test design, not the operator. Corrected here: intersect over a SHARED universe.

Round 2 also asks the question that actually decides adoption: for each algebraic operator, is the
same result already reachable with the six variability operators by re-modelling — and if so, when
is it NOT reachable?
"""
import sys, os
sys.path.insert(0, os.environ["PIB_VAF_SRC"])
from variant_dsl_parser_v1_0_0 import Component, MandatoryStmt, OptionalStmt, ExclusiveStmt, OrStmt, DependencyStmt
from variant_enumerator_v2_0_0 import enumerate_variants

def space(name, mandatory=(), optional=(), exclusive=(), ors=(), deps=()):
    st = [MandatoryStmt(f, []) for f in mandatory] + [OptionalStmt(f, []) for f in optional]
    st += [ExclusiveStmt(list(g)) for g in exclusive] + [OrStmt(list(g)) for g in ors]
    st += [DependencyStmt(a, b) for a, b in deps]
    return Component(name, st)

def V(c): return {frozenset(v.selected) for v in enumerate_variants(c)}

AD, MEAS, OQ, GAM, FID, PAMG = ("analysis_design", "radar_measures", "oee_ontology_quality",
                                "gamont_model", "thesis_fidelity", "pamg_grades")
UNIVERSE = [AD, MEAS, OQ, GAM, FID, PAMG]

# Both profiles now declared over the SAME universe: features a profile does not require are
# OPTIONAL rather than absent, so the two spaces are comparable as sets.
ontology_based = space("OntologyBased",
    mandatory=[AD, MEAS, PAMG], optional=[OQ, GAM, FID], deps=[(MEAS, AD), (FID, GAM)])
gamification = space("Gamification",
    mandatory=[GAM, PAMG], optional=[OQ, FID, AD, MEAS], deps=[(FID, GAM), (MEAS, AD)])

OB, GM = V(ontology_based), V(gamification)
both = OB & GM

print("=" * 94)
print("Round 2 — intersection over a shared universe (round 1's empty result was a test defect)")
print("=" * 94)
print(f"  ontology-based wiring space              : {len(OB)}")
print(f"  gamification wiring space                : {len(GM)}")
print(f"  INTERSECTION (admissible under BOTH)     : {len(both)}")
print(f"  strictly smaller than either input?      : {0 < len(both) < min(len(OB), len(GM))}")
if both:
    print("  a wiring valid for a gamified ontology deliverable:")
    for w in sorted(both, key=lambda s: (len(s), sorted(s)))[:2]:
        print(f"      {sorted(w)}")

# Is that intersection reachable WITHOUT a new operator, by re-modelling as one component?
conjunction = space("BothProfilesAtOnce",
    mandatory=[AD, MEAS, PAMG, GAM], optional=[OQ, FID], deps=[(MEAS, AD), (FID, GAM)])
CJ = V(conjunction)
print(f"\n  same thing re-modelled as ONE component  : {len(CJ)}")
print(f"  identical to the set intersection?       : {CJ == both}")

print("\n" + "=" * 94)
print("So when is an algebraic operator actually NECESSARY rather than convenient?")
print("=" * 94)
print("""  Re-modelling works whenever ONE session can see and rewrite BOTH feature models.
  It does NOT work when the two spaces are enumerated by different owners and only the
  RESULTS cross the boundary — which is PIB's normal situation: profiles are composed from
  interfaces contributed by separate sessions, and a spoke's model is not PIB's to rewrite.
  In that case set-level composition is the only available move.""")

# Demonstrate the cross-boundary case concretely: results only, no access to the models.
def opaque_result_set(c):
    """Simulates a peer session handing over ONLY its enumerated wirings."""
    return V(c)

peer_a, peer_b = opaque_result_set(ontology_based), opaque_result_set(gamification)
print(f"\n  peer A hands over {len(peer_a)} wirings, peer B hands over {len(peer_b)} — models not shared.")
print(f"  intersection computable from results alone : {len(peer_a & peer_b)}")
print(f"  re-modelling computable from results alone : impossible — the statements never crossed")
