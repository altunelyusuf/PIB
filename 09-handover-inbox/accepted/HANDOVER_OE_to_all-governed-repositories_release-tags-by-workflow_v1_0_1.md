# Handover — OEE → every session and repository governed by OEE: release tags are made by a workflow (v1.0.1)

**From:** `oee-governance-session-3`, 2026-10-05.
**Changes from v1.0.0:** the addressee line no longer names any repository (a broadcast must not name one session's repository to the others). Nothing else changed; the procedure and the workflow text are as v1.0.0.
**To:** every session that publishes a governed package, whether the package sits in the
`altunelyusuf/Ontologies` monorepo or in a repository of its own (a course repository, an administrative
repository, any later one).
**Where it lives:** filed once, here. It is not pushed into each repository from OEE's session; that
is not the practice followed so far. A session picks it up from the monorepo (`oe-pack/04-documentation/handovers/`)
or the owner passes it on. A session that reads it should say so in its own next handover.

Everything below was measured on 2026-10-05. **Re-derive every claim on the bytes before acting on it.**

---

## 1. What changed and why

A session's git proxy refuses tag pushes: `git push origin <tag>` returns HTTP 403 and "unexpected
disconnect", while branch pushes to the same repository succeed. The proxy's own status endpoint records no
denial, and its documentation says a 403 is an organization policy that must be reported, not worked
around. So no session in this environment can push a release tag, in any repository. The release is the
commit; the tag is only its label. The label is now made on GitHub's side, by a workflow, after the push.

## 2. If your package is in the `altunelyusuf/Ontologies` monorepo

Nothing to install. The workflow `.github/workflows/oe-tags.yml` there runs on every push to `main`,
whoever pushes, and tags the current version of every top-level package folder at the first commit whose
`VERSION.txt` held that version. It has already created tags this way (for example `oe-method-v2.34.1`,
`oe-pack-v20.89.9`).

What to do each time you publish:

1. Publish as usual. The publisher will print a notice that it could not push the tag. That is expected.
2. About a minute later, list the remote's tags for your package and confirm the tag for your version
   exists and points at your commit (`git ls-remote --tags origin 'refs/tags/<package>-v<version>*'`; the line
   ending in `^{}` is the commit). Check the remote in the same turn you report it; do not repeat an earlier turn's result.
3. If it is missing, open the repository's Actions tab, choose "OE tags", then "Run workflow", and give your
   package folder and version. This is also how an older version is backfilled. A push that carries two new
   versions of one package tags only the later one; the earlier needs this manual run.
4. If the run reports that a tag exists at a different commit, **do not move the tag**. The workflow never
   does, on purpose. Report it to OEE as a finding with both commits.

## 3. If your package is in a repository of its own

The monorepo workflow looks one folder down, so it does not fit a package at the repository root. The
variant in section 7 does, and it was tested (section 5). Add it once per repository; it then serves every
session that publishes there.

1. **Read your repository's existing tags first** (`git ls-remote --tags origin | head`). The prefix in front of
   `-v<version>` is your `TAG_PREFIX`. Do not invent one; a different prefix would start a second series of tags.
2. **Add the file** from section 7 as `.github/workflows/oe-tags.yml` and set the single `TAG_PREFIX` line.
   The file refuses to run while that line still holds its placeholder, so a forgotten edit fails loudly.
   The workflow asks for write permission inside the file itself, so no repository setting needs to change.
3. **Check that no rule restricts tag creation.** In the repository's Settings, open Rules, then Rulesets. A ruleset
   that targets branches (as the monorepo's `Governance` ruleset does, on `main` only) does not matter. One that
   targets tags would; add GitHub Actions to its bypass list, or report it.
4. **Commit it with a message that names its source**: the monorepo file `oe-tags.yml` at the commit you copied
   from, adapted to a root `VERSION.txt`. A copy is a deployment, and copies drift; the source of truth for the rules
   is the monorepo file.
5. **Push, then verify on the remote** as in section 2 step 2. If the current version is already tagged at its
   commit, the run reports "ok" and changes nothing; that is also a pass.
6. **Backfill** an older version through the manual run with its version number.

## 4. Rules that continue while a repository is governed by OEE

- **Do not push tags from a session environment, and do not look for another route.** The refusal is a policy;
  working around it is the failure the proxy's own documentation names. The workflow is the route.
- **Never move or delete a release tag to make a check pass.** A mismatch is a finding for OEE.
- **Check the published state, not the run.** The publisher printing a clean ending, or a workflow run being green,
  is not the tag existing at the right commit; list the remote.
- **The commit is the release.** A missing tag never blocks publishing, and a published commit is never re-published to get a tag.
- **When OEE changes the monorepo workflow**, it files a handover. Compare your copy with it before copying again, and keep your `TAG_PREFIX`.
- **Setup facts for a session in this environment** (they cost time): the session's GitHub access comes from attaching
  the repository to the session, not from a token (the environment's own `GH_TOKEN` was invalid, and the GitHub web pages are not
  fetchable); clones are shallow, so deepen history before counting commits or tags; do not run the bootstrap's `chmod +x`,
  which turns tracked scripts into mode-only changes the session's stop hook then asks you to commit.

## 5. What was verified, and what was not

Verified (monorepo version, before and after it went live):
- The workflow's own code, run with a dry-run switch against the real history, agreed with all 12 tags that already
  existed (0 mismatches), found `4dc48ac` as the commit for `oe-method` 2.34.0, and refused a planted wrong-commit tag, a
  version that never existed, and a version without a package.
- After the push, GitHub created exactly the six tags predicted, each at the predicted commit; a later push created `oe-pack-v20.89.9`; the
  owner's manual run created `oe-method-v2.34.0` at `4dc48ac`. The run after moving `actions/checkout` from v4 to v5 succeeded with no Node 20 notice.
- Root-layout variant (section 7), on a synthetic repository with a local bare remote, seven cases: placeholder prefix refused (exit 1);
  an existing correct tag left alone (exit 0); an existing tag at the wrong commit refused and not moved (exit 1); an unseen version
  refused (exit 1); the current version dry-run at its first-appearance commit and not at a later commit with the same version; a real
  create and push, after which the remote held the new tag and the wrong tag was still where it was; a second real run changed nothing (exit 0).

Not verified:
- The root-layout variant has never run on GitHub. No repository with a package at its root was attached to the session. Expect to
  watch its first run, and report anything that differs from the above.
- Whether the same tag refusal affects those repositories was not tested; the proxy rule itself cannot be read from a session.
  The variant is harmless if it does not.
- GitHub has announced that `ubuntu-latest` becomes Ubuntu 26 on 2026-10-19. These workflows need only git and bash, so they are not exposed.

## 6. What stays with OEE, not with you

Folding this procedure into the next bootstrap version so that every session receives it without a handover; changing the publisher's
notice so it says the workflow creates the tag; and the CI file `gates.yml`, which still carries `actions/checkout@v4` and
`ubuntu-latest` and is not an OEE-authored file as far as the history shows.

## 7. The workflow for a package at the repository root (tested; set `TAG_PREFIX`)

```yaml
name: OE tags
# Release tag for a repository that holds ONE governed package at its root (OE_PACKAGE_AT_ROOT).
# Copy of the monorepo workflow `.github/workflows/oe-tags.yml` in altunelyusuf/Ontologies, adapted to
# a root VERSION.txt. Source of truth for the rules is that file; a copy here is a deployment, so
# record the Ontologies commit it was taken from in the commit message that adds it.
#
# EDIT ONE LINE: TAG_PREFIX below must be exactly the prefix this repository's existing tags use
# (read it first:  git ls-remote --tags origin | head). New tags are  <TAG_PREFIX>-v<version>.
#
# Rules (identical to the monorepo workflow):
#   - a missing tag is created at the first commit whose VERSION.txt held that version (annotated);
#   - an existing tag at that commit is left alone;
#   - an existing tag elsewhere is NEVER moved: warning, and the run fails after finishing;
#   - a version that never appeared in VERSION.txt history fails the run.
# Manual run (Actions tab -> "OE tags" -> Run workflow): empty = the current version; or give an
# older version to backfill its tag.
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      version:
        description: 'Tag this version instead of the current one (empty = current)'
        required: false
        default: ''
concurrency:
  group: oe-tags
  cancel-in-progress: false
permissions:
  contents: write
env:
  TAG_PREFIX: CHANGE-ME-to-the-prefix-of-the-existing-tags
jobs:
  tags:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - name: Create the missing release tag
        env:
          INPUT_VERSION: ${{ github.event.inputs.version }}
        run: |
          set -uo pipefail
          DRY="${DRY_RUN:-0}"
          if [ "${TAG_PREFIX}" = "CHANGE-ME-to-the-prefix-of-the-existing-tags" ] || [ -z "${TAG_PREFIX}" ]; then
            echo "::error::TAG_PREFIX has not been set to this repository's tag prefix"; exit 1
          fi
          [ -f VERSION.txt ] || { echo "::error::no VERSION.txt at the repository root"; exit 1; }
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          ver="${INPUT_VERSION:-$(tr -d ' \n\r' < VERSION.txt)}"
          [ -n "$ver" ] || { echo "::error::empty version"; exit 1; }
          tag="${TAG_PREFIX}-v${ver}"
          commit=""
          for c in $(git log --reverse --format=%H -- VERSION.txt); do
            v="$(git show "$c:VERSION.txt" 2>/dev/null | tr -d ' \n\r' || true)"
            if [ "$v" = "$ver" ]; then commit="$c"; break; fi
          done
          if [ -z "$commit" ]; then
            echo "::error::$tag: version $ver never appeared in VERSION.txt history"; exit 1
          fi
          if have="$(git rev-parse -q --verify "refs/tags/${tag}^{commit}")"; then
            if [ "$have" = "$commit" ]; then
              echo "ok       $tag already at ${commit:0:7}"; exit 0
            fi
            echo "::error::$tag exists at ${have:0:7} but version $ver first appeared at ${commit:0:7}; not moved"
            exit 1
          fi
          if [ "$DRY" = "1" ]; then echo "would tag $tag at ${commit:0:7}"; exit 0; fi
          git tag -a "$tag" "$commit" -m "${TAG_PREFIX} v$ver"
          git push origin "refs/tags/$tag"
          echo "tagged   $tag at ${commit:0:7}"
```
