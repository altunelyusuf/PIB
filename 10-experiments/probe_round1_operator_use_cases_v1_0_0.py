#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.

Experiment requested by the owner: does PIB actually need the variant-algebra engine's full
twelve operators, rather than the six variability operators it currently imports?

Method, honestly stated: the pinned engine's DSL parses exactly six statement kinds (mandatory,
optional, exclusive, or, repetition, dependency) and its enumerator returns variant SETS. The
remaining operators are set-level operations over those results. So this prototype implements them
as a calculus layer ON TOP of real enumeration output and applies each to a real PIB question,
rather than arguing from category names. Every number below is computed, not asserted.
"""
import sys, os, itertools
sys.path.insert(0, os.environ["PIB_VAF_SRC"])
from variant_dsl_parser_v1_0_0 import Component, MandatoryStmt, OptionalStmt, ExclusiveStmt, OrStmt, DependencyStmt
from variant_enumerator_v2_0_0 import enumerate_variants

# ---------- build wiring spaces for real PIB profiles ----------
def space(name, mandatory=(), optional=(), exclusive=(), ors=(), deps=()):
    stmts = [MandatoryStmt(f, []) for f in mandatory] + [OptionalStmt(f, []) for f in optional]
    stmts += [ExclusiveStmt(list(gr)) for gr in exclusive]
    stmts += [OrStmt(list(gr)) for gr in ors]
    stmts += [DependencyStmt(a, b) for a, b in deps]
    return Component(name, stmts)

def variants(component):
    """Enumerated admissible wirings, each as a frozenset of selected feature names."""
    return {frozenset(v.selected) for v in enumerate_variants(component)}

# Real PIB edges. Feature names are the wiring edges/roles the published profiles use.
AD   = "o4sdlc_produces_analysis_design"
MEAS = "radar_measures_adequacy"
OQ   = "oee_measures_ontology_quality"
GAM  = "gamont_supplies_gamification_model"
FID  = "gamont_supplies_thesis_fidelity"
PAMG = "pamg_grades"
PAMG_OWN = "pamg_measures_source_fidelity_itself"   # PAMG's own documented open caveat

ontology_based = space("OntologyBased",
    mandatory=[AD, MEAS, PAMG], optional=[OQ, PAMG_OWN],
    exclusive=[[PAMG, "alt_grader"]], deps=[(MEAS, AD)])
gamification = space("Gamification",
    mandatory=[GAM, PAMG], optional=[FID, OQ],
    exclusive=[[PAMG, "alt_grader"]], deps=[(FID, GAM)])
core_dev = space("CoreSoftwareDevelopment",
    mandatory=[AD, MEAS, PAMG], optional=[PAMG_OWN], deps=[(MEAS, AD)])

# Two genuinely independent dimensions, for the cartesian test
measurement_dim = space("MeasurementSource", mandatory=[], ors=[[MEAS, OQ]])
grading_dim     = space("GradingMode", exclusive=[["grade_in_ontology", "grade_externally"]])

# ---------- the calculus layer (the six operators PIB does NOT currently import) ----------
def addition(A, B):      return A | B                              # co-inclusion of both spaces
def intersection(A, B):  return A & B                              # admissible under BOTH
def subtraction(A, B):   return A - B                              # in A, explicitly not in B
def division(A, B):      return (A | B) - (A & B)                  # removes common elements
def inverse(A, universe):return universe - A                       # complement within a universe
def cartesian(A, B):     return {a | b for a in A for b in B}      # all pairings

def report(title, result, note=""):
    print(f"  {title:52s} -> {len(result):5d} wirings   {note}")

print("=" * 96)
print("PIB variant-calculus experiment — computed against the pinned engine, not asserted")
print("=" * 96)

OB, GM, CD = variants(ontology_based), variants(gamification), variants(core_dev)
print("\n[baseline: what the six variability operators already give us]")
report("Ontology-based profile wiring space", OB)
report("Gamification profile wiring space", GM)
report("Core software development wiring space", CD)

print("\n[1] INTERSECTION — an artifact that is BOTH ontology-based AND a gamification project")
both = intersection(OB, GM)
report("wirings admissible under both profiles", both,
       "<-- THE QUESTION PIB CANNOT CURRENTLY ANSWER" if both else "<-- EMPTY: profiles are disjoint")
if both:
    for w in sorted(both, key=lambda s: (len(s), sorted(s)))[:3]:
        print(f"        {sorted(w)}")

print("\n[2] SUBTRACTION — core-dev wirings that do NOT rely on PAMG measuring source fidelity itself")
without_own = subtraction(CD, {w for w in CD if PAMG_OWN in w})
report("core-dev wirings free of PAMG self-measurement", without_own,
       f"(of {len(CD)}; PAMG's documented open caveat)")

print("\n[3] CARTESIAN — joint space across two genuinely independent dimensions")
MD, GD = variants(measurement_dim), variants(grading_dim)
report("measurement-source dimension", MD)
report("grading-mode dimension", GD)
report("cartesian product of the two", cartesian(MD, GD),
       f"= {len(MD)} x {len(GD)}; matches product?" )

print("\n[4] ADDITION — co-inclusion of the ontology-based and gamification spaces")
report("union of both wiring spaces", addition(OB, GM))

print("\n[5] DIVISION — wirings unique to one profile (common elements removed)")
report("symmetric difference of the two spaces", division(OB, GM))

print("\n[6] INVERSE — wirings in the combined universe NOT admissible for gamification")
universe = addition(OB, GM)
report("complement of gamification within that universe", inverse(GM, universe))

print("\n" + "=" * 96)
print("Does any of this change an answer PIB gives today?")
print("=" * 96)
print(f"  intersection non-empty and smaller than either input : "
      f"{bool(both) and len(both) < min(len(OB), len(GM))}")
print(f"  subtraction removes real wirings (caveat is material) : {len(without_own) < len(CD)}")
print(f"  cartesian equals the product of its dimensions        : "
      f"{len(cartesian(MD, GD)) == len(MD) * len(GD)}")
