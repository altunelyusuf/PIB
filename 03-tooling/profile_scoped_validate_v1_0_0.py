#!/usr/bin/env python3
"""
PIB Profile-Scoped Validation v1.0.0
====================================
Validates each artifact against exactly the rules that bind it: the domain's general rules, plus the rules
of the profile that artifact declares. No other profile's rules are ever evaluated against it.

Why this exists, in one sentence: profiles are variants, and applying one variant's rules to another does
not enforce a standard — it rejects a legal artifact for failing to be a different variant.

Measured before this was written: a rule requiring an ontology-quality measurement, authored for the
ontology-deliverable profile, invalidated a gamification artifact that was entirely legal under its own
profile. Nothing was wrong with the artifact, the profile, or the rule — only with which rules were applied
to whom.

How scope is determined, and why it cannot be forgotten: by the rule's HOME.
  - a shape carrying `pib:declaredByProfile <P>` is LOCAL to P; it is evaluated only against artifacts
    declaring P;
  - a shape with no profile home is a DOMAIN-GENERAL rule and is evaluated against everything.
An earlier version of this vocabulary made scope an optional annotation defaulting to general. That is the
unsafe direction: a profile-local rule that merely omitted its annotation silently became a domain rule and
invalidated other variants. Ownership is structural, so there is nothing to omit.

Usage:
    python3 03-tooling/profile_scoped_validate_v1_0_0.py <data.ttl> <shapes.ttl> [...]
    python3 03-tooling/profile_scoped_validate_v1_0_0.py --self-test
"""
import os, sys
import rdflib
from pyshacl import validate

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
PIB = rdflib.Namespace("http://purl.org/pib/profile#")


def partition(shapes):
    """Split shapes by home: (general graph, {profile: graph}). Ownership decides, nothing else."""
    general = rdflib.Graph()
    local = {}
    for s in shapes.subjects(rdflib.RDF.type, SH.NodeShape):
        homes = list(shapes.objects(s, PIB.declaredByProfile))
        stack, seen, sub = [s], set(), rdflib.Graph()
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            for p, o in shapes.predicate_objects(x):
                sub.add((x, p, o))
                if isinstance(o, rdflib.BNode):
                    stack.append(o)
        if homes:
            for h in homes:
                local.setdefault(str(h), rdflib.Graph())
                for q in sub:
                    local[str(h)].add(q)
        else:
            for q in sub:
                general.add(q)
    return general, local


def run(data_paths, shape_paths, verbose=True):
    data = rdflib.Graph()
    for p in data_paths:
        data.parse(p, format="turtle")
    shapes = rdflib.Graph()
    for p in shape_paths:
        shapes.parse(p, format="turtle")
    general, local = partition(shapes)

    artifacts = {}
    for a, prof in data.subject_objects(PIB.hasProfile):
        artifacts[a] = str(prof)
    if verbose:
        print(f"PIB profile-scoped validation v1.0.0")
        print(f"  rules: {len(list(general.subjects(rdflib.RDF.type, SH.NodeShape)))} general, "
              f"{sum(len(list(g.subjects(rdflib.RDF.type, SH.NodeShape))) for g in local.values())} "
              f"profile-local across {len(local)} profile(s)")

    total = 0
    for art, prof in sorted(artifacts.items(), key=lambda kv: str(kv[0])):
        applicable = rdflib.Graph()
        for q in general:
            applicable.add(q)
        for q in local.get(prof, rdflib.Graph()):
            applicable.add(q)
        # Evaluate this artifact alone, so another artifact's failures cannot be attributed to it.
        subject = rdflib.Graph()
        for q in data.triples((art, None, None)):
            subject.add(q)
        for q in data.triples((None, None, art)):
            subject.add(q)
        _, rep, _ = validate(subject, shacl_graph=applicable, advanced=True, inference="none")
        viol = [str(rep.value(r, SH.resultMessage)) for r in rep.subjects(rdflib.RDF.type, SH.ValidationResult)
                if str(rep.value(r, SH.resultSeverity)).endswith("Violation")]
        total += len(viol)
        if verbose:
            name, pname = str(art).split("#")[-1], prof.split("#")[-1]
            skipped = sum(1 for p, g in local.items() if p != prof
                          for _ in g.subjects(rdflib.RDF.type, SH.NodeShape))
            print(f"  {name} (profile {pname}): {len(viol)} violation(s); "
                  f"{skipped} foreign profile-local rule(s) correctly not applied")
            for v in viol:
                print(f"      {v[:100]}")
    return total


