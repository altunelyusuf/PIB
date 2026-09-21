#!/usr/bin/env python3
"""
REFERENCE_ONLY — NOT_A_RELEASE.
Criticality test-drive for PIB's fresh registration round: standard versus high.

Method: the registration protocol's own A/B method ("test-drive alternatives where it settles the
choice"), following the three-case pattern the four criticality gates were themselves built with.
No criteria for choosing a level exist in OE, so this measures what each choice actually CHANGES.

Arms:      A = standard, B = high. Critical is not tested separately: every one of the four gates
           filters on "high or critical" identically, so critical behaves exactly as high.
Scenarios: S0 register nothing but the declared level (the vacuous case OE itself noted)
           S1 register PIB's REAL evidence exactly as documented in its repository today
           S2 S1 plus the two treatments NOT yet documented — only to show what passing high costs
Teeth:     S1 at high plus one test lacking a result, to prove the harness detects a failure.

Every evidence item is real and was re-derived this session: four tests re-run and passing; one
performance measurement (median of three timed runs); twelve releases, each of whose own manifest
records a passing gate result; five risks, with only the treatments actually recorded in the repo.

This file is a harness: it builds RDF and runs OE's own shipped shapes. No gate logic lives here.
"""
import rdflib, glob, sys
from rdflib import Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, SKOS
from pyshacl import validate

OE = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/Ontologies/oe-pack"
PERF_MS = float(open("/tmp/perf_median_ms").read()) if len(sys.argv) < 3 else float(sys.argv[2])

CORE = Namespace("http://example.org/core#")
RISK = Namespace("http://example.org/risk#")
PERF = Namespace("http://example.org/performance#")
TEST = Namespace("http://example.org/testing#")
CONF = Namespace("http://example.org/configuration#")
REG  = Namespace("http://purl.org/pib/registration#")
SH   = Namespace("http://www.w3.org/ns/shacl#")

PIB = REG.Artifact_PIB
RELEASES = ["1.4.0","1.4.1","1.4.2","1.4.3","1.5.0","1.5.1","1.5.2","1.6.0","2.0.0","2.0.1","2.0.2","2.0.3"]
TESTS = [("T1","Capacity self-test: both profile spaces reproduce their reference answers"),
         ("T2","Operator expression gate self-test: satisfying candidate clean, violating one rejected"),
         ("T3","Invariants over the full package: conforms, no violations"),
         ("T4","Manifest self-verification: every file matches its recorded hash")]
# (id, label, documented treatment kind or None, treatment label)
RISKS = [("R1","The ZeroTime profile is blocked because its upstream component library is logically inconsistent as shipped","treatment","Deferred by owner decision, recorded in the assessment-profiles materialization record"),
         ("R2","Vendored operator rules can drift from the algebra's own current files","mitigation","Hash-pinned copies with a verified re-vendor procedure, recorded in the vendored-pins note"),
         ("R3","The fixpoint iteration lives in the harness rather than in the ontology",None,None),
         ("R4","The registration record no longer matches the files PIB ships","treatment","Fresh registration round, recorded in PIB's handover log"),
         ("R5","Capacity computation cost grows with the number of candidates, which doubles per feature",None,None)]
UNDOCUMENTED = {"R3":"Owner acceptance of the harness loop would have to be recorded in the repository",
                "R5":"A cost bound or scaling plan would have to be decided and recorded"}


def build(level, scenario, broken_test=False):
    g = rdflib.Graph()
    g.add((PIB, RDF.type, CORE.Artifact)); g.add((PIB, RDFS.label, Literal("PIB", lang="en")))
    g.add((PIB, CORE.hasCriticalityProfile, level))
    if scenario == "S0":
        return g
    for tid, lab in TESTS:
        t, r = REG["Test_"+tid], REG["Result_"+tid]
        g.add((t, RDF.type, TEST.Test)); g.add((t, RDFS.label, Literal(lab, lang="en")))
        g.add((t, TEST.testsArtifact, PIB)); g.add((t, TEST.hasTestResult, r))
        g.add((r, RDF.type, TEST.TestResult)); g.add((r, RDFS.label, Literal("Passed, re-run this session", lang="en")))
    if broken_test:
        t = REG.Test_Unrecorded
        g.add((t, RDF.type, TEST.Test)); g.add((t, RDFS.label, Literal("A test with no recorded result", lang="en")))
        g.add((t, TEST.testsArtifact, PIB))
    p = REG.Perf_P1
    g.add((p, RDF.type, PERF.PerformanceTest)); g.add((p, RDFS.label, Literal("Capacity computation over the consolidated profile spaces", lang="en")))
    g.add((p, SKOS.definition, Literal("Wall-clock time to enumerate and count every admissible wiring in PIB's consolidated profile spaces, computed entirely by rules in the ontology; median of three timed runs.", lang="en")))
    g.add((p, PERF.measuresArtifact, PIB)); g.add((p, PERF.hasLastMeasuredStatus, Literal("measured")))
    g.add((p, PERF.hasLastMeasuredMedianMs, Literal(round(PERF_MS, 1), datatype=XSD.decimal)))
    crit = REG.Criterion_GatesPass
    g.add((crit, RDF.type, CONF.AcceptanceCriterion))
    g.add((crit, RDFS.label, Literal("Release gates re-run and passing, recorded in the release's own manifest", lang="en")))
    for v in RELEASES:
        c = REG["Change_v"+v.replace(".", "_")]
        g.add((c, RDF.type, CONF.ChangeOperation)); g.add((c, RDFS.label, Literal(f"Release v{v}", lang="en")))
        g.add((c, CONF.appliesToArtifact, PIB)); g.add((c, CONF.satisfiesAcceptanceCriterion, crit))
    for rid, lab, kind, tlab in RISKS:
        r = REG["Risk_"+rid]
        g.add((r, RDF.type, RISK.Risk)); g.add((r, RDFS.label, Literal(lab, lang="en")))
        g.add((PIB, RISK.hasIdentifiedRisk, r))
        if kind is None and scenario == "S2":
            kind, tlab = "treatment", UNDOCUMENTED[rid]
        if kind == "treatment":
            t = REG["Treatment_"+rid]
            g.add((t, RDF.type, RISK.RiskTreatment)); g.add((t, RDFS.label, Literal(tlab, lang="en")))
            g.add((r, RISK.hasRiskTreatment, t))
        elif kind == "mitigation":
            m = REG["Mitigation_"+rid]
            g.add((m, RDF.type, RISK.Mitigation)); g.add((m, RDFS.label, Literal(tlab, lang="en")))
            g.add((r, RISK.hasMitigation, m))
    return g


