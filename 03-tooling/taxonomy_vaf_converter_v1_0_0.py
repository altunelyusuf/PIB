#!/usr/bin/env python3
r"""
PIB ↔ variant-algebra converter v1.0.0
======================================
Converts PIB's taxonomy — a variation space and its constraints — into the variant algebra's own DSL
text, and back again.

**The parser is the algebra's, not PIB's.** Reading the algebra's notation is the algebra's own
capability; writing a second parser here would be a parallel implementation of something that already
exists. This tool imports `variant_dsl_parser_v1_0_0` from the algebra's runtime and only maps between
its statement objects and PIB's vocabulary. Set `VAF_SRC` to that runtime's `src` directory.

That makes this an **interop tool with an optional dependency**, never part of PIB's gates: PIB's
calculation path stays in the ontology and needs nothing outside the package. Converting is the one task
that genuinely needs a text parser, and the algebra ships one.

Mapping, exact in both directions:

| PIB                                    | algebra DSL                  |
|----------------------------------------|------------------------------|
| `MandatoryConstraint requires f`       | `mandatory f`                |
| feature with no constraint             | `optional f`                 |
| `ExclusiveConstraint groupMember …`    | `atmost 1 of { a, b }`       |
| `OrConstraint groupMember …`           | `or { a, b }`                |
| `DependencyConstraint dependent/prereq`| `a requires b`               |
| `RepetitionConstraint budgetGroup/max` | `atmost N of { a, b, … }`    |

PIB's exclusive means AT MOST ONE; the algebra's `exclusive { … }` means EXACTLY one. That was checked
against the algebra's own enumerator rather than assumed, and the first mapping here was wrong because of
it: writing PIB's at-most-one as the algebra's `exclusive` dropped the "neither" variant, and reading the
algebra's `exclusive` as PIB's at-most-one added one. The faithful forms are `atmost 1 of { … }` outward,
and at-most-one plus at-least-one inward.

Not mapped, and reported rather than guessed: multiplicity repetition (`f[1..3]`), `unite`, `removes`,
`excludes`, and infix expression statements — PIB has no equivalent for these, and a silent approximation
would produce a space that counts something other than what was written.

Usage:
    python3 taxonomy_vaf_converter_v1_0_0.py to-dsl   <spaces.ttl> [space-name]
    python3 taxonomy_vaf_converter_v1_0_0.py from-dsl <component.dsl> [out.ttl]
    python3 taxonomy_vaf_converter_v1_0_0.py round-trip <spaces.ttl>
"""
import os, sys, rdflib
from rdflib.namespace import RDF

PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
EX = rdflib.Namespace("http://purl.org/pib/example#")
VAF_SRC = os.environ.get("VAF_SRC", "/home/claude/VAF/06-runtime/src")


def _parser():
    sys.path.insert(0, VAF_SRC)
    try:
        import variant_dsl_parser_v1_0_0 as p
        return p
    except ImportError as e:
        raise SystemExit(
            f"the algebra's parser is not importable from VAF_SRC={VAF_SRC} ({e}).\n"
            "This converter deliberately reuses the algebra's parser instead of carrying its own; "
            "point VAF_SRC at the algebra's runtime src directory.")


# ----------------------------------------------------------------- PIB -> DSL
def to_dsl(graph, space):
    """Render one PIB variation space as an algebra DSL component."""
    feats = sorted(graph.objects(space, PIBE.hasFeature), key=lambda f: int(graph.value(f, PIBE.featureIndex)))
    name = lambda f: str(f).split("#")[-1]
    constrained, lines = set(), []
    for c in graph.subjects(PIBE.inSpace, space):
        kinds = set(graph.objects(c, RDF.type))
        if PIBE.MandatoryConstraint in kinds:
            f = graph.value(c, PIBE.requires); constrained.add(f)
            lines.append(f"  mandatory {name(f)}")
        elif PIBE.ExclusiveConstraint in kinds or PIBE.OrConstraint in kinds:
            ms = sorted(graph.objects(c, PIBE.groupMember), key=lambda f: int(graph.value(f, PIBE.featureIndex)))
            constrained.update(ms)
            if PIBE.ExclusiveConstraint in kinds:
                # PIB's exclusive means AT MOST ONE. The algebra's `exclusive { a | b }` means EXACTLY
                # one, so writing it that way would silently drop the "neither" variant. Its `atmost 1 of`
                # statement is the faithful form — checked against the algebra's own enumerator.
                lines.append(f"  atmost 1 of {{ {', '.join(name(m) for m in ms)} }}")
            else:
                lines.append(f"  or {{ {', '.join(name(m) for m in ms)} }}")
        elif PIBE.DependencyConstraint in kinds:
            a, b = graph.value(c, PIBE.dependent), graph.value(c, PIBE.prerequisite)
            constrained.update((a, b))
            lines.append(f"  {name(a)} requires {name(b)}")
        elif PIBE.RepetitionConstraint in kinds:
            g, mx = graph.value(c, PIBE.budgetGroup), int(graph.value(c, PIBE.maxSelected))
            ms = [f for f in feats if (f, PIBE.contributesToGroup, g) in graph]
            constrained.update(ms)
            lines.append(f"  atmost {mx} of {{ {', '.join(name(m) for m in ms)} }}")
    for f in feats:                       # every feature must appear, or the component loses it
        if f not in constrained:
            lines.append(f"  optional {name(f)}")
    return f"component {str(space).split('#')[-1]} {{\n" + "\n".join(lines) + "\n}\n"


