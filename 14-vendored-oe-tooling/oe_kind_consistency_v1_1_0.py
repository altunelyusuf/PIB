#!/usr/bin/env python3
"""oe_kind_consistency - a class's kind agrees with the kinds of its named parents (discipline v2.34.0, BP-D59).

  oe_kind_consistency_v1_1_0.py <root> [--baseline FILE] [--list] [--abox FILE]

A subclass link says that every instance of the child is an instance of the parent, so the kind of the child must be the kind of the parent or lie under it (skos:broader of the kinds, read from the newest oe-method/09-governance/oegov_abox_v*.ttl). A child of a process that is a document, a child of a software product that is a software system, a child of a value domain that is a set: each is a contradiction, and either the kind or the subclass link is wrong. A class or a parent with no kind is NOT MEASURED, never a violation. The classes and parents are read from every Turtle file of every living package that declares a class (the newest version of each; fixtures, the teaching exemplar, archives, vendored copies, registrant deposits, snapshots and the governance A-Box are not read), joined into one graph, so a link across files is measured. The baseline holds, per file, the number of violations; it may fall and never grow (exit 1 on growth). A scan with no kinds or no class is refused: a scan of nothing is not a pass."""
import glob, os, re, sys
import rdflib
from rdflib import RDF, RDFS, OWL, Namespace, URIRef
KB = Namespace("http://example.org/knowledge-base#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
def retired(p):
    # a package directory that holds RETIRED_v*.md is retired history: frozen, not living, not processed (owner ruling 2026-10-22: living repositories are enough)
    try: return any(re.match(r"RETIRED_v\d", f) for f in os.listdir(p))
    except OSError: return False
def vkey(p): return [int(x) for x in re.findall(r"\d+", os.path.basename(p))]
def living(root, aboxes):
    files = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not retired(os.path.join(dp, d)) and d not in (".git", "fixtures", "archive", "node_modules", "exemplar") and not any(w in d for w in ("vendored", "deposit", "snapshot"))]
        for f in sorted(fn):
            p = os.path.join(dp, f)
            if not f.endswith(".ttl") or (aboxes and os.path.abspath(p) == os.path.abspath(aboxes[-1])): continue
            t = open(p, encoding="utf-8", errors="ignore").read()
            if "owl:Class" in t or "hasClassKind" in t or "/2002/07/owl#Class" in t: files.append(p)
    key = lambda q: os.path.dirname(q) + os.path.basename(q).split("_v")[0]
    return sorted(set(max([q for q in files if key(q) == k], key=vkey) for k in set(map(key, files))))
def under(broader, a, b):
    seen = set(); st = [a]
    while st:
        x = st.pop()
        if x == b: return True
        for y in broader.get(x, ()):
            if y not in seen: seen.add(y); st.append(y)
    return False
def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 2
    root = argv[0]; base = None; lst = False; abox = None; i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--baseline": base = argv[i + 1]; i += 2
        elif a == "--list": lst = True; i += 1
        elif a == "--abox": abox = argv[i + 1]; i += 2
        else: print("REFUSED: unknown argument " + a, file=sys.stderr); return 2
    aboxes = sorted(glob.glob(os.path.join(root, "oe-method", "09-governance", "oegov_abox_v*.ttl")), key=vkey)
    if abox: aboxes = [abox]   # a package published from its own repository names the governance knowledge base it was given (--abox), since it has no oe-method folder
    if not aboxes: print("REFUSED: no knowledge-base A-Box found: a scan of nothing is not a pass", file=sys.stderr); return 2
    k = rdflib.Graph(); k.parse(aboxes[-1])
    broader = {}
    for a, b in k.subject_objects(SKOS.broader): broader.setdefault(a, set()).add(b)
    files = living(root, aboxes)
    if not files: print("REFUSED: no file that declares a class: a scan of nothing is not a pass", file=sys.stderr); return 2
    kind = {}; parents = {}; where = {}
    for p in files:
        g = rdflib.Graph(); g.parse(p)
        rel = re.sub(r"_v\d+_\d+_\d+", "", os.path.relpath(p, root))
        for c, kk in g.subject_objects(KB.hasClassKind): kind[c] = kk; where.setdefault(c, rel)
        for c, par in g.subject_objects(RDFS.subClassOf):
            if isinstance(c, URIRef) and isinstance(par, URIRef): parents.setdefault(c, set()).add(par); where.setdefault(c, rel)
    if not kind: print("REFUSED: no class carries a kind: a scan of nothing is not a pass", file=sys.stderr); return 2
    B = {}
    if base:
        for ln in open(base, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 2: B[f[0]] = int(f[1])
    bad = {}; measured = 0
    for c, ps in sorted(parents.items(), key=lambda x: str(x[0])):
        if c not in kind: continue
        for par in sorted(ps, key=str):
            if par not in kind: continue
            measured += 1
            if not under(broader, kind[c], kind[par]):
                bad.setdefault(where[c], []).append("%s (kind %s) is under %s (kind %s)" % (str(c).split("#")[-1], str(kind[c]).split("_")[-1], str(par).split("#")[-1], str(kind[par]).split("_")[-1]))
    grow = 0
    for rel in sorted(set(bad) | set(B)):
        n = len(bad.get(rel, [])); rec = B.get(rel, 0)
        if n or rec: print("%s%s: %d violation(s) (recorded %d)" % ("NEW  " if n > rec else "", rel, n, rec))
        if n > rec: grow += 1
        if lst:
            for x in bad.get(rel, []): print("    " + x)
    print("%d subclass link(s) measured between two classes that both carry a kind" % measured)
    if grow: print("VERDICT: FAIL -- %d file(s) beyond the baseline: the kind or the subclass link is wrong; a link of a case or a record to an activity is no subclass link (replace it by a link), do not edit the baseline to hide it" % grow); return 1
    print("VERDICT: PASS"); return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
