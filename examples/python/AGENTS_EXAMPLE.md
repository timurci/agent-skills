# AGENTS.md — ledgerflow

<!--
  This file is read by AI coding agents at the start of every session.
  Keep it accurate, imperative, and free of speculation.
-->

## Project Overview

`ledgerflow` is a CLI tool and importable library that ingests bank export files (CSV, OFX), classifies transactions using a configurable rule engine, and produces categorised spending reports. It is used by individual users and small finance teams via terminal. There is no web server and no database — all state lives in files on disk. Correctness and determinism matter more than performance.

---

## Tech Stack

- **Language**: Python `3.12`
- **Package manager / runner**: `uv`
- **Dependencies declared in**: `pyproject.toml`
- **Linter + formatter**: `ruff` (config in `ruff.toml`)
- **Static type checker**: `ty`
- **Pre-commit hooks**: `prek`
- **Testing**: `pytest` with `pytest-snapshot` for report output tests
- **Key libraries**:
  - `typer` — CLI interface
  - `pydantic` — config and transaction model validation
  - `polars` — tabular data processing
  - `rich` — terminal output formatting

---

## Environment

### Install dependencies

```bash
uv sync
```

### Run the CLI (development)

```bash
uv run ledgerflow --help
```

### Run a one-off script

```bash
uv run python scripts/seed_fixtures.py
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
uv run pytest
```

Run these in order. Fix all errors and warnings before finishing. Do not submit a change that fails any of these.

---

## Pre-commit Hooks

Install once after cloning:

```bash
prek install
```

Run manually against all files:

```bash
prek run --all-files
```

---

## Project Structure

```
ledgerflow/
├── pyproject.toml              # Project metadata and dependencies
├── ruff.toml                   # Ruff config
├── AGENTS.md                   # This file
│
├── src/
│   └── ledgerflow/
│       ├── __init__.py
│       ├── cli.py              # Typer CLI entry point — thin, delegates to core
│       ├── config.py           # Pydantic models for user config (ledgerflow.toml)
│       ├── ingest/
│       │   ├── __init__.py
│       │   ├── csv.py          # CSV parser → list[Transaction]
│       │   └── ofx.py          # OFX parser → list[Transaction]
│       ├── classify/
│       │   ├── __init__.py
│       │   └── engine.py       # Rule engine: applies config rules to transactions
│       ├── report/
│       │   ├── __init__.py
│       │   └── builder.py      # Turns classified transactions into report data
│       ├── models.py           # Shared domain types: Transaction, Category, Report
│       └── errors.py           # All custom exceptions
│
├── tests/
│   ├── conftest.py             # Shared fixtures (sample transactions, temp config)
│   ├── test_ingest_csv.py
│   ├── test_ingest_ofx.py
│   ├── test_classify_engine.py
│   └── test_report_builder.py
│
└── scripts/
    └── seed_fixtures.py        # Dev-only: generate test CSV/OFX fixtures
```

---

## Architecture & Design

`ledgerflow` has three explicit layers. Maintain this boundary strictly:

```
CLI (cli.py)
    │  calls
    ▼
Core logic  (ingest/, classify/, report/)
    │  uses
    ▼
Domain models  (models.py, config.py, errors.py)
```

- **CLI layer** (`cli.py`): Parses arguments, reads files, calls core functions, formats and prints output. Contains no business logic. Never import `polars` or `pydantic` models directly in `cli.py` — receive plain domain types from core.
- **Core layer** (`ingest/`, `classify/`, `report/`): Pure functions and classes operating on domain models. No I/O except what is explicitly passed in. Functions here must be unit-testable without touching the filesystem.
- **Domain layer** (`models.py`, `config.py`, `errors.py`): Defines `Transaction`, `Category`, `ClassifiedTransaction`, `Report`, config schemas, and exceptions. No logic beyond validation.

**Design principles:**
- **YAGNI**: Do not add plugin systems, registries, or abstract base classes unless a concrete second implementation exists or is explicitly required by current specs.
- **KISS**: A plain function is preferred over a class. A class is preferred over a hierarchy. Only introduce a new abstraction when the duplication cost is clear.
- Ingest parsers are independent of each other — do not share state between `csv.py` and `ofx.py`. Share types via `models.py`.

---

## Code Conventions

### Naming
- Modules and packages: `snake_case`
- Classes: `PascalCase`
- Functions, variables, parameters: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Parser functions must be named `parse_[format](path: Path) -> list[Transaction]` for consistency.

### Typing
- All public function signatures must have complete type annotations.
- Use `from __future__ import annotations` at the top of every module.
- Prefer `X | None` over `Optional[X]`.
- Do not use `Any` unless interfacing with an untyped third-party library, and always add a comment explaining why.

### Error handling
- Raise exceptions defined in `errors.py` — never `Exception` or `ValueError` directly.
- Current exceptions: `ParseError`, `ConfigError`, `ClassificationError`. Add new ones to `errors.py` if needed.
- The CLI layer catches domain exceptions and converts them to a user-facing `rich` error message + non-zero exit.

### Imports
- Import order: stdlib → third-party → internal (ruff enforces this).
- Never use wildcard imports.

### Polars usage
- Prefer lazy frames (`pl.LazyFrame`) in `report/builder.py`; collect only at the output boundary.
- Never convert a `polars` frame to `pandas` — there is no `pandas` dependency.

---

## Testing Conventions

- Test files mirror `src/ledgerflow/` structure.
- Use `conftest.py` fixtures for shared sample data — do not hardcode transaction dicts inline in multiple tests.
- Use `pytest-snapshot` for report output tests; update snapshots intentionally with `uv run pytest --snapshot-update`.
- Core layer functions must be testable without filesystem access — use `tmp_path` fixture only in ingest tests that truly need files.
- Parametrize edge cases (empty files, unknown categories, malformed rows) explicitly.

---

## What NOT to Do

- **Do not** add dependencies without `uv add [package]` (updates `pyproject.toml` and lockfile).
- **Do not** use `pip install` directly.
- **Do not** put business logic in `cli.py` — it must remain a thin adapter.
- **Do not** add a database, HTTP client, or async code — this project is synchronous and file-based.
- **Do not** introduce a plugin or registry pattern for ingest parsers unless a third format is actually required.
- **Do not** suppress type errors with `# type: ignore` without an explanatory comment.
- **Do not** edit `ruff.toml` or add `# noqa` suppressions without a comment explaining the exception.

---

## Known Gotchas

- OFX files from some banks use Windows-1252 encoding. `ofx.py` handles this — do not change the encoding detection logic without testing against `tests/fixtures/windows1252.ofx`.
- `polars` lazy evaluation means errors surface at `.collect()`, not at the point of expression construction. Add `.collect()` calls in tests to catch schema errors early.
- `typer` wraps exceptions by default; the `cli.py` entry point sets `app = typer.Typer(pretty_exceptions_enable=False)` deliberately for cleaner error output.
