# Technical Specifications

> Core technical design for the Personal AI Agent System

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────┐  ┌─────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ CLI      │  │ Web UI      │  │ REST API   │  │ Python SDK │ │
│  └────┬─────┘  └──────┬──────┘  └─────┬──────┘  └─────┬──────┘ │
└───────┼────────────────┼───────────────┼───────────────┼────────┘
        └────────────────┴───────────────┴───────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                     ORCHESTRATION LAYER                          │
│  - Task routing and intent classification                       │
│  - Agent lifecycle management                                    │
│  - Context assembly from memory                                  │
│  - Result synthesis                                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────────┐
│ LiteLLM      │ │ Agent   │ │ Tool        │
│ Router       │ │ Registry│ │ Manager     │
└───────┬──────┘ └──┬──────┘ └──┬──────────┘
        │           │            │
┌───────▼───────────▼────────────▼─────────────────────────────────┐
│                      EXECUTION LAYER                              │
│  CodeAgent  │  ResearchAgent  │  FileOpsAgent  │  Custom Agents  │
└───────┬───────────┬───────────────┬───────────────┬──────────────┘
        │           │               │               │
┌───────▼───────────▼───────────────▼───────────────▼──────────────┐
│                      INFRASTRUCTURE LAYER                         │
│  Sandboxed Filesystem │ Memory System │ Approval Queue │ Models  │
└───────────────────────────────────────────────────────────────────┘
```

### Task Execution Flow

1. **Orchestrator** receives user input
2. **Intent classification** via local model (~100ms) determines task type
3. **Memory search** finds similar past tasks for context
4. **Agent selection** based on task type → spawn appropriate agent
5. **Agent execution** with model inference + tool calls (sandboxed)
6. **Post-processing**: save to task history, update vector memory, check for self-improvement triggers
7. **Return** formatted response to user

### Self-Improvement Flow

1. **Cron trigger** (every 6 hours) queries recent task history
2. **Analysis** identifies novel patterns, repeated failures, optimization opportunities
3. **Proposal generation** via CodeAgent - produces skill code + rationale
4. **Validation** - lint, security scan, test generation
5. **Approval queue** - human reviews and approves/rejects
6. **Application** - git commit, deploy to skills/, reload registry

---

## Data Models

### Task

```python
class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    task_id: str
    user_input: str
    status: TaskStatus
    agent_type: Optional[str]
    model_used: str
    output: Optional[str]
    error: Optional[str]
    input_tokens: int = 0
    output_tokens: int = 0
    execution_time_ms: int = 0
    tool_calls: List[Dict] = []
    context_sources: List[str] = []
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

### AgentConfig

```python
@dataclass
class AgentConfig:
    name: str
    description: str
    model_tier: str              # "local-fast", "local-smart", "cloud-smart"
    tools: List[str]
    max_iterations: int = 5
    approval_required: bool = False
    system_prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    timeout_seconds: Optional[int] = None
```

### Skill

```python
@dataclass
class Skill:
    skill_id: str
    name: str
    description: str
    filepath: Path
    language: str                # "python", "javascript", "bash"
    entry_point: str
    created_by: str
    version: str
    tags: List[str]
    times_used: int = 0
    success_rate: float = 0.0
    avg_execution_time_ms: int = 0
    dependencies: List[str] = []
    has_tests: bool = False
```

### ProposedChange

```python
class ChangeType(Enum):
    NEW_SKILL = "new_skill"
    MODIFY_SKILL = "modify_skill"
    NEW_AGENT = "new_agent"
    MODIFY_AGENT = "modify_agent"
    CONFIG_CHANGE = "config_change"

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"

@dataclass
class ProposedChange:
    proposal_id: str
    type: ChangeType
    status: ApprovalStatus = ApprovalStatus.PENDING
    title: str
    rationale: str
    code: Optional[str] = None
    config: Optional[Dict] = None
    triggered_by: str            # "cron", "user_request", "error"
    analysis_data: Dict = {}
    validation_results: Dict = {}
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None
    rollback_available: bool = True
    previous_version: Optional[str] = None
```

---

## Agent Specifications

### Base Agent Interface

```python
class BaseAgent(ABC):
    def __init__(self, config: AgentConfig, orchestrator: Orchestrator):
        self.config = config
        self.orchestrator = orchestrator
        self.model = orchestrator.router.get_model(config.model_tier)
        self.tools = self._load_tools(config.tools)

    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResult:
        pass

    @abstractmethod
    def validate_result(self, result: Any) -> bool:
        pass
```

### Agent Profiles

