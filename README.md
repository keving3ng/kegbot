# Personal AI Agent System

> A self-improving, privacy-focused AI agent orchestrator that runs on local hardware with optional cloud model fallback

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

An autonomous AI agent system designed for personal use that:

- **Orchestrates specialized agents** for different task types (code, research, file operations)
- **Runs primarily on local models** (Ollama) to minimize API costs and maximize privacy
- **Sandboxes all file operations** to prevent access to personal data
- **Self-improves with human approval** - proposes new skills and optimizations
- **Scales from modest hardware** (NAS) to powerful local inference (Mac Mini M4 Pro)

**Philosophy**: Privacy-first, cost-conscious, extensible, and transparent. You control what the agent can access and approve all self-modifications.

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Ollama installed (for local models)
- Optional: Anthropic API key (for cloud fallback)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/personal-ai-agent.git
cd personal-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen3:1.7b  # Fast classification model
ollama pull qwen3:8b    # General purpose model

# Run the agent
python agent.py --interactive
```

### First Run

```bash
# Test with a simple task
python agent.py "Write a haiku about coding"

# Start interactive mode
python agent.py -i

# View statistics
python agent.py stats
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│  Terminal CLI │ Web Dashboard │ API Gateway │ Cron Scheduler │
└────────────────────┬────────────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   ORCHESTRATOR      │ ← Routes tasks to agents
          │   LiteLLM Router    │ ← Manages model selection
          │   Persistent State  │ ← Tracks history
          └──────────┬──────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────────┐
│ Code Agent   │ │Research │ │FileOps Agent│
│Writes skills │ │ Agent   │ │Sandboxed FS │
└──────────────┘ └─────────┘ └─────────────┘
        │            │            │
┌───────▼────────────▼────────────▼──────────┐
│            SANDBOXED WORKSPACE              │
│  /skills  │  /memory  │  /temp  │ /outputs │
└─────────────────────────────────────────────┘
```

**Key Components**:

1. **Orchestrator**: Main routing brain, spawns specialized agents
2. **Agents**: Ephemeral workers with specific skills (code, research, file ops)
3. **Skill Library**: Reusable Python/JavaScript/Shell scripts created by agents
4. **Memory System**: SQLite + vector database for task history and learning
5. **Approval Queue**: Human-in-the-loop for self-modifications
6. **Model Router**: LiteLLM gateway supporting local (Ollama) and cloud (Claude, GPT)

---

## Features

### ✅ Current (Phase 0-2)

- [x] Basic orchestrator with task routing
- [x] Claude API integration with tier-based routing
- [x] SQLite task history and statistics
- [x] Interactive CLI interface
- [x] Cost tracking per model

### 🚧 In Progress (Phase 3-4)

- [ ] Ollama local model integration
- [ ] Specialized agent profiles (Code, Research, FileOps)
- [ ] Sandboxed filesystem with approval gates
- [ ] Skill library system
- [ ] Web dashboard for approval queue

### 🔮 Planned (Phase 5-6)

- [ ] Self-improvement cron jobs
- [ ] Vector memory (ChromaDB)
- [ ] RAG over past tasks
- [ ] Multi-agent collaboration
- [ ] Proactive skill optimization

---

## Project Structure

```
personal-ai-agent/
├── README.md                 # This file
├── SPEC.md                   # Technical specifications
├── DEVELOPMENT.md            # Development guide
├── requirements.txt          # Python dependencies
├── setup.py                  # Package configuration
│
├── agent/                    # Main application code
│   ├── __init__.py
│   ├── orchestrator.py      # Main orchestrator logic
│   ├── router.py            # Model routing (LiteLLM)
│   ├── database.py          # SQLite task storage
│   ├── sandbox.py           # File sandboxing
│   │
│   ├── agents/              # Specialized agent implementations
│   │   ├── __init__.py
│   │   ├── base.py          # Base agent class
│   │   ├── code_agent.py    # Code generation agent
│   │   ├── research_agent.py # Web research agent
│   │   └── fileops_agent.py # File operations agent
│   │
│   ├── memory/              # Memory and learning systems
│   │   ├── __init__.py
│   │   ├── task_history.py  # SQLite task logging
│   │   ├── vector_store.py  # ChromaDB semantic memory
│   │   └── skill_registry.py # Skill management
│   │
│   ├── tools/               # Tool implementations
│   │   ├── __init__.py
│   │   ├── web_search.py
│   │   ├── file_tools.py
│   │   └── code_exec.py
│   │
│   └── api/                 # Web API (FastAPI)
│       ├── __init__.py
│       ├── app.py           # FastAPI application
│       ├── routes/
│       └── models/
│
├── config/                   # Configuration files
│   ├── litellm.yaml         # Model routing config
│   ├── agents/              # Agent profile definitions
│   │   ├── code_agent.yaml
│   │   ├── research_agent.yaml
│   │   └── fileops_agent.yaml
│   └── tools.yaml           # Tool configurations
│
├── workspace/               # Sandboxed agent workspace
│   ├── skills/              # Agent-created skills
│   ├── memory/              # Persistent memory files
│   ├── temp/                # Temporary scratch space
│   └── outputs/             # User-facing outputs
│
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/                 # Utility scripts
│   ├── setup_ollama.sh     # Install and configure Ollama
│   ├── migrate_db.py       # Database migrations
│   └── benchmark.py        # Performance testing
│
└── docs/                    # Documentation
    ├── architecture.md
    ├── api.md
    ├── agents.md
    └── skills.md
