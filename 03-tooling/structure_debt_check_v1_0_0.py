#!/usr/bin/env python3
"""
PIB Structure Debt Check v1.0.0 — the ratchet, run inside PIB's own gate
========================================================================
Runs the governance session's two structure checkers against this package, with this package's own
registers, and exits non-zero if the debt has grown. Without this, PIB's registers would be files
nobody reads: the checkers live in the governance tree, PIB's release runs from PIB alone, and a
ratchet that is only checked somewhere else is not a ratchet here.

  * **Structure** (`oe_structure_check`): names, mixed roles, versions side by side, one file per
    role. Against `04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v1_2_0.tsv`.
  * **Kinds and categories** (`oe_kind_coverage`): every named class carries a kind and every object
    property a category, existing terms included (discipline v2.34.0). Against
    `KIND_COVERAGE_BASELINE_v1_1_0.tsv`, with `KIND_COVERAGE_DECISIONS_v1_0_0.tsv` for the terms this
    package does not type and why.

**`--as-package` is not optional.** A package published from its own repository resolves every
top-level folder as a separate package when the checker is pointed at the repository root, which
gives the wrong counts — 9 "packages" and 23 violations here, against 18 as one package. The
handover that brought the rule says so, and this wrapper passes it so the measurement cannot be
taken the wrong way by accident.

Both checkers are **vendored** under `14-vendored-oe-tooling/`, read-only and hash-pinned: they are
the governance session's, never edited here, and re-vendored when that session re-issues them.

Usage:
    python3 03-tooling/structure_debt_check_v1_0_0.py
    python3 03-tooling/structure_debt_check_v1_0_0.py --self-test
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(ROOT, "14-vendored-oe-tooling")
DEBT = os.path.join(ROOT, "04-documentation", "structure-debt")
STRUCTURE = os.path.join(TOOLS, "oe_structure_check_v1_7_1.py")
COVERAGE = os.path.join(TOOLS, "oe_kind_coverage_v1_1_0.py")
AS_PACKAGE = "pib-hub"      # the slug the publisher stages this repository under


def _run(cmd, cwd=ROOT):
    r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=cwd)
    return r.returncode, (r.stdout + r.stderr).strip()


def structure(root=ROOT, register=None):
    register = register or os.path.join(DEBT, "STRUCTURE_DEBT_REGISTER_v1_2_0.tsv")
    return _run([STRUCTURE, root, "--as-package", AS_PACKAGE, "--register", register])


def coverage(root=ROOT, baseline=None, decisions=None):
    baseline = baseline or os.path.join(DEBT, "KIND_COVERAGE_BASELINE_v1_1_0.tsv")
    decisions = decisions or os.path.join(DEBT, "KIND_COVERAGE_DECISIONS_v1_0_0.tsv")
    return _run([COVERAGE, root, "--baseline", baseline, "--decisions", decisions])


def run(verbose=True):
    failed = 0
    for name, (code, out) in (("structure", structure()), ("kinds and categories", coverage())):
        verdict = [l for l in out.splitlines() if l.startswith(("VERDICT", "REFUSED"))]
        if verbose:
            print(f"  {'pass' if code == 0 else 'FAIL'}  {name}: {verdict[-1] if verdict else out.splitlines()[-1]}")
        failed += (code != 0)
    return failed


def self_test():
    """Both checks must be able to fail on a real change, not on a flag.

    A copy of the package is made and one new defect is planted in each direction: a Turtle file
    whose name breaks the version pattern and whose single class carries no kind. The structure check
    must report it as NEW against the register, and the coverage check as NEW against the baseline.
    A checker that passes a planted defect is not guarding anything.
    """
    print("PIB structure debt check v1.0.0 — self-test")
    print(f"  as published: {run(verbose=False)} failing check(s)   (expected 0)")
    tmp = tempfile.mkdtemp()
    try:
        copy = os.path.join(tmp, "pkg")
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        planted = os.path.join(copy, "01-ontologies", "planted_defect_v9.ttl")      # name breaks the pattern
        open(planted, "w").write(
            "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
            "<http://purl.org/pib/planted#Thing> a owl:Class ; rdfs:label \"planted, untyped\"@en .\n")
        s_code, s_out = structure(root=copy, register=os.path.join(copy, "04-documentation", "structure-debt",
                                                                   "STRUCTURE_DEBT_REGISTER_v1_2_0.tsv"))
        c_code, c_out = coverage(root=copy,
                                 baseline=os.path.join(copy, "04-documentation", "structure-debt",
                                                       "KIND_COVERAGE_BASELINE_v1_1_0.tsv"),
                                 decisions=os.path.join(copy, "04-documentation", "structure-debt",
                                                        "KIND_COVERAGE_DECISIONS_v1_0_0.tsv"))
        s_new = s_code != 0 and "NEW" in s_out
        c_new = c_code != 0 and "new untyped" in c_out
        print(f"  a file whose name breaks the pattern is caught as NEW: {s_new}")
        print(f"  a class with no kind is caught as NEW: {c_new}")
        ok = s_new and c_new
        print(f"  both checks can fail: {ok}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if "--self-test" in sys.argv[1:]:
        sys.exit(self_test())
    print("PIB structure debt check v1.0.0")
    sys.exit(1 if run() else 0)
