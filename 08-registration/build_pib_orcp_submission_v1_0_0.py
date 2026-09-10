#!/usr/bin/env python3
"""
ORCP Phase B builder — PIB/HUB registrant submission v1.0.0.

Emits OEM-conformant instances registering the PIB/HUB component against the OEE roster,
using ONLY verified central anchors/hooks (no minted OEE vocabulary; instances live in the
registrant namespace pibreg: and REFERENCE OEE classes/hooks — B1/L-64, registration rule 1).

Phase A classification (recorded in the fit-gap note) drives what is emitted:
  - core            : CONFORMANCE  -> PIB is a core:Artifact; declares core:hasCriticalityProfile.
  - release-history : REGISTRATION -> PIB SubjectOntology + OntologyFile lineage records.
  - knowledge_base  : (available, light) — not emitted here; PIB defers (L-57) unless asked.
  - measurement/quality/reliability/risk/performance/testing/configuration : NO registration data
                      (PIB does not produce it — RADAR/PAMG do); conformance is by criticality
                      declaration (Standard => case-parameterized gates do not fire). Deferred honestly.
  - ae/meta         : internal, no relationship.

All central terms used here were verified present on disk before emission:
  core:Artifact, core:CriticalityProfile, core:Profile_Standard, core:hasCriticalityProfile,
  orh:SubjectOntology, orh:OntologyFile, orh:belongsToSubject, orh:hasFileSHA256, orh:hasVersionInfo.
"""
import rdflib, hashlib, datetime, os
from rdflib import Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD, DCTERMS

CORE = Namespace("http://example.org/core#")
ORH  = Namespace("http://example.org/oepack-release-history#")
PROV = Namespace("http://www.w3.org/ns/prov#")
PIBREG = Namespace("http://purl.org/pib/registration#")   # registrant namespace (PIB-owned)

PIB_FILES = {  # PIB blueprint v1.2.1 ontology files being registered (real SHAs computed live)
    "profile_tbox_v1_0_0_1.ttl":            ("1.0.0.1", "01-ontologies/profile_tbox_v1_0_0_1.ttl"),
    "integration_interface_tbox_v1_0_0_1.ttl": ("1.0.0.1", "01-ontologies/integration_interface_tbox_v1_0_0_1.ttl"),
    "pib_wiring_composition_v1_0_0.ttl":    ("1.0.0",   "01-ontologies/pib_wiring_composition_v1_0_0.ttl"),
}
PIB_ROOT = "/home/claude/pib/profile_integration_blueprint_v1_2_1"

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def build():
    g = rdflib.Graph()
    g.bind("core", CORE); g.bind("orh", ORH); g.bind("prov", PROV)
    g.bind("pibreg", PIBREG); g.bind("dcterms", DCTERMS)
    today = datetime.date.today().isoformat()

    # --- core CONFORMANCE: PIB as a core:Artifact with a declared criticality profile ---
    pib = PIBREG.Artifact_PIB
    g.add((pib, RDF.type, CORE.Artifact))
    g.add((pib, RDF.type, OWL.NamedIndividual))
    g.add((pib, RDFS.label, Literal("PIB / HUB — Profile + Integration-Interface Blueprint v1.2.1", lang="en")))
    g.add((pib, CORE.hasCriticalityProfile, CORE.Profile_Standard))  # honest: design-time governance scaffolding

    # --- release-history REGISTRATION: PIB subject + per-file lineage records ---
    subj = PIBREG.Subject_PIB
    g.add((subj, RDF.type, ORH.SubjectOntology))
    g.add((subj, RDF.type, OWL.NamedIndividual))
    g.add((subj, RDFS.label, Literal("Subject: PIB / HUB integration blueprint", lang="en")))
    g.add((subj, ORH.lifecycleStatus, Literal("active")))  # required by release-history SHACL (exactly one)

    for fname, (ver, relpath) in PIB_FILES.items():
        digest = sha(os.path.join(PIB_ROOT, relpath))
        f_iri = PIBREG["File_" + fname.replace(".ttl", "")]
        g.add((f_iri, RDF.type, ORH.OntologyFile))
        g.add((f_iri, RDF.type, OWL.NamedIndividual))
        g.add((f_iri, RDFS.label, Literal("OntologyFile: " + fname, lang="en")))
        g.add((f_iri, ORH.hasFileSHA256, Literal(digest)))
        g.add((f_iri, ORH.hasVersionInfo, Literal(ver)))
        g.add((f_iri, ORH.belongsToSubject, subj))
        g.add((f_iri, DCTERMS.source, Literal(
            "PIB blueprint v1.2.1 (Phases 1-3 + reproducibility remediation), registrant-emitted for ORCP Phase B.")))
        g.add((f_iri, PROV.wasAttributedTo, PIBREG.Agent_PIBSession))
        g.add((f_iri, PROV.generatedAtTime, Literal(today, datatype=XSD.date)))

    g.add((PIBREG.Agent_PIBSession, RDF.type, PROV.Agent))
    g.add((PIBREG.Agent_PIBSession, RDF.type, OWL.NamedIndividual))
    g.add((PIBREG.Agent_PIBSession, RDFS.label, Literal("PIB/HUB registrant session", lang="en")))
    return g

if __name__ == "__main__":
    out = "/home/claude/pib_orcp/pib_orcp_submission_v1_0_0.ttl"
    g = build()
    g.serialize(destination=out, format="turtle")
    print(f"emitted {len(g)} triples -> {out}")
