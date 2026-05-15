# Python Defaults

Use these defaults when writing `AGENTS.md` for a Python project and the user asks for recommended defaults or has not specified conflicting preferences.

Do not override existing repository facts. If the project already uses different package management, linting, formatting, testing, pre-commit, or type-checking tools, document the existing tools instead.

## General Preferences

- Emphasize YAGNI: do not add abstractions, configuration hooks, plugin systems, or extra layers unless a current requirement justifies them.
- Emphasize KISS: prefer the simplest implementation that satisfies the requirement. Use plain functions and direct data structures before introducing classes, frameworks, or indirection.
- Let errors propagate. Do not catch exceptions only to return a silent fallback such as empty bytes, `None`, an empty collection, or a default object. Only catch exceptions when the code can meaningfully recover or add useful context before re-raising.
- Separate raising exceptions from catching exceptions. "Let errors propagate" argues against unnecessary `try`/`except` blocks; it does not argue against raising meaningful exceptions.
- Raise exceptions directly when code detects a condition that violates a project rule, domain rule, invariant, required behavior, unsupported configuration, forbidden input shape, or impossible branch. Use a project-specific exception named `class <PascalCaseName>Error(Exception)` for these project or domain errors.
- Use `try`/`except` only when catching the exception is part of the intended behavior. The handler must do something meaningful: recover, return a documented fallback, translate the failure into a domain-level result, or add context before re-raising. Do not catch exceptions merely to hide failures or replace them with `None`, `False`, empty collections, or default objects unless that fallback is the documented behavior.
- Never use `cast`. Prefer improving type definitions, narrowing control flow, introducing typed helpers, or fixing the underlying type model.

## Preferred Development Stack

- Package management and environment execution: `uv`
- Linting: `ruff`
- Formatting: `ruff`
- Pre-commit hooks: `prek`
- Type checking: `ty`
- Testing: `pytest`

`ty` is a preferred default for personal projects, but it may be less production-proven than alternatives. For established or team projects, respect the repository's existing type checker.

## When Using uv

- Do not use `pip` directly.
- Manage dependencies through `uv`.
- Run Python commands through the project environment with `uv run`.
- Prefer copy-pasteable commands such as:

```bash
uv sync
uv run pytest
uv run ruff check
uv run ruff format
uv run ty check
```

Use `uv run pytest` as the default test command when the project uses `pytest`.

## When Using Ruff

- Use `ruff` for both linting and formatting when no conflicting formatter is specified.
- Do not edit linting configuration without a clear reason.
- Do not add `# noqa` suppressions without a comment explaining the exception.

## When Using Type Checkers

- Do not suppress type errors with `# type: ignore` or `# ty: ignore` without an explanatory comment.
- Prefer fixing annotations, control flow, or library typing boundaries over suppressing diagnostics.

## Suggested Quality Gates

When these tools are selected for the project, use this order:

```bash
uv run ruff check --fix
uv run ruff format
uv run ty check
uv run pytest
```

If the project does not use `pytest`, replace the final command with the repository's actual test command.

## Tool References

- `uv`: https://docs.astral.sh/uv/
- `ruff`: https://docs.astral.sh/ruff/
- `prek`: https://prek.j178.dev/
- `pre-commit`: https://pre-commit.com/
- `ty`: https://docs.astral.sh/ty/
- `pytest`: https://docs.pytest.org/
