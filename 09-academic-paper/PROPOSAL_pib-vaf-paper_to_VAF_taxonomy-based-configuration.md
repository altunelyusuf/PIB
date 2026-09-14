# Proposal to the VAF lineage (altunelyusuf/VAF)

**From:** pib-vaf academic paper session (a distinct thread from both HUB PIB and the VAF-maintaining
session; this thread does not own VAF or PIB, and files this as a proposal per B1, not an edit).
**To:** altunelyusuf/VAF — filed in **VAF's own** `07-handover-inbox/pending/`.
**Date:** 2026-09-14
**Status:** proposal only, unimplemented and untested. Nothing in VAF was modified from this side.

**Context for the owner:** this idea originated from the owner's own direct question about profile
proliferation (as more profiles accumulate, it becomes hard to distinguish and recognize recurring
patterns among them) and a concrete motivating case (a project-proposal template needing to categorize
project types with common, distinguishing, and dependent features). It was developed through discussion
in the paper thread, grounded against real literature, but has not been built or tested anywhere. It is
offered here as a candidate extension to VAF's own theory, for the owning session to accept, reject, or
revise.

---

## The proposal: Taxonomy-Based (Profile Family) Configuration

**Motivation.** VAF already defines a profile as a specific binding of the algebra's elements,
attributes, and constraints to one concrete use (the software profile realized by the thesis; the
integration profile realized by PIB). As the number of realized profiles grows, two needs recur: (1)
distinguishing genuinely different profiles from ones that are the same underlying pattern with
different labels, and (2) recognizing and reusing structure that repeats across profiles rather than
re-deriving it each time. Neither need is met by the current, flat treatment of a profile as an
independent, unrelated tuple.

**The formal sketch.** A profile family `F` is either:
- a base profile `P = <E_P, C_P, A_P>` (the existing definition, unchanged), or
- a tuple `F = <E_F, C_F, {F_1, ..., F_n}>`, where `E_F` and `C_F` are the family's own closed
  (inherited-by-all) element and constraint sets, and each `F_i` is itself a profile family, subject to
  `E_F ⊆ E_{F_i}` and `C_F ⊆ C_{F_i}` for every `i` — nothing in a parent's closed part is ever dropped
  or overridden by a child.

Discrimination among `{F_1, ..., F_n}` for a concrete case is proposed to use the algebra's own existing
Exclusive or Or operators over a designated type element — no new operator is introduced. Admissibility
for the whole family is proposed as: a concrete instance is admissible iff there exists a root-to-leaf
path whose accumulated constraint sets (`C_F ∪ C_{F_i} ∪ ... ∪ C_P`) the instance satisfies.

**The one genuinely new piece of machinery, named plainly:** not a seventh operator, but a composition
rule for how constraint sets accumulate across levels. This needs a real soundness check this proposal
has not performed: if some `F_{i,j}` adds a constraint contradicting an ancestor's (e.g. a descendant
marks Optional something an ancestor marked Mandatory), the accumulated set becomes unsatisfiable and no
leaf under that path is ever admissible — silently, unless checked for explicitly at every depth.

**Real, external grounding, not invented from nothing:**
- Gurov, D., Østvold, B. M., & Schaefer, I. (2012). "A Hierarchical Variability Model for Software
  Product Lines." ISoLA 2011 post-proceedings, CCIS vol. 336, pp. 181–199, Springer.
  DOI: 10.1007/978-3-642-34781-8_15. Establishes the recursive principle directly: "a variant is again
  a hierarchical variability model, leading to a hierarchical structure."
- de Lara, J., & Guerra, E. (2020). "Multi-level Model Product Lines." FASE 2020, LNCS vol. 12076,
  pp. 161–181, Springer. DOI: 10.1007/978-3-030-45234-6_8. Supplies the closed/open variability split
  this proposal's `E_F`/`C_F` versus each `F_i`'s own addition maps onto directly.
- Haber, A., Rendel, H., Rumpe, B., Schaefer, I., & van der Linden, F. (2011). "Hierarchical Variability
  Modeling for Software Architectures." SPLC 2011, IEEE, pp. 150–159. Confirms this has already been
  done for component-based architectures specifically, closer to VAF's own domain than pure language
  engineering.

## What this session is explicitly not claiming

This session has not built the consistency check the sketch itself identifies as necessary, has not
tested the recursive definition against a real multi-level example (the project-proposal case that
motivated it remains hypothetical), and has not verified the discrimination mechanism (Exclusive/Or
over a type element) against any real profile pair. The paper this session is developing will not state
this as an implemented result unless the owning session builds and verifies it; until then, if it
appears in the paper at all, it will be stated as motivated future work, explicitly unproven.

## Requested disposition

Standard proposal handling: accept, reject, or revise, per the owning session's own judgment of fit
against VAF's real roadmap and the still-unresolved operator-count question (Finding 2 of the prior
proposal filed this same session, `PROPOSAL_pib-vaf-paper_to_VAF_operator-classification-and-count.md`).
If accepted, this session would ask to be informed so the paper's own treatment can be updated from
"motivated" to "demonstrated," with a citation back to whichever VAF release implements and verifies it.
