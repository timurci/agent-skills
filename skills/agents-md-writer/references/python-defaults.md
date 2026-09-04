# Python Defaults

Use these defaults when writing `AGENTS.md` for a Python project and the user asks for recommended defaults or has not specified conflicting preferences.

Existing repository facts take precedence — when the project already uses different package management, linting, formatting, testing, pre-commit, or type-checking tools, document those tools instead.

Apply the lean filter from the main skill: include a default only if it is load-bearing for the agent (changes how code is written or checked). Prefer omission over exhaustive coverage.

## General Preferences

- Emphasize YAGNI: add abstractions, configuration hooks, plugin systems, and extra layers only when a current requirement justifies them.
- Emphasize KISS: prefer the simplest implementation that satisfies the requirement. Use plain functions and direct data structures before introducing classes, frameworks, or indirection.
- Raise deliberately. When code detects a violated project rule, domain rule, invariant, required behavior, unsupported configuration, forbidden input shape, or impossible branch, raise a project-specific exception named `class <PascalCaseName>Error(Exception)`.
- Let errors propagate. Catch to recover, return a documented fallback, translate the failure into a domain-level result, or add context before re-raising; express failures as exceptions, reserving `None`, `False`, empty collections, and default objects for documented fallback behavior.
- Resolve type mismatches by improving type definitions, narrowing control flow, introducing typed helpers, or fixing the underlying type model instead of reaching for `cast`.

## Preferred Development Stack

- Package management and environment execution: `uv`
- Linting: `ruff`
- Formatting: `ruff`
- Pre-commit hooks: `prek`
- Type checking: `ty`
- Testing: `pytest`

`ty` is a preferred default for personal projects, but it may be less production-proven than alternatives. For established or team projects, respect the repository's existing type checker.

## When Using uv

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
- Edit ruff configuration only with a clear reason.
- Pair every `# noqa` suppression with a comment explaining the exception.

## When Using Type Checkers

- Pair every `# type: ignore` or `# ty: ignore` with an explanatory comment.
- Prefer fixing annotations, control flow, or library typing boundaries over suppressing diagnostics.

## Suggested Quality Gates

When these tools are selected for the project, use this order:

```bash
uv run ruff check --fix
uv run ruff format
uv run ty check
uv run pytest
```

When the project uses a different test runner, replace the final command with the repository's actual test command.

## Tool References

- `uv`: https://docs.astral.sh/uv/
- `ruff`: https://docs.astral.sh/ruff/
- `prek`: https://prek.j178.dev/
- `pre-commit`: https://pre-commit.com/
- `ty`: https://docs.astral.sh/ty/
- `pytest`: https://docs.pytest.org/
