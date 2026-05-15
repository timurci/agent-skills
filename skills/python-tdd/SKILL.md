---
name: python-tdd
description: Use when implementing Python changes with test-driven development, adding or improving pytest tests, reproducing bugs with tests before fixing them, or deciding whether a Python change needs tests.
---

# Python TDD

Use `pytest` for Python tests. Run tests with `uv run pytest` when the project uses `uv`.

## Workflow

### Feature Development

1. Define the intended behavior from the user's specification.
2. Write a failing pytest test for the happy path or primary intended behavior before implementing it.
3. If the test needs an importable contract, create the smallest interface needed: a function, class, method, or placeholder implementation that raises `NotImplementedError`.
4. Run the targeted test and confirm it fails for the expected reason.
5. Write the minimal implementation needed to make the test pass.
6. Refactor only after the targeted test passes.
7. Run the relevant broader test set before finishing.

After the primary behavior test passes, add edge-case or error-path tests only when they are specified, risky, or introduced by meaningful branching in the implementation.

### Bug Fixes

1. Write a regression test that reproduces the bug before changing the implementation.
2. Run the test and confirm it fails for the bug, not for an unrelated setup problem.
3. Fix the bug with the smallest implementation change that satisfies the regression test.
4. Run the new test, then run the relevant existing tests to check for regressions.

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

Prefer a roughly one-to-one relationship between source modules and test files. Combining tests for multiple modules is acceptable when the behavior is tightly related, but split the file when unrelated concerns are mixed or the test file grows beyond about 500 lines.

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

- Prefer testing observable behavior over implementation details. Do not assert private helper calls, internal ordering, or intermediate data structures unless they are part of the contract.
- Test only behavior introduced by this project. Do not test Python, the standard library, or third-party library behavior as though it were project behavior.
- Do not duplicate coverage. If two tests exercise the same code path with the same assertions, keep one.
- Use `@pytest.mark.parametrize` when inputs differ only in data and each case adds real behavioral value.
- Name tests descriptively: `test_<scenario>_<expected_outcome>`.
- Use plain `assert` freely in test files.
- Public docstrings and return type annotations are not required in test files.
- Keep tests fast and deterministic.
- Avoid real network calls. Use mocks, stubs, or fakes for external dependencies.

## Boundaries and Test Doubles

- Do not mock the code under test. Mock or fake external boundaries such as network clients, clocks, random sources, subprocesses, databases, expensive services, and third-party APIs.
- Use `tmp_path` for filesystem tests. Do not write to repository paths, user home directories, or global temp locations unless the test explicitly covers that behavior.
- Use `monkeypatch` for environment variables, current working directory changes, module attributes, `sys.path`, and other process-global state.
- Avoid leaving global state modified after a test.
- Control time, randomness, and generated identifiers in tests. Inject clocks, seeds, or ID providers when needed.
- Use `pytest.raises` to assert expected exceptions. Assert on the message or custom attributes when they are part of the contract.
- Keep fixture scope as narrow as possible. Use function-scoped fixtures by default; widen scope only when setup cost or shared immutable state justifies it.

## Organization Patterns

- Group tests by class or concern when it improves scanability, such as `TestToolMetadata` or `TestEdgeCases`.
- Parametrize data-driven inputs instead of copy-pasting test methods with different values.
- Keep fixtures in `conftest.py` when reused across test files.
- Prefer inline helper definitions for single-use helpers.
- Use parametrization for edge cases such as empty inputs, unsupported types, and error conditions when each case exercises meaningful project behavior.

## Commands

Run the narrowest relevant test first:

```bash
uv run pytest path/to/test_file.py::test_name
uv run pytest path/to/test_file.py
uv run pytest
```

If the project does not use `uv`, use the repository's existing test command while preserving the same narrow-to-broad workflow.
