#!/usr/bin/env python3
"""
PIB Algebra Conformance Check v3.0.0 — variant sets, against the algebra's LIVE ontology rules
==============================================================================================
Checks PIB's enumeration against the variant algebra's own ontology rules — the generation the
algebra ships today, not the one PIB used to pin. Nothing is compared against a Python enumerator.

Why v2.0.0 was replaced rather than kept
----------------------------------------
v2.0.0 ran the algebra's **1.x** rules, which checked one candidate at a time: PIB generated the
candidates and asked the rules whether each was violated. The algebra quarantined that generation on
2026-09-28. Its current rules do the whole job in the ontology — they build the variation space,
generate the candidates by branching with carry-over, decide every statement in each candidate, and
mark and count the variants. Two consequences, both measured here rather than argued:

  * **The comparison got stronger.** The question is no longer "do we agree on this candidate?" but
    "is PIB's set of variants the same set the algebra's rules produce?" — compared element by
    element, so a capacity that matched with different variants admitted can no longer pass.
  * **Mandatory is cross-checked at last.** v2.0.0 had to report mandatory as not cross-checked,
    because the 1.x rules shipped no mandatory rule. The current rules enforce it (measured: a model
    of one mandatory and one optional feature yields 2 variants, not 4), so every operator PIB uses
    is now decided by the algebra.

What is PIB's and what is the algebra's
---------------------------------------
The calculus is entirely the algebra's: its rule file and its rule executor are vendored verbatim
under `11-vendored-operator-rules/` and are never edited here. What PIB contributes is the mapping
from its own profile vocabulary to the algebra's input vocabulary — the same table as the converter's,
one step shorter because it emits triples rather than notation text. A construct PIB cannot map is
refused and reported, never approximated: a silent approximation would compare something other than
what PIB published.

The input vocabulary is the algebra's, read off its own parser's emitter:

| PIB                                        | algebra input                                                     |
|--------------------------------------------|-------------------------------------------------------------------|
| `VariationSpace`                           | `va:Component` with `va:hasFeature`                               |
| `MandatoryConstraint requires f`           | `va:MandatoryOperator ; va:appliesTo f`                           |
| `ExclusiveConstraint groupMember a, b`     | `va:RepetitionOperator ; va:members (a b) ; va:hasMaxRepetitions 1` |
| `OrConstraint groupMember a, b`            | `va:OrOperator ; va:members (a b)`                                |
| `DependencyConstraint dependent/prereq`    | `va:DependencyOperator` with antecedent/consequent and both sets   |
| `RepetitionConstraint budgetGroup/maxSelected` | `va:RepetitionOperator ; va:members (…) ; va:hasMaxRepetitions N` |
| a feature carrying no constraint           | nothing — unconstrained is the algebra's default too              |

PIB's exclusive means AT MOST ONE and the algebra's `va:ExclusiveOperator` means EXACTLY ONE, so the
exclusive is mapped to a budget of one, exactly as the converter maps it to `atmost 1 of { … }`.
That is not a preference: writing it as the algebra's exclusive drops the "neither" variant.

Known divergence, reported and not papered over
-----------------------------------------------
PIB's EmptySpace fixture has no counterpart here. The algebra refuses a component with no features
("an empty component is not a component"), while PIB's owner ruled that an empty profile is a
possible drift to be MARKED and validated, not rejected. A profile is not a component; the divergence
is deliberate on both sides, and this tool skips that space by name rather than recording a false
disagreement.

Usage:
    python3 03-tooling/algebra_conformance_check_v3_0_0.py [spaces.ttl ...]
    python3 03-tooling/algebra_conformance_check_v3_0_0.py --self-test
"""
import os, sys, glob, itertools, importlib.util

