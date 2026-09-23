"""Feasibility: can a consumer-PROPOSED profile be approved or rejected today, with VAF as the
mechanism for the variation layer? Nothing new is built here; only shipped pieces are used."""
import importlib.util, subprocess, rdflib, os
conv = "03-tooling/taxonomy_vaf_converter_v1_0_0.py"
spec = importlib.util.spec_from_file_location("vc", "03-tooling/variation_capacity_v1_2_0.py")
vc = importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)

# A consumer proposes its profile's variation space in the ALGEBRA's own notation.
PROPOSALS = {
 "good — a coherent assessment profile": """component ProposedCourseworkProfile {
  mandatory analysis_design
  mandatory grade
  exclusive { radar_measures | pamg_measures }
  or { rubric_scoring, peer_review }
  grade requires analysis_design
}""",
 "bad — the consumer's own constraints contradict": """component ContradictoryProfile {
  mandatory fast
  mandatory small
  exclusive { fast | small }
}""",
}
for label, dsl in PROPOSALS.items():
    open("/tmp/p.dsl","w").write(dsl)
    r = subprocess.run(["python3", conv, "from-dsl", "/tmp/p.dsl", "/tmp/p.ttl"],
                       capture_output=True, text=True, env={**os.environ})
    if r.returncode:
        print(f"  {label}: REJECTED at conversion — {r.stderr.strip()[:80]}"); continue
    caps, _, _ = vc.compute(["/tmp/p.ttl"], verbose=False)
    cap = next(iter(caps.values())) if caps else None
    verdict = "APPROVE" if cap and cap > 0 else "REJECT"
    why = (f"{cap} admissible wirings — the profile can pin exactly one" if cap
           else "no admissible wiring exists; the proposal is unsatisfiable as written")
    print(f"  {label}\n      capacity {cap} -> {verdict}: {why}")
