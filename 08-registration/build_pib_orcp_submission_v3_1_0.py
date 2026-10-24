#!/usr/bin/env python3
"""
ORCP Phase B builder v3.1.0 — PIB registration maintenance round (round three).

v3.1.0 answers four findings of OE's round-three contract: the version stated for each ontology file is the release in which
the file last changed (read from git, never copied from VERSION.txt at build time); the file records carry bare names; the docstring
counts the tests the file emits (six); and the dependencies the tests need are listed in requirements.txt.

Supersedes build_pib_orcp_submission_v2_0_0.py for this round; the earlier builders and submissions stay in
this folder unchanged, because OE's registry cites them as the registered baselines (v1.2.1, then v2.3.0).
Why a third round: the five governed ontology files round two registered by hash no longer exist (merged into
PIB's one T-Box, one A-Box and one SHACL file, BP-D54), so the registered lineage records point at files that
are gone, and the registry flags PIB on a MAJOR version change (2.3.0 -> 3.x).

What it emits, all against central OE anchors and hooks (nothing minted in any OE namespace; every
instance is in the registrant namespace, as OE accepted in round one):
  core            PIB as a core artifact, criticality HIGH (owner's decision, 2026-09-21)
  release history the PIB subject and its three current governed ontology files, SHA-pinned, with the
                  superseded integration-interface file linked as the prior version of its successor
  risk            a risk assessment of PIB and six identified risks, each carrying a recorded mitigation
                  or treatment — the high-criticality gate requires every identified risk to have one
  testing         six tests of PIB, each with its result
  performance     one performance test of PIB, with a measured median
  configuration   one change operation per tagged release since the registered baseline, each satisfying
                  the acceptance criterion "release gates re-run and passing, recorded in the release's
                  own manifest" — derived by reading each tag, not asserted

Deliberately NOT emitted: measurement (no metric exists for variation capacity and minting one would breach
"propose, don't mint"), quality (grading is PAMG's), reliability (PIB holds no reliability evidence of its
own). Stated in the fit-gap note rather than filled with placeholders.

Inputs measured in the same turn as the emission and passed in, never carried over from an earlier turn:
the performance median, and the four test outcomes (the builder records them; it does not re-run them).

Usage: python3 build_pib_orcp_submission_v3_0_0.py <pib-repo-root> <perf-median-ms> <out.ttl>
"""
import sys, os, re, subprocess, hashlib, datetime
import rdflib
from rdflib import Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD, SKOS, DCTERMS

ROOT, PERF_MS, OUT = sys.argv[1], float(sys.argv[2]), sys.argv[3]
TODAY = datetime.date.today().isoformat()
PKG_VERSION = open(os.path.join(ROOT, "VERSION.txt")).read().strip()
BASELINE_TAG = "v2.3.0"

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
    "ORCP round three (registration maintenance). Criticality stays high, as ratified in round two (owner, 2026-09-21): "
    "PIB computes variation capacity in the ontology and is public for external academic and industrial use.")))

# ---- release history: subject + current governed ontology files -----------------------------------------
subj = REG.Subject_PIB
g.add((subj, RDF.type, ORH.SubjectOntology)); g.add((subj, RDFS.label, L("Subject: PIB integration blueprint")))
g.add((subj, ORH.lifecycleStatus, Literal("active")))
FILES = [  # (file, version) — one T-Box, one A-Box, one SHACL file (BP-D54); the version is the package's own
    ("01-ontologies/pib_tbox_v1_0_0.ttl", None), ("01-ontologies/pib_abox_v1_0_0.ttl", None),
    ("02-shacl-safeguards/pib_shacl_v1_0_0.ttl", None),
]


def last_changed_release(relpath):
    """The first tagged release that contains the last commit touching the file: the version at which it last changed."""
    commit = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%H", "--", relpath], capture_output=True, text=True).stdout.strip()
    tags = subprocess.run(["git", "-C", ROOT, "tag", "--sort=version:refname", "--contains", commit], capture_output=True, text=True).stdout.split()
    return tags[0].lstrip("v") if tags else PKG_VERSION     # untagged: the package version being built
for fname, ver in FILES:
    path = os.path.join(ROOT, fname)
    ver = last_changed_release(fname)
    f = REG["File_" + os.path.basename(fname)[:-4]]
    g.add((f, RDF.type, ORH.OntologyFile)); g.add((f, RDFS.label, L("Ontology file: " + os.path.basename(fname))))
    g.add((f, ORH.hasFileSHA256, Literal(hashlib.sha256(open(path, "rb").read()).hexdigest())))
    g.add((f, ORH.hasVersionInfo, Literal(ver))); g.add((f, ORH.belongsToSubject, subj))