import rdflib
from rdflib import Literal
from rdflib.collection import Collection

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VENDORED = os.path.join(ROOT, "11-vendored-operator-rules", "vendored")
PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
VA = rdflib.Namespace("http://example.org/variant-algebra#")
IN = rdflib.Namespace("http://purl.org/pib/algebra-input#")
DEFAULT = [os.path.join(ROOT, "12-operator-fixtures", "fixtures", "profile_variation_spaces_v1_0_0.ttl"),
           os.path.join(ROOT, "12-operator-fixtures", "fixtures", "enumeration_conformance_spaces_v1_0_0.ttl")]

# The space the algebra refuses by design; see "Known divergence" above.
SKIP_SPACES = {"EmptySpace"}

_spec = importlib.util.spec_from_file_location("tx", os.path.join(HERE, "profile_taxonomy_v1_0_0.py"))
tx = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(tx)


class Unmappable(ValueError):
    """A PIB construct the algebra's input vocabulary has no faithful form for. Reported, never approximated."""


# ---------------------------------------------------------------- the algebra's side

def _executor():
    """The algebra's own rule executor, vendored. Imported by path so the vendored copy is the one that runs."""
    path = os.path.join(VENDORED, "variant_rule_executor_v1_0_0.py")
    spec = importlib.util.spec_from_file_location("vaf_rule_executor", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def _rules_graph():
    g = rdflib.Graph()
    for f in sorted(glob.glob(os.path.join(VENDORED, "*.ttl"))):
        g.parse(f, format="turtle")
    return g


def algebra_variant_sets(input_ttl):
    """Run the algebra's vendored rules over the emitted model and read back the variants it marked.

    Blank nodes are skolemised first: the generation rules build candidate IRIs by string
    concatenation on the nodes they branch from, which a blank node has no form for. The algebra's
    own evaluator skolemises for the same reason.
    """
    import pyoxigraph as ox
    ex = _executor()
    rules = ex.compile_rules(_rules_graph())
    staging = ox.Store(); staging.load(input_ttl.encode("utf-8"), format=ox.RdfFormat.TURTLE)
    sk = lambda t: ox.NamedNode("urn:pib:node:" + t.value) if isinstance(t, ox.BlankNode) else t
    store = ox.Store(); store.extend(ox.Quad(sk(q.subject), q.predicate, sk(q.object)) for q in staging)
    ex.run(store, rules)
    pfx = "PREFIX va: <http://example.org/variant-algebra#>\n"
    sets = set()
    rows = store.query(pfx + """
        SELECT ?v (GROUP_CONCAT(?f; separator=",") AS ?fs) WHERE {
            ?v a va:Variant ; va:hasAssignment ?a .
            ?a va:assignedFeature ?x ; va:assignedCount ?k . FILTER(?k > 0)
            BIND(REPLACE(STR(?x), "^.*#", "") AS ?f)
        } GROUP BY ?v""")
    for r in rows:
        sets.add(frozenset(r["fs"].value.split(",")) if r["fs"].value else frozenset())
    # A variant selecting nothing marks no assignment above zero, so it is counted separately.
    total = list(store.query(pfx + "SELECT (COUNT(?v) AS ?n) WHERE { ?v a va:Variant }"))[0]["n"].value
    if int(total) == len(sets) + 1:
        sets.add(frozenset())
    return sets, int(total)


# ---------------------------------------------------------------- PIB's side

def _members(graph, head):
    return [str(x).split("#")[-1] for x in Collection(graph, head)] if head else []


def emit_algebra_input(graph, space):
    """PIB's variation space, written in the algebra's own input vocabulary."""
    name = str(space).split("#")[-1]
    feats = [str(f).split("#")[-1] for f in graph.objects(space, PIBE.hasFeature)]
    if not feats:
        raise Unmappable(f"{name} declares no feature; the algebra refuses an empty component")
    lines = ["@prefix i: <http://purl.org/pib/algebra-input#> .",
             "@prefix va: <http://example.org/variant-algebra#> .", ""]
    lines.append(f"i:{name} a va:Component ; va:hasFeature " + " , ".join(f"i:{f}" for f in feats) + " .")
    for f in feats:
        lines.append(f"i:{f} a va:Feature, va:TerminalFeature .")
    ops = []

    def op(n, body):
        ops.append(f"i:{name}_Op{n} {body} .")

    n = 0
    for c in graph.subjects(PIBE.inSpace, space):
        kinds = set(graph.objects(c, rdflib.RDF.type))
        n += 1
        if PIBE.MandatoryConstraint in kinds:
            for f in graph.objects(c, PIBE.requires):
                op(n, f"a va:MandatoryOperator ; va:appliesTo i:{str(f).split('#')[-1]}")
        elif PIBE.ExclusiveConstraint in kinds:
            ms = [str(m).split("#")[-1] for m in graph.objects(c, PIBE.groupMember)]
            # PIB's exclusive is AT MOST ONE: a budget of one, never the algebra's exactly-one operator.
            op(n, "a va:RepetitionOperator ; va:members ( " + " ".join(f"i:{m}" for m in sorted(ms))
                  + " ) ; va:hasMaxRepetitions 1")
        elif PIBE.OrConstraint in kinds:
            ms = [str(m).split("#")[-1] for m in graph.objects(c, PIBE.groupMember)]
            op(n, "a va:OrOperator ; va:members ( " + " ".join(f"i:{m}" for m in sorted(ms)) + " )")
        elif PIBE.DependencyConstraint in kinds:
            d = [str(x).split("#")[-1] for x in graph.objects(c, PIBE.dependent)]
            p = [str(x).split("#")[-1] for x in graph.objects(c, PIBE.prerequisite)]
            if len(d) != 1 or len(p) != 1:
                raise Unmappable(f"{name}: a dependency with {len(d)} dependents and {len(p)} prerequisites")
            op(n, f"a va:DependencyOperator ; va:antecedent i:{d[0]} ; va:consequent i:{p[0]} ; "
                  f"va:dependentSet ( i:{d[0]} ) ; va:prerequisiteSet ( i:{p[0]} )")
        elif PIBE.RepetitionConstraint in kinds:
            grp = next(graph.objects(c, PIBE.budgetGroup), None)
            mx = next(graph.objects(c, PIBE.maxSelected), None)
            if grp is None or mx is None:
                raise Unmappable(f"{name}: a repetition with no budget group or no maximum")
            ms = sorted(str(f).split("#")[-1] for f in graph.subjects(PIBE.contributesToGroup, grp))
            op(n, "a va:RepetitionOperator ; va:members ( " + " ".join(f"i:{m}" for m in ms)
                  + f" ) ; va:hasMaxRepetitions {int(mx)}")
        else:
            raise Unmappable(f"{name}: a constraint of kind {sorted(str(k).split('#')[-1] for k in kinds)}")
    if ops:
        lines.append(f"i:{name} va:hasOperator " + " , ".join(f"i:{name}_Op{i+1}" for i in range(n)) + " .")
        lines += ops
    return "\n".join(lines) + "\n"


def pib_variant_sets(graph, space):
    """PIB's own admitted variants: each group's admissible candidates, combined across the groups.

    PIB partitions a space into independent groups and enumerates each separately, so a whole-space
    variant is one admissible candidate from every group. Reading only the groups' candidates would
    compare parts against wholes.
    """
    groups = sorted(graph.subjects(PIBE.groupOf, space), key=str)
    if not groups:
        return set()
    per = []
    for grp in groups:
        sets = []
        for c in graph.subjects(rdflib.RDF.type, PIBE.CompleteCandidate):
            if (c, PIBE.inSpace, grp) in graph and (c, PIBE.isInadmissible, Literal(True)) not in graph:
                sets.append(frozenset(str(s).split("#")[-1] for s in graph.objects(c, PIBE.includes)))
        if not sets:
            return set()          # a group admitting nothing makes the whole space empty
        per.append(sets)
    return {frozenset().union(*combo) for combo in itertools.product(*per)}


# ---------------------------------------------------------------- the run

def run(paths=None, verbose=True, graphs=None, mutate=None):
    paths = paths or DEFAULT
    built = graphs if graphs is not None else [(p, tx.build(p)) for p in paths]
    agree = disagree = skipped = 0
    if verbose:
        print("PIB algebra conformance check v3.0.0 — variant sets from the algebra's LIVE ontology rules")
    for _, graph in built:
        if mutate:
            mutate(graph)
        spaces = [s for s in graph.subjects(rdflib.RDF.type, PIBE.VariationSpace)
                  if (s, PIBE.groupOf, None) not in graph]
        for space in sorted(spaces, key=str):
            name = str(space).split("#")[-1]
            if name in SKIP_SPACES:
                skipped += 1
                if verbose:
                    print(f"  {name:26} skipped — the algebra refuses an empty component; PIB marks it as drift")
                continue
            try:
                model = emit_algebra_input(graph, space)
            except Unmappable as e:
                disagree += 1
                if verbose:
                    print(f"  {name:26} UNMAPPABLE — {e}")
                continue
            alg, total = algebra_variant_sets(model)
            pib = pib_variant_sets(graph, space)
            if pib == alg:
                agree += 1
                if verbose:
                    print(f"  {name:26} PIB {len(pib):>4} variants   algebra {total:>4}   sets identical")
            else:
                disagree += 1
                if verbose:
                    print(f"  {name:26} DISAGREE — PIB {len(pib)}, algebra {total}")
                    for lbl, d in (("only PIB", pib - alg), ("only the algebra", alg - pib)):
                        for s in sorted(map(sorted, d))[:3]:
                            print(f"      {lbl}: {{{', '.join(s)}}}")
    if verbose:
        print(f"  spaces in agreement {agree}, disagreements {disagree}, skipped by design {skipped}")
        print("  every operator PIB uses is decided by the algebra's rules, mandatory included")
    return disagree


def self_test():
    """The check must be able to fail, in both directions, on real verdicts — not on a planted constant.

    Two mutations, each of something the comparison actually reads:
      1. PIB's side: one admissible complete candidate is marked inadmissible. PIB then withholds a
         variant the algebra's rules produce, and the sets must differ. The first draft of this test
         mutated the other way — unmarking an inadmissible candidate — and reported no disagreement,
         because PIB's pruning means no complete candidate is ever marked inadmissible: the mutation
         changed nothing. The mutation that cannot fire is the decorative one, so this is the direction
         that exercises the admissibility filter the comparison reads.
      2. The algebra's side: the emitted budget is loosened by one. The algebra then produces variants
         PIB does not, and the sets must differ.
    """
    print("PIB algebra conformance check v3.0.0 — self-test")
    base = run(verbose=False)
    print(f"  as published: {base} disagreement(s)   (expected 0)")

    def mark_one(graph):
        for c in sorted(graph.subjects(rdflib.RDF.type, PIBE.CompleteCandidate), key=str):
            graph.add((c, PIBE.isInadmissible, Literal(True)))
            return
    built = [(p, tx.build(p)) for p in DEFAULT]
    flipped = run(graphs=built, verbose=False, mutate=mark_one)
    print(f"  one admissible candidate marked inadmissible: {flipped} disagreement(s)   (expected >0)")

    real_emit = emit_algebra_input
    def loosened(graph, space):
        return real_emit(graph, space).replace("va:hasMaxRepetitions 1", "va:hasMaxRepetitions 2")
    globals()["emit_algebra_input"] = loosened
    try:
        built2 = [(p, tx.build(p)) for p in DEFAULT]
        loose = run(graphs=built2, verbose=False)
    finally:
        globals()["emit_algebra_input"] = real_emit
    print(f"  every budget of one loosened to two: {loose} disagreement(s)   (expected >0)")

    ok = (base == 0 and flipped > 0 and loose > 0)
    print(f"  the check can fail in both directions: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--self-test"]
    if "--self-test" in sys.argv[1:]:
        sys.exit(self_test())
    sys.exit(1 if run(args or None) else 0)
