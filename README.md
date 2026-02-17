# Personal AI Agent System

> A self-improving, privacy-focused AI agent orchestrator that runs on local hardware with optional cloud model fallback

## What This Is

An autonomous AI agent system for personal use that:

- **Orchestrates specialized agents** for different task types (code, research, file operations)
- **Runs primarily on local models** (Ollama) to minimize API costs and maximize privacy
- **Sandboxes all file operations** to prevent access to personal data
- **Self-improves with human approval** - proposes new skills and optimizations

**Philosophy**: Privacy-first, cost-conscious, extensible, and transparent. You control what the agent can access and approve all self-modifications.

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

## Tech Stack

- **Python 3.11+** - Implementation language
- **Ollama** - Local model inference (Qwen3 1.7B/8B)
- **LiteLLM** - Model routing abstraction (local + cloud)
- **Anthropic Claude API** - Cloud fallback
- **SQLite** - Task history and metadata
- **ChromaDB** - Vector memory (future)
- **FastAPI** - Web API (future)
- **Click** - CLI framework
- **Pydantic** - Data validation

## Current Status

**Pre-implementation.** The architecture, data models, security model, and roadmap are defined. No application code has been written yet. See [docs/roadmap.md](docs/roadmap.md) for the implementation plan.

## Documentation

- **[docs/spec.md](docs/spec.md)** - Technical spec: data models, API design, security model, database schema
- **[docs/dev-guide.md](docs/dev-guide.md)** - Development setup and coding standards
- **[docs/roadmap.md](docs/roadmap.md)** - Implementation phases and task breakdown

