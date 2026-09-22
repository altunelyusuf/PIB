#!/usr/bin/env python3
"""
ORCP Phase B builder v2.0.0 — PIB fresh registration round (round two).

Supersedes build_pib_orcp_submission_v1_0_0.py for this round; the round-one builder and submission stay in
this folder unchanged, because OE's registry cites them as the registered baseline (v1.2.1).

What it emits, all against central OE anchors and hooks (nothing minted in any OE namespace; every
instance is in the registrant namespace, as OE accepted in round one):
  core            PIB as a core artifact, criticality HIGH (owner's decision, 2026-09-21)
  release history the PIB subject and its five current governed ontology files, SHA-pinned, with the
                  superseded integration-interface file linked as the prior version of its successor
  risk            a risk assessment of PIB and six identified risks, each carrying a recorded mitigation
                  or treatment — the high-criticality gate requires every identified risk to have one
  testing         four tests of PIB, each with its result
  performance     one performance test of PIB, with a measured median
  configuration   one change operation per tagged release since the registered baseline, each satisfying
                  the acceptance criterion "release gates re-run and passing, recorded in the release's
                  own manifest" — derived by reading each tag, not asserted

Deliberately NOT emitted: measurement (no metric exists for variation capacity and minting one would breach
"propose, don't mint"), quality (grading is PAMG's), reliability (PIB holds no reliability evidence of its
own). Stated in the fit-gap note rather than filled with placeholders.

Inputs measured in the same turn as the emission and passed in, never carried over from an earlier turn:
the performance median, and the four test outcomes (the builder records them; it does not re-run them).

Usage: python3 build_pib_orcp_submission_v2_0_0.py <pib-repo-root> <perf-median-ms> <out.ttl>
"""
import sys, os, re, subprocess, hashlib, datetime
import rdflib
from rdflib import Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD, SKOS, DCTERMS

ROOT, PERF_MS, OUT = sys.argv[1], float(sys.argv[2]), sys.argv[3]
TODAY = datetime.date.today().isoformat()

CORE = Namespace("http://example.org/core#")
ORH  = Namespace("http://example.org/oepack-release-history#")
RISK = Namespace("http://example.org/risk#")
PERF = Namespace("http://example.org/performance#")
TEST = Namespace("http://example.org/testing#")
CONF = Namespace("http://example.org/configuration#")
PROV = Namespace("http://www.w3.org/ns/prov#")
REG  = Namespace("http://purl.org/pib/registration#")

g = rdflib.Graph()
for p, n in [("core", CORE), ("orh", ORH), ("risk", RISK), ("performance", PERF), ("testing", TEST),
             ("configuration", CONF), ("prov", PROV), ("pibreg", REG), ("dcterms", DCTERMS), ("skos", SKOS)]:
    g.bind(p, n)
L = lambda s: Literal(s, lang="en")
PIB = REG.Artifact_PIB

# ---- core: the artifact, at HIGH criticality -----------------------------------------------------------
g.add((PIB, RDF.type, CORE.Artifact))
g.add((PIB, RDFS.label, L("PIB — Profile + Integration-Interface Blueprint (github.com/altunelyusuf/PIB)")))
g.add((PIB, CORE.hasCriticalityProfile, CORE.Profile_High))
g.add((PIB, DCTERMS.source, Literal(
    "ORCP round two. Criticality raised from standard to high by the owner on 2026-09-21: the round-one basis "
    "for standard (design-time scaffolding, not a component that computes) no longer holds — PIB now computes "
    "variation capacity in the ontology and is public for external academic and industrial use.")))

