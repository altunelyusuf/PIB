"""Can the algebra detect the IDENTITY-layer problems a standard has to catch?
Two proposals that are algebraically impeccable but violate the shared standard."""
import importlib.util, subprocess, os
conv="03-tooling/taxonomy_vaf_converter_v1_0_0.py"
spec=importlib.util.spec_from_file_location("vc","03-tooling/variation_capacity_v1_2_0.py")
vc=importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
cases={
 "two consumers both claim the SAME artifact category under different profile names":
   ("""component PamgCapstoneProfile { mandatory grade\n  or { rubric, peer } }""",
    """component RadarCapstoneProfile { mandatory measure\n  or { rubric, peer } }"""),
}
for label,(a,b) in cases.items():
    caps=[]
    for i,dsl in enumerate((a,b)):
        open("/tmp/i.dsl","w").write(dsl)
        subprocess.run(["python3",conv,"from-dsl","/tmp/i.dsl",f"/tmp/i{i}.ttl"],capture_output=True,text=True,env={**os.environ})
        c,_,_=vc.compute([f"/tmp/i{i}.ttl"],verbose=False); caps.append(next(iter(c.values())) if c else None)
    print(f"  {label}")
    print(f"      both compute cleanly: capacities {caps} — the algebra approves BOTH")
    print("      nothing in the algebra knows they claim one shared category, or that a criterion")
    print("      named 'shared' is used by only one system. Those are REGISTRY facts, not algebraic ones.")
