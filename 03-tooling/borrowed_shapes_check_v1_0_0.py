#!/usr/bin/env python3
"""
PIB Borrowed-Shapes Check v1.0.0 — PIB's content against the shapes of the algebra it borrows from
=================================================================================================
PIB uses the variant algebra's classes (operators, features). A class carries its owner's constraints
wherever it is used, and until now nothing on PIB's side was watching: PIB validated its own invariants
only, so three expression nodes typed with a class whose shapes require three properties they never had
passed every PIB gate until the algebra's session explained what the class means.

This check validates PIB's A-Box against the algebra's own shapes, vendored verbatim and pinned under
`11-vendored-operator-rules/vendored-shapes/`, and fails on any violation whose focus node is one of PIB's.
Violations on the algebra's own terms (its T-Box is loaded as the ontology) are the algebra's and are
not PIB's to fail on. The constraints only are used (no rules are run).

Usage:
    python3 03-tooling/borrowed_shapes_check_v1_0_0.py
    python3 03-tooling/borrowed_shapes_check_v1_0_0.py --self-test
"""
import os, sys, glob
import rdflib
import pyshacl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ABOX = os.path.join(ROOT, "01-ontologies", "pib_abox_v1_0_0.ttl")
VENDORED = os.path.join(ROOT, "11-vendored-operator-rules", "vendored")
SHAPES = os.path.join(ROOT, "11-vendored-operator-rules", "vendored-shapes")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
PIB_IRI = "http://purl.org/pib/"


def violations(data_extra=None):
    """(focus, message) for every violation of the algebra's shapes on a node of PIB."""
    data = rdflib.Graph().parse(ABOX, format="turtle")
    if data_extra:
        data.parse(data=data_extra, format="turtle")
    tbox = rdflib.Graph()
    for f in sorted(glob.glob(os.path.join(VENDORED, "vaf_domain_tbox_*.ttl"))):
        tbox.parse(f, format="turtle")
    shapes = rdflib.Graph()
    for f in sorted(glob.glob(os.path.join(SHAPES, "variant_algebra_shapes_*.ttl"))):
        shapes.parse(f, format="turtle")
    _, report, _ = pyshacl.validate(data + tbox, shacl_graph=shapes, ont_graph=tbox, inference="rdfs", advanced=False)
    out = set()
    for r in report.subjects(rdflib.RDF.type, SH.ValidationResult):
        focus = str(report.value(r, SH.focusNode))
        if focus.startswith(PIB_IRI):
            out.add((focus, str(report.value(r, SH.resultMessage))[:140]))
    return sorted(out)


def run(verbose=True):
    v = violations()
    if verbose:
        print("PIB borrowed-shapes check v1.0.0 — PIB's A-Box against the algebra's own shapes")
        print(f"  violations on PIB's nodes: {len(v)}")
        for f, m in v[:8]:
            print(f"    {f.split('#')[-1]}: {m}")
    return len(v)


PLANT = """@prefix va: <http://example.org/variant-algebra#> . @prefix pibx: <http://purl.org/pib/wiring-expression#> .
pibx:PlantedNode a va:OperatorApplication ."""


def self_test():
    print("PIB borrowed-shapes check v1.0.0 — self-test")
    base = len(violations())
    print(f"  as published: {base} violation(s)   (expected 0)")
    planted = len(violations(PLANT))
    print(f"  a node typed with the algebra's record-of-a-run class and nothing it requires: {planted} violation(s)   (expected >0)")
    ok = base == 0 and planted > 0
    print(f"  the check can fail: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(1 if run() else 0)
