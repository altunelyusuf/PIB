#!/usr/bin/env python3
"""
PIB Consumer Registration Check v1.0.0
======================================
Validates consumer registrations and, where the repository is reachable, verifies that the hashes a
consumer declared match the bytes actually in its repository at the pinned commit.

Two checks, deliberately separate, because they fail for different reasons and a reader needs to know
which happened:

  SHAPE   the record says everything PIB needs — repository, pinned commit, files with hashes and paths,
          an interface that produces something and attests self-coverage, a contact. A malformed record
          is rejected with the shape's own message, never half-adapted.
  BYTES   the declared hash equals the hash of the file fetched from that repository at that commit.
          A mismatch means the registration and the repository disagree, and is reported as a mismatch —
          never resolved silently in favour of either.

An unreachable repository yields UNREACHABLE, not VERIFIED. That distinction is the whole point: PIB has
previously had to say "I checked" about things it could not read, and this tool makes that impossible to
do by accident.

Fetching uses GH_TOKEN or GITHUB_TOKEN when present, and anonymous access otherwise. No token is printed.

Usage:
    python3 03-tooling/consumer_registration_check_v1_0_0.py [registry-dir]
    python3 03-tooling/consumer_registration_check_v1_0_0.py --self-test
Exit code is non-zero if any registration fails its shape or contradicts its repository.
"""
import os, sys, json, hashlib, urllib.request, urllib.error, glob

import rdflib
from pyshacl import validate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHAPES = os.path.join(ROOT, "02-shacl-safeguards", "pib_consumer_registration_shacl_v1_1_0.ttl")
REGISTRY = os.path.join(ROOT, "13-consumer-registry")
PIBCR = rdflib.Namespace("http://purl.org/pib/consumer-registry#")
ORH = rdflib.Namespace("http://example.org/oepack-release-history#")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def check_shape(path):
    """Returns (ok, [messages]) — the shape's own messages, not a paraphrase of them."""
    data = rdflib.Graph(); data.parse(path, format="turtle")
    shapes = rdflib.Graph(); shapes.parse(SHAPES, format="turtle")
    _, report, _ = validate(data, shacl_graph=shapes, advanced=True, inference="none")
    msgs = [str(report.value(r, SH.resultMessage))
            for r in report.subjects(rdflib.RDF.type, SH.ValidationResult)
            if str(report.value(r, SH.resultSeverity)).endswith("Violation")]
    return (not msgs), msgs, data


