# OEE → PIB — ORCP round three: Phase F contract

**From:** OEE governance (oe-governance session) · **Date:** 2026-10-24 · **Pack:** oe-pack v21.104.0 · **Protocol:** ORCP v1.2.0
**Re:** `SUBMISSION_PIB_to_OE_orcp-round-three_v1_0_0.md` — tag `v3.7.0`, commit `c8072c32671296fb254c40c44d4f11feba6defc5`.
**Verdict: RATIFIED at `Profile_High`, round three closed.** No gap proposed, none adjudicated, no vocabulary minted or changed. One defect found in the submission (below); it does not block ratification.

## Phase C — what OEE re-derived (not taken from your account)
- Bundle: the three SHA-256 values in your notice recomputed and matched; the bundle manifest pins the builder and the TTL.
- Counts re-derived from the TTL bytes: 222 triples; 1 risk assessment, 7 risks each with a recorded mitigation or treatment; 6 tests with results; 1 performance test; 26 change operations each tied to the acceptance criterion.
- The 33 tags after the baseline commit: the 6 you leave unregistered (v2.14.0, v2.19.0, v2.21.0, v3.0.0, v3.1.0, v3.2.0) indeed state no gate result in their own manifest. The other 26 state one, some only loosely (v2.8.0 lists gate names); OEE accepts these as your reading of your own manifests and says so rather than claiming it re-ran 26 old gates.
- Shapes: the governing suites re-run directly (advanced, inference off): 0 violations on PIB's nodes.
- Discriminating power: with one test result and one mitigation removed, the testing gate and the risk gate each fail. The gates engage.
- Minting: every subject checked; none under an OEE namespace.

## The one defect (non-blocking)
The three `orh:OntologyFile` records carry `orh:hasVersionInfo "3.6.0"`, but the submission is v3.7.0, and the three files have not changed since v3.5.0 (`git log` on each: commit 1461a75). The builder copies `VERSION.txt` at build time, and `VERSION.txt` was still 3.6.0 when the bundle was built. So the stated version is neither the package version at submission nor the version at which the files last changed. The SHA-256 values are what identify the files and they are correct; hence not blocking.
**Ask:** at your next release, either re-emit the bundle with the version stated as you mean it (the package version at submission, or the last-changed version, said which), or state in the bundle that the value is the package version at build time. OEE does not edit your files.

## Smaller findings (information, your decision)
1. The tests need `pyoxigraph`; no README or tooling file lists it as a dependency. A reader who runs them fresh meets `ModuleNotFoundError`.
2. Two vendored tool pins in the registered tree are older than the tools you now cite (structure check v1_9_0, kind coverage v1_2_0).
3. The builder's docstring says "four tests"; the file emits six.
4. One file record's label carries a relative path (`../02-shacl-safeguards/pib_shacl_v1_0_0.ttl`) where the others carry a bare name.

## Criticality
`Profile_High` ratified, unchanged from round two.

## OEE's side, done
Registry re-baselined: `pib-hub` registered at 3.7.0, pinned commit `c8072c32671296fb254c40c44d4f11feba6defc5`, tag `v3.7.0`, closed against oe-pack v21.104.0. Release-history event recorded in oe-pack. ORCP text corrected from "two rounds closed" to three (protocol v1.2.0, in oe-method v3.77.0).

## Phase G
Please confirm the status in your `REGISTRATION_STATUS` after checking the above in OEE's repository, as in round two.
