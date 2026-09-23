#!/usr/bin/env python3
"""
PIB Profile Architecture Check v1.0.0
=====================================
Enforces the two-layer architecture that makes profile management safe, using the variant algebra's own
semantics rather than a convention invented here.

The algebra defines its mandatory operator as: **the feature must appear in every variant.** That is what
decides where a rule belongs. A requirement true of every variant is a statement about the *domain* and
belongs at the meta level; a requirement true of one variant describes that *variant* and belongs to its
profile. Everything below follows from that single definition.

  META LAYER      the domain: what an artifact must satisfy to be an artifact of this domain at all.
  PROFILE LAYER   the variants: optional, exclusive, or, dependency, repetition — the operators that make
                  one variant differ from another, and which are meaningless as domain-wide claims.

Two enforcement rules, both computed from the spaces themselves, not asserted:

  E1  A META RULE MUST NOT REJECT A LEGAL VARIANT.
      Computed: enumerate each profile's admissible variants from its own constraints, then again with the
      meta constraints added. If the capacity drops, the meta layer is rejecting variants that profile
      declares legal — the exact harm that invalidates a legal profile. A drop to zero means the profile
      becomes impossible. This is a FAILURE: either the rule is not general, or the profile is not legal,
      and someone must decide which. It is never resolved silently.

  E2  A REQUIREMENT TRUE OF EVERY VARIANT BELONGS AT META.
      Computed: a feature that every profile mandates, but which the meta layer does not, is the same
      requirement restated N times. Restated requirements drift — one copy gets updated, the others do
      not, and a later variant inherits the stale one. Reported as a LIFT, not a failure: it is correct
      today and fragile tomorrow.

What it deliberately does not do: decide whether a rule *should* be general. That is a modelling judgement.
It only reports where the spaces disagree with where the rules currently live.

Usage:
    python3 03-tooling/profile_architecture_check_v1_0_0.py [spaces.ttl]
    python3 03-tooling/profile_architecture_check_v1_0_0.py --self-test
"""
import os, sys, importlib.util, tempfile

import rdflib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIBE = rdflib.Namespace("http://purl.org/pib/enumeration#")
DEFAULT = os.path.join(ROOT, "12-operator-fixtures", "profile_architecture_spaces_v1_0_0.ttl")

_spec = importlib.util.spec_from_file_location("vc", os.path.join(HERE, "variation_capacity_v1_2_0.py"))
vc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(vc)


def _capacity(graph, space, include_meta_from=None):
    """Capacity of one space, optionally with another space's constraints folded in."""
    g = rdflib.Graph()
    for q in graph.triples((space, None, None)):
        g.add(q)
    for f in graph.objects(space, PIBE.hasFeature):
        for q in graph.triples((f, None, None)):
            g.add(q)
    for c in graph.subjects(PIBE.inSpace, space):
        for q in graph.triples((c, None, None)):
            g.add(q)
    if include_meta_from is not None:
        for c in graph.subjects(PIBE.inSpace, include_meta_from):
            for p, o in graph.predicate_objects(c):
                g.add((c, PIBE.inSpace, space) if p == PIBE.inSpace else (c, p, o))
    path = os.path.join(tempfile.mkdtemp(), "space.ttl")
    g.serialize(destination=path, format="turtle")
    caps, _, _ = vc.compute([path], verbose=False)
    return caps.get(str(space))


def check(path=DEFAULT, verbose=True):
    graph = rdflib.Graph(); graph.parse(path, format="turtle")
    metas = [s for s in graph.subjects(PIBE.isMetaSpace, rdflib.Literal(True))]
    if not metas:
        if verbose:
            print("  no meta space declared — nothing to enforce against")
        return 0
    meta = metas[0]
    profiles = sorted(graph.subjects(PIBE.refinesMetaSpace, meta), key=str)
    failures, lifts = [], []

    if verbose:
        print(f"PIB profile architecture check v1.0.0")
        print(f"  meta layer: {str(meta).split('#')[-1]}; variants: {[str(p).split('#')[-1] for p in profiles]}")

    # E1 — a meta rule must not reject a legal variant.
    for p in profiles:
        own = _capacity(graph, p)
        with_meta = _capacity(graph, p, include_meta_from=meta)
        name = str(p).split("#")[-1]
        if own is None:
            continue
        if with_meta is None or with_meta < own:
            failures.append((name, own, with_meta))
            if verbose:
                lost = own - (with_meta or 0)
                print(f"  E1 FAIL: {name} declares {own} legal variant(s); the meta layer admits only "
                      f"{with_meta} — {lost} legal variant(s) rejected by a domain rule")
        elif verbose:
            print(f"  E1 ok: {name} — {own} legal variant(s), all admitted by the meta layer")

    # E2 — a requirement every variant mandates belongs at meta.
    def mandated(space):
        return {str(graph.value(c, PIBE.requires)) for c in graph.subjects(PIBE.inSpace, space)
                if (c, rdflib.RDF.type, PIBE.MandatoryConstraint) in graph}
    meta_mandated = mandated(meta)
    if profiles:
        common = set.intersection(*(mandated(p) for p in profiles))
        for f in sorted(common - meta_mandated):
            lifts.append(f)
            if verbose:
                print(f"  E2 LIFT: every variant mandates {f.split('#')[-1]} but the meta layer does not — "
                      f"the same requirement is restated {len(profiles)} times and can drift apart")
    if verbose:
        for f in sorted(meta_mandated):
            print(f"  E2 ok: {f.split('#')[-1]} is mandated once, at the meta layer")
        print("  PASS — the architecture is safe" if not failures else
              f"  FAIL — {len(failures)} profile(s) have legal variants rejected by the meta layer")
    return len(failures)


def self_test():
    graph = rdflib.Graph(); graph.parse(DEFAULT, format="turtle")
    print("PIB profile architecture check — self-test")
    print("  [1] the shipped architecture:")
    f_ok = check(DEFAULT)

    # negative: add a meta rule true of only one variant — it must reject the other's legal variants.
    tmp = os.path.join(tempfile.mkdtemp(), "bad.ttl")
    text = open(DEFAULT).read() + """
ex:MetaQualityWrongly a pibe:MandatoryConstraint ; pibe:inSpace ex:MetaSpace ;
    pibe:requires ex:ontology_quality ;
    rdfs:label "A rule true of one variant only, wrongly placed at the meta layer"@en .
"""
    open(tmp, "w").write(text)
    print("  [2] a one-variant rule wrongly placed at the meta layer:")
    f_bad = check(tmp)

    # E2 must be exercised too: drop the meta requirement so both variants restate it locally.
    tmp2 = os.path.join(tempfile.mkdtemp(), "lift.ttl")
    text2 = open(DEFAULT).read().replace(
        """ex:MetaIdentity a pibe:MandatoryConstraint ; pibe:inSpace ex:MetaSpace ;
    pibe:requires ex:identity ;
    rdfs:label "Every artifact of this domain carries an identity record"@en .""", "")
    open(tmp2, "w").write(text2)
    print("  [3] the same requirement restated by every variant, absent from the meta layer:")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        check(tmp2)
    out = buf.getvalue()
    for line in out.splitlines():
        if "E2" in line or "E1" in line:
            print("   " + line.strip())
    lifted = "E2 LIFT" in out
    print(f"      a lift was reported: {lifted}")

    ok = f_ok == 0 and f_bad >= 1 and lifted
    print(f"  the check discriminates: {ok} (safe {f_ok} failure(s), unsafe {f_bad}, lift reported {lifted})")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raise SystemExit(1 if check(args[0] if args else DEFAULT) else 0)
