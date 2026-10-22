# PIB Published Vocabulary — Phase 1 (HUB) shared IRIs

Published 2026-06-06 by Session 00 (PIB HUB). These are the STABLE
IRIs spokes (O4SDLC / RADAR / PAMG / RDODI) declare their interfaces AGAINST in Phase 2.
Ontology IRIs are version-independent; only versionIRI changes across releases.

## http://purl.org/pib/profile  (versionInfo 1.3.0)
8 classes, 8 object properties. The four below were the published set at 1.0.0.1; rule scope (1.1.0, corrected in 1.2.0) and the kinds (1.3.0) added the rest.

- **Class** `http://purl.org/pib/profile#ArtifactCategory` — ArtifactCategory
- **Class** `http://purl.org/pib/profile#Profile` — Profile
- **Class** `http://purl.org/pib/profile#SharedCriterion` — SharedCriterion
- **Class** `http://purl.org/pib/profile#WiringVariant` — WiringVariant
- **Property** `http://purl.org/pib/profile#canonicalProfileOf` — canonicalProfileOf
- **Property** `http://purl.org/pib/profile#hasCategory` — hasCategory
- **Property** `http://purl.org/pib/profile#hasSharedCriterion` — hasSharedCriterion
- **Property** `http://purl.org/pib/profile#selectsWiring` — selectsWiring

## http://purl.org/pib/integration-interface  (versionInfo 1.1.0)
7 classes, 10 object properties.

- **Class** `http://purl.org/pib/integration-interface#Capability` — Capability
- **Class** `http://purl.org/pib/integration-interface#IntegrationEdge` — IntegrationEdge
- **Class** `http://purl.org/pib/integration-interface#OntologyInterface` — OntologyInterface
- **Class** `http://purl.org/pib/integration-interface#SelfCoverageAttestation` — SelfCoverageAttestation
- **Class** `http://purl.org/pib/integration-interface#VariabilityOperator` — VariabilityOperator
- **Class** `http://purl.org/pib/integration-interface#VariationCapacity` — VariationCapacity
- **Class** `http://purl.org/pib/integration-interface#WiringVariant` — WiringVariant
- **Property** `http://purl.org/pib/integration-interface#activeEdge` — activeEdge
- **Property** `http://purl.org/pib/integration-interface#consumes` — consumes
- **Property** `http://purl.org/pib/integration-interface#edgeCapability` — edgeCapability
- **Property** `http://purl.org/pib/integration-interface#edgeSource` — edgeSource
- **Property** `http://purl.org/pib/integration-interface#edgeTarget` — edgeTarget
- **Property** `http://purl.org/pib/integration-interface#forProfile` — forProfile
- **Property** `http://purl.org/pib/integration-interface#governedByOperator` — governedByOperator
- **Property** `http://purl.org/pib/integration-interface#hasInterface` — hasInterface
- **Property** `http://purl.org/pib/integration-interface#hasSelfCoverage` — hasSelfCoverage
- **Property** `http://purl.org/pib/integration-interface#produces` — produces

## Phase-2 declaration contract (how a spoke declares against this vocabulary)

A spoke declares its interface WITHOUT owl:imports — names referenced, not merged:

```turtle
@prefix iif: <http://purl.org/pib/integration-interface#> .
# <spoke>_if  iif:produces  <Capability IRI> ;   # public exports
#            iif:consumes  <Capability IRI> ;   # required inputs
#            iif:hasSelfCoverage <attestation> . # REQUIRED before wiring (G3)
```

Each contributed produces/consumes edge feeds the HUB's Phase-3 per-profile wiring
composition (wiring_validator + G4 contract closure); a wiring is publishable only if
the VAF engine reports it admissible AND every participating interface self-covers.


---

## Every term carries its kind or category (1.3.0 / 1.1.0, 2026-10-22)

Each class in these vocabularies now states what kind of thing it is (`kb:hasClassKind`) and each
object property what category of relationship it is (`kb:hasRelationshipCategory`), under the
governance standard that reaches existing terms and not only new ones. **A kind classifies a class; it
makes it a subclass of nothing**, so nothing a spoke imports changes and no declaration a spoke has
made against these IRIs is affected.

What a spoke can now read without asking: that a `Capability` is an information entity rather than a
quality, that an `IntegrationEdge` is a relationship made an object, that an `OntologyInterface` and a
`Profile` are specifications, that a `SelfCoverageAttestation` is a claim, that `VariationCapacity` is
a measurement, that a `WiringVariant` is a model element, and that `ArtifactCategory` and `RuleScope`
are value domains — closed sets of values, not things with instances of their own in the world.

The assignments follow the ecosystem's own precedents, read from the governance vocabulary rather than
chosen here: a constraint is a specification, a criterion and a candidate are information artifacts, a
closed list of category values is a value domain, a phase is a process.


---

## The files changed and the IRIs did not (PIB v3.0.0, 2026-10-22)

The package now ships **one T-Box, one A-Box and one SHACL file** (BP-D54): eleven files became
`01-ontologies/pib_tbox_v1_0_0.ttl`, `01-ontologies/pib_abox_v1_0_0.ttl` and
`02-shacl-safeguards/pib_shacl_v1_0_0.ttl`. Each former subject — profile, integration-interface,
wiring-expression, composition, assessment, consumer-registry, enumeration — is recorded inside as a
**module at its own former IRI**, carrying the metadata its file header carried.

**Nothing a spoke declares against has moved.** Every term keeps the IRI it always had, the ontology
IRIs above are unchanged, and `rdfs:isDefinedBy` still points at the former subject's IRI. A spoke that
names a term needs no change at all.

**What does change** is a consumer that loaded a PIB *file* by path: the eleven files are gone from the
package and recoverable from git history and the release tags. The package IRI `http://purl.org/pib`
is what the three files declare, each with its own version, and the modules are `dcterms:isPartOf` it.