```

---

## Configuration

### Model Configuration (`config/litellm.yaml`)

```yaml
model_list:
  # Local models (free, private)
  - model_name: local-fast
    litellm_params:
      model: ollama/qwen3:1.7b
      api_base: http://localhost:11434
      
  - model_name: local-smart
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://localhost:11434
  
  # Cloud fallback (optional)
  - model_name: cloud-smart
    litellm_params:
      model: claude-sonnet-4-20250514
      api_key: ${ANTHROPIC_API_KEY}

router_settings:
  routing_strategy: "usage-based-routing"
  fallback_models:
    - local-smart
    - cloud-smart
```

### Agent Configuration (`config/agents/code_agent.yaml`)

```yaml
name: CodeAgent
description: Writes Python/JavaScript/Shell skills for the system
model_tier: smart  # Uses local-smart or cloud-smart
max_iterations: 3
approval_required: true

tools:
  - file_write
  - bash_execution
  - skill_validator

system_prompt: |
  You are a code generation specialist. Write clean, tested, 
  documented skills that follow best practices.
  
  Rules:
  1. Include SKILL.md header with usage examples
  2. Add error handling and input validation
  3. Write deterministic, testable code
  4. Never access files outside /skills directory
```

---

## Usage Examples

### CLI Commands

```bash
# Single task execution
python agent.py "Summarize this article: https://example.com/article"

# Force specific model tier
python agent.py --tier smart "Design a database schema for a blog"

# Interactive mode
python agent.py --interactive

# View statistics
python agent.py stats --days 30

# View recent history
python agent.py history --limit 20

# Export task history
python agent.py export --format json --output tasks.json
```

### Python API

```python
from agent import Orchestrator, TaskDatabase

# Initialize
db = TaskDatabase("workspace/memory/tasks.db")
orchestrator = Orchestrator(db=db)

# Execute task
result = await orchestrator.execute_task(
    user_input="Write a Python script to parse CSV files",
    force_tier="smart"
)

print(result.output)
print(f"Used model: {result.model}")
print(f"Tokens: {result.tokens}")
```

### Web API (Future)

```bash
# Start web server
python -m agent.api

# API endpoints
POST   /api/tasks              # Execute task
GET    /api/tasks/{task_id}    # Get task result
GET    /api/approvals          # List pending approvals
POST   /api/approvals/{id}     # Approve/reject proposal
GET    /api/stats              # Usage statistics
```

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agent --cov-report=html

# Run specific test file
pytest tests/unit/test_orchestrator.py

# Run integration tests
pytest tests/integration/ -v
```

### Code Quality

```bash
# Linting
ruff check agent/
black --check agent/

# Type checking
mypy agent/

# Format code
black agent/
ruff check --fix agent/
```

### Adding a New Agent

1. Create agent profile in `config/agents/your_agent.yaml`
2. Implement agent class in `agent/agents/your_agent.py`
3. Register in `agent/agents/__init__.py`
4. Add tests in `tests/unit/test_your_agent.py`
5. Update documentation

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guidelines.

