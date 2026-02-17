# CLAUDE.md

**Canonical context:** [AGENTS.md](AGENTS.md) is the single source of truth for this repo. Follow it for full context, structure, and workflow. The rules below are the non-negotiable subset that must always be enforced in this IDE.

## Code Rules — Non-Negotiable

- **Python 3.11+.** Do not use constructs unavailable in 3.11.
- **Type hints on everything.** Every function signature and return type. `disallow_untyped_defs = true` in mypy. No shortcuts.
- **Line length: 100.** Black enforces this. Do not fight it.
- **Google-style docstrings** on all public functions and classes.
- **Ruff must pass clean.** Rules: E, W, F, I, B, C4, UP, ARG, SIM. `E501` is ignored (Black handles line length).
- **MyPy must pass strict.** `warn_return_any`, `strict_equality`, `no_implicit_optional` — all enabled. Fix type errors, do not suppress them with `# type: ignore` unless absolutely unavoidable and documented why.
- **80% minimum test coverage.** Orchestrator, router, and sandbox modules require 100%.
- **Imports sorted by Ruff/isort.** First-party module is `agent`.

## Naming

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Test files: `test_*.py`, test classes: `Test*`, test functions: `test_*`

## Security — Read This

- All file operations are sandboxed to `workspace/`. Never access files outside it.
- Never commit `.env`, credentials, or API keys.
- Path traversal is a critical vulnerability in this project. Validate all paths.
- Human approval is required before any self-improvement changes are applied. Do not bypass this.
