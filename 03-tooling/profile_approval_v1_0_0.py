#!/usr/bin/env python3
"""
PIB Profile Approval v1.0.0 — autonomous
========================================
Decides a consumer's profile proposal. No human sign-off: the gates approve or reject, the proposal moves
to `approved/` or `rejected/`, and a line stating what was actually verified is appended to the registry.

Autonomy is why the gates are split by what can see each failure, and why none of them is a formality:

  SHAPE      the record says what approval needs — proposer, one category, criteria with the systems that
             use them, a variation space in the algebra's notation.
  IDENTITY   what only the REGISTRY can see. A new category whose name collides with one already
             published is rejected: bind to the existing identity instead of minting a second one for the
             same thing. This is the failure the algebra is blind to, so nothing else would catch it.
  VARIATION  what only the ALGEBRA can see. The proposal's own DSL is converted and enumerated; a space
             with no admissible wiring is rejected, because a profile must pin exactly one.
  PARALLEL   a consumer that declares its own `Profile` class in its own namespace is rejected: a second
             profile concept defeats the single shared identity this package exists to provide. Checked
             against the consumer's registered files when they are reachable, and reported as unchecked
             when they are not — never assumed clean.

The owner's rulings this implements (2026-09-23): approval is autonomous, and a consumer MAY introduce a
new category. The second ruling is why the identity gate checks for a *collision* rather than refusing new
categories outright.

Usage:
    python3 03-tooling/profile_approval_v1_0_0.py [--dry-run] [registry-dir]
    python3 03-tooling/profile_approval_v1_0_0.py --self-test
"""
import os, sys, glob, shutil, subprocess, datetime, csv

import rdflib
from pyshacl import validate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHAPES = os.path.join(ROOT, "02-shacl-safeguards", "pib_consumer_registration_shacl_v1_1_0.ttl")
CONVERTER = os.path.join(HERE, "taxonomy_vaf_converter_v1_0_0.py")
CAPACITY = os.path.join(HERE, "variation_capacity_v1_2_0.py")
REGISTRY = os.path.join(ROOT, "13-consumer-registry")
PIBCR = rdflib.Namespace("http://purl.org/pib/consumer-registry#")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def _norm(label):
    """Category names collide on meaning, not punctuation: 'Capstone Report' == 'capstone_report'."""
    return "".join(c for c in str(label).lower() if c.isalnum())


def known_categories(registry):
    """Categories already published, from the registry's own plain-text list."""
    path = os.path.join(registry, "CATEGORIES.tsv")
    out = {}
    if os.path.exists(path):
        for row in csv.reader((l for l in open(path) if not l.startswith("#")), delimiter="\t"):
            if len(row) >= 2 and row[0].strip():
                out[_norm(row[0])] = (row[0].strip(), row[1].strip())
    return out


def gate_shape(path):
    data = rdflib.Graph(); data.parse(path, format="turtle")
    shapes = rdflib.Graph(); shapes.parse(SHAPES, format="turtle")
    _, rep, _ = validate(data, shacl_graph=shapes, advanced=True, inference="none")
    msgs = [str(rep.value(r, SH.resultMessage)) for r in rep.subjects(rdflib.RDF.type, SH.ValidationResult)
            if str(rep.value(r, SH.resultSeverity)).endswith("Violation")]
    return msgs, data


def gate_identity(data, categories):
    """The gate the algebra cannot supply: is this category already someone else's identity?"""
    problems, notes = [], []
    for prop in data.subjects(rdflib.RDF.type, PIBCR.ProfileProposal):
        for cat in data.objects(prop, PIBCR.proposesCategory):
            label = str(data.value(cat, PIBCR.categoryLabel) or "")
            is_new = str(data.value(cat, PIBCR.isNewCategory)).lower() == "true"
            hit = categories.get(_norm(label))
            if is_new and hit:
                problems.append(f"category '{label}' is claimed as new but '{hit[0]}' is already published "
                                f"(by {hit[1]}); bind to the existing identity rather than minting a second one")
            elif not is_new and not hit:
                problems.append(f"category '{label}' is declared as already published, but the registry has no "
                                f"such category; introduce it as new or correct the name")
            elif is_new:
                notes.append(f"new category '{label}' accepted — no collision in the registry")
            else:
                notes.append(f"binds to published category '{hit[0]}'")
    return problems, notes


