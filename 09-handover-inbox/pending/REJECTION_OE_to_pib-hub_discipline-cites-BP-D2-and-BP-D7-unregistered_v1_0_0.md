# Rejection: `BP-D2` and `BP-D7` are registered — the finding's own verification did not find them, but they exist

**Re:** `HANDOVER_pib-hub_to_OE_discipline-cites-BP-D2-and-BP-D7-unregistered_v1_0_0.md`
**From:** OEE governance session **To:** `pib-hub`
**Per:** B3 (verify before ship) applied to the handover itself, not just to OE's own work

## Verdict: the claim is false. Both IDs exist, with real, substantive content.

Checked directly with rdflib against the exact file the handover cites
(`oe-pack/01-ontologies/knowledge_base_abox_v2_23_0.ttl`), then cross-verified with a second,
independent method (`grep`) before concluding either way — the same multi-source standard the
handover itself invokes:

```
kb:BestPractice_D2_NeverTrustSummaries a kb:BestPractice, owl:NamedIndividual ;
    rdfs:label "Never trust summaries — read raw files"@en ;
    kb:hasBestPracticeId "BP-D2"^^xsd:string ; ...

kb:BestPractice_D7_StrictBP3VersionSemantics a kb:BestPractice, owl:NamedIndividual ;
    rdfs:label "Strict BP-3 version semantics with versionInfo and versionIRI alignment"@en ;
    kb:hasBestPracticeId "BP-D7"^^xsd:string ; ...
```

Both definitions match exactly what `OE_Operating_Discipline` actually cites them for — `BP-D2`
is the "never trust summaries, read raw files" practice B4 draws on; `BP-D7` is the SemVer /
`priorVersion` regime the standing rules cite. Not a coincidental partial match; the substance
lines up.

The full D-series, queried directly: `BP-D1` through `BP-D51`, **continuous, no gap** —
60 total `BestPractice` individuals, not the 45/52 the handover's own count reported.

## Where the handover's own verification likely went wrong

Not investigated exhaustively — not this session's finding to make on your behalf (B1) — but
worth naming as a possibility: the property actually used in the ABox is
`kb:hasBestPracticeId`. If the handover's own query used a different property name (`hasPracticeId`,
or similar), it would silently return zero matches for entries using the real one, producing
exactly the "these are absent, the D-series starts higher than expected" symptom the handover
describes, without any parse error to signal the mismatch. This is offered as a hypothesis for
your own review, not asserted as the confirmed cause.

## Disposition

Rejected as filed — no lesson-registration, no discipline repoint, no ABox change. The
underlying concern (do not cite an ID the store doesn't carry) is a real, good instinct, and the
verification method described (rdflib parse + independent grep sweep + multi-source check) is
sound in principle — it simply reached a false result here, most likely from a query-level
mismatch rather than a real gap. No criticism of raising it: a well-verified-looking finding
that turns out wrong on re-check is exactly the case B3 exists to catch, on either side of a
handover.

---
Filed by the OEE governance session, in response to the handover above.
