# AGENTS.md — [PROJECT NAME]

<!--
  This file is read by AI coding agents (Claude, Codex, Cursor, etc.) at the start
  of every session. Keep it accurate, imperative, and free of speculation.
  Update it whenever the project's tooling or conventions change.
-->

## Project Overview

<!-- One paragraph: what this project does, its primary purpose, and any domain constraints
     the agent needs to know to make correct decisions. -->

[TODO: Describe what this project does, who it's for, and any non-obvious domain rules.]

---

## Tech Stack

- **Language**: Python `[VERSION]`
- **Package manager / runner**: `uv`
- **Dependencies declared in**: `pyproject.toml`
- **Linter + formatter**: `ruff` (config in `ruff.toml`)
- **Static type checker**: `ty`
- **Pre-commit hooks**: `prek`
- **Testing**: [e.g. `pytest` / `unittest` — fill in]
- **Key libraries**: [list the important ones and their role]

---

## Environment

### Install dependencies

```bash
uv sync
```

### Run the project

```bash
uv run [ENTRY POINT OR COMMAND]
```

### Run a one-off script

```bash
uv run python [path/to/script.py]
```

---

## Quality Gates

**Every change must pass all of the following before it is considered complete:**

```bash
# 1. Fix lint issues
uv run ruff check --fix

# 2. Format code
uv run ruff format

# 3. Type check
uv run ty check

# 4. Run tests
[uv run pytest / fill in your test command]
```

Run these in order. Fix all errors and warnings before finishing. Do not leave a change in a state where any of these commands fail.

---

## Pre-commit Hooks

Install hooks once after cloning:

```bash
prek install
```

Hooks run automatically on `git commit`. To run them manually against all files:

```bash
prek run --all-files
```

---

## Project Structure

```
[PROJECT NAME]/
├── pyproject.toml         # Project metadata and dependencies
├── ruff.toml              # Ruff linter/formatter config
├── AGENTS.md              # This file
│
├── src/
│   └── [package_name]/
│       ├── __init__.py
│       ├── [module].py
│       └── ...
│
├── tests/
│   ├── conftest.py
│   └── test_[module].py
│
└── [other top-level dirs as needed]
```

<!-- Update this tree to match your actual structure. Annotate each
     directory with one line describing what lives there. -->

---

## Architecture & Design

<!-- Fill in the layering / separation of concerns for this project.
     Be explicit about which layers may depend on which others.
     Remove or simplify this section for small/simple projects. -->

[TODO: Describe the main components, their responsibilities, and the dependency direction between them.]

**General principles in force:**
- **YAGNI**: Do not add abstractions, interfaces, or configuration hooks unless a current requirement demands them.
- **KISS**: Prefer the simplest implementation that satisfies the requirement. Introduce complexity only when justified by the project specs.
- Respect existing module boundaries — do not collapse or bypass the established layering without a clear reason stated in a comment.

---

## Code Conventions

### Naming
- Modules and packages: `snake_case`
- Classes: `PascalCase`
- Functions, variables, parameters: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- [Add any project-specific naming rules]

### Typing
- All public function signatures must have complete type annotations.
- Prefer `X | None` over `Optional[X]`.
- Use `TypeAlias` for complex types that appear more than once.

### Error handling
- [TODO: define your error strategy — e.g. "raise domain-specific exceptions defined in `errors.py`; never raise bare `Exception`"]

### Imports
- Standard library → third-party → internal (ruff enforces this automatically).
- Never use wildcard imports (`from x import *`).

### General
- [Add any other non-obvious conventions specific to this project]

---

## Testing Conventions

- Test files live in `tests/` and mirror the `src/` structure.
- Every new function or class must have at least one test.
- Tests should be independent and not rely on external state or execution order.
- [Add conventions for fixtures, mocking, parametrize usage, etc.]

---

## What NOT to Do

- **Do not** add dependencies without updating `pyproject.toml` via `uv add [package]`.
- **Do not** use `pip install` directly — always go through `uv`.
- **Do not** bypass the type checker by casting to `Any` unless absolutely unavoidable and commented.
- **Do not** introduce new abstractions (base classes, factories, registries) unless the current requirements explicitly call for them.
- **Do not** edit `ruff.toml` or disable ruff rules inline (`# noqa`) without a comment explaining why.
- [Add project-specific anti-patterns here]

---

## Known Gotchas

<!-- Document non-obvious environmental or behavioural quirks here. Remove if none. -->

- [TODO: e.g. "The database requires a running Docker container — see `docker-compose.yml`"]
- [TODO: e.g. "Module X has a heavy import cost; don't import it at module level in hot paths"]