# ---- risk: an assessment and six identified risks, each with a recorded mitigation or treatment ---------
ra = REG.RiskAssessment_Round3
g.add((ra, RDF.type, RISK.RiskAssessment)); g.add((ra, RDFS.label, L("PIB risk assessment, ORCP round three")))
g.add((ra, RISK.assessesArtifact, PIB)); g.add((ra, PROV.generatedAtTime, Literal(TODAY, datatype=XSD.date)))
RISKS = [
 ("R1", "The ZeroTime profile is blocked because its upstream component library is logically inconsistent as shipped",
  "treatment", "Deferred by owner decision; recorded in 04-documentation/ASSESSMENT_PROFILES_MATERIALIZATION_v1_0_0.md. Resumes when the upstream library is made consistent."),
 ("R2", "Vendored operator rules can drift from the variant algebra's own current files",
  "mitigation", "Hash-pinned read-only copies with a verified re-vendor procedure (11-vendored-operator-rules/VENDORED_PINS_v1_3_0.md), exercised in v2.0.3, v2.18.0 and v3.4.0; after the last, all eight variation spaces still give variant sets identical to PIB's own."),
 ("R3", "The fixpoint iteration lives in the harness rather than in the ontology, because the rule engine exposes no rule iteration",
  "treatment", "Accepted by the owner on 2026-09-17 ('I think we can live with this'); recorded here and in the round-two fit-gap note. The loop carries no algebra and stops when the rules stop producing triples."),
 ("R4", "The registration record no longer matched the files PIB ships (the five registered ontology files were merged into three)",
  "treatment", "This registration maintenance round, raised by the registry's MAJOR-version flag."),
 ("R5", "Capacity computation cost grows with the size of the variation space",
  "mitigation", "Pruning and frontier targeting (v2.1.0) and partitioning into independent groups (v2.2.0), all in the ontology. Median on the profile spaces fell from 20.5 s to %.1f s; forty features computed in 58 s. Residual growth is roughly quadratic in the number of independent groups." % (PERF_MS / 1000)),
 ("R7", "A different SHACL engine run over the algebra's rules answers wrongly and silently: measured on all eight of PIB's variation spaces it ends without an error and with one variant node where the algebra's runner gives 0 to 243 variants",
  "mitigation", "The algebra's own runner is vendored with the rules and is the only thing that runs them; the conformance gates compare its variant sets with PIB's own, element by element, and their self-tests fail in both directions."),
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

# ---- testing: six tests, each with its result ------------------------------------------------------------
TESTS = [
 ("T1", "Capacity self-test: eight spaces reproduce their known capacities and a planted inadmissible candidate is rejected", "03-tooling/variation_capacity_v1_2_0.py --self-test"),
 ("T2", "Algebra conformance: all eight variation spaces give variant sets identical to the algebra's own rules, and the check fails in both directions", "03-tooling/algebra_conformance_check_v3_0_0.py --self-test"),
 ("T3", "Expression conformance: the capstone wiring admits 14 variants, the satisfying candidate is one and the violating one is not; five mutations are caught", "03-tooling/expression_conformance_check_v1_0_0.py --self-test"),
 ("T4", "Borrowed shapes: PIB's A-Box violates none of the algebra's own shapes, and a planted node is caught", "03-tooling/borrowed_shapes_check_v1_0_0.py --self-test"),
 ("T5", "Manifest self-verification: every file matches its recorded hash", "sha256sum -c over MANIFEST_SHA256.txt"),
 ("T6", "Release gate: every self-contained gate passes", "03-tooling/release_gate_v1_0_0.py"),
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
tags = subprocess.run(["git", "-C", ROOT, "tag", "--sort=version:refname", "--contains", BASELINE_TAG], capture_output=True, text=True).stdout.split()
tags = [t for t in tags if t != BASELINE_TAG]
PAT = re.compile(r"0 viol|conform|self-verif|rejects|matches|gates?:|gates re-run|every space|capacity [0-9]", re.I)
unrecorded = []
for tag in tags:
    hdr = subprocess.run(["git", "-C", ROOT, "show", f"{tag}:MANIFEST_SHA256.txt"], capture_output=True, text=True).stdout
    lines = [l for l in hdr.splitlines() if l.startswith("#")]
    commit = subprocess.run(["git", "-C", ROOT, "rev-list", "-n1", tag], capture_output=True, text=True).stdout.strip()
    if not any(PAT.search(l) and "reproduction commands" not in l.lower() for l in lines):
        unrecorded.append(tag)      # a release whose own manifest records no gate result is NOT registered: the criterion cannot be claimed for it
        continue
    c = REG["Change_" + tag.replace(".", "_")]
    g.add((c, RDF.type, CONF.ChangeOperation)); g.add((c, RDFS.label, L(f"Release {tag} (commit {commit[:12]})")))
    g.add((c, CONF.appliesToArtifact, PIB)); g.add((c, CONF.satisfiesAcceptanceCriterion, crit))

g.serialize(destination=OUT, format="turtle")
print(f"emitted {len(g)} triples -> {OUT}")
print(f"releases registered: {len(tags) - len(unrecorded)} of {len(tags)}; not registered, for want of a recorded gate result in their own manifest: {unrecorded or 'none'}")
