#!/usr/bin/env python3
"""
PIB Handover Inbox Check v1.0.0
===============================
Enforces the parts of the ecosystem's handover standard that a reader cannot verify by looking.

Three rules, each because its violation is invisible otherwise:

  STRUCTURE   the four states exist — pending, accepted, rejected, deferred — and a plain-text log. A
              missing state silently becomes an item nobody can file.
  LOGGED      every dispositioned item has a line in the log. This is the rule that actually decays: a
              file is easy to move and easy to forget to record, and an item sitting in accepted/ with
              no line is indistinguishable from one nobody ever reviewed. Found exactly that in PIB's
              own inbox the first time this ran.
  OUTGOING    every item held in outgoing/ says why it was not filed in its target's inbox. The standard
              calls filing in one's own documentation the weaker path and the fallback; an unexplained
              outgoing item is that fallback used as a default.

What it deliberately does NOT judge: whether a disposition was correct. That is a claim about evidence,
which the log line must state and a reader must weigh; a script cannot re-run someone's judgement.

Usage:
    python3 03-tooling/handover_inbox_check_v1_0_0.py [inbox-dir]
    python3 03-tooling/handover_inbox_check_v1_0_0.py --self-test
"""
import os, sys, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INBOX = os.path.join(ROOT, "09-handover-inbox")
STATES = ("pending", "accepted", "rejected", "deferred")
DISPOSITIONED = ("accepted", "rejected", "deferred")
# Phrases that count as saying why an outgoing item is held rather than filed.
HELD_REASON = re.compile(r"no inbox|cannot reach|unreachable|no reachable|not filed in|held .* rout", re.I)


def items(d):
    return [os.path.basename(p) for p in sorted(glob.glob(os.path.join(d, "*.md")))
            if os.path.basename(p) != "README.md"]


def check(inbox=INBOX, verbose=True):
    problems = []
    if verbose:
        print(f"PIB handover inbox check v1.0.0 — {os.path.relpath(inbox, ROOT)}")

    # STRUCTURE
    for st in STATES:
        if not os.path.isdir(os.path.join(inbox, st)):
            problems.append(f"missing state directory '{st}/' — items of that disposition have nowhere to go")
    log_path = os.path.join(inbox, "HANDOVER_LOG.md")
    if not os.path.exists(log_path):
        problems.append("missing HANDOVER_LOG.md — dispositions would leave no record of what was verified")
        log = ""
    else:
        log = open(log_path, encoding="utf-8").read()

    # LOGGED
    logged = unlogged = 0
    for st in DISPOSITIONED:
        for name in items(os.path.join(inbox, st)):
            if name in log:
                logged += 1
            else:
                unlogged += 1
                problems.append(f"{st}/{name} has no line in HANDOVER_LOG.md — a dispositioned item with no "
                                f"record is indistinguishable from one nobody reviewed")

    # OUTGOING
    out_dir = os.path.join(inbox, "outgoing")
    outgoing = items(out_dir) if os.path.isdir(out_dir) else []
    for name in outgoing:
        text = open(os.path.join(out_dir, name), encoding="utf-8").read()
        if not HELD_REASON.search(text):
            problems.append(f"outgoing/{name} does not say why it is held rather than filed in its target's "
                            f"inbox — the standard makes this the fallback, not the default")

    pending = items(os.path.join(inbox, "pending"))
    if verbose:
        print(f"  structure: {sum(os.path.isdir(os.path.join(inbox, s)) for s in STATES)}/4 states, "
              f"log {'present' if log else 'MISSING'}")
        print(f"  dispositioned items logged: {logged}, unlogged: {unlogged}")
        print(f"  outgoing items held: {len(outgoing)}")
        print(f"  pending (the session-start read): {pending if pending else 'none'}")
        for p in problems:
            print(f"  FAIL: {p}")
        print("  PASS — the inbox meets the standard" if not problems else
              f"  FAIL — {len(problems)} problem(s)")
    return problems


def self_test():
    """Prove each rule can fail, on a fixture built to break exactly one thing at a time."""
    import tempfile, shutil
    ok = True
    # positive: a well-formed inbox
    good = tempfile.mkdtemp()
    for st in STATES:
        os.makedirs(os.path.join(good, st))
    open(os.path.join(good, "accepted", "X_to_PIB_thing_v1_0_0.md"), "w").write("x")
    open(os.path.join(good, "HANDOVER_LOG.md"), "w").write("| `X_to_PIB_thing_v1_0_0.md` | verified by re-running it |\n")
    p = check(good, verbose=False); print(f"  well-formed inbox -> {len(p)} problem(s) (expected 0)"); ok &= not p

    # negative 1: a dispositioned item with no log line
    bad1 = tempfile.mkdtemp()
    for st in STATES:
        os.makedirs(os.path.join(bad1, st))
    open(os.path.join(bad1, "accepted", "Y_to_PIB_thing_v1_0_0.md"), "w").write("y")
    open(os.path.join(bad1, "HANDOVER_LOG.md"), "w").write("| header |\n")
    p = check(bad1, verbose=False); print(f"  unlogged dispositioned item -> {len(p)} problem(s) (expected 1)"); ok &= len(p) == 1

    # negative 2: a missing state directory
    bad2 = tempfile.mkdtemp()
    for st in ("pending", "accepted"):
        os.makedirs(os.path.join(bad2, st))
    open(os.path.join(bad2, "HANDOVER_LOG.md"), "w").write("")
    p = check(bad2, verbose=False); print(f"  missing state directories -> {len(p)} problem(s) (expected 2)"); ok &= len(p) == 2

    # negative 3: an outgoing item that does not say why it is held
    bad3 = tempfile.mkdtemp()
    for st in STATES + ("outgoing",):
        os.makedirs(os.path.join(bad3, st))
    open(os.path.join(bad3, "HANDOVER_LOG.md"), "w").write("")
    open(os.path.join(bad3, "outgoing", "Z_PIB_to_other_v1_0_0.md"), "w").write("a proposal with no routing note")
    p = check(bad3, verbose=False); print(f"  unexplained outgoing item -> {len(p)} problem(s) (expected 1)"); ok &= len(p) == 1

    print(f"  every rule can fail: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raise SystemExit(1 if check(args[0] if args else INBOX) else 0)
