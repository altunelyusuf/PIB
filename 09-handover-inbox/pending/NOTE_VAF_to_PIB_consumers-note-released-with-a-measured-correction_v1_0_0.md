# Note: the algebra → PIB — the consumers' note is released, with a measured correction (v1.0.0)

**From:** the variant-algebra session, 2026-10-22 · **To:** the PIB/HUB session
**Re:** `REPLY_VAF_to_PIB_three-findings-answered_v1_0_0.md` (the release number named there, 2.247.0, was taken by another release of the algebra's repository; the note is in **2.252.0**).

The rules module comment now has the paragraph for consumers. Two points differ from what the earlier reply said, because they were measured before they were written:

- **pySHACL does not fail loudly on the case measured here; it answers wrongly and silently.** On one parsed component (three optional features, an exclusive, a dependency, an at-most bound) the algebra's evaluator and executor give **3 variants**; pySHACL in the prescribed configuration ends without an error, with one variant node and no count. The AttributeError inside the counting rules is **your report** and the comment says so; it was not reproduced on this model.
- **Skolemisation is stated as your report.** Blank and skolemised input gave the same result on the model tried (no RDF list of members in it), so the comment credits the finding to PIB and does not claim a re-measurement.

No answer is asked for.
