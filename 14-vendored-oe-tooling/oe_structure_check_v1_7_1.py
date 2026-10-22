#!/usr/bin/env python3
"""oe_structure_check_v1_7_1 - one T-Box, one A-Box and one SHACL file per package, and the file naming/version conventions, enforced (BP-D54, BP-D53, BP-D6, BP-D7).

v1.6.0 (plan v1.10.0 item 38(b)): the folders and files the check does not read come from ONE class table, OE_STRUCTURE_CLASSES_v*.tsv, through oe_structure_classes_v1_0_0.py, the same reader the release check and the publisher use; the lists that were written in this file are gone (a built-in copy of them is used, and announced, only when no table is found). New rule X1: a nested folder with its own VERSION.txt that no `unit=` row of the table names is reported, because a path that matches no class must be reported, not skipped. `--classes FILE` names the table. The run also prints, per class, how many Turtle files it did not read.

v1.7.1 (the O4DE session, 2026-10-13): the notice for a tree with no class table names the folders it is looked for in (oe-pack, oe-method, the tree's own 04-documentation), says what the built-in copy holds, and the header names this file's version.
v1.7.0: a rule the aggregate records as `enforce` with a recorded ruling is in force before the package's own register carries the line (see merge_registers).
v1.5.1: a line in a package's own register that opts in to M1 or D1 (status `enforce`) is no longer refused for being absent from the aggregate. It adds a check and records no debt, and without this a new rule could never be adopted: the publisher compares a package with the aggregate already published.

v1.4.0 (the owner's ruling of 2026-10-07): A PACKAGE HOLDS ITS OWN DEBT, AND THE GOVERNANCE AGGREGATE HOLDS THE CEILINGS.

Until now one file in the governance package carried every package's lines: 264 of 268 belonged to packages that file's
owner does not own, and BP-D54's own sentence -- "the owning session clears its own register lines" -- could not be obeyed,
because clearing one meant editing another session's package, which boundary B1 forbids. A session had to file a handover
and wait. The owner ruled that each package carries its own register and the governance package keeps the rules and a
generated aggregate.

What this version reads, per package:
  <package>/04-documentation/structure-debt/STRUCTURE_DEBT_REGISTER_v*.tsv   the package's OWN lines, highest version
  the file given with --register                                            the governance aggregate: the CEILING baseline

  - A package with its own register is governed by it. The owning session clears a line by fixing the file and removing
    the line in its own release; nobody else is involved.
  - A package with no register of its own behaves exactly as before, governed by the aggregate alone, so adoption is
    incremental and nothing is blocked while packages adopt.
  - Three guards keep the ratchet from becoming self-certified, which is the one thing the old single file bought and a
    remedy must not lose. Against the aggregate, a local register may not: raise a count (U1, A1, M1 files=/missing=),
    introduce a line the aggregate does not carry, or upgrade a status to `exception`. Each is reported as a violation of
    the line itself and fails the run. Shrinking, and removing a line whose violation is gone, need no permission.

v1.3.0, two defects, both measured on real work:

(1) A LINE FOR A PACKAGE THIS SCAN CANNOT SEE WAS REPORTED CLEARED. The register is one file governing many packages, and
some of them live in their own repositories. Run inside the monorepo, every line naming a package that is not there had
no violation to match, so it was reported CLEARED -- "remove it, the violation is gone" -- when the truth was that nothing
had been examined. Six lines for two course repositories were removed on that report in register v1.9.0, and the owning
session's publisher then refused both repositories for a violation outside the register, which is the defect arriving
back as a block on real work. A line whose package root is absent from the scan is now reported NOT MEASURED, counted
separately, and never listed as CLEARED; the exit code ignores it, because a line nobody measured is neither cleared nor
new. Same reasoning as the existing "a scan of nothing is not a pass": absence of evidence is not evidence of absence.

(2) THE SAME REPOSITORY MEASURED TWO DIFFERENT PACKAGE NAMES. A package resolves as the nearest ancestor folder holding a
VERSION.txt, else the top-level folder. The publisher stages a package-at-root repository under its SLUG and checks that,
so it sees one package named after the slug; the same repository checked at its own root has VERSION.txt at the root, so
every file falls to its own top-level folder and the counts are per folder. Two true answers to different questions, and
the register can only carry the publisher's one. --as-package NAME resolves the scan root itself as NAME, so a session can
run locally exactly what its publisher will run, and the counts and the paths agree. Measured on a course repository: at
its root the checker reports 03-materials/A files=27, staged under its slug it reports sen0401/A files=34, and only the
second is what the register must hold.

v1.5.0: rule D1 (copies), opt-in per package like M1: `D1  <package>  enforce  copies=N`. Merging two files that define the same shape or class does not
drop the anonymous nodes (a blank node is not the same node in two files), so a shape's constraints or a class's restriction were found twice -- 117 copies in 47
shapes of the OE pack and the method, 2 more in the pack's T-Box (2026-10-07) -- and the earlier merge proof compared by signature and could not see them. D1 counts, per
named subject and predicate, the blank-node objects whose whole content is identical beyond the first. A count above the recorded N fails (the ratchet), a line with status
`enforce` is kept at 0.
v1.2.1: rule M1 no longer takes every IRI below a header IRI for a version IRI (66 quality individuals and one shape of the OE pack were not counted); only the version IRIs a header declares are skipped.

v1.2.0: rule M1 (membership), opt-in per package. When a package is consolidated, every named subject must say which module it belongs to
(dcterms:isPartOf <module>), or a merged file cannot be sliced back into its former subjects. M1 is checked only for a package that has an M1 line in the
register (`M1  <package>  enforce  missing=N`): the line is the opt-in and the ceiling, so no other package is affected. A count above N fails (the ratchet),
a count below N is reported as LOWER (rewrite the line), and a line with status `enforce` is kept even at missing=0 (it is what keeps the rule on).
A module is an untyped resource carrying dcterms:identifier and dcterms:isPartOf the file's ontology; before a merge the file's own header is the module.

v1.1.0 (owner's ruling, 2026-10-06): the unit is the PACKAGE, not the subject. A package ships ONE T-Box, ONE A-Box and ONE SHACL file in all,
each with ONE owl:Ontology header; its former subjects live inside as modules. Its retired history is held the same way in the archive folder:
one T-Box, one A-Box, one SHACL file. v1.0.0 asked for one triad per subject (BP-D53); its rule I1 is retired and replaced by U1 and H1.

Each Turtle file is read by its PARSED CONTENT (not its name) and reported against:
  N1  name        the file name does not match  ^[a-z][a-z0-9_]*_v<MAJOR>_<MINOR>_<PATCH>.ttl$   (BP-D6)
  N2  patch-name  the name says it is an extension, follow-up, addition, patch, re-emit or draft  (no such files)
  V1  versions    several versions of one file are shipped side by side  (BP-D7: one current file per identity)
  R1  mixed-roles the file holds more than one role: classes/properties (T-Box), instances (A-Box), shapes (SHACL)
  H1  headers     the file declares more than one owl:Ontology  (one file, one identity, one version)
  U1  files       a package ships more than one active file of a role (reported once per package and role, path <package>/<T|A|S>, note files=N)
  A1  archive     a package's archive folders hold more than one file of a role (path <package>/archive/<T|A|S>, note files=N)
  D1  copies      (opt-in, see v1.5.0) identical anonymous nodes under one subject and predicate -- a union of two files keeps both copies of a blank node (path <package>, note copies=N)
  M1  membership  (opt-in, see v1.2.0) named subjects of an active file with no dcterms:isPartOf a module of that file (path <package>, note missing=N)
Folders named fixtures hold deliberate test inputs, 06-registrant-deposits and 06-audit-artifacts hold other parties' deposits and preserved
snapshots (the pack's release check has always excluded them), folders named vendored* or *-snapshot hold copies of other packages; none of these is
read. Folders named archive are read only for A1. PUBLISH_RECORD.ttl is a generated record and is not read.

Ratchet: with --register FILE (tab-separated: rule, path, status, note) the check fails only on a violation that is NOT in the register, so the
recorded debt can only shrink; for U1 and A1 a count that GREW beyond the recorded files=N also fails. An entry whose violation is gone is reported
CLEARED (remove it). An entry may be marked `exception` only with the owner's ruling in the note.

A package is the nearest folder holding a VERSION.txt (else the top-level folder).

Usage: oe_structure_check_v1_7_1.py [ROOT] [--package NAME ...] [--register FILE] [--list] [--write-register FILE] [--as-package NAME]
       [--no-local]   ignore the packages' own registers and read only the file given with --register (what v1.3.0 did)
Exit: 0 no violation outside the register; 1 a violation outside it; 2 REFUSED (nothing examined, unreadable register).
A scan that examined zero files is refused, never reported as a pass."""
import glob, importlib.util, os, re, sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_libs = sorted(glob.glob(os.path.join(_HERE, "oe_structure_classes_v*.py")), key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))])
if not _libs:
    raise SystemExit("REFUSED: oe_structure_classes_v*.py is missing next to this tool; it is the one reader of the class table")
