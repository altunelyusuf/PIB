#!/usr/bin/env python3
"""
PIB Release Gate v1.0.0
=======================
Runs every self-contained gate and exits non-zero if any fails. Nothing is released while it does.

Why this exists rather than a checklist: three releases in a single session went out after a gate printed
FAIL on the line directly above the push — v2.4.0 with a dead operator gate, v2.6.0 with three stale
references, v2.14.0 with two. Each time the check worked and its output was stepped over. A control that
depends on someone reading output is not a control; this one returns an exit code the release step obeys.

Gates needing credentials or an external source are named as skipped rather than silently omitted, so
their absence is visible rather than assumed.

Usage: python3 03-tooling/release_gate_v1_0_0.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GATES = [
    ("reference check", ["reference_check_v1_0_0.py"]),
    ("handover inbox", ["handover_inbox_check_v1_0_0.py"]),
    ("rule scope", ["rule_scope_check_v1_0_0.py"]),
    ("profile-scoped validation", ["profile_scoped_validate_v1_0_0.py", "--self-test"]),
    ("profile architecture", ["profile_architecture_check_v1_0_0.py", "--self-test"]),
    ("profile taxonomy", ["profile_taxonomy_v1_0_0.py", "--self-test"]),
    ("variation capacity", ["variation_capacity_v1_2_0.py", "--self-test"]),
    ("operator expression gate", ["operator_rule_runner_v1_0_0.py"]),
]
NEEDS_EXTERNAL = ["consumer registration check (needs a token)",
                  "profile approval (needs a token and the algebra's parser)"]


def main():
    failed = []
    print("PIB release gate v1.0.0")
    for name, cmd in GATES:
        r = subprocess.run([sys.executable, os.path.join(HERE, cmd[0])] + cmd[1:],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode != 0:
            failed.append(name)
        print(f"  {'pass' if r.returncode == 0 else 'FAIL'}  {name}")
        if r.returncode != 0:
            for line in (r.stdout + r.stderr).strip().splitlines()[-4:]:
                print(f"          {line}")
    for name in NEEDS_EXTERNAL:
        print(f"  skip  {name}")
    if failed:
        print(f"  RELEASE BLOCKED — {len(failed)} gate(s) failed: {', '.join(failed)}")
        return 1
    print("  all self-contained gates pass — release may proceed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
