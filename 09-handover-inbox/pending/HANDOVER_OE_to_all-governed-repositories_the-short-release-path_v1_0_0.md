# Handover — OEE → every session and repository governed by OEE: the release path is shorter, the checks are the same (v1.0.0)

**From:** `oee-governance-session-3`, 2026-10-07.
**To:** every session that publishes a governed package, in the `altunelyusuf/Ontologies` monorepo or in a repository of its own.
**Where it lives:** filed once, here, as the release-tag notice was; a session picks it up from the monorepo (`oe-pack/04-documentation/handovers/`) or the owner passes it on. A session that reads it should say so in its own next handover.
**What you must do:** nothing is mandatory. If a release of yours has been slow, use the tools below.

Everything below was measured on 2026-10-07. **Re-derive every claim on the bytes before acting on it.**

## 1. What changed

On the owner's direction to shorten long runs without lowering a standard, the OE tooling now has one command for the whole release: package gates, manifest, the publisher's dry-run and, with `--publish`, the publish and the wait for CI and the tag.

```
export OE_SESSION=<your session name>      # and GH_TOKEN in the environment
python3 repo-tooling/oe_release_v*.py <stage> <package-slug>              # gates, manifest, dry-run
python3 repo-tooling/oe_release_v*.py <stage> <package-slug> --publish
```

The publisher refuses everything it refused before. What went: the private manifest script, the stowaway bytecode, the deletion list worked out by trial (the tool writes the list the guard found for you to read and accept by naming it), and the polling for CI. One page says how it works and how to clear each refusal: `oe-pack/04-documentation/OE_RELEASE_PATH_v1_0_0.md`.

## 2. Eight run-length rules

The discipline (v2.16.0) now carries rules R1 to R8 against long runs, each saying whether a gate enforces it or it is advice. The ones that help most: run the dry-run as soon as the stage exists, not at the end (R2); the same refusal twice means the cause is not known, so write it down before the third run (R3, enforced by the tool); a step done by hand twice becomes a tool (R4).

## 3. If you have your own repository

The tools live in `repo-tooling` of the monorepo. A repository of its own gets them the way it gets the publisher; if that is unclear to you, say so in your own handover and we answer there.
