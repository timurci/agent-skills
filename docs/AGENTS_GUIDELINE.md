# How to Write a Good AGENTS.md

An `AGENTS.md` file is the **operating manual for AI coding agents** (Claude, Codex, Cursor, etc.) working inside your repository. Think of it as the onboarding doc you would write for a very capable but context-free new engineer: precise, actionable, and never ambiguous.

---

## Purpose

Agents read `AGENTS.md` at the start of every session. Its job is to:

1. Tell the agent **what this project is** and what it should produce.
2. Tell the agent **how to work** — commands, conventions, constraints.
3. Tell the agent **what not to do** — common mistakes, off-limits patterns.
4. Give the agent **enough context** to make locally correct decisions without asking.

---

## Core Principles for Writing One

### 1. Be imperative, not descriptive
Write instructions, not narration.

| ❌ Weak | ✅ Strong |
|---|---|
| "The project uses ruff for formatting." | "Always run `uv run ruff format` before committing." |
| "Tests exist in the tests/ folder." | "After every code change, run `uv run pytest` and fix any failures before finishing." |

### 2. Prefer exact commands over prose
Every task the agent might perform should have a copy-pasteable command. Ambiguity about *how* to do something causes hallucinated commands.

### 3. Layer from general to specific
Structure: project overview → environment setup → conventions → workflow → constraints. Agents scan top-to-bottom; front-load the most load-bearing decisions.

### 4. Encode your non-obvious decisions
Obvious things ("don't break syntax") don't need to be said. Non-obvious things ("we never raise bare `Exception`, always use domain-specific error classes") absolutely do.

### 5. Keep it honest and current
A stale `AGENTS.md` is worse than none. If the file says `pytest` but you've migrated to `unittest`, the agent will silently run the wrong thing. Treat it like code — update it when the project changes.

### 6. Be explicit about quality gates
The agent must know what "done" means. List every check that must pass before a change is considered complete.

### 7. Scope to what changes
Don't pad with things that never affect a coding session (e.g., deployment docs, org chart). Every line should answer the question: *"Would this change how the agent writes or checks code?"*

---

## What to Include

| Section | Purpose | Required? |
|---|---|---|
| **Project overview** | One-paragraph orientation | Yes |
| **Tech stack** | Languages, frameworks, key libraries | Yes |
| **Environment setup** | How to install deps and run the project | Yes |
| **Linting / formatting** | Exact commands, when to run them | Yes |
| **Type checking** | Tool + command | Yes if used |
| **Testing** | Command, coverage expectations, test conventions | Yes |
| **Pre-commit hooks** | How to install and run | Yes if used |
| **Project structure** | Directory map + what lives where | Yes |
| **Architecture / design notes** | Layering rules, dependency direction, key invariants | For non-trivial projects |
| **Code conventions** | Naming, patterns to use/avoid, style decisions not caught by linters | Yes |
| **Git / PR conventions** | Branch naming, commit style, PR scope | Optional but useful |
| **What NOT to do** | Explicit anti-patterns, forbidden patterns | Highly recommended |
| **Known gotchas** | Non-obvious env issues, quirks | As needed |

---

## What to Leave Out

- **Documentation for humans only** — deployment runbooks, org context, roadmap.
- **Things enforced by tooling** — if ruff catches it, you don't need to describe it.
- **Speculation** — don't document intended future architecture that doesn't exist yet.
- **Redundant repetition** — say each convention once, clearly.

---

## Placement

| File | Scope |
|---|---|
| `/AGENTS.md` | Entire repo |
| `/backend/AGENTS.md` | Only the `backend/` subtree |
| `/scripts/AGENTS.md` | Only the `scripts/` subtree |

Agents typically merge parent + subdirectory files. Use subdirectory files to override or extend, not repeat.

---

## Checklist Before Publishing

- [ ] Every command is copy-pasteable and tested
- [ ] Quality gates are explicit (what must pass = "done")
- [ ] Architecture layering rules are stated if the project has them
- [ ] Forbidden patterns are listed
- [ ] The file is ≤ ~200 lines (if longer, consider subdirectory files)
- [ ] No stale or aspirational information
