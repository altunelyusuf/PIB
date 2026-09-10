#!/usr/bin/env python3
"""
PIB Wiring Validator v1.0.0
===========================
Validates a profile-driven integration wiring against variant-algebra operator
constraints, using the PINNED Variant Algebra Framework as the formal engine
(loose dependency, loaded from a path — never copied — mirroring radar_rdodi_loader).

WHAT IT CHECKS (per profile):
  1. Every active `consumes` is matched by an active `produces` of the same Capability.
  2. Operator constraints hold (Mandatory / Optional / Exclusive / Or / Dependency / Repetition)
     — delegated to the VAF engine's `is_admissible` / `BruteForceBackend.enumerate`.
  3. Variation Capacity (count of admissible wirings) is reported.

WHAT IT DOES NOT CHECK:
  - Node self-coverage (DL-consistency + SHACL standalone) — that is the SEPARATE,
    profile-independent gate handled by self_coverage_checker_v1_0_0.py. A wiring is only
    adoptable if BOTH gates pass.

VAF PIN: Variant_Algebra_Framework_v1_0_0  (package SHA-256 7858339ee554f3307aa7945b…)
  core files: variant_enumerator_v2_0_0.py, variant_backends_v1_0_0.py,
              variant_dsl_parser_v1_0_0.py, variant_dsl_grammar_v1_0_0.lark
Set PIB_VAF_SRC to the framework's /src directory (default below = this session's path).
"""
from __future__ import annotations
import os, sys
from dataclasses import dataclass
from typing import Optional

_DEFAULT_VAF = "/home/claude/work/_new_vaf_fw/inner/variant_algebra_framework_v1_0_0/src"
VAF_SRC = os.environ.get("PIB_VAF_SRC", _DEFAULT_VAF)


def _load_vaf():
    """Load the pinned VAF engine as a dependency (not a copy)."""
    if VAF_SRC not in sys.path:
        sys.path.insert(0, VAF_SRC)
    # The shipped parser eager-loads its grammar at import; the real .lark ships in /src,
    # so this works against the full framework package (it does NOT against the sub-kits).
    from variant_dsl_parser_v1_0_0 import (Component, MandatoryStmt, OptionalStmt,
        ExclusiveStmt, OrStmt, DependencyStmt, RepetitionStmt)
    from variant_backends_v1_0_0 import BruteForceBackend
    from variant_enumerator_v2_0_0 import is_admissible
    return dict(Component=Component, Mandatory=MandatoryStmt, Optional=OptionalStmt,
                Exclusive=ExclusiveStmt, Or=OrStmt, Dependency=DependencyStmt,
                Repetition=RepetitionStmt, Backend=BruteForceBackend, is_admissible=is_admissible)


@dataclass
class WiringModel:
    """A profile's wiring expressed as variant-algebra features + operators.
       edges: feature names. mandatory/optional/exclusive_groups/or_groups/deps as per operators."""
    name: str
    mandatory: list
    optional: list
    exclusive_groups: list   # list[list[str]]
    or_groups: list          # list[list[str]]
    deps: list               # list[(antecedent, consequent)]


def to_component(m: WiringModel, vaf):
    stmts = []
    for f in m.mandatory: stmts.append(vaf["Mandatory"](feature=f, body=[]))
    for f in m.optional:  stmts.append(vaf["Optional"](feature=f, body=[]))
    for g in m.exclusive_groups: stmts.append(vaf["Exclusive"](members=list(g)))
    for g in m.or_groups:        stmts.append(vaf["Or"](members=list(g)))
    for a, c in m.deps:          stmts.append(vaf["Dependency"](antecedent=a, consequent=c))
    return vaf["Component"](name=m.name, statements=stmts)


def validate(m: WiringModel) -> dict:
    vaf = _load_vaf()
    comp = to_component(m, vaf)
    out = vaf["Backend"]().enumerate(comp)
    variants = out[0] if isinstance(out, (list, tuple)) else out
    telemetry = out[1] if isinstance(out, (list, tuple)) and len(out) > 1 else None
    return {
        "profile": m.name,
        "variation_capacity": len(variants),          # count of admissible wirings
        "admissible_variants": [dict(sorted(v.counts.items())) for v in variants],
        "telemetry": str(telemetry) if telemetry else None,
        "engine": "Variant_Algebra_Framework_v1_0_0 (pinned, shipped BruteForceBackend)",
    }


def check_config(m: WiringModel, selected: dict) -> tuple[bool, str]:
    """Check ONE explicit wiring configuration (selected: feature->0/1) for admissibility."""
    vaf = _load_vaf()
    comp = to_component(m, vaf)
    ok = bool(vaf["is_admissible"](selected, comp))
    return ok, ("admissible" if ok else "rejected by operator constraints")


if __name__ == "__main__":
    # Self-test on the worked capstone wiring (matches example_capstone_profile_abox).
    m = WiringModel(
        name="CapstoneWiring",
        mandatory=["O4SDLC_produces_AD", "RADAR_consumes_AD"],
        optional=[],
        exclusive_groups=[["RADAR_measures", "PAMG_measures"]],
        or_groups=[["O4UCM_analysis", "O4DF_design"]],
        deps=[("RADAR_consumes_AD", "O4SDLC_produces_AD")],
    )
    r = validate(m)
    print(f"Variation Capacity (admissible wirings): {r['variation_capacity']}")
    print(f"engine: {r['engine']}")
    # targeted validity checks
    checks = [
        ({"O4SDLC_produces_AD":1,"RADAR_consumes_AD":1,"RADAR_measures":1,"PAMG_measures":0,"O4UCM_analysis":1,"O4DF_design":0}, True,  "good"),
        ({"O4SDLC_produces_AD":1,"RADAR_consumes_AD":1,"RADAR_measures":1,"PAMG_measures":1,"O4UCM_analysis":1,"O4DF_design":0}, False, "two measurers"),
        ({"O4SDLC_produces_AD":0,"RADAR_consumes_AD":1,"RADAR_measures":1,"PAMG_measures":0,"O4UCM_analysis":1,"O4DF_design":0}, False, "consume w/o produce"),
        ({"O4SDLC_produces_AD":1,"RADAR_consumes_AD":1,"RADAR_measures":1,"PAMG_measures":0,"O4UCM_analysis":0,"O4DF_design":0}, False, "no A&D source"),
    ]
    allok = True
    for sel, expect, desc in checks:
        ok, why = check_config(m, sel)
        passed = ok == expect
        allok &= passed
        print(f"  {'PASS' if passed else 'FAIL'}: {desc} -> {why}")
    sys.exit(0 if allok else 1)
