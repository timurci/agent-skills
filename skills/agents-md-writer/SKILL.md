---
name: agents-md-writer
description: Use when creating, reviewing, or improving an AGENTS.md file for a repository.
---

# How to Write a Good AGENTS.md

An `AGENTS.md` is the operating manual for AI coding agents — what an agent reads at the start of a session to make locally correct decisions without asking. It should give high-level design decisions and insight into project conventions, not an exhaustive rulebook.

Every line must be **grounded**: traceable to a repository fact or a confirmed user decision, never invented or aspirational.

## Process

1. **Ground.** Inspect manifests, configs, tests, scripts, and CI; derive tooling, commands, structure, and conventions from what exists. For a fresh or skeletal repo, use the user's spec as source of truth but do not claim files/commands exist unless they do. Where repo and description conflict, treat the repo as current fact and the description as intended direction.

   *Done when every instruction traces to a repository fact or a confirmed user decision.*

2. **Draft lean.** Start with the root `AGENTS.md`. Add only what an agent needs to work correctly in that scope (see what to include/omit). Extract scoped content into subdirectory files per the splitting rules — do not repeat.

   *Done when every included line passes the omit tests and sits in its scope-matched file.*

3. **Verify.** Run the completion check.

   *Done when the completion check passes.*

## What to include / what to omit

Include only what changes how the agent writes or checks code:

- One-paragraph project orientation (what the project is + load-bearing design choice, e.g. DDD).
- Project structure map — where things live, with links to subdirectory `AGENTS.md` for deep conventions.
- Quality gate — exact, copy-pasteable commands that define "done" (e.g. `cargo test`, `cargo clippy --all-targets`).
- Architectural invariants and conventions that are non-obvious and not enforced by linters (e.g. aggregate-root ownership, error handling shape).

Omit:

- Anything that does not affect how code is written or checked — deployment runbooks, org charts, roadmaps.
- What the agent already knows ("don't break syntax") or what tooling enforces (if ruff/clippy catches it, don't restate it).
- Speculative or aspirational rules. Ask of each line: "Would omitting this cause the agent to make a wrong decision?" If not, omit. Ask also: "Could this constrain a future decision we haven't made?" If yes, omit or soften.

For each convention, say it once, in its single home.

## Writing rules

- **Imperative and concise.** Write instructions, not narration. Front-load load-bearing decisions; agents scan top-to-bottom.
- **Exact commands for gates, prose otherwise.** Give copy-pasteable commands for the quality gate and setup when a command exists; do not describe a command in prose when the exact command is known. Do not invent exact commands outside gates.
- **Define "done" explicitly.** List every check that must pass before a change is complete; that list is the quality gate.

## Placement and splitting

| File | Scope |
|---|---|
| `/AGENTS.md` | Entire repo |
| `/backend/AGENTS.md` | Only the `backend/` subtree |
| `/scripts/AGENTS.md` | Only the `scripts/` subtree |

Agents merge parent + subdirectory files. Use subdirectory files to extend or specialize, not repeat.

Split into a subdirectory `AGENTS.md` when **either** condition holds:

1. **Size — parent passes 200 lines.** Move scoped content to the subdirectory that owns it until the parent is back under 200 lines.
2. **Scope/path mismatch — instruction scope does not match file location.** If a rule applies only to a subtree (e.g. domain-model invariants that live in `src/model/`), it belongs in that subtree's `AGENTS.md` even if the parent is still under 200 lines. Audit each block: "Does this apply repo-wide? If not, relocate."

Keep each file ≤200 lines. Prefer a short root that links out over a long root that exhausts every sub-area.

## Relationship to README and CONTRIBUTING

| File | Audience | Content |
|---|---|---|
| `README.md` | Human contributors | Quick start, project description, contribution guidelines |
| `CONTRIBUTING.md` | Human contributors | Detailed process for submitting changes, code of conduct |
| `AGENTS.md` | AI agents | High-level design decisions, project conventions, quality gates |

Never duplicate human-oriented content from `README.md` or `CONTRIBUTING.md` in `AGENTS.md`. Cross-reference them if an agent needs to know they exist.

## Reference defaults

For a Python project where the user asks for recommended defaults, read [`references/python-defaults.md`](references/python-defaults.md).

Defaults fill gaps only — they never override existing repository facts or explicit user choices.

## Completion check

Before finishing, confirm:

- [ ] Every instruction is **grounded** — traced to a repository fact or a confirmed user decision; no invented or aspirational content.
- [ ] File is **lean** — every line changes how the agent writes or checks code; no tool-enforced restatements or speculative constraints.
- [ ] Quality gate (if applicable) lists exact, copy-pasteable commands that define "done".
- [ ] No human-only content duplicated from `README.md` or `CONTRIBUTING.md`.
- [ ] Each file is ≤200 lines and scope-matched — the splitting rules are applied.
