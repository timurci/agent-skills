---
name: review-additions
description: Review a git diff (unstaged, staged, a commit, or one branch against another) for net-new material that isn't needed, and say what to delete, reuse, inline, or shrink. Use when the user asks to review changes for bloat or scope creep, or to review just the docs or just the implementation of a change — even if they don't say additions.
---

# Review additions

Agents add and patch; they rarely delete or shrink. This review reads a diff for what was *added* and judges each addition: **delete**, **reuse**, **inline**, or **shrink**.

Replacements and in-place edits are not the target. A line that swaps an old line for a new one is normal work. What matters is net-new material: new files, definitions, parameters, branches, doc sections, comments. Report only; don't edit files unless asked.

## Inputs

All optional, any order:
- **Source**: `unstaged`, `staged`, a commit sha, or two branches/refs. Default: all uncommitted work; if the tree is clean, the current branch against the default branch.
- **Focus**: `docs`, `impl`, or both (default). Each is its own pass over the same diff, using the matching lens below.
- **Intent**: text, a file, or a PR description saying what was asked for.

## 1. Know what was asked

Find the intent before reading code, in this order: what the user passed, then `$(git rev-parse --git-dir)/change-intent.md` (usually `.git/change-intent.md`, written by the `change-intent` skill), then commit messages in range (`git log <range> --format=%B`). Restate the request in one line at the top of the report.

With no intent, say so and flag only what is wrong regardless of intent: dead code, duplicates, leftovers, narrating comments. Don't guess what was wanted, because a guess turns every unfamiliar addition into either a false alarm or a pass.

If a note exists but plainly describes a different change, say so and don't lean on it. If you wrote the change yourself in this session, review it as if you hadn't: the note and the diff are your only evidence that something belongs.

## 2. Get the diff

| Source | Command |
|---|---|
| unstaged | `git diff` |
| staged | `git diff --staged` |
| all uncommitted | `git diff HEAD` |
| one commit | `git show <sha>` (merge commit: `git diff <sha>^1 <sha>`) |
| branch vs base | `git diff <base>...<head>` |

Three dots show only what `head` added since it diverged; two dots would also show what `base` gained since. Default base: `git symbolic-ref --short refs/remotes/origin/HEAD`, else `main` or `master`.

`git diff` never shows untracked files, and new files are the purest additions. List them with `git ls-files --others --exclude-standard`, read each one (skip binaries and generated output), and count them as 100% added.

Triage before reading line by line. Add these flags to whichever command above you used:
- `--numstat` for per-file adds and removes.
- `-U0` for bare hunks. A header like `@@ -12,0 +13,8 @@` (old side `,0`) is a pure insertion, your main target. A header like `@@ -10,2 +10,30 @@` replaced 2 lines with 30; grown replacements deserve a look too.
- `-w` if re-indentation or reformatting drowns the change.

Skip lockfiles, generated code, snapshots and vendored files, but a lockfile change is a hint to check the manifest for a new dependency. Read the code around anything you flag: you can't tell from a hunk that a helper duplicates an existing one or that an old path is still live.

## 3. Judge each addition

Tie it to the intent. In a `change-intent` note, **Asked** and **Did** are the expected content; **Beyond the ask** is the author's own extras, so check those first; an addition named nowhere is undeclared, so flag it.

Then ask, in order, stopping at the first yes (earlier answers save more):
1. Does the request not call for it? **Delete.**
2. Does the repo, stdlib, or an existing dependency already do it? **Reuse.**
3. Is it used from one place only? **Inline.**
4. Is it bigger than it needs to be? **Shrink.**

Separately, for every addition that stays: does it replace something that is still there? That old thing goes under *Left behind* — the half agents skip: what the change made obsolete. Look for the old function, the old flag, the doc paragraph describing the previous behavior.

A large addition is fine when the request needs it. Tests that cover the request, validation at real system boundaries, and comments giving a *why* the code can't are all legitimate.

### Implementation lens
- **Parallel versions**: new code beside the code it replaces. The old function, flag, compat shim or deprecated alias kept alive without being asked.
- **Patching around**: a special-case branch, retry, sleep, fallback or adapter that works around a problem instead of fixing where it starts; a condition added only to make one case pass.
- **Reinvention**: a helper or class the repo, stdlib, or an existing dependency already provides. Search before accepting a new one.
- **One-use abstraction**: a wrapper, interface, factory or type with a single caller or implementation.
- **Speculative surface**: parameters, options, config keys, env vars, hooks, extension points nobody asked for; defaults that are never varied.
- **Defensive excess**: `except: pass`, null checks for states that can't occur, validation repeated at every layer, `or default` that hides errors.
- **Leftovers**: debug prints, commented-out code, unused imports and variables, stray TODOs.
- **New files and dependencies**: a module where an edit would do; a package for a few lines of stdlib.
- **Tests**: near-duplicate cases that one parametrized test covers, tests that mirror the implementation or only assert mocks were called, tests edited to pass instead of the code fixed.
- **Scope creep**: refactors, renames, formatting or fixes unrelated to the request.

### Docs lens
Plain docs (`.md`, `.rst`, `.txt`):
- **Docs nobody asked for**: a new summary, notes, design or changes file.
- **Restating**: sections that repeat the code, `--help`, or another doc; parameter tables that mirror a signature.
- **Change narration**: "now", "previously", "we changed". Docs describe the current state; history belongs in the commit.
- **Padding**: marketing tone, emoji headers, exhaustive feature lists, a tutorial where one example would do.
- **New beside stale**: behavior changed, but the old statement was left standing and a new section added next to it.

In-code docs (comments, docstrings):
- **Narration**: comments that say what the code plainly does, or describe the change ("added for X", "fixed", "new").
- **Boilerplate docstrings**: Args/Returns that repeat the name and type hints, especially on private or trivial functions. Match the codebase: if neighbors have none, new ones are noise; if lint requires them, they're required.
- **Clutter**: commented-out code, banner comments, TODOs with nothing actionable.
- Keep comments that give a *why* the code can't: a constraint, a workaround and its reason, an invariant.

## 4. Report

Keep it short. Order findings by lines saved, merge similar ones, skip style nitpicks, and stop at about ten. If the diff is clean, say so in a line; padding the report defeats its purpose.

```
## Additions review: <source>, <impl | docs | both>
Request: <one line, and where it came from; or "none found">
Size: +A / -D across F files (N new). Could drop roughly K lines.

### Cut or shrink
1. `path:12-48` (+37): <what was added>. <why it isn't needed>. -> delete | reuse `fn` (path:line) | inline into <caller> | shrink to ~N lines

### Left behind
- `path:line`: <old code or doc this change made dead or false, which should now go>

### Questions for the author
- `path:line`: <addition you couldn't tie to the request, or something Asked/Did claims that the diff doesn't show>
```