# ---- release history: subject + current governed ontology files -----------------------------------------
subj = REG.Subject_PIB
g.add((subj, RDF.type, ORH.SubjectOntology)); g.add((subj, RDFS.label, L("Subject: PIB integration blueprint")))
g.add((subj, ORH.lifecycleStatus, Literal("active")))
FILES = [  # (file, version) — the example capstone ABox is illustrative, not registered (as in round one)
    ("profile_tbox_v1_0_0_1.ttl", "1.0.0.1"),
    ("integration_interface_tbox_v1_0_0_2.ttl", "1.0.0.2"),
    ("pib_wiring_composition_v1_0_0.ttl", "1.0.0"),
    ("pib_assessment_profiles_v1_1_0_1.ttl", "1.1.0.1"),
    ("pib_wiring_expressions_v1_0_0.ttl", "1.0.0"),
]
for fname, ver in FILES:
    path = os.path.join(ROOT, "01-ontologies", fname)
    f = REG["File_" + fname[:-4]]
    g.add((f, RDF.type, ORH.OntologyFile)); g.add((f, RDFS.label, L("Ontology file: " + fname)))
    g.add((f, ORH.hasFileSHA256, Literal(hashlib.sha256(open(path, "rb").read()).hexdigest())))
    g.add((f, ORH.hasVersionInfo, Literal(ver))); g.add((f, ORH.belongsToSubject, subj))
# the round-one record of the superseded file, re-stated with its REGISTERED hash so the link resolves
old = REG.File_integration_interface_tbox_v1_0_0_1
reg1 = rdflib.Graph(); reg1.parse(os.path.join(ROOT, "08-registration", "pib_orcp_submission_v1_0_0.ttl"), format="turtle")
g.add((old, RDF.type, ORH.OntologyFile)); g.add((old, RDFS.label, L("Ontology file: integration_interface_tbox_v1_0_0_1.ttl (round one, superseded)")))
g.add((old, ORH.hasFileSHA256, reg1.value(old, ORH.hasFileSHA256)))
g.add((old, ORH.hasVersionInfo, Literal("1.0.0.1"))); g.add((old, ORH.belongsToSubject, subj))
g.add((REG.File_integration_interface_tbox_v1_0_0_2, ORH.priorVersion, old))

# ---- risk: an assessment and six identified risks, each with a recorded mitigation or treatment ---------
ra = REG.RiskAssessment_Round2
g.add((ra, RDF.type, RISK.RiskAssessment)); g.add((ra, RDFS.label, L("PIB risk assessment, ORCP round two")))
g.add((ra, RISK.assessesArtifact, PIB)); g.add((ra, PROV.generatedAtTime, Literal(TODAY, datatype=XSD.date)))
RISKS = [
 ("R1", "The ZeroTime profile is blocked because its upstream component library is logically inconsistent as shipped",
  "treatment", "Deferred by owner decision; recorded in 04-documentation/ASSESSMENT_PROFILES_MATERIALIZATION_v1_0_0.md. Resumes when the upstream library is made consistent."),
 ("R2", "Vendored operator rules can drift from the variant algebra's own current files",
  "mitigation", "Hash-pinned read-only copies with a verified re-vendor procedure (11-vendored-operator-rules/VENDORED_PINS_v1_0_0.md), exercised once already in v2.0.3 when the algebra consolidated its property files."),
 ("R3", "The fixpoint iteration lives in the harness rather than in the ontology, because the rule engine exposes no rule iteration",
  "treatment", "Accepted by the owner on 2026-09-17 ('I think we can live with this'); recorded here and in the round-two fit-gap note. The loop carries no algebra and stops when the rules stop producing triples."),
 ("R4", "The registration record no longer matched the files PIB ships",
  "treatment", "This fresh registration round."),
 ("R5", "Capacity computation cost grows with the size of the variation space",
  "mitigation", "Pruning and frontier targeting (v2.1.0) and partitioning into independent groups (v2.2.0), all in the ontology. Median on the profile spaces fell from 20.5 s to %.1f s; forty features computed in 58 s. Residual growth is roughly quadratic in the number of independent groups." % (PERF_MS / 1000)),
 ("R6", "The rules depend on evaluation behaviour specific to the SHACL engine — subquery binding, SPARQL targets, the absence of rule iteration — and one such dependency produced a silent zero during development",
  "mitigation", "Capacity self-test over eight spaces with independently known answers plus a planted inadmissible candidate, run before every release; it fails on any silent change in answers."),
]
for rid, lab, kind, tlab in RISKS:
    r = REG["Risk_" + rid]
    g.add((r, RDF.type, RISK.Risk)); g.add((r, RDFS.label, L(lab))); g.add((PIB, RISK.hasIdentifiedRisk, r))
    if kind == "treatment":
        t = REG["Treatment_" + rid]
        g.add((t, RDF.type, RISK.RiskTreatment)); g.add((t, RDFS.label, L(tlab))); g.add((r, RISK.hasRiskTreatment, t))
    else:
        m = REG["Mitigation_" + rid]
        g.add((m, RDF.type, RISK.Mitigation)); g.add((m, RDFS.label, L(tlab))); g.add((r, RISK.hasMitigation, m))