_sp = importlib.util.spec_from_file_location("oe_structure_classes", _libs[-1]); CLASSES = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(CLASSES)
CLS = CLASSES.Table(CLASSES.BUILTIN_TEXT, None, builtin=True)     # replaced in main() by the table found for the scanned root

NAME = re.compile(r"^[a-z][a-z0-9_]*_v\d+_\d+_\d+\.ttl$")
VER = re.compile(r"^(.*)_v(\d+_\d+_\d+)\.ttl$")
PATCHWORDS = {"patch", "followup", "extension", "addition", "reemit", "draft", "fixup", "hotfix"}
OWL = "http://www.w3.org/2002/07/owl#"; RDFS = "http://www.w3.org/2000/01/rdf-schema#"; SH = "http://www.w3.org/ns/shacl#"
T_TYPES = {OWL + "Class", RDFS + "Class", OWL + "ObjectProperty", OWL + "DatatypeProperty", OWL + "AnnotationProperty",
           OWL + "TransitiveProperty", OWL + "SymmetricProperty", OWL + "FunctionalProperty", OWL + "InverseFunctionalProperty",
           "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"}
S_TYPES = {SH + "NodeShape", SH + "PropertyShape"}
# any type from the OWL, RDFS, RDF or SHACL vocabularies is language machinery (an ontology header, a datatype, a SPARQL constraint),
# not an instance of a domain class
META_NS = (OWL, RDFS, SH, "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
META = T_TYPES | S_TYPES | {OWL + "Ontology", OWL + "NamedIndividual", OWL + "Restriction", OWL + "AllDisjointClasses"}


def files(root, packages):
    out = []
    tops = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and not d.startswith("."))
    for top in tops:
        if packages and top not in packages:
            continue
        for r, d, f in os.walk(os.path.join(root, top)):
            d[:] = sorted(x for x in d if CLS.dir_action(x, "structure") == "read")
            for n in sorted(f):
                if n.endswith(".ttl") and CLS.file_action(n, "structure") == "read":
                    out.append(os.path.relpath(os.path.join(r, n), root))
    return out


