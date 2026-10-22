#!/usr/bin/env python3
"""oe_kind_coverage - every named class carries a kind and every object property a category (discipline v2.34.0, BP-D58 and BP-D59).

  oe_kind_coverage_v1_1_0.py <root> [--baseline FILE] [--decisions FILE] [--write-baseline FILE] [--list]

Scans every Turtle file of every living package that declares a class or an object property, whether or not it already declares a kind or a category (v1.1.0, owner\'s ruling of 2026-10-22: every ontology reaches the standard, not only the new terms), the newest version of each; fixtures, the teaching exemplar, archives, vendored copies, registrant deposits and snapshots of another package, and the governance A-Box are not read. A named class (an IRI declared there with a label or a definition) without hasClassKind, and an object property without hasRelationshipCategory (its own or its super-property's), is untyped. The baseline (a register with columns kind, subject, iri, definition, reason) holds the untyped terms that exist: it may fall and never grow. A new untyped term fails (NEW) unless the decisions ledger (columns iri, reason) records it with a reason (for example an umbrella of mixed members, which takes no kind). A term in the baseline that is now typed or gone is reported CLEARED (remove it from the register). A scan of nothing is not a pass."""
import glob, os, re, sys
import rdflib
from rdflib import RDF, RDFS, OWL, Namespace, URIRef
KB = Namespace("http://example.org/knowledge-base#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
def vkey(p): return [int(x) for x in re.findall(r"\d+", os.path.basename(p))]
def untyped(path):
    g = rdflib.Graph(); g.parse(path)
    out = []
    def declared(t): return (t, SKOS.definition, None) in g or (t, RDFS.label, None) in g
    for c in sorted(set(g.subjects(RDF.type, OWL.Class)), key=str):
        if isinstance(c, URIRef) and declared(c) and (c, KB.hasClassKind, None) not in g:
            d = g.value(c, SKOS.definition); out.append(("class", str(c), " ".join(str(d or "").split())[:110]))
    def cat(p, seen=()):
        if (p, KB.hasRelationshipCategory, None) in g: return True
        return any(cat(s, seen + (p,)) for s in g.objects(p, RDFS.subPropertyOf) if s not in seen)
    for p in sorted(set(g.subjects(RDF.type, OWL.ObjectProperty)), key=str):
        if isinstance(p, URIRef) and declared(p) and not cat(p):
            d = g.value(p, SKOS.definition); out.append(("property", str(p), " ".join(str(d or "").split())[:110]))
    return out
def table(path, col):
    R = {}
    if path:
        for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) > col: R[f[2] if col == 4 else f[0]] = f
    return R
def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 2
    root = argv[0]; base = dec = wb = None; lst = False; i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--baseline": base = argv[i + 1]; i += 2
        elif a == "--decisions": dec = argv[i + 1]; i += 2
        elif a == "--write-baseline": wb = argv[i + 1]; i += 2
        elif a == "--list": lst = True; i += 1
        else: print("REFUSED: unknown argument " + a, file=sys.stderr); return 2
    aboxes = sorted(glob.glob(os.path.join(root, "oe-method", "09-governance", "oegov_abox_v*.ttl")), key=vkey)
    files = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "fixtures", "archive", "node_modules", "exemplar") and not any(w in d for w in ("vendored", "deposit", "snapshot"))]
        for f in sorted(fn):
            p = os.path.join(dp, f)
            if not f.endswith(".ttl") or (aboxes and os.path.abspath(p) == os.path.abspath(aboxes[-1])): continue
            t = open(p, encoding="utf-8", errors="ignore").read()
            if "owl:Class" in t or "owl:ObjectProperty" in t or "hasClassKind" in t or "hasRelationshipCategory" in t or "/2002/07/owl#Class" in t or "/2002/07/owl#ObjectProperty" in t: files.append(p)
    key = lambda q: os.path.dirname(q) + os.path.basename(q).split("_v")[0]
    files = sorted(set(max([q for q in files if key(q) == k], key=vkey) for k in set(map(key, files))))
    if not files: print("REFUSED: no file that declares a class or an object property: a scan of nothing is not a pass", file=sys.stderr); return 2
    B = {}
    if base:
        for ln in open(base, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 3: B[f[2]] = f
    D = {}
    if dec:
        for ln in open(dec, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 2 and f[1].strip(): D[f[0]] = f[1]
    allrows = []; new = []
    for p in files:
        rel = re.sub(r"_v\d+_\d+_\d+", "", os.path.relpath(p, root))
        u = untyped(p)
        n = len(u); nn = [x for x in u if x[1] not in B and x[1] not in D]
        print("%s%s: %d untyped term(s), %d held by the baseline or a decision, %d new" % ("NEW  " if nn else "", rel, n, n - len(nn), len(nn)))
        allrows += [(rel,) + x for x in u]; new += nn
        if lst:
            for x in nn: print("    NEW %s %s -- %s" % x)
    present = {x[2] for x in allrows}
    cleared = [i for i in B if i not in present]
    for i in cleared: print("CLEARED (remove from the register): " + i)
    if wb:
        with open(wb, "w", encoding="utf-8") as fh:
            fh.write("kind\tsubject\tiri\tdefinition (start)\treason\n")
            for rel, k, iri, d in allrows:
                prev = B.get(iri); reason = prev[4] if prev and len(prev) > 4 else "held: no kind or category is stated yet"
                fh.write("%s\t%s\t%s\t%s\t%s\n" % (k, iri.split("/")[-1].split("#")[0], iri, d, reason))
    if new: print("VERDICT: FAIL -- %d new untyped term(s): give each its kind or category, or record the reason in the decisions ledger; do not edit the baseline to hide it" % len(new)); return 1
    print("VERDICT: PASS -- %d untyped term(s), all held; %d cleared" % (len(allrows), len(cleared))); return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
