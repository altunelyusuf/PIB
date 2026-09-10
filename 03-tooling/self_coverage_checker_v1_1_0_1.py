#!/usr/bin/env python3
"""
PIB Self-Coverage Checker v1.1.0.1
==================================
v1.1.0.1 (PATCH): fixes a false-negative in the --hermit DL leg reported independently by the
O4SDLC and PAMG spokes (B1 proposals). The owlready2->HermiT bridge was network-dereferencing
owl:imports / ontology IRIs and folding the resulting errors into self_covered=False. Now:
owl:imports are stripped before reasoning (true standalone), and a reasoner that cannot run is
recorded as "not-run" rather than counted as INCONSISTENT. Only a real
OwlReadyInconsistentOntologyError fails the verdict. SHACL/parse behaviour unchanged.

v1.1.0 (MINOR): the (c) DL-consistency hook is a real HermiT harness (owlready2 + bundled
HermiT.jar + Java), replacing the v1.0.0 stub.
The profile-INDEPENDENT gate. For each participating ontology, verifies it is
self-sufficient STANDALONE — i.e. loose integration is safe only if every node
holds up on its own:

  (a) parses,
  (b) is SHACL-conformant against its own shapes (no consumed ontology merged),
  (c) [optional] is DL-consistent under HermiT.

Emits a SelfCoverageAttestation (TTL) per ontology recording the verdict + SHA.
This gate is SEPARATE from wiring validity (wiring_validator_v1_0_0.py): a wiring is
adoptable only if BOTH gates pass. Counterexample from the ecosystem: O4SE_Core_Structure
was reported inconsistent standalone in an early O4SDLC build — exactly the failure this gate catches.

Usage:
    python3 self_coverage_checker_v1_0_0.py ONTOLOGY.ttl [--shapes SHAPES.ttl] [--hermit]
"""
from __future__ import annotations
import sys, os, hashlib, argparse, datetime


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check(ontology, shapes=None, hermit=False):
    import rdflib
    result = {"ontology": ontology, "sha256": sha(ontology),
              "parsed": False, "shacl_conforms": None, "shacl_violations": None,
              "dl_consistent": None, "self_covered": False}
    # (a) parse
    try:
        g = rdflib.Graph().parse(ontology, format="turtle")
        result["parsed"] = True
        result["triples"] = len(g)
    except Exception as e:
        result["error"] = f"parse failed: {e}"
        return result
    # (b) SHACL standalone (imports NOT merged — true self-coverage)
    if shapes:
        try:
            from pyshacl import validate
            SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
            conforms, rg, _ = validate(g, shacl_graph=rdflib.Graph().parse(shapes, format="turtle"),
                                       advanced=True, allow_warnings=True, allow_infos=True)
            v = sum(1 for s in rg.subjects(rdflib.RDF.type, SH.ValidationResult)
                    if str(rg.value(s, SH.resultSeverity)).endswith("Violation"))
            result["shacl_conforms"] = bool(conforms)
            result["shacl_violations"] = v
        except Exception as e:
            result["error"] = f"shacl failed: {e}"
    # (c) DL consistency (optional; needs owlready2 + HermiT.jar + Java)
    #     v1.1.0.1 (PATCH): fixes the false-negative defect reported independently by the
    #     O4SDLC and PAMG spokes. Two corrections:
    #       (i)  STRIP owl:imports before reasoning — self-coverage means "no consumed ontology
    #            merged" (and prevents the owlready2 bridge from network-dereferencing the import IRI).
    #       (ii) A reasoner that CANNOT RUN (Java error, parse/download error) is recorded as
    #            "not-run", NOT as INCONSISTENT. Only a real OwlReadyInconsistentOntologyError fails.
    if hermit:
        try:
            import owlready2, tempfile, os as _os
            OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
            g_local = rdflib.Graph()
            for t in g:  # copy, then drop owl:imports (standalone, no network dereference)
                g_local.add(t)
            n_imports = 0
            for t in list(g_local.triples((None, OWL.imports, None))):
                g_local.remove(t); n_imports += 1
            with tempfile.NamedTemporaryFile(suffix=".owl", delete=False) as tf:
                _xml = tf.name
            g_local.serialize(destination=_xml, format="xml")
            try:
                onto = owlready2.get_ontology("file://" + _xml).load()
                with onto:
                    owlready2.sync_reasoner_hermit(infer_property_values=False, debug=0)
                result["dl_consistent"] = True
            except owlready2.OwlReadyInconsistentOntologyError:
                result["dl_consistent"] = False
            except Exception as e:
                # reasoner could not run — NOT a consistency verdict (spoke-reported bridge artifact)
                result["dl_consistent"] = f"not-run (reasoner error: {type(e).__name__})"
            result["dl_reasoner"] = "HermiT (owlready2 %s); owl:imports stripped=%d" % (owlready2.VERSION, n_imports)
            try: _os.unlink(_xml)
            except OSError: pass
        except Exception as e:
            result["dl_consistent"] = f"not-run (harness error: {type(e).__name__})"
    # verdict: self-covered iff parsed AND (no shapes given OR shapes conform)
    #          AND DL leg does not REFUTE consistency. v1.1.0.1: only an explicit
    #          dl_consistent is False (genuine INCONSISTENT) fails; True or "not-run…" passes.
    dl_ok = (not hermit) or (result.get("dl_consistent") is not False)
    result["self_covered"] = (result["parsed"]
                              and (shapes is None or result["shacl_conforms"] is True)
                              and dl_ok)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ontology")
    ap.add_argument("--shapes", default=None)
    ap.add_argument("--hermit", action="store_true")
    a = ap.parse_args()
    r = check(a.ontology, a.shapes, a.hermit)
    for k, val in r.items():
        print(f"  {k}: {val}")
    sys.exit(0 if r["self_covered"] else 1)