def roles_of(path):
    import rdflib
    from rdflib import RDF, URIRef
    g = rdflib.Graph(); g.parse(path)
    t = s = a = 0; onts = []
    typed = defaultdict(set)
    for sub, o in g.subject_objects(RDF.type):
        typed[sub].add(str(o))
    for sub, types in typed.items():
        if types & T_TYPES and isinstance(sub, URIRef): t += 1
        if types & S_TYPES: s += 1
        if isinstance(sub, URIRef) and {x for x in types if not x.startswith(META_NS)} - META and not (types & (T_TYPES | S_TYPES)): a += 1
        if OWL + "Ontology" in types and isinstance(sub, URIRef): onts.append(str(sub))
    roles = [r for r, c in (("T", t), ("A", a), ("S", s)) if c]
    return roles, onts, (t, a, s)


DCT = "http://purl.org/dc/terms/"


def membership_missing(path):
    """Named subjects of the file that carry no dcterms:isPartOf a module (the file's header or an untyped, identified module resource)."""
    import rdflib
    from rdflib import RDF, URIRef
    g = rdflib.Graph(); g.parse(path)
    isp = URIRef(DCT + "isPartOf"); ident = URIRef(DCT + "identifier")
    hs = {s for s in g.subjects(RDF.type, URIRef(OWL + "Ontology")) if isinstance(s, URIRef)}
    mods = {m for m, p in g.subject_objects(isp) if p in hs and m not in hs and isinstance(m, URIRef) and (m, RDF.type, None) not in g and (m, ident, None) in g}
    targets = hs | mods
    OWLN = rdflib.URIRef(OWL + "versionIRI"); PRIOR = rdflib.URIRef(OWL + "priorVersion")
    vis = {o for h in hs for p in (OWLN, PRIOR) for o in g.objects(h, p)}
    missing = 0
    for s in set(g.subjects()):
        if not isinstance(s, URIRef) or s in hs or s in mods: continue
        if s in vis: continue
        if not any(o in targets for o in g.objects(s, isp)): missing += 1
    return missing


