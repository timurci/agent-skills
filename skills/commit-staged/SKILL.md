---
name: commit-staged
description: Commit the currently staged files with a conventional commit message.
disable-model-invocation: true
allowed-tools: Bash(git diff --staged:*), Bash(git log:*), Bash(git commit:*)
---

# commit-staged

## Steps

1. Run `git diff --staged` to see what is staged.
2. If nothing is staged, tell the user and stop.
3. Run `git log -n 5 --oneline` to match the repo's scope naming and style.
4. Write the commit message following the rules below.
5. Run `git commit -m "<subject>"` (add a second `-m "<body>"` only if a body is warranted).
6. Report the resulting commit hash and subject in one line.

## Message format

```
<type>(<optional scope>): <subject>

<optional body>

<optional BREAKING CHANGE: footer>
```

**Types:** `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `revert`.

- Pick the type that describes the dominant change. If the changes are mixed, choose the one with the greatest impact.
- Add `!` after the type/scope (e.g. `feat(api)!:`) and a `BREAKING CHANGE:` footer if the change breaks backwards compatibility.

## Content rules

- **High-level only.** Describe the change's effect, not its implementation.
- Subject line: imperative mood, lowercase, no trailing period, 72 characters or fewer.
- Do not narrate minor changes (formatting, renames, import tweaks) unless they are the whole commit.
- Include a body only when the subject cannot capture the change. Keep it to 1-3 short lines or bullets, each describing a major outcome or the reason for the change.
- Write the message as a human contributor would, and add co-author trailers only if the user asks.

## Examples

```
feat(auth): add OAuth login with Google
```
```
fix(checkout): prevent duplicate orders on retry
```
```
refactor(api): split request handling into separate modules

Separates validation, routing, and response formatting for easier testing.
```

## Constraints

- Commit only what is already staged; never stage, amend, or push. Leave unstaged changes untouched.
- Never use `--no-verify`. If a hook fails, report the failure and stop.
