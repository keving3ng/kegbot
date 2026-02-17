# Implementation Roadmap

> Step-by-step plan for building the Personal AI Agent System

---

## Overview

| Phase | Focus | Key Deliverable |
|-------|-------|-----------------|
| 1 | Foundation | Working CLI agent with Claude API |
| 2 | Local Models | Ollama + LiteLLM routing, cost reduction |
| 3 | Agents & Sandboxing | Specialized agents, file sandboxing |
| 4 | Skill System | Reusable skill creation and execution |
| 5 | Self-Improvement | Cron analysis, proposal generation, approval queue |
| 6 | Web Interface | FastAPI dashboard, WebSocket updates |
| 7 | Memory & RAG | ChromaDB vector search over past tasks |

---

## Phase 1: Foundation

**Goal**: Basic CLI agent that routes to cloud API.

- Project structure (`agent/` package with `__init__.py`)
- Orchestrator class with task routing
- Claude API integration via `anthropic` SDK
- CLI interface with Click (interactive + single-task modes)
- SQLite task history and statistics
- Simple routing: fast vs smart tier
- Cost tracking per model

**Deliverable**: `python agent.py "your task"` works end-to-end.

---

## Phase 2: Local Models

**Goal**: Add Ollama for local inference, reduce API costs.

- Install and configure Ollama with Qwen3 models (1.7B for classification, 8B for reasoning)
- LiteLLM Router with `config/litellm.yaml`
- Intent classification using local model to decide routing
- Confidence scoring - low confidence falls back to cloud
- Track local vs cloud usage in cost stats
- Response caching for repeated queries

**Deliverable**: Simple tasks handled locally at zero cost, complex tasks routed to cloud.

---

## Phase 3: Agents & Sandboxing

**Goal**: Specialized agents with sandboxed file operations.

- `BaseAgent` abstract class with `execute()` and `validate_result()`
- Agent registry and YAML-based configuration loader
- CodeAgent (smart tier): writes scripts, validates with linter
- ResearchAgent (fast tier): web search, fetch, summarize
- FileOpsAgent (local-fast): file read/list/search within sandbox
- `SandboxedFileSystem` class with path whitelist validation
- Approval gates for sensitive operations
- Orchestrator updated to spawn and manage agents

**Deliverable**: Tasks automatically route to the right specialized agent. File access restricted to workspace.

---

## Phase 4: Skill System

**Goal**: Agents can create and reuse skills (scripts/functions).

- `Skill` data model and `skills` database table
- `SkillRegistry` for loading, searching, and executing skills
- Skill templates (Python, JavaScript, Bash) with standard header
- Validation pipeline: linting, security scan, path checks
- Safe execution with timeout and stdout/stderr capture
- Usage tracking and success rate metrics

**Deliverable**: CodeAgent creates a skill, skill is persisted and reusable for future tasks.

---

## Phase 5: Self-Improvement

**Goal**: Proactive analysis and improvement proposals with human approval.

- APScheduler cron job running every 6 hours
- Analysis of recent task history: novel patterns, repeated failures, optimization opportunities
- CodeAgent generates improvement proposals with code + rationale
- Validation pipeline runs on proposals (lint, security, tests)
- Approval queue in SQLite with pending/approved/rejected status
- Approved changes committed via git, deployed to skills/, registry reloaded
- Rollback support for applied changes

**Deliverable**: System proposes improvements automatically, applies them only after human approval.

---

## Phase 6: Web Interface

**Goal**: Web dashboard for approvals and monitoring.

- FastAPI app with REST endpoints (see spec.md for API design)
- Static HTML + JavaScript frontend with Tailwind CSS
- Approval interface: list proposals, view diffs, approve/reject
- Task execution and statistics views
- WebSocket for real-time task progress and notifications

**Deliverable**: Web UI at `http://localhost:8000`.

---

## Phase 7: Memory & RAG

**Goal**: Semantic memory and learning from experience.

- ChromaDB collection for task embeddings
- Embedding generation on task completion
- Semantic search for similar past tasks during context assembly
- Relevance ranking and token budget management
- Track skill performance over time, trigger retraining proposals

**Deliverable**: Agent improves over time by learning from past task results.

---

## Success Criteria

- 80%+ test coverage
- 90%+ task success rate
- Local routing reduces cloud API costs by 30-40%
- All self-modifications require human approval
- Zero unauthorized file access outside workspace