# ----------------------------------------------------------------- DSL -> PIB
UNSUPPORTED = {"RepetitionStmt": "multiplicity repetition (f[min..max]) — PIB candidates only include or exclude",
               "UniteStmt": "unite — PIB has no co-inclusion constraint",
               "RemovesStmt": "removes — element-level, not a space constraint in PIB",
               "ExcludesStmt": "excludes — element-level, not a space constraint in PIB",
               "ExprStmt": "infix expression statement — PIB expresses constraints as typed individuals"}


def from_dsl(text):
    """Parse algebra DSL with the algebra's own parser and emit PIB space TTL. Refuses to approximate."""
    p = _parser()
    spec = p.parse(text)
    out = ["@prefix pibe: <http://purl.org/pib/enumeration#> .", "@prefix ex: <http://purl.org/pib/example#> ."]
    for comp in spec.components:
        feats, body, n = [], [], comp.name
        def idx(f):
            if f not in feats: feats.append(f)
            return feats.index(f) + 1
        for i, st in enumerate(comp.statements):
            t = type(st).__name__
            if t in UNSUPPORTED:
                raise SystemExit(f"cannot convert: {UNSUPPORTED[t]}. Reported rather than approximated.")
            if t == "MandatoryStmt":
                idx(st.feature); body.append(f"ex:{n}_m{i} a pibe:MandatoryConstraint ; pibe:inSpace ex:{n} ; pibe:requires ex:{st.feature} .")
            elif t == "OptionalStmt":
                idx(st.feature)
            elif t in ("ExclusiveStmt", "OrStmt"):
                for m in st.members: idx(m)
                members = " , ".join(f"ex:{m}" for m in st.members)
                if t == "OrStmt":
                    body.append(f"ex:{n}_c{i} a pibe:OrConstraint ; pibe:inSpace ex:{n} ; pibe:groupMember {members} .")
                else:
                    # The algebra's exclusive is EXACTLY one: at most one AND at least one. Mapping it to
                    # PIB's at-most-one alone would silently ADD the "neither" variant.
                    body.append(f"ex:{n}_c{i} a pibe:ExclusiveConstraint ; pibe:inSpace ex:{n} ; pibe:groupMember {members} .")
                    body.append(f"ex:{n}_c{i}b a pibe:OrConstraint ; pibe:inSpace ex:{n} ; pibe:groupMember {members} .")
            elif t == "DependencyStmt":
                idx(st.antecedent); idx(st.consequent)
                body.append(f"ex:{n}_d{i} a pibe:DependencyConstraint ; pibe:inSpace ex:{n} ; "
                            f"pibe:dependent ex:{st.antecedent} ; pibe:prerequisite ex:{st.consequent} .")
            elif t == "AtMostStmt":
                for m in st.members: idx(m)
                body += [f"ex:{m} pibe:contributesToGroup ex:{n}_g{i} ." for m in st.members]
                body.append(f"ex:{n}_r{i} a pibe:RepetitionConstraint ; pibe:inSpace ex:{n} ; "
                            f"pibe:budgetGroup ex:{n}_g{i} ; pibe:maxSelected {st.max_n} .")
            else:
                raise SystemExit(f"cannot convert: unhandled statement {t}. Reported rather than approximated.")
        out.append(f"ex:{n} a pibe:VariationSpace ; pibe:featureCount {len(feats)} ; pibe:hasFeature " +
                   " , ".join(f"ex:{f}" for f in feats) + " .")
        out += [f"ex:{f} pibe:featureIndex {i+1} ." for i, f in enumerate(feats)]
        out += body
    return "\n".join(out) + "\n"


def main():
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    mode, path = sys.argv[1], sys.argv[2]
    if mode == "to-dsl":
        g = rdflib.Graph(); g.parse(path, format="turtle")
        spaces = [s for s in g.subjects(RDF.type, PIBE.VariationSpace) if (s, PIBE.groupOf, None) not in g]
        if len(sys.argv) > 3: spaces = [s for s in spaces if str(s).endswith("#" + sys.argv[3])]
        for s in sorted(spaces, key=str): print(to_dsl(g, s))
    elif mode == "from-dsl":
        ttl = from_dsl(open(path).read())
        (open(sys.argv[3], "w").write(ttl) if len(sys.argv) > 3 else print(ttl))
    elif mode == "round-trip":
        import importlib.util
        spec = importlib.util.spec_from_file_location("vc", os.path.join(os.path.dirname(__file__), "variation_capacity_v1_2_0.py"))
        vc = importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
        g = rdflib.Graph(); g.parse(path, format="turtle")
        before, _, _ = vc.compute([path], verbose=False)
        ok = True
        for s in sorted((s for s in g.subjects(RDF.type, PIBE.VariationSpace) if (s, PIBE.groupOf, None) not in g), key=str):
            name = str(s).split("#")[-1]
            if before.get(str(s)) is None:
                print(f"  {name:26s} no capacity to compare (empty space) — skipped"); continue
            open("/tmp/rt.dsl", "w").write(to_dsl(g, s))
            open("/tmp/rt.ttl", "w").write(from_dsl(open("/tmp/rt.dsl").read()))
            after, _, _ = vc.compute(["/tmp/rt.ttl"], verbose=False)
            got = next(iter(after.values())) if after else None
            same = got == before.get(str(s)); ok &= same
            print(f"  {name:26s} capacity {before.get(str(s))} -> DSL -> back {got}  {'same' if same else 'DIFFERENT'}")
        print(f"  round-trip preserves every capacity: {ok}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
