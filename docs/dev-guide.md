# Development Guide

For AI assistants, start with root [AGENTS.md](../AGENTS.md).

---

## Setup

```bash
git clone https://github.com/yourusername/personal-ai-agent.git
cd personal-ai-agent

python3.11 -m venv venv
source venv/bin/activate

pip install -e ".[dev]"
pre-commit install

# Optional: local model testing
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen3:1.7b
ollama pull qwen3:8b
```

Create a `.env` file:

```bash
WORKSPACE_PATH=./workspace
DATABASE_PATH=./workspace/memory/tasks.db
OLLAMA_HOST=http://localhost:11434
LOG_LEVEL=DEBUG
# Optional
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Project Structure

```
personal-ai-agent/
├── agent/                    # Main application code
│   ├── orchestrator.py      # Core orchestrator logic
│   ├── router.py            # Model routing (LiteLLM)
│   ├── database.py          # SQLite operations
│   ├── sandbox.py           # File sandboxing
│   ├── agents/              # Agent implementations
│   │   ├── base.py          # BaseAgent abstract class
│   │   ├── code_agent.py
│   │   ├── research_agent.py
│   │   └── fileops_agent.py
│   ├── memory/              # Memory systems
│   │   ├── task_history.py
│   │   ├── vector_store.py
│   │   └── skill_registry.py
│   ├── tools/               # Tool implementations
│   │   ├── web_search.py
│   │   ├── file_tools.py
│   │   └── code_exec.py
│   ├── api/                 # Web API (FastAPI)
│   └── cli/                 # CLI interface (Click)
├── config/
│   ├── litellm.yaml         # Model routing config
│   └── agents/              # Agent profile YAMLs
├── workspace/               # Sandboxed agent workspace (gitignored)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
└── pyproject.toml           # Tool configs (black, ruff, mypy, pytest)
```

---

## Coding standards and testing

Code rules, coverage requirements, and format/lint/typecheck/test commands are defined in root [AGENTS.md](../AGENTS.md). Pre-commit hooks and CI enforce those rules.

---

## Git Workflow

Branch from `develop`, use [conventional commits](https://www.conventionalcommits.org/):

```
feat(agents): add ResearchAgent with web search
fix(sandbox): prevent path traversal vulnerability
docs(api): add OpenAPI specification
test(agents): add unit tests for CodeAgent
```

---

## Adding a New Agent

1. Create `config/agents/your_agent.yaml` with name, model_tier, tools, system_prompt
2. Implement in `agent/agents/your_agent.py` extending `BaseAgent`
3. Register in `agent/agents/__init__.py`
4. Add tests in `tests/unit/test_agents/`

## Adding a New Tool

1. Implement in `agent/tools/your_tool.py` extending `BaseTool` with `get_schema()` and `execute()`
2. Register in `agent/tools/__init__.py`
3. Add to relevant agent configs in `config/agents/`