| Agent | Purpose | Model Tier | Tools | Key Validation |
|-------|---------|-----------|-------|----------------|
| **CodeAgent** | Write scripts and skills | smart | file_write, bash_execution, skill_validator, package_search | Docstrings, type hints, passes linter |
| **ResearchAgent** | Web research and synthesis | fast | web_search, web_fetch, document_parser, summarizer | Cites sources, handles 404s |
| **FileOpsAgent** | Sandboxed file operations | local-fast | file_read, file_list, file_search, metadata_extract | Never accesses paths outside workspace |

---

## Security Model

### What We Protect

1. User's personal files (home directory, documents, photos)
2. System integrity (OS files, installed applications)
3. Network security (prevent unauthorized connections)
4. API credentials (prevent exfiltration)

### Defense Layers

**Layer 1 - Filesystem Sandboxing**: Whitelist of allowed paths under workspace. All file operations validated against this list. Path traversal attacks blocked via `Path.resolve()`.

**Layer 2 - Tool Permissions**: Each tool declares capabilities. Agents can only use tools they're explicitly granted. Rate limiting per tool.

**Layer 3 - Approval Gates**: Human approval required for: writing to `/outputs`, creating skills, modifying agent configs, running shell commands, first-time domain access.

**Layer 4 - Code Validation**: Static analysis on all self-generated code. Blocks `os.system`, `eval`, `exec`, paths outside workspace, hardcoded secrets, suspicious domains.

---

## REST API

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tasks` | Execute a new task |
| `GET` | `/api/tasks/{task_id}` | Get task status/results |
| `GET` | `/api/tasks` | List recent tasks (params: `limit`, `status`, `agent_type`) |
| `GET` | `/api/approvals` | List pending approvals |
| `POST` | `/api/approvals/{id}/approve` | Approve a proposed change |
| `POST` | `/api/approvals/{id}/reject` | Reject a proposed change |
| `GET` | `/api/stats` | Usage statistics (param: `days`) |

---

## Database Schema

### SQLite

```sql
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    user_input TEXT NOT NULL,
    status TEXT NOT NULL,
    agent_type TEXT,
    model_used TEXT NOT NULL,
    output TEXT,
    error TEXT,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    execution_time_ms INTEGER DEFAULT 0,
    tool_calls TEXT,          -- JSON array
    context_sources TEXT,     -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_completed ON tasks(completed_at DESC);
CREATE INDEX idx_tasks_agent ON tasks(agent_type);

CREATE TABLE skills (
    skill_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    filepath TEXT NOT NULL,
    language TEXT NOT NULL,
    created_by TEXT,
    version TEXT DEFAULT '1.0.0',
    tags TEXT,                -- JSON array
    times_used INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    avg_execution_time_ms INTEGER DEFAULT 0,
    has_tests BOOLEAN DEFAULT FALSE,
    last_tested TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE approval_queue (
    proposal_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    title TEXT NOT NULL,
    rationale TEXT,
    code TEXT,
    config TEXT,              -- JSON
    triggered_by TEXT,
    analysis_data TEXT,       -- JSON
    validation_results TEXT,  -- JSON
    reviewer_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    applied_at TIMESTAMP
);

CREATE TABLE agent_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_type TEXT NOT NULL,
    total_tasks INTEGER DEFAULT 0,
    successful_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    avg_tokens_in INTEGER DEFAULT 0,
    avg_tokens_out INTEGER DEFAULT 0,
    avg_execution_time_ms INTEGER DEFAULT 0,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    UNIQUE(agent_type, period_start)
);
```

### ChromaDB (Phase 6)

Collection `task_memory` with cosine similarity. Each document stores the task input/output pair with metadata (agent_type, success, timestamp, tags) for semantic search over past tasks.

---

## Configuration

### Model Routing (`config/litellm.yaml`)

```yaml
model_list:
  - model_name: local-fast
    litellm_params:
      model: ollama/qwen3:1.7b
      api_base: http://localhost:11434

  - model_name: local-smart
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://localhost:11434

  - model_name: cloud-smart
    litellm_params:
      model: claude-sonnet-4-20250514
      api_key: ${ANTHROPIC_API_KEY}

router_settings:
  routing_strategy: "usage-based-routing"
  fallbacks:
    - model: local-smart
      fallback: cloud-smart
```

### Agent Profile (`config/agents/code_agent.yaml`)

```yaml
name: CodeAgent
description: Writes Python/JavaScript/Shell skills
model_tier: smart
max_iterations: 3
timeout_seconds: 300
approval_required: true

tools:
  - file_write
  - bash_execution
  - skill_validator
  - package_search

system_prompt: |
  You are a code generation specialist. Write high-quality,
  tested, documented skills for the agent system.
  Never access files outside /skills directory.
```