def anonymous_copies(path):
    """Extra identical copies of an anonymous node: per named subject and predicate, blank-node objects whose whole content (their own
    predicates and, recursively, the blank nodes below them) is identical to an earlier one. RDF lists are not counted (their cells
    are distinct by position)."""
    import rdflib
    from rdflib import BNode, RDF
    g = rdflib.Graph(); g.parse(path)
    memo = {}
    def canon(n):
        if n in memo: return memo[n]
        r = tuple(sorted(((str(p), canon(o) if isinstance(o, BNode) else o.n3()) for p, o in g.predicate_objects(n)), key=repr))
        memo[n] = r; return r
    total = 0
    for s in set(g.subjects()):
        if isinstance(s, BNode): continue
        by = {}
        for p, o in g.predicate_objects(s):
            if isinstance(o, BNode) and (o, RDF.first, None) not in g: by.setdefault(p, []).append(canon(o))
        for p, l in by.items():
            seen = set()
            for c in l:
                if c in seen: total += 1
                else: seen.add(c)
    return total


def pkg_of(root, rel):
    """The package a file belongs to: the nearest ancestor folder holding a VERSION.txt, else its top-level folder."""
    parts = rel.split(os.sep)[:-1]
    for i in range(len(parts), 0, -1):
        if os.path.isfile(os.path.join(root, *parts[:i], "VERSION.txt")): return "/".join(parts[:i])
    return parts[0] if parts else ""


def archive_files(root, packages):
    """Turtle files that sit under a folder named archive (read only for rule A1)."""
    out = []
    tops = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and not d.startswith("."))
    for top in tops:
        if packages and top not in packages: continue
        for r, d, f in os.walk(os.path.join(root, top)):
            d[:] = sorted(x for x in d if CLS.dir_action(x, "structure") in ("read", "a1"))
            if not any(CLS.dir_action(x, "structure") == "a1" for x in os.path.relpath(r, root).split(os.sep)): continue
            for n in sorted(f):
                if n.endswith(".ttl") and CLS.file_action(n, "structure") == "read": out.append(os.path.relpath(os.path.join(r, n), root))
    return out


