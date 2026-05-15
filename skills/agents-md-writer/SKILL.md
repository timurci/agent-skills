---
name: agents-md-writer
description: Use when creating, reviewing, or improving AGENTS.md files that instruct AI coding agents how to work in a repository, including project commands, conventions, constraints, quality gates, and examples.
---

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

## Source of Truth

Before writing or updating `AGENTS.md`, determine which source of truth applies:

1. **Existing repository**: If implementation files, manifests, configs, tests, scripts, or CI files exist, inspect them first. Derive commands, tooling, structure, and conventions from the repository.
2. **Fresh or skeletal repository**: If the repository is empty or only partially initialized, use the user's project specification as the source of truth. Write instructions for the intended project, but do not claim that commands, files, or tooling already exist unless they do.
3. **Mixed signals**: If repository contents conflict with the user's description, treat repository contents as current facts and the user's description as intended direction. Ask before encoding future intentions as present-tense instructions.

For greenfield work, distinguish confirmed decisions from unresolved ones. If the user asks you to choose reasonable defaults, choose simple conventional defaults and encode them directly. If the user has not delegated that choice, ask before inventing tooling, directory structure, quality gates, or commands.

---

## Core Principles for Writing One

### 1. Be imperative, not descriptive
Write instructions. Never write narration.

| ❌ Weak | ✅ Strong |
|---|---|
| "The project uses ruff for formatting." | "Always run `uv run ruff format` before committing." |
| "Tests exist in the tests/ folder." | "After every code change, run `uv run pytest` and fix any failures before finishing." |

### 2. Prefer exact commands over prose
Provide a copy-pasteable command for every task the agent might perform. Never describe a command in prose when an exact command exists.

### 3. Layer from general to specific
Structure the file from general to specific: project overview → environment setup → conventions → workflow → constraints. Front-load the most load-bearing decisions because agents scan top-to-bottom.

### 4. Encode your non-obvious decisions
Document only non-obvious decisions. Omit obvious rules like "don't break syntax". Include non-obvious rules like "we never raise bare `Exception`; always use domain-specific error classes".

### 5. Keep it honest and current
Keep the file current. A stale `AGENTS.md` is worse than none. Update it every time the project changes—commands, dependencies, or workflow.

Do not invent precision. For fresh or not-yet-implemented repositories, distinguish confirmed project decisions from placeholders. Never document commands, directories, dependencies, CI checks, or quality gates as existing facts unless the repository or user specification confirms them.

### 6. Be explicit about quality gates
Define "done" explicitly. List every check that must pass before a change is considered complete.

### 7. Scope to what changes
Scope every line to what changes. Omit anything that does not affect how the agent writes or checks code, such as deployment runbooks or org charts. Ask yourself: "Would this change how the agent writes or checks code?"

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
- **Unconfirmed speculation** — don't document intended future architecture, commands, or workflows as facts unless the user has explicitly chosen them.
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

## Relationship to Other Documentation

| File | Audience | Content |
|---|---|---|
| `README.md` | Human contributors | Quick start, project description, contribution guidelines |
| `CONTRIBUTING.md` | Human contributors | Detailed process for submitting changes, code of conduct |
| `AGENTS.md` | AI agents | Exact commands, conventions, constraints, and quality gates |

Never duplicate human-oriented content from `README.md` or `CONTRIBUTING.md` in `AGENTS.md`. Cross-reference them if an agent needs to know they exist.

---

## Clarification Questions

When instructing an agent to write an `AGENTS.md`, answer these questions first. For existing repositories, infer answers from files when possible. For fresh repositories, use the user's project specification and ask focused questions only for decisions that would otherwise make the file misleading.

- [ ] Is this an existing repository, a fresh repository, or a skeletal repository with intended specs?
- [ ] What is the primary language and framework?
- [ ] What is the tech stack? (languages, build tools, package managers)
- [ ] How are dependencies installed and the project run?
- [ ] What linting, formatting, and type-checking tools are used?
- [ ] What is the test command and are there coverage requirements?
- [ ] Are there pre-commit hooks or CI checks to document?
- [ ] What is the project structure and where do different file types live?
- [ ] Are there architecture rules or layering constraints?
- [ ] Are there naming conventions or patterns the agent must follow?
- [ ] Are there forbidden patterns or anti-patterns?
- [ ] Should the agent follow an existing convention or style guide?

---

## Checklist Before Publishing

- [ ] The source of truth is clear: existing repository, user specification, or both
- [ ] Every existing command is copy-pasteable and tested when feasible
- [ ] Any proposed greenfield command or structure is based on confirmed specs or explicitly chosen defaults
- [ ] Quality gates are explicit (what must pass = "done")
- [ ] Architecture layering rules are stated if the project has them
- [ ] Forbidden patterns are listed
- [ ] The file is ≤ ~200 lines (if longer, consider subdirectory files)
- [ ] No stale or aspirational information
