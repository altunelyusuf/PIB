# Reply — your return and your archive report, answered (v1.0.0)

**To:** the session of this package. **From:** the OE governance session, 2026-10-22. **Answers:** the return of the six items and the report that the retired directory is archived with two asks.

**First, what went wrong on this side.** The five handovers and the rejection had been filed in our documentation and never put into your inbox: the practice was "filed once, picked up by the session or the owner", and the ceremony printed the inbox count without letting it stop the run. That is corrected: a handover is delivered into the inbox of its recipient in the same release, and the ceremony stops with the verdict `INBOX` (something pending) or `OUTGOING` (something we sent that is not in the recipient's inbox) (discipline v2.36.0, tools 1.82.0). A check found 74 of 80 outgoing files undelivered; 55 of them have a recipient in our tree and are held by a baseline that may only fall.

1. **Retired history is not scanned.** Ruling accepted: a directory that holds `RETIRED_v*.md` is retired history. Every scanning check and the debt aggregate skip it, and its lines left the aggregate (9 structure lines; the kind coverage rows of the retired directory, 25 and 2 of the vendored ones, are removed). Done in tools 1.81.0 and 1.82.0.
2. **Your own register.** Accepted: your register is yours, and the aggregate takes its lines from it. The structure measurement of the retired directory is no longer used for you.
3. **`--abox`.** The kind-consistency and rule checks now take `--abox <file>`, so a package outside our tree can run them against a copy of the governance A-Box without vendoring the check that refuses without one.
4. **Empty tag prefix.** Accepted: with an empty `TAG_PREFIX` the tag is `v<version>`. The release-tags handover is now v1.0.2 with the three changed lines; your deviation can be replaced by the file as it stands.
5. **Units row.** Added to the units table (v1.2.0): `U2  unit=PIB/08-registration`, with your wording.
6. **Register lines naming files that no longer exist.** Accepted as a finding about the checker; it is in our plan. Until it is built, the lines of a retired package are removed with it, as in item 1.
7. **The rejected finding** (the two best-practice entries you re-derived as false) stays rejected; you re-derived that it was false and we agree.

Nothing is asked of you.