def gate_variation(data, workdir):
    """The gate only the algebra can supply: does any admissible wiring exist?"""
    problems, notes = [], []
    for prop in data.subjects(rdflib.RDF.type, PIBCR.ProfileProposal):
        dsl = str(data.value(prop, PIBCR.wiringInDSL) or "")
        dsl_path = os.path.join(workdir, "proposal.dsl"); open(dsl_path, "w").write(dsl)
        ttl_path = os.path.join(workdir, "proposal.ttl")
        r = subprocess.run([sys.executable, CONVERTER, "from-dsl", dsl_path, ttl_path],
                           capture_output=True, text=True)
        if r.returncode:
            problems.append(f"the variation space could not be converted: {r.stderr.strip().splitlines()[-1][:120]}")
            continue
        import importlib.util
        spec = importlib.util.spec_from_file_location("vc", CAPACITY)
        vc = importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
        caps, _, _ = vc.compute([ttl_path], verbose=False)
        cap = next(iter(caps.values())) if caps else None
        if not cap:
            problems.append(f"no admissible wiring exists (capacity {cap}); a profile must pin exactly one")
        else:
            notes.append(f"{cap} admissible wirings — the profile can pin one")
    return problems, notes


def _fetch(repo_url, commit, path):
    import urllib.request
    owner_repo = repo_url.rstrip("/").replace("https://github.com/", "")
    req = urllib.request.Request(f"https://api.github.com/repos/{owner_repo}/contents/{path}?ref={commit}",
                                 headers={"Accept": "application/vnd.github.raw"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def gate_parallel_profile(data, registry=None):
    """A consumer must not carry its own Profile class.

    Really checked, not asserted: the consumer's registered files are fetched and parsed, and any class
    whose local name is Profile in the consumer's OWN namespace is a rejection. When the files cannot be
    read the result is UNCHECKED — stated as unchecked, never assumed clean.
    """
    registry = registry or REGISTRY
    problems, notes = [], []
    for prop in data.subjects(rdflib.RDF.type, PIBCR.ProfileProposal):
        who = str(data.value(prop, PIBCR.proposedBy) or "")
        match = None
        for cand in glob.glob(os.path.join(registry, "registered", "*.ttl")) + \
                    glob.glob(os.path.join(registry, "pending", "*.ttl")):
            g = rdflib.Graph(); g.parse(cand, format="turtle")
            for r in g.subjects(rdflib.RDF.type, PIBCR.ConsumerRegistration):
                blob = (str(g.value(r, rdflib.RDFS.label) or "") + " " + os.path.basename(cand)).lower()
                if who.lower() and who.lower() in blob:
                    match = (g, r)
        if match is None:
            notes.append(f"parallel-profile check UNCHECKED — {who} has registered no files to read")
            continue
        g, r = match
        repo, commit = str(g.value(r, PIBCR.atRepository)), str(g.value(r, PIBCR.atCommit))
        for f in g.objects(r, PIBCR.registersFile):
            path = str(g.value(f, PIBCR.atPath))
            try:
                text = _fetch(repo, commit, path).decode("utf-8", "replace")
                fg = rdflib.Graph(); fg.parse(data=text, format="turtle")
            except Exception as e:
                notes.append(f"parallel-profile check UNCHECKED for {path} ({type(e).__name__})")
                continue
            own = [str(c) for c in fg.subjects(rdflib.RDF.type, rdflib.OWL.Class)
                   if str(c).rsplit("#", 1)[-1].rsplit("/", 1)[-1] == "Profile"]
            if own:
                problems.append(f"{who} declares its own Profile class ({own[0]}) in {path}; retire it in "
                                f"favour of the shared identity, or attach its behaviour to the shared Profile IRI")
            else:
                notes.append(f"parallel-profile check clean for {path}")
    return problems, notes


def decide(path, registry, dry_run=False):
    import tempfile
    workdir = tempfile.mkdtemp()
    name = os.path.basename(path)
    msgs, data = gate_shape(path)
    problems, notes = list(msgs), []
    if not msgs:
        for gate in (lambda: gate_identity(data, known_categories(registry)),
                     lambda: gate_variation(data, workdir),
                     lambda: gate_parallel_profile(data, registry)):
            p, n = gate(); problems += p; notes += n
    verdict = "APPROVED" if not problems else "REJECTED"
    print(f"  {name}: {verdict}")
    for n in notes:    print(f"      verified: {n}")
    for p in problems: print(f"      blocked:  {p}")
    if not dry_run:
        dest = os.path.join(registry, "profiles", "approved" if verdict == "APPROVED" else "rejected")
        os.makedirs(dest, exist_ok=True); shutil.move(path, os.path.join(dest, name))
        log = os.path.join(registry, "PROFILE_REGISTRY.tsv")
        with open(log, "a") as fh:
            fh.write(f"{name}\t{datetime.date.today().isoformat()}\t{verdict}\t"
                     f"{'; '.join(notes) if verdict=='APPROVED' else '; '.join(problems)}\n")
    return verdict == "APPROVED"


def run(registry=REGISTRY, dry_run=False):
    pend = sorted(glob.glob(os.path.join(registry, "profiles", "pending", "*.ttl")))
    print(f"PIB profile approval v1.0.0 — autonomous — {len(pend)} proposal(s) pending")
    if not pend:
        print("  nothing to decide — see 13-consumer-registry/README.md")
    return sum(0 if decide(p, registry, dry_run) else 1 for p in pend)


def self_test():
    """Approval must APPROVE a sound proposal and REJECT each way it can be unsound."""
    import tempfile
    tmp = tempfile.mkdtemp(); os.makedirs(os.path.join(tmp, "profiles", "pending"))
    open(os.path.join(tmp, "CATEGORIES.tsv"), "w").write(
        "# category\tintroduced by\nCapstone Report\tpamg\n")
    def proposal(tag, cat, is_new, dsl, criteria=2):
        crit = ""
        if criteria:
            crit = f'    pibcr:proposesSharedCriterion ex:C{tag} ;\n'
        body = f"""@prefix pibcr: <http://purl.org/pib/consumer-registry#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/t#> .
ex:P{tag} a pibcr:ProfileProposal ; rdfs:label "Proposal {tag}"@en ;
    pibcr:proposedBy "testconsumer" ;
{crit}    pibcr:proposesCategory ex:Cat{tag} ;
    pibcr:wiringInDSL \"\"\"{dsl}\"\"\" .
ex:Cat{tag} rdfs:label "{cat}"@en ; pibcr:categoryLabel "{cat}" ; pibcr:isNewCategory {str(is_new).lower()} .
"""
        if criteria:
            systems = "\n".join(f'    pibcr:criterionUsedBySystem "sys{i}" ;' for i in range(criteria))
            body += f'ex:C{tag} a rdfs:Resource ; rdfs:label "a criterion"@en ;\n{systems}\n    rdfs:comment "x"@en .\n'
        open(os.path.join(tmp, "profiles", "pending", f"proposal_{tag}.ttl"), "w").write(body)
    GOOD = "component Good {\n  mandatory a\n  exclusive { b | c }\n}"
    BAD  = "component Bad {\n  mandatory a\n  mandatory b\n  exclusive { a | b }\n}"
    proposal("Sound", "Thesis Draft", True, GOOD)
    proposal("Collide", "capstone_report", True, GOOD)          # same identity, different spelling
    proposal("Unsat", "Lab Report", True, BAD)                   # no admissible wiring
    proposal("OneSystem", "Poster", True, GOOD, criteria=1)      # "shared" criterion only one system uses
    print("PIB profile approval — self-test")
    failures = run(tmp)
    approved = len(glob.glob(os.path.join(tmp, "profiles", "approved", "*.ttl")))
    rejected = len(glob.glob(os.path.join(tmp, "profiles", "rejected", "*.ttl")))
    ok = approved == 1 and rejected == 3
    print(f"  approved {approved} (expected 1), rejected {rejected} (expected 3) -> gates discriminate: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raise SystemExit(1 if run(args[0] if args else REGISTRY, "--dry-run" in sys.argv) else 0)
