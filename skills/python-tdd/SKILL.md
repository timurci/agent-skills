---
name: python-tdd
description: Use when the user wants TDD for a Python change — implementing features, adding or improving pytest tests, reproducing a bug with a test before fixing it, or deciding whether a change needs tests.
---

# Python TDD

Use `pytest` for Python tests.

The workflow is the **red-green-refactor** loop:

- **Red** — a failing test pins the intended behavior. Red is a binary gate, not a feeling: the test must fail for the *expected* reason (missing behavior, not an import error or setup fault).
- **Green** — the smallest implementation that passes the red test. Code written without a failing test abandons the loop.
- **Refactor** — improve the code while the test stays green. Never refactor against a red or unwritten test.

## Workflow

### Feature Development

1. Define the intended behavior from the user's specification.
2. **Red** — write a failing pytest test for the happy path or primary behavior before implementing it.
3. If the test needs an importable contract, create the smallest interface needed — a function, class, method, or placeholder that raises `NotImplementedError` — so the test is red for the missing behavior, not an import error.
4. Run the targeted test and confirm it is red for the expected reason.
5. **Green** — write the minimal implementation needed to make the test pass.
6. **Refactor** only after the targeted test is green.
7. Run the relevant broader test set — done when it stays green.

After the primary behavior is green, add edge-case or error-path tests only when they are specified, risky, or introduced by meaningful branching in the implementation.

### Bug Fixes

1. **Red** — write a regression test that reproduces the bug before changing the implementation.
2. Run it and confirm it is red for the bug, not an unrelated setup problem.
3. **Green** — fix the bug with the smallest implementation change that satisfies the regression test.
4. Run the new test, then the relevant existing tests — done when the regression test is green and no existing test turned red.

## Test Placement

Tests should reflect the project structure.

For a `src` layout project, tests for:

```text
project_root/src/project_name/subpackage_a/
```

should live under:

```text
project_root/tests/unit/subpackage_a/
```

Prefer a roughly one-to-one relationship between source modules and test files. Combine tests for multiple modules only when the behavior is closely related; split when unrelated concerns mix or the file grows beyond about 500 lines.

## Test Scope

Prefer the smallest test that gives useful confidence:

- Use unit tests for local behavior in functions, classes, and modules.
- Use integration tests when behavior depends on wiring between modules, filesystem behavior, CLI boundaries, configuration loading, databases, or external service boundaries.
- Use regression tests for bugs.

Not every change needs a new test:

- Pure refactors that preserve behavior do not need new tests.
- Changes to private helpers with no new branching logic may not need tests if existing tests already exercise them.
- Documentation, config-only, and formatting changes do not need tests.

## Test Quality

- Test observable behavior, not implementation details. Do not assert private helper calls, internal ordering, or intermediate data structures unless they are part of the contract.
- Test only behavior introduced by this project. Do not test Python, the standard library, or third-party library behavior as though it were project behavior.
- Do not duplicate coverage. If two tests exercise the same code path with the same assertions, keep one.
- Name tests descriptively: `test_<scenario>_<expected_outcome>`.
- Use plain `assert` freely in test files; public docstrings and return type annotations are not required there.
- Keep tests tight — fast and deterministic; see [Boundaries and Test Doubles](#boundaries-and-test-doubles) for faking slow dependencies and controlling non-determinism.

## Boundaries and Test Doubles

- Do not mock the code under test. Mock or fake external boundaries — network clients, subprocesses, databases, expensive services, and third-party APIs.
- Control non-determinism (time, randomness, generated identifiers) by injecting clocks, seeds, or ID providers rather than depending on real ones.
- Use `tmp_path` for filesystem tests. Do not write to repository paths, user home directories, or global temp locations unless the test explicitly covers that behavior.
- Use `monkeypatch` for environment variables, current working directory, module attributes, `sys.path`, and other process-global state — it restores them automatically after the test.
- Use `pytest.raises` to assert expected exceptions; assert on the message or custom attributes only when they are part of the contract.
- Keep fixture scope as narrow as possible. Use function-scoped fixtures by default; widen only when setup cost or shared immutable state justifies it.

## Organization Patterns

- Use `@pytest.mark.parametrize` when inputs differ only in data and each case adds real behavioral value — including edge cases such as empty inputs, unsupported types, and error conditions. Do not copy-paste test methods that vary only in values.
- Group tests by class or concern when it improves scanability, such as `TestToolMetadata` or `TestEdgeCases`.
- Keep fixtures in `conftest.py` when reused across test files; prefer inline definitions for single-use helpers.

## Commands

Run the narrowest relevant test first:

```bash
uv run pytest path/to/test_file.py::test_name
uv run pytest path/to/test_file.py
uv run pytest
```

If the project does not use `uv`, use the repository's existing test command while preserving the same narrow-to-broad workflow.
