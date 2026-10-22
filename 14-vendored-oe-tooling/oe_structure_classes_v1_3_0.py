#!/usr/bin/env python3
"""oe_structure_classes_v1_3_0 - the ONE reader of the structure class table (OE_STRUCTURE_CLASSES_v*.tsv).

Why it exists. Three tools decided what to skip, from three lists of their own: the structure check (folder names), the release
check (a pattern over names, so a real file called "..._invalid_..." was skipped silently) and the publisher's Turtle parse
(two folder names). When the registrations are consolidated, all three must change together, and a list that nobody reads as a
whole drifts. The table is the one place; this module is the one reader; a tool that needs to know whether to read a folder or a
file asks here.

The table (tab-separated, `#` lines are comments, the first non-comment line is the header). Columns used here:
  class      G1 generated | G2 generated shapes | T1 test input | C1 copy of another package | H1 archive | R1 registration |
             U3 example unit | U2 out-of-domain unit | U1 domain unit | X not allowed
  match      one or more of `dir=NAME` `dirstart=PREFIX` `dirend=SUFFIX` `file=NAME` `unit=PATH` separated by `;`
             (`unit=` names a nested folder that has its own VERSION.txt, relative to the repository root)
  structure  skip | a1 (read for rule A1 only) | read       what the structure check does with a folder or file this row matches
  release    skip | read                                     the release check
  publish    skip | read                                     the publisher's Turtle parse
A row with no `match` documents a class (X) and is not read as a rule.

What it reports. `classify_dir(name)` and `classify_file(name)` return the class of a matching row, or None. A folder that
holds its own VERSION.txt below a package root (a nested unit) that no `unit=` row names is UNCLASSIFIED: `unclassified_units`
lists them, and the structure check reports each as rule X1. Nothing is skipped without a row, and nothing is "not a class" in
silence.

v1.1.0 (plan v1.15.0): the built-in table no longer skips `06-registrant-deposits` and `06-audit-artifacts`; both are units (or gone) since oe-pack 21.14.0 and 21.15.0, and a fallback that skipped them would hide files the table reads.

v1.2.0 (plan v1.20.0; found by the sessions of two packages, 2026-10-13): (1) the table is also looked for in <root>/oe-method/04-documentation, where the
shared table has lived since the method became the one authored home (v1.1.0 looked only in oe-pack and so fell back to the built-in copy in every governed tree); (2) the NAMED UNITS of a
tree are private content (they name its packages' folders) and no longer sit in the shared table: they are rows of a second file, OE_STRUCTURE_UNITS_v*.tsv (columns class, match, reason;
the highest version, looked for in the same folders), each row adds its `unit=` tokens to the row of the same class in the table; a row for a class the table lacks, or a token that is not
`unit=`, is refused. `Table.units_path` says which file was read.

When no table is found (an old checkout, a stage without governance), `load` returns the built-in table, which holds exactly the
lists the tools carried before this module, and says so: `Table.builtin` is true and the tools print a notice."""
import glob
import os
import re

COLUMNS = ("class", "name", "match", "structure", "release", "publish")

BUILTIN_TEXT = """class\tname\tmatch\tstructure\trelease\tpublish
G1\tgenerated record\tfile=PUBLISH_RECORD.ttl\tskip\tread\tread
G1\tgenerated or foreign tool folder\tdir=.git;dir=__pycache__;dir=node_modules\tskip\tskip\tread
T1\ttest input\tdir=fixtures\tskip\tskip\tskip
H1\tarchive\tdir=archive\ta1\tskip\tskip
C1\tcopy of another package\tdirstart=vendored;dirend=-snapshot\tskip\tread\tread
R1\tregistration\t\tread\tread\tread\nU3\texample unit\t\tread\tread\tread\nU2\tout-of-domain unit\t\tread\tread\tread\nU1\tdomain unit\t\tread\tread\tread\n"""


