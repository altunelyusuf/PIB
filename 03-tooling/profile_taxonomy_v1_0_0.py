#!/usr/bin/env python3
"""
PIB Profile Taxonomy v1.0.0
===========================
Renders the profile taxonomy derived from a variation space, and checks that each operator produced the
branch structure its own semantics require.

Nothing is generated twice. The enumeration rules already build the branch tree — every candidate records
the parent it came from and the feature it decided — and the taxonomy phase expresses that structure
taxonomically. This tool reads the result.

How each operator shapes the taxonomy, and why:

  Mandatory (meta)       no branch. The feature is in every variant, so it characterises the ROOT and
                         distinguishes nothing below. This is the structural reason mandatory belongs at
                         the meta layer rather than in a profile.
  Mandatory (in-profile) no branch: the 'leaves it' side is pruned, so the decision is FORCED — one child,
                         recorded as forced rather than drawn as a fork, because showing a fork where no
                         choice exists misleads a reader about the space.
  Optional               TWO branches, takes and leaves, disjoint and jointly covering the parent.
  Exclusive {a,b}        THREE leaves in that subtree — a, b, neither — since at most one may be taken.
  Or {a,b}               THREE — a, b, both — since the 'neither' branch is pruned.
  Dependency a→b         no branch of its own; it prunes branches taking a without b.
  Repetition (k-of-n)    no branch of its own; it prunes branches exceeding the budget.

Siblings are disjoint by construction: one takes the feature the other leaves.

Usage:
    python3 03-tooling/profile_taxonomy_v1_0_0.py <spaces.ttl> [space-name]
    python3 03-tooling/profile_taxonomy_v1_0_0.py --self-test
"""
import os, sys, importlib.util, tempfile
import rdflib
from rdflib.namespace import RDFS, OWL

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
_spec = importlib.util.spec_from_file_location("vc", os.path.join(HERE, "variation_capacity_v1_2_0.py"))
vc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(vc)


def build(path):
    """Run the phases, then hand back the graph with its taxonomy materialised."""
    import rdflib as R
    from pyshacl import validate
    data = R.Graph(); data.parse(path, format="turtle")
    for _, shapes in vc.phased_shapes():
        prev = -1
        while len(data) != prev:
            prev = len(data)
            validate(data, shacl_graph=shapes, advanced=True, inplace=True, inference="none")
    return data


def render(data, space=None, verbose=True):
    spaces = [s for s in data.subjects(rdflib.RDF.type, PIBE.VariationSpace)
              if (s, PIBE.groupOf, None) not in data]
    if space:
        spaces = [s for s in spaces if str(s).endswith("#" + space)]
    out = {}
    for sp in sorted(spaces, key=str):
        # Candidates live in the space's GROUPS: partitioning splits a space into independent groups, and
        # independent groups are separate taxonomic DIMENSIONS combined by product, not one tree. A space
        # with a single group has one tree; several groups mean several, and saying so is the honest shape.
        groups = sorted(data.subjects(PIBE.groupOf, sp), key=str) or [sp]
        nodes = [c for g in groups for c in data.subjects(PIBE.inSpace, g)
                 if (c, rdflib.RDF.type, PIBE.Candidate) in data]
        roots = [c for c in nodes if (c, PIBE.derivedFrom, None) not in data]
        leaves = [c for c in nodes if (c, rdflib.RDF.type, PIBE.ProfileVariant) in data]
        out_groups = len(groups)
        forced = [c for c in nodes if (c, PIBE.forcedDecision, rdflib.Literal(True)) in data]
        disjoint = len(list(data.subject_objects(OWL.disjointWith)))
        out[str(sp)] = dict(nodes=len(nodes), leaves=len(leaves), forced=len(forced), groups=out_groups)
        if not verbose:
            continue
        name = str(sp).split("#")[-1]
        print(f"  taxonomy of {name}: {len(nodes)} node(s), {len(leaves)} variant(s) at the leaves, "
              f"{len(forced)} forced decision(s), {disjoint} disjoint sibling pair(s), "
              f"{out_groups} independent dimension(s)")

        def walk(node, depth):
            label = str(data.value(node, PIBE.differsBy) or "")
            kind = str(data.value(node, PIBE.branchKind) or "")
            mark = ""
            if label:
                f = label.split("#")[-1]
                mark = f"{'takes' if kind == 'takes' else 'leaves'} {f}"
                if (node, PIBE.forcedDecision, rdflib.Literal(True)) in data:
                    mark += "  [forced — no alternative survived]"
            leaf = " *variant*" if (node, rdflib.RDF.type, PIBE.ProfileVariant) in data else ""
            if depth:
                print(f"      {'  ' * depth}└─ {mark}{leaf}")
            kids = sorted(data.subjects(PIBE.derivedFrom, node), key=str)
            for k in kids:
                walk(k, depth + 1)
        roots = [c for c in nodes if (c, PIBE.derivedFrom, None) not in data]
        for r in roots:
            print(f"      root: every variant of {name}")
            walk(r, 0)
    return out