def scan(root, packages=None, m1pkgs=(), d1pkgs=()):
    fs = files(root, packages)
    viol = defaultdict(list)       # (rule, path) -> note
    info = {}
    for p in fs:
        b = os.path.basename(p)
        if not NAME.match(b):
            viol[("N1", p)] = "name does not match <name>_v<MAJOR>_<MINOR>_<PATCH>.ttl"
        if PATCHWORDS & set(re.split(r"[_\-]", b.lower().rsplit(".", 1)[0])):
            viol[("N2", p)] = "name says extension, follow-up, addition, patch, re-emit or draft"
        try:
            roles, onts, counts = roles_of(os.path.join(root, p))
        except Exception as e:
            viol[("P0", p)] = "does not parse: " + str(e)[:60]
            continue
        info[p] = (roles, onts)
        if len(roles) > 1:
            viol[("R1", p)] = "holds roles " + "+".join(roles) + f" (T {counts[0]}, A {counts[1]}, S {counts[2]})"
    miss = defaultdict(int)
    for p in info:
        pk = pkg_of(root, p)
        if pk in m1pkgs:
            try: miss[pk] += membership_missing(os.path.join(root, p))
            except Exception as e: viol[("P0", p)] = "does not parse: " + str(e)[:60]
    cp = defaultdict(int)
    for p in info:
        pk = pkg_of(root, p)
        if pk in d1pkgs:
            try: cp[pk] += anonymous_copies(os.path.join(root, p))
            except Exception as e: viol[("P0", p)] = "does not parse: " + str(e)[:60]
    for pk, n in cp.items():
        if n: viol[("D1", pk)] = f"copies={n}: {n} identical anonymous node(s) under one subject and predicate; a merge kept both copies"
    for pk, n in miss.items():
        if n: viol[("M1", pk)] = f"missing={n}: {n} named subject(s) carry no dcterms:isPartOf a module of their file"
    groups = defaultdict(list)
    for p in fs:
        m = VER.match(os.path.basename(p))
        if m: groups[(os.path.dirname(p), m.group(1))].append((m.group(2), p))
    for (d, stem), vs in groups.items():
        if len(vs) > 1:
            for v, p in vs:
                viol[("V1", p)] = f"{len(vs)} versions of {stem} shipped side by side"
    for p, (roles, onts) in info.items():
        if len(onts) > 1:
            viol[("H1", p)] = f"declares {len(onts)} owl:Ontology headers; a consolidated file has one"
    perrole = defaultdict(list)    # (package, role) -> files
    for p, (roles, onts) in info.items():
        for r in roles: perrole[(pkg_of(root, p), r)].append(p)
    for (pkg, role), ps in perrole.items():
        if len(ps) > 1:
            viol[("U1", f"{pkg}/{role}")] = f"files={len(ps)}: {len(ps)} active {role} files; the package ships one"
    arole = defaultdict(list)
    for p in archive_files(root, packages):
        try: roles, onts, counts = roles_of(os.path.join(root, p))
        except Exception: continue
        for r in roles: arole[(pkg_of(root, p), r)].append(p)
    for (pkg, role), ps in arole.items():
        if len(ps) > 1:
            viol[("A1", f"{pkg}/archive/{role}")] = f"files={len(ps)}: {len(ps)} archived {role} files; the archive holds one"
    for u in ([] if CLS.builtin else CLASSES.unclassified_units(root, CLS, "structure", packages)):
        viol[("X1", u)] = "a folder with its own VERSION.txt that no row of the class table names: its class is unknown"
    return fs, viol


def skipped_counts(root, packages):
    """Turtle files this run did not read, per class of the folder or file that took them out (never silent)"""
    out = defaultdict(int)
    tops = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and not d.startswith("."))
    for top in tops:
        if packages and top not in packages: continue
        def walk(path, cls):
            for n in sorted(os.listdir(path)):
                q = os.path.join(path, n)
                if os.path.isdir(q):
                    c = CLS.classify_dir(n)
                    if CLS.dir_action(n, "structure") == "read": walk(q, cls)
                    elif CLS.dir_action(n, "structure") == "skip": walk(q, cls or c)
                    else: walk(q, cls)
                elif n.endswith(".ttl") and cls:
                    out[cls] += 1
                elif n.endswith(".ttl") and CLS.file_action(n, "structure") != "read":
                    out[CLS.classify_file(n)] += 1
        walk(os.path.join(root, top), None)
    return out