---

## Performance

### Model Performance (Intel i3-10100F NAS, CPU-only)

| Model | Size | Tokens/sec | Use Case |
|-------|------|------------|----------|
| Qwen3-1.7B (Q4) | 1.2GB | 15-25 | Fast classification |
| Qwen3-8B (Q4) | 5GB | 3-8 | General reasoning |
| Llama 3.2-3B (Q4) | 2GB | 10-20 | Summarization |

### Model Performance (Mac Mini M4 Pro, 48GB RAM)

| Model | Size | Tokens/sec | Use Case |
|-------|------|------------|----------|
| Qwen3-30B-A3B (Q4) | 18GB | 40-50 | Primary reasoning |
| Qwen3-8B (Q4) | 5GB | 60-90 | Fast tasks |
| gpt-oss-20b (Q4) | 16GB | 45-60 | Complex analysis |

### Cost Comparison

| Configuration | Monthly Cost | Quality | Speed |
|---------------|--------------|---------|-------|
| 100% Local (NAS) | $0 | Medium | Slow |
| 100% Local (Mac Mini) | $0 | High | Fast |
| Hybrid (Local + Haiku) | $5-15 | High | Fast |
| 100% Cloud (Sonnet) | $50-150 | Highest | Fast |

---

## Security & Privacy

### File Sandboxing

All file operations are restricted to the workspace directory:

```
workspace/
├── skills/      # Agent can write (with approval)
├── memory/      # Agent can read/write
├── temp/        # Agent can read/write
└── outputs/     # Agent can write

/home/user/      # Agent CANNOT access
```

### Approval Gates

Operations requiring human approval:
- Creating new skills
- Modifying agent configurations
- Writing to output directory
- Installing packages
- Running shell commands (optional)

### Data Privacy

- **All personal files isolated** - agent never sees them
- **Local-first architecture** - data stays on your hardware
- **Optional cloud routing** - you control when/if data goes to APIs
- **Audit logging** - all actions logged to SQLite

---

## Roadmap

### Phase 1: Foundation ✅
- [x] Basic orchestrator
- [x] Claude API integration
- [x] Task history database

### Phase 2: Local Models 🚧
- [ ] Ollama integration
- [ ] LiteLLM routing
- [ ] Cost optimization

### Phase 3: Agents & Sandboxing 📋
- [ ] Specialized agent profiles
- [ ] File sandboxing
- [ ] Skill library system

### Phase 4: Self-Improvement 📋
- [ ] Cron-based analysis
- [ ] Skill proposals
- [ ] Approval queue UI

### Phase 5: Memory & Learning 📋
- [ ] Vector database
- [ ] RAG over task history
- [ ] Pattern recognition

### Phase 6: Production Ready 📋
- [ ] Web dashboard
- [ ] Multi-agent orchestration
- [ ] Performance monitoring

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/personal-ai-agent.git
cd personal-ai-agent

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by [OpenClaw](https://openclaw.ai/) architecture
- Built on [LiteLLM](https://github.com/BerriAI/litellm) for model routing
- Uses [Ollama](https://ollama.ai/) for local inference
- Powered by [Qwen](https://github.com/QwenLM) models

---

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/personal-ai-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/personal-ai-agent/discussions)

---

## FAQ

**Q: Do I need an API key?**  
A: No! The system is designed to run 100% locally with Ollama. API keys are optional for cloud fallback.

**Q: What hardware do I need?**  
A: Minimum: 8GB RAM, modern CPU. Recommended: 16GB+ RAM, or Mac with M-series chip for best performance.

**Q: How much does it cost to run?**  
A: $0 if you run locally. Optional cloud API usage: $5-20/month for light use.

**Q: Is my data safe?**  
A: Yes. All file operations are sandboxed. The agent cannot access your personal files unless you explicitly move them into the workspace.

**Q: Can it modify itself?**  
A: Only with your approval. All self-modifications go to an approval queue that you review via web UI or CLI.

**Q: How is this different from OpenClaw?**  
A: We add: file sandboxing, approval gates, orchestrator pattern, and cost optimization. OpenClaw is more powerful but less safe.
