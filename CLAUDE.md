# CLAUDE.md

## What This Is

Personal AI agent orchestrator. Python 3.11+. Privacy-first, local-model-first, self-improving with human approval gates. Pre-implementation phase — architecture and tooling are set, application code is not.

## Commands

```bash
# Install
pip install -e ".[dev]"

# Format — run before every commit, no exceptions
black agent/ tests/

# Lint
ruff check agent/
ruff check --fix agent/    # auto-fix

# Type check — strict mode, no untyped defs allowed
mypy agent/

# Test
pytest                                   # all tests
pytest tests/unit/                       # unit only
pytest tests/integration/ -v             # integration only
pytest --cov=agent --cov-report=html     # with coverage
```

## Code Rules — Non-Negotiable

- **Python 3.11+**. Do not use constructs unavailable in 3.11.
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

## Architecture

- `agent/` — all application code lives here
- `agent/agents/` — agent implementations extending `BaseAgent`
- `agent/tools/` — tool implementations extending `BaseTool`
- `agent/memory/` — task history, vector store, skill registry
- `agent/cli/` — Click CLI (`agent` entry point)
- `agent/api/` — FastAPI web API
- `config/` — LiteLLM yaml and agent profile yamls
- `tests/` — mirrors `agent/` structure with `unit/` and `integration/`
- `workspace/` — sandboxed runtime directory, gitignored

## Git

Conventional commits. No exceptions.

```
feat(scope): description
fix(scope): description
docs(scope): description
test(scope): description
refactor(scope): description
```

## Security — Read This

- All file operations are sandboxed to `workspace/`. Never access files outside it.
- Never commit `.env`, credentials, or API keys.
- Path traversal is a critical vulnerability in this project. Validate all paths.
- Human approval is required before any self-improvement changes are applied. Do not bypass this.

## Adding Components

**New agent:** config yaml in `config/agents/` -> implement in `agent/agents/` extending `BaseAgent` -> register in `__init__.py` -> add tests.

**New tool:** implement in `agent/tools/` extending `BaseTool` with `get_schema()` and `execute()` -> register in `__init__.py` -> add to agent configs.

## Dependencies

Core: `anthropic`, `click`, `pydantic`, `python-dotenv`, `requests`. Extras: `local` (ollama + litellm), `api` (fastapi + uvicorn), `memory` (chromadb), `scheduler` (apscheduler), `monitoring` (prometheus + structlog). Do not add dependencies without justification.
