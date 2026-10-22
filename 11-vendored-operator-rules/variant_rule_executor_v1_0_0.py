"""Runs SHACL-AF SPARQL rules on Oxigraph (VAF-WI-100).

The rules stay in the ontology's rule files; this module only executes them. Each sh:SPARQLRule's CONSTRUCT becomes
a SPARQL update, INSERT { template } WHERE { focus-node pattern . body }, with $this joined from the shape's targets
(sh:targetClass, sh:targetSubjectsOf). Rules run by sh:order stratum: all rules of the lowest order until the store
stops growing, then the next order. pySHACL's iterate_rules gives the same fixpoint on monotone rules but took 56 s
for eight features where this takes 0.2 s (VAF-WI-100 measurement).
"""
from __future__ import annotations
import re
from itertools import groupby

import rdflib
import pyoxigraph as ox

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def _prefixes(shapes: rdflib.Graph, rule) -> str:
    out = {}
    for holder in shapes.objects(rule, SH.prefixes):
        for d in shapes.objects(holder, SH.declare):
            out[str(shapes.value(d, SH.prefix))] = str(shapes.value(d, SH.namespace))
    return "".join(f"PREFIX {p}: <{n}>\n" for p, n in sorted(out.items()))


def _focus(shapes: rdflib.Graph, shape) -> str:
    alts = [f"{{ ?this a <{c}> }}" for c in shapes.objects(shape, SH.targetClass)]
    alts += [f"{{ ?this <{p}> ?_focusObject }}" for p in shapes.objects(shape, SH.targetSubjectsOf)]
    if not alts:
        raise ValueError(f"shape {shape} has a rule but no target this executor supports")
    return "SELECT DISTINCT ?this WHERE { " + " UNION ".join(alts) + " }"


def compile_rules(shapes: rdflib.Graph) -> list[tuple[float, str, str]]:
    """(order, shape, SPARQL update) for every SPARQLRule, sorted by order."""
    rules = []
    for shape in set(shapes.subjects(SH.rule, None)):
        for r in shapes.objects(shape, SH.rule):
            q = str(shapes.value(r, SH.construct))
            m = re.search(r"CONSTRUCT\s*\{(.*?)\}\s*WHERE\s*\{(.*)\}\s*$", q, re.S)
            if not m:
                raise ValueError(f"rule of {shape} is not CONSTRUCT {{ }} WHERE {{ }}")
            tmpl, body = (x.replace("$this", "?this") for x in m.groups())
            inline = "".join(line + "\n" for line in re.findall(r"^\s*PREFIX[^\n]*", q, re.M))
            upd = (f"{_prefixes(shapes, r)}{inline}INSERT {{ {tmpl} }}\n"
                   f"WHERE {{ {{ {_focus(shapes, shape)} }}\n{body} }}")
            rules.append((float(shapes.value(r, SH.order) or 0), str(shape), upd))
    return sorted(rules)


def run(store: ox.Store, rules, max_rounds: int = 100000) -> dict:
    """Run the rules stratum by stratum to a fixpoint. Returns the rounds each stratum took."""
    rounds = {}
    for order, group in groupby(rules, key=lambda r: r[0]):
        group = list(group)
        for n in range(1, max_rounds + 1):
            before = len(store)
            for _, _, update in group:
                store.update(update)
            if len(store) == before:
                rounds[order] = n
                break
        else:
            raise RuntimeError(f"stratum {order} reached no fixpoint in {max_rounds} rounds")
    return rounds