def self_test():
    """Each operator must produce the branch shape its own definition requires."""
    cases = {
        "optional alone — two branches": ("""ex:S a pibe:VariationSpace ; pibe:featureCount 1 ; pibe:hasFeature ex:a .
ex:a pibe:featureIndex 1 .""", 2),
        "mandatory — no branch, one forced child": ("""ex:S a pibe:VariationSpace ; pibe:featureCount 1 ; pibe:hasFeature ex:a .
ex:a pibe:featureIndex 1 .
ex:m a pibe:MandatoryConstraint ; pibe:inSpace ex:S ; pibe:requires ex:a .""", 1),
        "exclusive {a,b} — three variants: a, b, neither": ("""ex:S a pibe:VariationSpace ; pibe:featureCount 2 ; pibe:hasFeature ex:a , ex:b .
ex:a pibe:featureIndex 1 . ex:b pibe:featureIndex 2 .
ex:x a pibe:ExclusiveConstraint ; pibe:inSpace ex:S ; pibe:groupMember ex:a , ex:b .""", 3),
        "or {a,b} — three variants: a, b, both": ("""ex:S a pibe:VariationSpace ; pibe:featureCount 2 ; pibe:hasFeature ex:a , ex:b .
ex:a pibe:featureIndex 1 . ex:b pibe:featureIndex 2 .
ex:o a pibe:OrConstraint ; pibe:inSpace ex:S ; pibe:groupMember ex:a , ex:b .""", 3),
        "dependency a needs b — prunes, adds no branch": ("""ex:S a pibe:VariationSpace ; pibe:featureCount 2 ; pibe:hasFeature ex:a , ex:b .
ex:a pibe:featureIndex 1 . ex:b pibe:featureIndex 2 .
ex:d a pibe:DependencyConstraint ; pibe:inSpace ex:S ; pibe:dependent ex:a ; pibe:prerequisite ex:b .""", 3),
    }
    HEAD = "@prefix pibe: <http://purl.org/pib/enumeration#> .\n@prefix ex: <http://purl.org/pib/example#> .\n"
    print("PIB profile taxonomy — self-test: does each operator branch as its definition requires?")
    ok = True
    for label, (body, expect) in cases.items():
        p = os.path.join(tempfile.mkdtemp(), "s.ttl"); open(p, "w").write(HEAD + body)
        got = render(build(p), verbose=False)
        leaves = next(iter(got.values()))["leaves"] if got else 0
        match = leaves == expect
        ok &= match
        print(f"  {label:52s} leaves {leaves} (expected {expect})  {'ok' if match else 'MISMATCH'}")
    print(f"  every operator branches as defined: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    render(build(args[0]), args[1] if len(args) > 1 else None)
    raise SystemExit(0)