def read_register(path):
    reg = {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln or ln.startswith("#"): continue
        parts = ln.split("\t")
        if len(parts) < 3: raise ValueError("register line needs rule, path, status: " + ln[:80])
        if parts[2] == "exception" and (len(parts) < 4 or not parts[3].strip()):
            raise ValueError("an exception needs the owner's ruling in the note: " + ln[:80])
        reg[(parts[0], parts[1])] = parts[2:]
    return reg


LOCAL_GLOB = os.path.join("04-documentation", "structure-debt", "STRUCTURE_DEBT_REGISTER_v")


def local_register_path(root, pkg, not_this=None):
    """the package's own register, highest version, or None. A file that IS the aggregate given with --register is not a
    local register, however it is named: the governance package holds both, and before the aggregate was renamed the two
    names were the same file. Measured the hard way -- the central file was read as the governance package's own register
    and every line for another package tripped the guard."""
    import glob as _g
    d = os.path.join(root, pkg, "04-documentation", "structure-debt")
    c = _g.glob(os.path.join(d, "STRUCTURE_DEBT_REGISTER_v*.tsv"))
    if not_this:
        c = [p for p in c if not (os.path.exists(not_this) and os.path.samefile(p, not_this))]
    if not c:
        return None
    return sorted(c, key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))])[-1]


def count_of(note):
    m = re.search(r"(?:files|missing|copies)=(\d+)", note or "")
    return int(m.group(1)) if m else None


def merge_registers(root, agg, pkgs, not_this=None, no_local=False):
    """(register in force, per-package source, guard violations). A package with its own register is governed by it;
    the aggregate stays the ceiling baseline and the three guards below are what keep the ratchet honest."""
    reg = {}; src = {}; bad = {}
    local_pkgs = {}
    for p in ([] if no_local else sorted(pkgs)):
        lp = local_register_path(root, p, not_this)
        if lp:
            local_pkgs[p] = (lp, read_register(lp))
    for k, v in (agg or {}).items():
        if k[1].split(os.sep)[0] in local_pkgs:
            continue                      # that package speaks for itself below
        reg[k] = v; src[k] = "aggregate"
    for p, (lp, lreg) in local_pkgs.items():
        for k, v in lreg.items():
            if k[1].split(os.sep)[0] != p:
                bad[k] = (f"{p}'s own register carries a line for another package ({k[1]}); a package records only its own debt")
                continue
            reg[k] = v; src[k] = lp
            if agg is None:
                continue
            a = agg.get(k)
            if a is None and v[0] == "enforce" and k[0] in ("M1", "D1"):
                continue                      # an opt-in to a rule adds a check and records no debt: tightening needs no ruling
            if a is None:
                bad[k] = (f"{k[1]} is in {p}'s own register but not in the governance aggregate: new debt needs a ruling, "
                          f"not a local line")
                continue
            if v[0] == "exception" and a[0] != "exception":
                bad[k] = (f"{k[1]} is marked exception in {p}'s own register while the aggregate has it as {a[0]}: "
                          f"an exception is the owner's ruling, not a local edit")
                continue
            cn, ca = count_of(" ".join(v[1:])), count_of(" ".join(a[1:]))
            if cn is not None and ca is not None and cn > ca:
                bad[k] = (f"{k[1]} raises its own ceiling from {ca} to {cn} in {p}'s own register; a ceiling rises only in "
                          f"the governance aggregate, with the ruling recorded")
    # v1.7.0: a rule the aggregate records as `enforce` WITH the owner's ruling is in force at once, even while the package's own register does not carry the line yet.
    # Without this the aggregate (which a package needs first, to publish) turned the whole tree red until that package's next release (oe-pack 21.43.0, 2026-10-13).
    for k, v in (agg or {}).items():
        if k[0] in ("M1", "D1") and v[0] == "enforce" and "ruling:" in " ".join(v[1:]) and k[1].split(os.sep)[0] in local_pkgs and k not in reg:
            reg[k] = v; src[k] = "aggregate"
    return reg, src, bad