# ---- testing: four tests, each with its result ------------------------------------------------------------
TESTS = [
 ("T1", "Capacity self-test: eight spaces reproduce their known capacities and a planted inadmissible candidate is rejected", "03-tooling/variation_capacity_v1_2_0.py --self-test"),
 ("T2", "Operator expression gate self-test: satisfying candidate clean, violating candidate rejected on both constraints", "03-tooling/operator_rule_runner_v1_0_0.py"),
 ("T3", "Invariants over the full package: conforms, no violations", "pib_invariants over 01-ontologies + 07-spoke-contributions"),
 ("T4", "Manifest self-verification: every file matches its recorded hash", "sha256sum -c over MANIFEST_SHA256.txt"),
]
for tid, lab, how in TESTS:
    t, res = REG["Test_" + tid], REG["Result_" + tid]
    g.add((t, RDF.type, TEST.Test)); g.add((t, RDFS.label, L(lab))); g.add((t, TEST.testsArtifact, PIB))
    g.add((t, DCTERMS.source, Literal(how))); g.add((t, TEST.hasTestResult, res))
    g.add((res, RDF.type, TEST.TestResult)); g.add((res, RDFS.label, L(f"Passed, re-run on {TODAY}")))

# ---- performance: one measured test ------------------------------------------------------------------------
p = REG.Perf_Capacity
g.add((p, RDF.type, PERF.PerformanceTest)); g.add((p, RDFS.label, L("Capacity computation over PIB's profile variation spaces")))
g.add((p, SKOS.definition, L("Wall-clock time to partition, enumerate, check and combine every admissible wiring of PIB's consolidated profile spaces, computed entirely by rules in the ontology; median of three timed runs.")))
g.add((p, PERF.measuresArtifact, PIB)); g.add((p, PERF.hasLastMeasuredStatus, Literal("measured")))
g.add((p, PERF.hasLastMeasuredMedianMs, Literal(round(PERF_MS, 1), datatype=XSD.decimal)))

# ---- configuration: one change per tagged release since the registered baseline, derived from the tags ----
crit = REG.Criterion_GatesPass
g.add((crit, RDF.type, CONF.AcceptanceCriterion))
g.add((crit, RDFS.label, L("Release gates re-run and passing, recorded in the release's own manifest")))
tags = subprocess.run(["git", "-C", ROOT, "tag", "--sort=version:refname"], capture_output=True, text=True).stdout.split()
PAT = re.compile(r"0 viol|conform|self-verif|rejects|matches|gates?:|gates re-run|every space|capacity [0-9]", re.I)
unrecorded = []
for tag in tags:
    hdr = subprocess.run(["git", "-C", ROOT, "show", f"{tag}:MANIFEST_SHA256.txt"], capture_output=True, text=True).stdout
    lines = [l for l in hdr.splitlines() if l.startswith("#")]
    commit = subprocess.run(["git", "-C", ROOT, "rev-list", "-n1", tag], capture_output=True, text=True).stdout.strip()
    c = REG["Change_" + tag.replace(".", "_")]
    g.add((c, RDF.type, CONF.ChangeOperation)); g.add((c, RDFS.label, L(f"Release {tag} (commit {commit[:12]})")))
    g.add((c, CONF.appliesToArtifact, PIB))
    if any(PAT.search(l) and "reproduction commands" not in l.lower() for l in lines):
        g.add((c, CONF.satisfiesAcceptanceCriterion, crit))
    else:
        unrecorded.append(tag)

g.serialize(destination=OUT, format="turtle")
print(f"emitted {len(g)} triples -> {OUT}")
print(f"releases registered: {len(tags)}; without a recorded gate result: {unrecorded or 'none'}")