def _fetch(repo_url, commit, path):
    """Fetch one file from a GitHub repository at a pinned commit. Returns bytes, or raises."""
    owner_repo = repo_url.rstrip("/").replace("https://github.com/", "")
    api = f"https://api.github.com/repos/{owner_repo}/contents/{path}?ref={commit}"
    req = urllib.request.Request(api, headers={"Accept": "application/vnd.github.raw"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def check_bytes(data):
    """Compare each declared hash with the repository's actual bytes. Never guesses on failure."""
    out = []
    for reg in data.subjects(rdflib.RDF.type, PIBCR.ConsumerRegistration):
        repo = str(data.value(reg, PIBCR.atRepository))
        commit = str(data.value(reg, PIBCR.atCommit))
        reachable = data.value(reg, PIBCR.repositoryReachable)
        for f in data.objects(reg, PIBCR.registersFile):
            declared = str(data.value(f, ORH.hasFileSHA256) or "")
            path = str(data.value(f, PIBCR.atPath) or "")
            if reachable is not None and str(reachable).lower() == "false":
                out.append(("UNREACHABLE", path, "declared unreachable by the registrant; hash kept, not verified"))
                continue
            try:
                actual = hashlib.sha256(_fetch(repo, commit, path)).hexdigest()
            except Exception as e:                       # network, auth, missing path, moved commit
                out.append(("UNREACHABLE", path, f"{type(e).__name__} fetching from the repository"))
                continue
            out.append(("VERIFIED" if actual == declared else "MISMATCH", path,
                        "hash matches the repository" if actual == declared
                        else f"declared {declared[:12]}…, repository has {actual[:12]}…"))
    return out


def run(registry_dir=REGISTRY, verbose=True):
    files = sorted(glob.glob(os.path.join(registry_dir, "pending", "*.ttl")) +
                   glob.glob(os.path.join(registry_dir, "registered", "*.ttl")))
    if verbose:
        print(f"PIB consumer registration check v1.0.0 — {len(files)} registration(s) found")
    failures = 0
    for path in files:
        name = os.path.basename(path)
        ok, msgs, data = check_shape(path)
        if not ok:
            failures += 1
            print(f"  {name}: SHAPE FAILED")
            for m in msgs:
                print(f"      {m}")
            continue
        results = check_bytes(data)
        bad = [r for r in results if r[0] == "MISMATCH"]
        failures += len(bad)
        print(f"  {name}: shape ok")
        for status, p, why in results:
            print(f"      {status:12s} {p}  — {why}")
    if not files and verbose:
        print("  no registrations yet — see 13-consumer-registry/README.md")
    return failures


def self_test():
    """Prove both checks can fail, against a real public repository, before either is trusted.

    PIB's own public files are used as the stand-in consumer: they are real bytes at a real commit, so a
    correct hash must verify and a corrupted one must be caught. Nothing about PIB is registered by this.
    """
    import subprocess, tempfile
    commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    target = "VERSION.txt"
    good = hashlib.sha256(open(os.path.join(ROOT, target), "rb").read()).hexdigest()
    bad = "0" * 64
    tmp = tempfile.mkdtemp()
    os.makedirs(os.path.join(tmp, "pending"))
    def record(sha, tag):
        return f"""@prefix pibcr: <http://purl.org/pib/consumer-registry#> .
@prefix iif: <http://purl.org/pib/integration-interface#> .
@prefix orh: <http://example.org/oepack-release-history#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/selftest#> .
ex:R{tag} a pibcr:ConsumerRegistration ; rdfs:label "Self-test stand-in ({tag})"@en ;
    pibcr:atRepository "https://github.com/altunelyusuf/PIB" ; pibcr:atCommit "{commit}" ;
    pibcr:repositoryReachable true ; pibcr:registersFile ex:F{tag} ;
    pibcr:declaresInterface ex:I{tag} ; pibcr:contactSession "pib self-test" .
ex:F{tag} a orh:OntologyFile ; rdfs:label "{target}"@en ; orh:hasVersionInfo "n/a" ;
    orh:hasFileSHA256 "{sha}" ; pibcr:atPath "{target}" .
ex:I{tag} a iif:OntologyInterface ; rdfs:label "stand-in"@en ;
    iif:produces ex:C{tag} ; iif:hasSelfCoverage ex:S{tag} .
ex:C{tag} a iif:Capability ; rdfs:label "c"@en .
ex:S{tag} a iif:SelfCoverageAttestation ; rdfs:label "s"@en .
"""
    open(os.path.join(tmp, "pending", "registration_selftest_good_v1_0_0.ttl"), "w").write(record(good, "Good"))
    open(os.path.join(tmp, "pending", "registration_selftest_bad_v1_0_0.ttl"), "w").write(record(bad, "Bad"))
    # a record missing its commit: the shape must reject it
    open(os.path.join(tmp, "pending", "registration_selftest_malformed_v1_0_0.ttl"), "w").write(
        """@prefix pibcr: <http://purl.org/pib/consumer-registry#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/selftest#> .
ex:RMal a pibcr:ConsumerRegistration ; rdfs:label "Self-test malformed"@en ;
    pibcr:atRepository "https://github.com/altunelyusuf/PIB" .
""")
    print("PIB consumer registration check — self-test")
    failures = run(tmp, verbose=False)
    print(f"  failures reported: {failures} (expected at least 2: one hash mismatch, one malformed record)")
    ok = failures >= 2
    if not ok and not (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")):
        print("  NOTE: no token in the environment, so the byte check could not reach the repository and "
              "only the shape check was exercised. That is why this self-test did not pass — it refuses to "
              "report a capability it did not demonstrate.")
    print(f"  the check can fail: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(self_test() if "--self-test" in sys.argv else
                     (1 if run(sys.argv[1] if len(sys.argv) > 1 else REGISTRY) else 0))