def main(argv):
    global CLS
    pos = []; pk = []; reg_path = write = None; lst = False; as_pkg = None; no_local = False; classes_arg = None; i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--package": pk.append(argv[i + 1]); i += 1
        elif a == "--register": reg_path = argv[i + 1]; i += 1
        elif a == "--write-register": write = argv[i + 1]; i += 1
        elif a == "--as-package": as_pkg = argv[i + 1]; i += 1
        elif a == "--classes": classes_arg = argv[i + 1]; i += 1
        elif a == "--no-local": no_local = True
        elif a == "--list": lst = True
        elif not a.startswith("-"): pos.append(a)
        i += 1
    root = pos[0] if pos else "."
    try:
        CLS = CLASSES.load(root, classes_arg)
    except (OSError, ValueError) as e:
        print("REFUSED: class table unreadable: " + str(e), file=sys.stderr); return 2
    if classes_arg and CLS.builtin:
        print("REFUSED: --classes names a file that does not exist: " + classes_arg, file=sys.stderr); return 2
    agg = None; m1pkgs = set(); d1pkgs = set()
    if reg_path:
        try:
            agg = read_register(reg_path)
        except (OSError, ValueError) as e:
            print("REFUSED: register unreadable: " + str(e), file=sys.stderr); return 2
        m1pkgs = {k[1] for k in agg if k[0] == "M1" and (not pk or k[1] in pk)}
        d1pkgs = {k[1] for k in agg if k[0] == "D1" and (not pk or k[1] in pk)}
    # A package's M1 opt-in may live in its own register, and the scan needs the opt-ins before it runs.
    local_seen = {}
    if not no_local and os.path.isdir(root):
        for d in sorted(x for x in os.listdir(root) if os.path.isdir(os.path.join(root, x)) and not x.startswith(".")):
            lp = local_register_path(root, d, reg_path)
            if not lp:
                continue
            try:
                local_seen[d] = read_register(lp)
            except (OSError, ValueError) as e:
                print(f"REFUSED: {d}'s own register unreadable: {e}", file=sys.stderr); return 2
            m1pkgs |= {k[1] for k in local_seen[d] if k[0] == "M1" and (not pk or k[1] in pk)}
            d1pkgs |= {k[1] for k in local_seen[d] if k[0] == "D1" and (not pk or k[1] in pk)}

    if as_pkg:
        # The root itself is the package the publisher will check, under the name it will use. Staging it under that name
        # is what the publisher does; doing the same here is why the two runs agree.
        import shutil, tempfile
        stage = tempfile.mkdtemp(); dest = os.path.join(stage, as_pkg)
        shutil.copytree(root, dest, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
        root = stage
        if not pk:
            pk = [as_pkg]
    fs, viol = scan(root, pk or None, m1pkgs, d1pkgs)
    if not fs:
        print("REFUSED: examined 0 Turtle files under " + root + "; a scan of nothing is not a pass", file=sys.stderr)
        return 2
    pkgs = {p.split(os.sep)[0] for p in fs}
    print(f"examined {len(fs)} Turtle file(s) in {len(pkgs)} package(s); {len(viol)} violation(s)")
    if CLS.builtin:
        print("  NOTICE: no class table found; the built-in copy was used: it holds the same folder and file rules as OE_STRUCTURE_CLASSES v1.7.0 and knows no named unit (the table is read from oe-pack/04-documentation, oe-method/04-documentation or 04-documentation of the tree, or named with --classes)")
    else:
        sk = skipped_counts(root, pk or None)
        print("  class table: " + os.path.basename(CLS.path) + "; not read, by class: " + (", ".join(f"{k} {v}" for k, v in sorted(sk.items())) or "none"))
    by = defaultdict(int)
    for (rule, _p) in viol: by[rule] += 1
    print("by rule: " + ", ".join(f"{k} {v}" for k, v in sorted(by.items())))
    if write:
        with open(write, "w", encoding="utf-8") as f:
            f.write("# rule\tpath\tstatus\tnote   (status: debt | pending-ruling | exception; an exception names the owner's ruling)\n")
            for (rule, p), note in sorted(viol.items(), key=lambda kv: (kv[0][1], kv[0][0])):
                f.write(f"{rule}\t{p}\tdebt\t{note}\n")
        print("register written: " + write)
    new = []
    reg = None; src = {}; guard = {}
    if agg is not None or local_seen:
        reg, src, guard = merge_registers(root, agg, pkgs | set(local_seen), reg_path, no_local)
        if pk:
            reg = {k: v for k, v in reg.items() if k[1].split(os.sep)[0] in pk}
            guard = {k: v for k, v in guard.items() if k[1].split(os.sep)[0] in pk}
    if reg is not None:
        new = sorted(k for k in viol if k not in reg)
        for k in sorted(k for k in viol if k in reg and k[0] in ("U1", "A1", "M1", "D1")):
            rec = re.search(r"(?:files|missing|copies)=(\d+)", " ".join(reg[k])); now = re.search(r"(?:files|missing|copies)=(\d+)", viol[k])
            if rec and now and int(now.group(1)) > int(rec.group(1)):
                viol[k] = f"GREW from {rec.group(1)} to {now.group(1)}; " + viol[k]; new.append(k)
        new = sorted(set(new))
        # A line whose package root is not in this scan was not measured: no violation matched it because nothing was
        # read, which is not the same as the violation being gone. Reported separately, never as CLEARED.
        scanned_pkgs = {p.split(os.sep)[0] for p in fs}
        unmeasured = sorted(k for k in reg if k[1].split(os.sep)[0] not in scanned_pkgs)
        cleared = sorted(k for k in reg if k not in viol and k not in unmeasured
                         and not (k[0] in ("M1", "D1") and reg[k][0] == "enforce"))
        for k in sorted(k for k in viol if k in reg and k[0] in ("M1", "D1")):
            rec = re.search(r"(?:missing|copies)=(\d+)", " ".join(reg[k])); now = re.search(r"(?:missing|copies)=(\d+)", viol[k])
            if rec and now and int(now.group(1)) < int(rec.group(1)):
                print(f"  LOWER {k[0]} {k[1]}: recorded {rec.group(1)}, now {now.group(1)} (rewrite the line)")
        own = sorted({k[1].split(os.sep)[0] for k, v in src.items() if v != "aggregate"})
        print(f"register: {len(reg)} entr(ies); {len(viol) - len(new)} violation(s) recorded, {len(new)} NEW, "
              f"{len(cleared)} CLEARED (remove from the register), {len(unmeasured)} NOT MEASURED (package not in this scan)")
        if own:
            print(f"  own registers in force: {', '.join(own)}  (the rest are governed by the aggregate)")
        for k, why in sorted(guard.items()):
            print(f"  GUARD {k[0]} {k[1]} -- {why}")
        for k in cleared[:20]: print(f"  CLEARED {k[0]} {k[1]}")
        for k in unmeasured[:20]: print(f"  NOT MEASURED {k[0]} {k[1]} -- its package is not in this scan; measure it where it lives")
        if len(unmeasured) > 20: print(f"  ... and {len(unmeasured) - 20} more not measured")
    if lst and reg is None:
        for rule, p in sorted(viol): print(f"  {rule} {p} -- {viol[(rule, p)]}")
    if new:
        for rule, p in new: print(f"  {'NEW ' if reg_path else ''}{rule} {p} -- {viol[(rule, p)]}")
    if reg is not None:
        if guard:
            print("VERDICT: FAIL -- a package's own register tried to widen what the governance aggregate records")
            return 1
        print("VERDICT: " + ("FAIL -- violations outside the register" if new else "PASS -- no violation outside the register"))
        return 1 if new else 0
    print("VERDICT: " + ("VIOLATIONS" if viol else "CLEAN") + " (no register given)")
    return 1 if viol else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