def latest(pattern):
    return sorted(glob.glob(f"{OE}/{pattern}"))[-1]

FACETS = {
    "risk":          ("02-shacl-safeguards/risk_shacl_v*.ttl",          "01-ontologies/risk_tbox_v*.ttl",          "RiskManagementCompletenessGate"),
    "performance":   ("02-shacl-safeguards/performance_shacl_v*.ttl",   "01-ontologies/performance_tbox_v*.ttl",   "PerformanceTestingCompletenessGate"),
    "testing":       ("02-shacl-safeguards/testing_shacl_v*.ttl",       "01-ontologies/testing_tbox_v*.ttl",       "TestingCompletenessGate"),
    "configuration": ("02-shacl-safeguards/configuration_shacl_v*.ttl", "01-ontologies/configuration_tbox_v*.ttl", "ChangeValidationGate"),
}
CORE_FILES = [latest("01-ontologies/core_tbox_v*.ttl"), latest("01-ontologies/core_abox_v*.ttl")]


def run(level, scenario, broken_test=False):
    """For each facet: violations from its criticality gate, and from every other shape in its suite."""
    data = build(level, scenario, broken_test)
    out = {}
    for fac, (shp, tbox, gate) in FACETS.items():
        g = rdflib.Graph()
        for q in data: g.add(q)
        for f in CORE_FILES + [latest(tbox)]: g.parse(f, format="turtle")
        shapes = rdflib.Graph(); shapes.parse(latest(shp), format="turtle")
        _, rg, _ = validate(g, shacl_graph=shapes, advanced=True, inference="none",
                            allow_warnings=True, allow_infos=True)
        gate_v = other_v = 0
        for r in rg.subjects(RDF.type, SH.ValidationResult):
            if not str(rg.value(r, SH.resultSeverity)).endswith("Violation"):
                continue
            src = str(rg.value(r, SH.sourceShape))
            if gate in src: gate_v += 1
            else: other_v += 1
        out[fac] = (gate_v, other_v)
    return out


if __name__ == "__main__":
    arms = [("standard", CORE.Profile_Standard), ("high", CORE.Profile_High)]
    print("Suites:", ", ".join(latest(s).split("/")[-1] for s, _, _ in FACETS.values()))
    print("Config: pySHACL advanced, inference=none, each facet's own suite over data + core + facet vocabulary")
    print(f"Performance evidence: median {PERF_MS:.0f} ms over three timed runs\n")
    print(f"{'scenario':46s} {'level':9s} " + " ".join(f"{f[:11]:>12s}" for f in FACETS) + "   verdict")
    rows = [("S0  nothing registered but the level", "S0", False),
            ("S1  PIB's real evidence, as documented today", "S1", False),
            ("S2  S1 + the two undocumented treatments", "S2", False),
            ("teeth  S1 + one test with no result", "S1", True)]
    for title, sc, broken in rows:
        for name, lvl in arms:
            if broken and name == "standard":
                continue
            res = run(lvl, sc, broken)
            cells = " ".join(f"{('gate '+str(g) if g else 'ok'):>12s}" for g, _ in res.values())
            other = sum(o for _, o in res.values())
            fails = sum(g for g, _ in res.values())
            verdict = "PASS" if fails == 0 else f"FAIL ({fails} gate hit{'s' if fails>1 else ''})"
            if other: verdict += f"  [+{other} other-shape violations]"
            print(f"{title:46s} {name:9s} {cells}   {verdict}")