class Table:
    def __init__(self, text, path=None, builtin=False):
        self.path = path
        self.builtin = builtin
        self.rows = []
        header = None
        for ln in text.splitlines():
            if not ln.strip() or ln.startswith("#"):
                continue
            f = ln.split("\t")
            if header is None:
                header = f
                missing = [c for c in COLUMNS if c not in header]
                if missing:
                    raise ValueError("class table lacks the column(s): " + ", ".join(missing))
                continue
            row = dict(zip(header, f + [""] * (len(header) - len(f))))
            self.rows.append(row)
        if header is None:
            raise ValueError("class table is empty")
        self.units_path = None
        self._build()

    def _build(self):
        self._rules = []      # (kind, value, row)
        for r in self.rows:
            for tok in filter(None, (t.strip() for t in r["match"].split(";"))):
                if "=" not in tok:
                    raise ValueError("match token without kind: " + tok)
                kind, val = tok.split("=", 1)
                if kind not in ("dir", "dirstart", "dirend", "file", "unit"):
                    raise ValueError("unknown match kind: " + kind)
                self._rules.append((kind, val, r))

    def add_units(self, text, path=None):
        """rows of an OE_STRUCTURE_UNITS file: each adds its unit= tokens to the row of its class (see v1.2.0)"""
        header = None
        for ln in text.splitlines():
            if not ln.strip() or ln.startswith("#"):
                continue
            f = ln.split("\t")
            if header is None:
                header = f
                if "class" not in header or "match" not in header:
                    raise ValueError("units file lacks the column(s) class and match")
                continue
            row = dict(zip(header, f + [""] * (len(header) - len(f))))
            toks = [t.strip() for t in row["match"].split(";") if t.strip()]
            if not toks or any(not t.startswith("unit=") for t in toks):
                raise ValueError("a units row may carry unit= tokens only: " + ln[:80])
            target = next((r for r in self.rows if r["class"] == row["class"]), None)
            if target is None:
                raise ValueError("a units row names a class the table lacks: " + row["class"])
            target["match"] = ";".join(filter(None, [target["match"]] + toks))
        self.units_path = path
        self._build()

    def _find(self, kinds, test):
        for kind, val, r in self._rules:
            if kind in kinds and test(kind, val):
                return r
        return None

    def dir_row(self, name):
        return self._find(("dir", "dirstart", "dirend"), lambda k, v: (name == v if k == "dir" else name.startswith(v) if k == "dirstart" else name.endswith(v)))

    def file_row(self, name):
        return self._find(("file",), lambda k, v: name == v)

    def classify_dir(self, name):
        r = self.dir_row(name)
        return r["class"] if r else None

    def classify_file(self, name):
        r = self.file_row(name)
        return r["class"] if r else None

    def dir_action(self, name, tool):
        """'skip', 'a1' or 'read' for a folder name; a folder no row names is read."""
        r = self.dir_row(name)
        return r[tool] if r else "read"

    def file_action(self, name, tool):
        r = self.file_row(name)
        return r[tool] if r else "read"

    def skips_dir(self, name, tool):
        return self.dir_action(name, tool) == "skip"

    def release_exclude(self):
        """the release check's exclusion, built from the rows whose release action is skip: whole folders, never name words"""
        parts = []
        for kind, val, r in self._rules:
            if r["release"] != "skip":
                continue
            if kind == "dir":
                parts.append("/" + re.escape(val) + "/")
            elif kind == "dirstart":
                parts.append("/" + re.escape(val) + "[^/]*/")
            elif kind == "dirend":
                parts.append("/[^/]*" + re.escape(val) + "/")
            elif kind == "file":
                parts.append("/" + re.escape(val) + "$")
        return re.compile("|".join(parts)) if parts else re.compile(r"(?!x)x")

    def publish_skip_dirs(self):
        return {val for kind, val, r in self._rules if kind == "dir" and r["publish"] == "skip"}

    def units(self):
        return {val: r["class"] for kind, val, r in self._rules if kind == "unit"}

    def classes(self):
        return sorted({r["class"] for r in self.rows})


def _vkey(p):
    return [int(x) for x in re.findall(r"\d+", os.path.basename(p))]


def _dirs(root):
    return (os.path.join(root, "oe-pack", "04-documentation"), os.path.join(root, "oe-method", "04-documentation"), os.path.join(root, "04-documentation"))


def find(root, explicit=None):
    """path of the highest-version class table that has a machine header, or None. Looked for, in order: the file named by
    `explicit`; <root>/oe-pack/04-documentation; <root>/oe-method/04-documentation; <root>/04-documentation (a package that carries its own copy)."""
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    c = []
    for d in _dirs(root):
        c += glob.glob(os.path.join(d, "OE_STRUCTURE_CLASSES_v*.tsv"))
    for p in sorted(c, key=_vkey, reverse=True):
        try:
            Table(open(p, encoding="utf-8").read(), p)
            return p
        except ValueError:
            continue          # an older table without the machine columns is documentation, not a table to read
    return None


def find_units(root):
    """the highest OE_STRUCTURE_UNITS_v*.tsv in the same folders, or None. v1.3.0: a file named by the environment variable OE_STRUCTURE_UNITS
    wins when it exists: a release or a publish checks a stage that stands alone, and the governance source (which holds the units file) is a
    separate clone; the tool that made that clone names the file here."""
    e = os.environ.get("OE_STRUCTURE_UNITS")
    if e and os.path.isfile(e):
        return e
    c = []
    for d in _dirs(root):
        c += glob.glob(os.path.join(d, "OE_STRUCTURE_UNITS_v*.tsv"))
    return sorted(c, key=_vkey)[-1] if c else None


def load(root, explicit=None):
    p = find(root, explicit)
    t = Table(open(p, encoding="utf-8").read(), p) if p else Table(BUILTIN_TEXT, None, builtin=True)
    u = find_units(root) if (not explicit or os.environ.get("OE_STRUCTURE_UNITS")) else None   # v1.3.0: an explicit table still gets the named units file
    if u:
        t.add_units(open(u, encoding="utf-8").read(), u)
    return t


def nested_units(root, table, tool="structure", packages=None):
    """relative paths of folders below a package root that have their own VERSION.txt, outside skipped folders"""
    out = []
    tops = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and not d.startswith("."))
    for top in tops:
        if packages and top not in packages:
            continue
        for r, d, f in os.walk(os.path.join(root, top)):
            d[:] = sorted(x for x in d if not table.skips_dir(x, tool) and table.dir_action(x, tool) != "a1")
            if "VERSION.txt" in f and os.path.normpath(r) != os.path.normpath(os.path.join(root, top)):
                out.append(os.path.relpath(r, root).replace(os.sep, "/"))
    return out


def unclassified_units(root, table, tool="structure", packages=None):
    """nested units that no `unit=` row names (rule X1)"""
    known = set(table.units())
    return [u for u in nested_units(root, table, tool, packages) if u not in known]
