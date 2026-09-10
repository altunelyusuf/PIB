# PIB Published Vocabulary — Phase 1 (HUB) shared IRIs

Published 2026-06-06 by Session 00 (PIB HUB). These are the STABLE
IRIs spokes (O4SDLC / RADAR / PAMG / RDODI) declare their interfaces AGAINST in Phase 2.
Ontology IRIs are version-independent; only versionIRI changes across releases.

## http://purl.org/pib/profile  (versionInfo 1.0.0.1)
4 classes, 4 object properties.

- **Class** `http://purl.org/pib/profile#ArtifactCategory` — ArtifactCategory
- **Class** `http://purl.org/pib/profile#Profile` — Profile
- **Class** `http://purl.org/pib/profile#SharedCriterion` — SharedCriterion
- **Class** `http://purl.org/pib/profile#WiringVariant` — WiringVariant
- **Property** `http://purl.org/pib/profile#canonicalProfileOf` — canonicalProfileOf
- **Property** `http://purl.org/pib/profile#hasCategory` — hasCategory
- **Property** `http://purl.org/pib/profile#hasSharedCriterion` — hasSharedCriterion
- **Property** `http://purl.org/pib/profile#selectsWiring` — selectsWiring

## http://purl.org/pib/integration-interface  (versionInfo 1.0.0.1)
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
