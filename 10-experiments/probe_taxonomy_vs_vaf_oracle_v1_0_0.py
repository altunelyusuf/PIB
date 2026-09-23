#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.
Checks PIB's taxonomy against the variant algebra's OWN enumerator as the oracle, rather than against
expectations PIB wrote for itself.

Why this is different from what came before: PIB's earlier round-trip test converted a space to the
algebra's DSL and back through PIB's own converter and PIB's own enumeration. That proves self-consistency
and nothing about meaning. Here the DSL text is enumerated by the ALGEBRA, and the resulting selections are
compared as SETS with the leaves of PIB's taxonomy. A count match with different members would be a false
pass, so members are compared, not counts.

Usage: python3 10-experiments/probe_taxonomy_vs_vaf_oracle_v1_0_0.py [VAF_SRC]
"""
import os, sys, subprocess, tempfile, importlib.util
import rdflib

VAF_SRC = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("VAF_SRC", "/home/claude/VAF/06-runtime/src")
sys.path.insert(0, VAF_SRC)
from variant_dsl_parser_v1_0_0 import parse
import variant_enumerator_v2_0_0 as ve

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
CONVERTER = os.path.join(ROOT, "03-tooling", "taxonomy_vaf_converter_v1_0_0.py")
_spec = importlib.util.spec_from_file_location("tx", os.path.join(ROOT, "03-tooling", "profile_taxonomy_v1_0_0.py"))
tx = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(tx)

CASES = {
    "mandatory only":            "component C {\n  mandatory a\n}",
    "optional only":             "component C {\n  optional a\n}",
    "exclusive {a|b}":           "component C {\n  exclusive { a | b }\n}",
    "or {a,b}":                  "component C {\n  or { a, b }\n}",
    "dependency a requires b":   "component C {\n  optional a\n  optional b\n  a requires b\n}",
    "atmost 1 of {a,b}":         "component C {\n  atmost 1 of { a, b }\n}",
    "mandatory + exclusive":     "component C {\n  mandatory a\n  exclusive { b | c }\n}",
}


def vaf_variants(dsl):
    """The algebra's own answer: each variant as the SET of features it selects."""
    comp = parse(dsl).components[0]
    out = set()
    for v in ve.enumerate_variants(comp):
        out.add(frozenset(f for f, n in v.counts.items() if n and n > 0))
    return out


def pib_leaves(dsl):
    """PIB's answer: each taxonomy leaf as the SET of features it includes."""
    d = tempfile.mkdtemp()
    dsl_p, ttl_p = os.path.join(d, "c.dsl"), os.path.join(d, "c.ttl")
    open(dsl_p, "w").write(dsl)
    r = subprocess.run([sys.executable, CONVERTER, "from-dsl", dsl_p, ttl_p], capture_output=True, text=True)
    if r.returncode:
        return None, r.stderr.strip().splitlines()[-1][:70]
    g = tx.build(ttl_p)
    # A leaf is a variant OF ITS DIMENSION. Partitioning splits a space into independent groups, so a
    # whole-space variant is one leaf from each dimension combined — the product the capacity computation
    # already takes. Comparing raw leaves against whole-space variants would compare different things.
    spaces = [s for s in g.subjects(rdflib.RDF.type, PIBE.VariationSpace) if (s, PIBE.groupOf, None) not in g]
    combos = {frozenset()}
    for sp in spaces:
        for grp in sorted(g.subjects(PIBE.groupOf, sp), key=str):
            leaves = [frozenset(str(f).split("#")[-1] for f in g.objects(l, PIBE.includes))
                      for l in g.subjects(rdflib.RDF.type, PIBE.ProfileVariant)
                      if (l, PIBE.inSpace, grp) in g]
            if not leaves:
                continue
            combos = {c | l for c in combos for l in leaves}
    return combos, None


def main():
    print("PIB taxonomy vs the algebra's own enumerator — sets of selections, not counts")
    agree = disagree = 0
    for label, dsl in CASES.items():
        oracle = vaf_variants(dsl)
        mine, err = pib_leaves(dsl)
        if mine is None:
            print(f"  {label:26s} algebra {len(oracle):2d} | PIB could not convert: {err}")
            disagree += 1
            continue
        same = oracle == mine
        agree, disagree = agree + int(same), disagree + int(not same)
        print(f"  {label:26s} algebra {len(oracle):2d} | PIB {len(mine):2d} | {'AGREE' if same else 'DISAGREE'}")
        if not same:
            fmt = lambda S: sorted("{" + ",".join(sorted(x)) + "}" for x in S) or ["{}"]
            print(f"      algebra: {fmt(oracle)}")
            print(f"      PIB    : {fmt(mine)}")
            print(f"      only PIB: {fmt(mine - oracle)}   only algebra: {fmt(oracle - mine)}")
    print(f"\n  agree {agree}, disagree {disagree}")
    return 1 if disagree else 0


if __name__ == "__main__":
    raise SystemExit(main())
