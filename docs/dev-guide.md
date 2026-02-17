# Development Guide

> How to contribute to and develop the Personal AI Agent System

---

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Git Workflow](#git-workflow)
5. [Testing](#testing)
6. [Adding New Features](#adding-new-features)
7. [Debugging](#debugging)
8. [Performance Optimization](#performance-optimization)

---

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- Git
- Docker (optional, for containerized development)
- Ollama (for local model testing)

### Initial Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/personal-ai-agent.git
cd personal-ai-agent

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e ".[dev]"

# This installs:
# - Main dependencies from requirements.txt
# - Development tools: pytest, ruff, black, mypy, pre-commit
# - Optional tools: ipython, jupyter

# 4. Install pre-commit hooks
pre-commit install

# 5. Set up Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen3:1.7b
ollama pull qwen3:8b

# 6. Initialize workspace
python scripts/init_workspace.py

# 7. Run tests to verify setup
pytest
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# .env
WORKSPACE_PATH=./workspace
DATABASE_PATH=./workspace/memory/tasks.db
OLLAMA_HOST=http://localhost:11434
LOG_LEVEL=DEBUG

# Optional: Cloud API keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

Load with:
```bash
# Install python-dotenv
pip install python-dotenv

# In your code
from dotenv import load_dotenv
load_dotenv()
```

### IDE Setup

#### VS Code

Install extensions:
- Python (Microsoft)
- Pylance
- Ruff
- Black Formatter
- Git Graph

`.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### PyCharm

1. File → Settings → Project → Python Interpreter
2. Select the virtual environment
3. Enable Black and Ruff in Code Style settings
4. Configure pytest as test runner

---

## Project Structure

```
personal-ai-agent/
│
├── agent/                          # Main application code
│   ├── __init__.py                # Package initialization
│   ├── orchestrator.py            # Core orchestrator logic
│   ├── router.py                  # Model routing (LiteLLM)
│   ├── database.py                # SQLite operations
│   ├── sandbox.py                 # File sandboxing
│   │
│   ├── agents/                    # Agent implementations
│   │   ├── __init__.py
│   │   ├── base.py               # BaseAgent abstract class
│   │   ├── code_agent.py         # Code generation agent
│   │   ├── research_agent.py     # Research agent
│   │   └── fileops_agent.py      # File operations agent
│   │
│   ├── memory/                    # Memory systems
│   │   ├── __init__.py
│   │   ├── task_history.py       # Task logging
│   │   ├── vector_store.py       # ChromaDB wrapper
│   │   └── skill_registry.py     # Skill management
│   │
│   ├── tools/                     # Tool implementations
│   │   ├── __init__.py
│   │   ├── base.py               # BaseTool interface
│   │   ├── web_search.py         # Web search tool
│   │   ├── file_tools.py         # File operation tools
│   │   └── code_exec.py          # Code execution tool
│   │
│   ├── api/                       # Web API (FastAPI)
│   │   ├── __init__.py
│   │   ├── app.py                # FastAPI app
│   │   ├── routes/
│   │   │   ├── tasks.py
│   │   │   ├── approvals.py
│   │   │   └── stats.py
│   │   └── models/               # Pydantic models
│   │       ├── task.py
│   │       └── approval.py
│   │
│   └── cli/                       # CLI interface
│       ├── __init__.py
│       └── commands.py           # Click commands
│
├── config/                        # Configuration files
│   ├── litellm.yaml              # Model routing config
│   ├── agents/                   # Agent profiles
│   │   ├── code_agent.yaml
│   │   ├── research_agent.yaml
│   │   └── fileops_agent.yaml
│   └── tools.yaml                # Tool configurations
│
├── workspace/                     # Agent workspace (gitignored)
│   ├── skills/                   # Agent-created skills
│   ├── memory/                   # Persistent memory
│   ├── temp/                     # Temporary files
│   └── outputs/                  # User-facing outputs
│
├── tests/                         # Test suite
│   ├── unit/                     # Unit tests
│   │   ├── test_orchestrator.py
│   │   ├── test_router.py
│   │   └── test_agents/
│   ├── integration/              # Integration tests
│   │   ├── test_task_flow.py
│   │   └── test_skill_creation.py
│   ├── fixtures/                 # Test fixtures
│   │   ├── mock_tasks.py
│   │   └── sample_configs.py
│   └── conftest.py               # Pytest configuration
│
├── scripts/                       # Utility scripts
│   ├── init_workspace.py         # Initialize workspace
│   ├── setup_ollama.sh           # Setup Ollama models
│   ├── migrate_db.py             # Database migrations
│   └── benchmark.py              # Performance benchmarks
│
├── docs/                          # Documentation
│   ├── architecture.md
│   ├── api.md
│   ├── agents.md
│   └── skills.md
│
├── .github/                       # GitHub configuration
│   └── workflows/
│       ├── tests.yml             # CI/CD pipeline
│       └── release.yml           # Release automation
│
├── agent.py                       # Main entry point
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
├── setup.py                       # Package setup
├── pyproject.toml                # Tool configuration
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── SPEC.md
├── DEVELOPMENT.md                 # This file
└── LICENSE
```

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with these tools enforcing standards:

- **Black**: Code formatting (line length: 100)
- **Ruff**: Linting (replaces flake8, isort, pylint)
- **MyPy**: Type checking

### Code Formatting

```bash
# Format code with Black
black agent/ tests/

# Check formatting without making changes
black --check agent/

# Sort imports with Ruff
ruff check --select I --fix agent/

# Run all formatters
make format  # or: pre-commit run --all-files
```

### Linting

```bash
# Run Ruff linter
ruff check agent/

# Auto-fix issues
ruff check --fix agent/

# Check specific rules
ruff check --select E,F agent/  # pycodestyle errors, pyflakes
```

### Type Checking

All new code must include type hints:

```python
from typing import Optional, List, Dict

def execute_task(
    task_input: str,
    context: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> TaskResult:
    """Execute a task with optional context.
    
    Args:
        task_input: The user's request
        context: Additional context for the task
        timeout: Maximum execution time in seconds
        
    Returns:
        TaskResult with output and metadata
        
    Raises:
        TimeoutError: If task exceeds timeout
        ValidationError: If input is invalid
    """
    pass
```

Check types:
```bash
mypy agent/
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_confidence(
    task: str,
    model_output: str,
    context: Dict[str, Any]
) -> float:
    """Calculate confidence score for model output.
    
    Analyzes the model's output and contextual factors to estimate
    how confident we should be in the result.
    
    Args:
        task: The original task description
        model_output: The model's response
        context: Additional context including model metadata
        
    Returns:
        Confidence score between 0.0 and 1.0
        
    Examples:
        >>> calculate_confidence(
        ...     "What is 2+2?",
        ...     "4",
        ...     {"model": "qwen3:8b"}
        ... )
        0.95
    """
    pass
```

### Naming Conventions

- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `lowercase_with_underscores()`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore()`

### Code Organization

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import click
from anthropic import Anthropic

# 3. Local imports
from agent.orchestrator import Orchestrator
from agent.database import TaskDatabase

# 4. Constants
DEFAULT_MODEL = "qwen3:8b"
MAX_RETRIES = 3

# 5. Classes
class MyClass:
    pass

# 6. Functions
def my_function():
    pass

# 7. Main execution
if __name__ == "__main__":
    main()
```

---

## Git Workflow

### Branch Strategy

```
main            # Production-ready code
├── develop     # Integration branch
    ├── feature/add-research-agent
    ├── feature/improve-routing
    ├── fix/sandbox-path-bug
    └── docs/api-documentation
```

### Workflow Steps

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 2. Make changes
# ... edit code ...

# 3. Run pre-commit checks
pre-commit run --all-files

# 4. Commit with conventional commits
git add .
git commit -m "feat(agents): add ResearchAgent with web search

- Implement BaseAgent interface
- Add web_search and web_fetch tools
- Include integration tests
- Update documentation

Closes #42"

# 5. Push to GitHub
git push origin feature/your-feature-name

# 6. Create Pull Request on GitHub
# Title: "[Feature] Add ResearchAgent with web search capabilities"
# Description: Link to issue, describe changes, testing done

# 7. After review and approval, merge to develop
# Then periodically merge develop → main for releases
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
feat(orchestrator): add confidence-based routing
fix(sandbox): prevent path traversal vulnerability
docs(api): add OpenAPI specification
test(agents): add unit tests for CodeAgent
```

---

## Testing

### Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_orchestrator.py
│   ├── test_router.py
│   └── test_agents/
│       ├── test_base_agent.py
│       └── test_code_agent.py
│
├── integration/             # Multi-component tests
│   ├── test_task_flow.py
│   └── test_skill_creation.py
│
├── fixtures/                # Reusable test data
│   ├── mock_tasks.py
│   └── sample_configs.py
│
└── conftest.py             # Pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_orchestrator.py

# Run specific test function
pytest tests/unit/test_orchestrator.py::test_task_routing

# Run with coverage
pytest --cov=agent --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run only integration tests (slower)
pytest tests/integration/ -v

# Run tests matching pattern
pytest -k "routing"
```

### Writing Unit Tests

```python
# tests/unit/test_router.py
import pytest
from agent.router import TaskRouter

class TestTaskRouter:
    """Test suite for TaskRouter"""
    
    @pytest.fixture
    def router(self):
        """Fixture providing a TaskRouter instance"""
        return TaskRouter()
    
    def test_simple_task_routes_to_fast(self, router):
        """Simple tasks should use fast model"""
        task = "What is the weather?"
        tier = router.decide_tier(task)
        assert tier == "fast"
    
    def test_complex_task_routes_to_smart(self, router):
        """Complex tasks should use smart model"""
        task = "Write a comprehensive analysis of quantum computing"
        tier = router.decide_tier(task)
        assert tier == "smart"
    
    @pytest.mark.parametrize("task,expected_tier", [
        ("Summarize this article", "fast"),
        ("Write code for a web scraper", "smart"),
        ("What is 2+2?", "fast"),
        ("Design a database schema", "smart"),
    ])
    def test_routing_examples(self, router, task, expected_tier):
        """Test routing for various task types"""
        assert router.decide_tier(task) == expected_tier
```

### Writing Integration Tests

```python
# tests/integration/test_task_flow.py
import pytest
from agent import Orchestrator, TaskDatabase

@pytest.mark.integration
class TestTaskFlow:
    """End-to-end task execution tests"""
    
    @pytest.fixture
    def orchestrator(self, tmp_path):
        """Fixture providing configured Orchestrator"""
        db_path = tmp_path / "test.db"
        db = TaskDatabase(db_path)
        return Orchestrator(db=db)
    
    async def test_complete_task_execution(self, orchestrator):
        """Test full task lifecycle"""
        # Execute task
        result = await orchestrator.execute_task(
            "Write a Python function to calculate factorial"
        )
        
        # Verify results
        assert result.success
        assert "def factorial" in result.output
        assert result.agent_type == "CodeAgent"
        
        # Verify database
        task = orchestrator.db.get_task(result.task_id)
        assert task is not None
        assert task.status == "completed"
```

### Test Coverage Requirements

- **Minimum coverage**: 80%
- **Critical paths**: 100% (orchestrator, router, sandbox)
- **New features**: Must include tests

Check coverage:
```bash
pytest --cov=agent --cov-report=term-missing
```

---

## Adding New Features

### Adding a New Agent

**Step 1**: Create agent configuration

```yaml
# config/agents/my_agent.yaml
name: MyAgent
description: What this agent does
model_tier: smart
max_iterations: 3
approval_required: false

tools:
  - tool_one
  - tool_two

system_prompt: |
  You are a specialist in...
```

**Step 2**: Implement agent class

```python
# agent/agents/my_agent.py
from agent.agents.base import BaseAgent
from agent.models import AgentResult

class MyAgent(BaseAgent):
    """Agent description"""
    
    async def execute(
        self,
        task: str,
        context: Dict[str, Any]
    ) -> AgentResult:
        """Execute agent-specific logic"""
        
        # Build prompt
        prompt = self.build_prompt(task, context)
        
        # Call model
        response = await self.model.generate(
            system=self.config.system_prompt,
            messages=[{"role": "user", "content": prompt}],
            tools=self.get_tool_schemas()
        )
        
        # Handle tool calls if any
        if response.tool_calls:
            results = await self.execute_tools(response.tool_calls)
            # ... process results
        
        return AgentResult(
            success=True,
            output=response.content,
            agent_type="MyAgent"
        )
    
    def validate_result(self, result: Any) -> bool:
        """Validate output meets requirements"""
        # Custom validation logic
        return True
```

**Step 3**: Register agent

```python
# agent/agents/__init__.py
from agent.agents.code_agent import CodeAgent
from agent.agents.research_agent import ResearchAgent
from agent.agents.my_agent import MyAgent  # Add this

AGENT_REGISTRY = {
    "CodeAgent": CodeAgent,
    "ResearchAgent": ResearchAgent,
    "MyAgent": MyAgent,  # Add this
}
```

**Step 4**: Add tests

```python
# tests/unit/test_agents/test_my_agent.py
import pytest
from agent.agents.my_agent import MyAgent

class TestMyAgent:
    @pytest.fixture
    def agent(self):
        # Create test agent instance
        pass
    
    async def test_execute_success(self, agent):
        result = await agent.execute("test task", {})
        assert result.success
```

**Step 5**: Update documentation

Add to `docs/agents.md` with examples and use cases.

### Adding a New Tool

**Step 1**: Implement tool

```python
# agent/tools/my_tool.py
from agent.tools.base import BaseTool
from typing import Dict, Any

class MyTool(BaseTool):
    """Tool description"""
    
    name = "my_tool"
    description = "What this tool does"
    
    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for LLM"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tool logic"""
        param1 = kwargs.get("param1")
        
        # Validate
        self.validate_params(kwargs)
        
        # Execute
        result = self._do_work(param1)
        
        return {
            "success": True,
            "result": result
        }
    
    def _do_work(self, param):
        """Internal implementation"""
        pass
```

**Step 2**: Register tool

```python
# agent/tools/__init__.py
from agent.tools.my_tool import MyTool

TOOL_REGISTRY = {
    "web_search": WebSearchTool,
    "my_tool": MyTool,  # Add this
}
```

**Step 3**: Add to agent config

```yaml
# config/agents/some_agent.yaml
tools:
  - web_search
  - my_tool  # Add this
```

---

## Debugging

### Logging

```python
import structlog

logger = structlog.get_logger()

# Use structured logging
logger.info(
    "task_started",
    task_id=task.task_id,
    agent_type="CodeAgent",
    user_input=task.user_input[:100]
)

logger.error(
    "tool_execution_failed",
    tool_name="web_search",
    error=str(e),
    exc_info=True  # Include stack trace
)
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python agent.py -i

# Or in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Interactive Debugging

```python
# Add breakpoint
breakpoint()  # Python 3.7+

# Or use ipdb
import ipdb; ipdb.set_trace()

# Or use pdb
import pdb; pdb.set_trace()
```

### Common Issues

**Issue**: "Model not found"
```bash
# Solution: Pull the model
ollama pull qwen3:8b
ollama list  # Verify it's installed
```

**Issue**: "Permission denied" on workspace
```bash
# Solution: Fix permissions
chmod -R 755 workspace/
```

**Issue**: Tests failing with "no module named agent"
```bash
# Solution: Install in development mode
pip install -e .
```

---

## Performance Optimization

### Profiling

```python
# Use cProfile
python -m cProfile -o output.prof agent.py "your task"

# Analyze results
python -m pstats output.prof
# In pstats shell:
# sort cumtime
# stats 20

# Or use line_profiler
pip install line_profiler
@profile
def slow_function():
    pass

kernprof -l -v script.py
```

### Database Optimization

```python
# Add indexes for common queries
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_tasks_status_created
    ON tasks(status, created_at DESC)
""")

# Use connection pooling for concurrent access
from sqlalchemy import create_engine, pool

engine = create_engine(
    f"sqlite:///{db_path}",
    poolclass=pool.QueuePool,
    pool_size=5
)
```

### Caching

```python
from functools import lru_cache
from cachetools import TTLCache
import time

# LRU cache for pure functions
@lru_cache(maxsize=128)
def expensive_computation(x):
    return x ** 2

# TTL cache for time-sensitive data
cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes

def get_with_cache(key):
    if key in cache:
        return cache[key]
    
    result = expensive_api_call(key)
    cache[key] = result
    return result
```

---

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH (e.g., 1.2.3)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### Creating a Release

```bash
# 1. Update version
echo "0.2.0" > VERSION

# 2. Update CHANGELOG.md
# Add release notes under "## [0.2.0] - 2026-02-16"

# 3. Commit version bump
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"

# 4. Create tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# 5. Push
git push origin develop
git push origin v0.2.0

# 6. Merge to main
git checkout main
git merge develop
git push origin main

# 7. Create GitHub release from tag
# GitHub Actions will automatically build and publish
```

---

## Resources

- [Python Best Practices](https://docs.python-guide.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
