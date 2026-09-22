#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.
Differential test on the VARIANT ALGEBRA'S OWN data: every profile family in its shipped examples is
counted twice — by the algebra's unmodified Python enumerator (the reference, via its own bridge) and by
PIB's ontology-native rules — and the two counts must agree.

The mapping follows the algebra's own bridge construct for construct. One construct cannot be mapped:
repetition as a MULTIPLICITY (an element occurring between a minimum and maximum number of times),
because PIB's candidates only include or exclude a feature. Families using it are reported as not
expressible, never silently mapped.
"""
import sys, os, importlib.util, rdflib
from pyshacl import validate
VAF = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/VAF"
PIB = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/PIB"
sys.path.insert(0, f"{VAF}/06-runtime/src")
from variant_profile_family_generation_bridge_v1_0_0 import build_component_from_profile_family
from variant_enumerator_v2_0_0 import enumerate_variants
spec = importlib.util.spec_from_file_location("vc", f"{PIB}/03-tooling/variation_capacity_v1_2_0.py")
vc = importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)

VA = rdflib.Namespace("http://example.org/variant-algebra#")
g = rdflib.Graph()
for f in ["01-ontologies/variant_algebra_profile_family_v1_0_0.ttl",
          "01-ontologies/variant_algebra_profile_family_examples_v1_0_0.ttl",
          "01-ontologies/variant_algebra_profile_family_advanced_examples_v1_0_0.ttl"]:
    if os.path.exists(f"{VAF}/{f}"): g.parse(f"{VAF}/{f}", format="turtle")
rules = rdflib.Graph(); rules.parse(f"{VAF}/02-shacl-safeguards/variant_algebra_profile_family_generation_rules_v1_0_0.ttl", format="turtle")
validate(g, shacl_graph=rules, advanced=True, inplace=True, inference="none")   # the algebra's own accumulation

def to_pib(name, comp):
    """Translate the algebra's Component into a PIB variation space, construct for construct."""
    feats, stmts = [], []
    def F(x):
        if x not in feats: feats.append(x)
        return f"ex:{name}_f{feats.index(x)+1}"
    body = []
    for s in comp.statements:
        t = type(s).__name__
        if t == "MandatoryStmt":
            body.append(f"ex:{name}_m{len(body)} a pibe:MandatoryConstraint ; pibe:inSpace ex:{name} ; pibe:requires {F(s.feature)} .")
        elif t == "OptionalStmt":
            F(s.feature)
        elif t in ("ExclusiveStmt", "OrStmt"):
            kind = "ExclusiveConstraint" if t == "ExclusiveStmt" else "OrConstraint"
            ms = " , ".join(F(m) for m in s.members)
            body.append(f"ex:{name}_c{len(body)} a pibe:{kind} ; pibe:inSpace ex:{name} ; pibe:groupMember {ms} .")
        elif t == "DependencyStmt":
            body.append(f"ex:{name}_d{len(body)} a pibe:DependencyConstraint ; pibe:inSpace ex:{name} ; "
                        f"pibe:dependent {F(s.antecedent)} ; pibe:prerequisite {F(s.consequent)} .")
        elif t == "RepetitionStmt":
            return None, "multiplicity repetition — not expressible in include/exclude candidates"
        else:
            return None, f"unhandled construct {t}"
    idx = "\n".join(f"ex:{name}_f{i+1} pibe:featureIndex {i+1} ." for i in range(len(feats)))
    head = f"ex:{name} a pibe:VariationSpace ; pibe:featureCount {len(feats)} ; pibe:hasFeature {', '.join(f'ex:{name}_f{i+1}' for i in range(len(feats)))} ."
    return ("@prefix pibe: <http://purl.org/pib/enumeration#> .\n@prefix ex: <http://purl.org/pib/example#> .\n"
            + head + "\n" + idx + "\n" + "\n".join(body) + "\n"), None

nodes = sorted(set(g.subjects(rdflib.RDF.type, VA.ProfileFamily)) | set(g.subjects(rdflib.RDF.type, VA.Profile)), key=str)
agree = disagree = skipped = 0
for n in nodes:
    name = str(n).split("#")[-1]
    try:
        comp = build_component_from_profile_family(g, n)
    except ValueError as e:
        print(f"  {name:44s} bridge refuses (no elements): skipped"); skipped += 1; continue
    ref = len(enumerate_variants(comp))
    ttl, why = to_pib(name, comp)
    if ttl is None:
        print(f"  {name:44s} reference {ref:>4}  PIB: NOT EXPRESSIBLE ({why})"); skipped += 1; continue
    path = f"/tmp/vafpf_{name}.ttl"; open(path, "w").write(ttl)
    res, tot, rej = vc.compute([path], verbose=False)
    got = next(iter(res.values())) if res else None
    ok = got == ref; agree += ok; disagree += (not ok)
    print(f"  {name:44s} reference {ref:>4}  PIB {str(got):>4}  {'AGREE' if ok else 'DISAGREE'}")
print(f"\n  agree {agree}, disagree {disagree}, not expressible or skipped {skipped}, of {len(nodes)} families")
