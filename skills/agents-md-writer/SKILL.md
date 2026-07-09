---
name: agents-md-writer
description: Use when creating, reviewing, or improving an AGENTS.md file for a repository.
---

# How to Write a Good AGENTS.md

An `AGENTS.md` is the operating manual for AI coding agents in a repository — what an agent reads at the start of every session to learn what the project is, how to work in it, and what not to do, with enough context to make locally correct decisions without asking.

Every line must be **grounded**: traceable to a repository fact or a confirmed user decision, never invented or aspirational.

## Process

1. **Ground the file.** Establish the source of truth before writing:
   - **Existing repository** — inspect manifests, configs, tests, scripts, and CI; derive commands, tooling, structure, and conventions from what exists.
   - **Fresh or skeletal repository** — use the user's project spec as the source of truth. Write for the intended project, but do not claim commands, files, or tooling exist unless they do.
   - **Mixed signals** — where repo contents conflict with the user's description, treat the repo as current fact and the description as intended direction. Ask before encoding future intentions as present-tense instructions.

   For greenfield work, separate confirmed decisions from unresolved ones. If the user delegates the choice, pick simple conventional defaults and encode them directly; if not, ask before inventing tooling, directory structure, quality gates, or commands.

   *Done when every instruction traces to a repository fact or a confirmed user decision.*

2. **Write the sections.** Cover every applicable section in the table below, following the writing rules. Each section is imperative and gives exact, copy-pasteable commands.

   *Done when every applicable section is present, imperative, and grounded.*

3. **Verify.** Run the completion check.

   *Done when the completion check passes.*

## Writing rules

- **Be imperative, not descriptive.** Write instructions, never narration. "Always run `uv run ruff format` before committing" — not "The project uses ruff for formatting."
- **Prefer exact commands over prose.** Give a copy-pasteable command for every task; never describe a command in prose when an exact command exists.
- **Layer general to specific.** Project overview → environment setup → conventions → workflow → constraints. Agents scan top-to-bottom, so front-load the most load-bearing decisions.
- **Encode only non-obvious decisions.** Omit what the agent already knows ("don't break syntax") and what tooling enforces (if ruff catches it, don't describe it). Keep the non-obvious, like "never raise bare `Exception`; use domain-specific error classes."
- **Define "done" explicitly.** List every check that must pass before a change is complete; that list is the quality gate.
- **Scope to what changes.** Omit anything that doesn't affect how the agent writes or checks code — deployment runbooks, org charts, roadmaps. Ask of each line: "Would this change how the agent writes or checks code?"
- **Say each convention once.** One clear statement per rule, in its single home.

## Sections

| Section | Purpose | Required? |
|---|---|---|
| **Project overview** | One-paragraph orientation | Yes |
| **Tech stack** | Languages, frameworks, key libraries | Yes |
| **Environment setup** | How to install deps and run the project | Yes |
| **Linting / formatting** | Exact commands, when to run | Yes |
| **Type checking** | Tool + command | Yes if used |
| **Testing** | Command, coverage expectations, test conventions | Yes |
| **Pre-commit hooks** | How to install and run | Yes if used |
| **Project structure** | Directory map + what lives where | Yes |
| **Architecture / design notes** | Layering rules, dependency direction, key invariants | For non-trivial projects |
| **Code conventions** | Naming, patterns to use/avoid, style linters don't catch | Yes |
| **Git / PR conventions** | Branch naming, commit style, PR scope | Optional but useful |
| **What NOT to do** | Explicit anti-patterns, forbidden patterns | Highly recommended |
| **Known gotchas** | Non-obvious env issues, quirks | As needed |

## Placement

| File | Scope |
|---|---|
| `/AGENTS.md` | Entire repo |
| `/backend/AGENTS.md` | Only the `backend/` subtree |
| `/scripts/AGENTS.md` | Only the `scripts/` subtree |

Agents merge parent + subdirectory files. Use subdirectory files to override or extend, not repeat. Keep each file ≤ ~200 lines; split into subdirectory files when it grows past that.

## Relationship to README and CONTRIBUTING

| File | Audience | Content |
|---|---|---|
| `README.md` | Human contributors | Quick start, project description, contribution guidelines |
| `CONTRIBUTING.md` | Human contributors | Detailed process for submitting changes, code of conduct |
| `AGENTS.md` | AI agents | Exact commands, conventions, constraints, quality gates |

Never duplicate human-oriented content from `README.md` or `CONTRIBUTING.md` in `AGENTS.md`. Cross-reference them if an agent needs to know they exist.

## Reference defaults

For a Python project where the user asks for recommended defaults, read [`references/python-defaults.md`](references/python-defaults.md).

Defaults fill gaps only — they never override existing repository facts or explicit user choices.

## Completion check

Before finishing, confirm:

- [ ] Every instruction is **grounded** — traced to a repository fact or a confirmed user decision; no invented or aspirational content.
- [ ] Every applicable section in the table is present, imperative, and gives exact commands.
- [ ] No human-only content is duplicated from `README.md` or `CONTRIBUTING.md`.
- [ ] The file is ≤ ~200 lines, or split into subdirectory files.
