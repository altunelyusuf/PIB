#!/usr/bin/env python3
"""
PIB Reference Check v1.0.0
==========================
Fails when a current document or tool cites a package file that does not exist.

Why this exists: twice in one day a release went out citing a renamed file — once breaking a gate
outright, once leaving three stale references in documentation. Both times the release output printed a
warning line about it, and both times the release was pushed anyway. A warning nobody stops for is not a
safeguard, so the warning is now a gate with a non-zero exit.

Only citations of a file the package still ships under a DIFFERENT version count as stale; names the
package does not carry at all belong to other packages and are ignored, as is a file citing its own
earlier version in its history.

Records of past state are exempt by design, and named explicitly rather than by a blanket pattern:
dated status notes, the handover inbox, the registration folders and the experiments folder all describe
what was true when they were written. Repointing them would be the corruption this package's own
discipline warns about — a file that records a past state must not be mechanically updated.

Usage: python3 03-tooling/reference_check_v1_0_0.py [package-root]
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
# Folders whose contents record past state, or are not PIB's to repoint.
EXEMPT_DIRS = ("09-handover-inbox", "08-registration", "10-experiments", "11-vendored-operator-rules", ".git")
# Within a current document, text after one of these markers is a dated record and is left alone.
RECORD_MARKERS = ("## Status note appended", "## Correction appended", "## Re-vendored in PIB",
                  "## Execution record", "## Note appended", "---\n\n## Appended")
CITATION = re.compile(r"[\w./-]*(?:0\d-[\w-]+/)?[\w-]+_v\d+(?:_\d+)*\.(?:ttl|py|md|txt)")


VERSION_SUFFIX = re.compile(r"_v\d+(?:_\d+)*(?=\.[a-z]+$)")


def stem(basename):
    """A file's identity without its version: pib_enumeration_rules_v2_2_0.ttl -> pib_enumeration_rules.ttl"""
    return VERSION_SUFFIX.sub("", basename)


def current_files(root):
    """Every file the package currently ships, and the set of version-less identities among them."""
    names = set()
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in EXEMPT_DIRS and d != "__pycache__"]
        names.update(fns)
    return names, {stem(n) for n in names}


def main():
    root = os.path.abspath(ROOT)
    present, stems = current_files(root)
    stale, checked = [], 0
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in EXEMPT_DIRS and d != "__pycache__"]
        for fn in fns:
            if not fn.endswith((".md", ".py", ".ttl")) or fn.startswith("RETIRED_"):
                continue   # a RETIRED_ note is wholly a record of what was true at retirement
            path = os.path.join(dp, fn)
            try:
                text = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            cut = len(text)
            for m in RECORD_MARKERS:                       # ignore everything from the first record marker on
                i = text.find(m)
                if i != -1:
                    cut = min(cut, i)
            checked += 1
            for cited in set(CITATION.findall(text[:cut])):
                base = os.path.basename(cited)
                if base == fn or base in present:
                    continue
                # Only citations of a file THIS package still ships under another version are stale.
                # A name whose identity the package does not carry belongs to another package — the
                # algebra's files, a spoke's sources, a governance artifact — and is none of this
                # check's business. Self-citation of an older version is a file's own history.
                if stem(base) not in stems or stem(base) == stem(fn):
                    continue
                stale.append((os.path.relpath(path, root), base))
    print(f"PIB reference check v1.0.0 — {checked} current files scanned")
    for where, what in sorted(set(stale)):
        print(f"  STALE: {where} cites {what}, which no longer exists")
    if stale:
        print(f"  FAIL — {len(set(stale))} stale reference(s). Repoint them, or move the text into a dated record.")
        return 1
    print("  PASS — every cited package file exists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