def self_test():
    """Two things must both hold: a legal variant survives, and rules still bite where they belong."""
    import tempfile
    tmp = tempfile.mkdtemp()
    data = os.path.join(tmp, "d.ttl"); shapes = os.path.join(tmp, "s.ttl")
    open(data, "w").write("""@prefix ex: <http://example.org/d#> .
@prefix pib: <http://purl.org/pib/profile#> .
ex:OntologyArtifact a ex:Artifact ; pib:hasProfile ex:OntologyDeliverable ; ex:ontologyQuality "0.91" ; ex:title "t" .
ex:GameArtifact     a ex:Artifact ; pib:hasProfile ex:Gamification     ; ex:playEvidence "log" ; ex:title "t" .
ex:BadOntology      a ex:Artifact ; pib:hasProfile ex:OntologyDeliverable ; ex:title "t" .
ex:Untitled         a ex:Artifact ; pib:hasProfile ex:Gamification     ; ex:playEvidence "log" .
""")
    open(shapes, "w").write("""@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix pib: <http://purl.org/pib/profile#> .
@prefix ex: <http://example.org/d#> .
# domain-general: owned by no profile, binds every variant
ex:TitleRequired a sh:NodeShape ; sh:targetClass ex:Artifact ;
    sh:property [ sh:path ex:title ; sh:minCount 1 ; sh:message "every artifact needs a title" ] .
# profile-local to the ontology deliverable
ex:OntologyQualityRequired a sh:NodeShape ; pib:declaredByProfile ex:OntologyDeliverable ;
    sh:targetClass ex:Artifact ;
    sh:property [ sh:path ex:ontologyQuality ; sh:minCount 1 ; sh:message "ontology quality required" ] .
# profile-local to gamification
ex:PlayEvidenceRequired a sh:NodeShape ; pib:declaredByProfile ex:Gamification ;
    sh:targetClass ex:Artifact ;
    sh:property [ sh:path ex:playEvidence ; sh:minCount 1 ; sh:message "play evidence required" ] .
""")
    print("PIB profile-scoped validation — self-test")
    print("  [1] every rule applied to everything, as an unscoped validator would:")
    d = rdflib.Graph(); d.parse(data, format="turtle")
    s = rdflib.Graph(); s.parse(shapes, format="turtle")
    _, rep, _ = validate(d, shacl_graph=s, advanced=True, inference="none")
    naive = {str(rep.value(r, SH.focusNode)).split("#")[-1]
             for r in rep.subjects(rdflib.RDF.type, SH.ValidationResult)
             if str(rep.value(r, SH.resultSeverity)).endswith("Violation")}
    print(f"      invalidated: {sorted(naive)}")
    legal_rejected = "GameArtifact" in naive and "OntologyArtifact" in naive
    print(f"      legal variants rejected by foreign rules: {legal_rejected} (this is the harm)")
    print("  [2] scoped to each artifact's own profile plus the domain's general rules:")
    total = run([data], [shapes])
    ok_legal = total == 2          # exactly the two genuinely-bad artifacts
    print(f"      violations: {total} — expected exactly 2 (the artifact missing its own profile's "
          f"requirement, and the one missing the domain-general title)")
    print(f"  legal variants preserved AND real faults still caught: {ok_legal and legal_rejected}")
    return 0 if (ok_legal and legal_rejected) else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        raise SystemExit(__doc__)
    raise SystemExit(1 if run([args[0]], args[1:]) else 0)
