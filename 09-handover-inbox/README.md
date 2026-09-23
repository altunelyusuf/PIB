# PIB handover inbox — for parallel sessions

This is where a finding, proposal or contract **for PIB** is filed. It follows the ecosystem's standard
layout — `pending/`, `accepted/`, `rejected/`, `deferred/`, and a plain-text `HANDOVER_LOG.md` — because
this is bookkeeping ("has it been looked at, with what outcome"), not domain knowledge, and deliberately
not RDF.

`pending/` is read at the start of every PIB session, as a standing ceremony step. Nothing arrives
automatically: an item is placed here by its sender, by the owner, or archived here by a session that
received it elsewhere.

## Filing a handover for PIB

One Markdown file in `pending/`, named so the direction is readable without opening it:

```
<KIND>_<from>_to_PIB_<short-subject>_v<major>_<minor>_<patch>.md
```

`KIND` is what you are sending — `PROPOSAL`, `FINDING`, `HANDOVER`, `NOTE`, `CORRECTION`, `REPLY`. Say in
the document: what you found or want, the evidence, and what you are asking PIB to do. If you are
reporting a defect, say how you verified it — PIB will re-derive it before acting, and stating your method
makes that cheap rather than duplicated.

## What PIB does with it

PIB verifies the claim against real artifacts, then moves the file to `accepted/`, `rejected/` or
`deferred/` and appends a line to `HANDOVER_LOG.md`. **Every line states the verification actually
performed**, not how persuasive the document read: a disposition is itself a claim, and an unverifiable
disposition is worth nothing. A rejection says what was checked and why it did not hold — PIB has had one
of its own findings correctly rejected this way, which is the mechanism working, not failing.

`03-tooling/handover_inbox_check_v1_0_0.py` enforces the parts a reader cannot see for themselves: that
the four states exist, that **every dispositioned item has a log line**, and that every outgoing item says
why it was not filed in its target's inbox.

## Direction — where a proposal belongs

A proposal arriving **at** PIB goes here. A proposal PIB sends **to** another package goes into **that
package's own inbox**, where one exists. Leaving it in PIB's own documentation for the target to discover
by chance is the weaker path, and is the fallback rather than the default.

`outgoing/` is that fallback, and only that: it holds items PIB has written for a package whose inbox it
cannot reach. Each such item must say why it is held rather than filed, and it is routed as soon as a real
inbox exists. It is not a parking place for proposals PIB could have delivered.

## What PIB will not do with what you file

Registering, proposing or editing **on your behalf**. A handover is a claim PIB verifies and answers; it is
not permission to change your package's content. Findings about your ontology go back to you.
