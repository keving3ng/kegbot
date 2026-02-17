# Technical Specifications

> Detailed technical design and implementation specifications for the Personal AI Agent System

Version: 0.1.0  
Last Updated: February 2026

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Models](#data-models)
3. [API Specifications](#api-specifications)
4. [Agent Specifications](#agent-specifications)
5. [Security Model](#security-model)
6. [Performance Requirements](#performance-requirements)
7. [Database Schema](#database-schema)
8. [Configuration Format](#configuration-format)

---

## System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────┐  ┌─────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ CLI      │  │ Web UI      │  │ REST API   │  │ Python SDK │ │
│  └────┬─────┘  └──────┬──────┘  └─────┬──────┘  └─────┬──────┘ │
└───────┼────────────────┼───────────────┼───────────────┼────────┘
        │                │               │               │
        └────────────────┴───────────────┴───────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                     ORCHESTRATION LAYER                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Orchestrator                               │   │
│  │  - Task routing                                          │   │
│  │  - Agent lifecycle management                            │   │
│  │  - Context assembly                                      │   │
│  │  - Result synthesis                                      │   │
│  └─────────────────┬───────────────────────────────────────┘   │
└────────────────────┼────────────────────────────────────────────┘
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
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │CodeAgent │  │Research  │  │FileOps   │  │ Custom Agents    │ │
│  │          │  │Agent     │  │Agent     │  │                  │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────────────┘ │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
┌───────▼─────────────▼─────────────▼─────────────▼───────────────┐
│                      INFRASTRUCTURE LAYER                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │Sandboxed │  │ Memory   │  │ Approval │  │ Model Providers  │ │
│  │Filesystem│  │ System   │  │ Queue    │  │ (Ollama/Claude)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### Data Flow

#### Task Execution Flow

```
User Input
    │
    ├─> 1. Orchestrator receives task
    │       │
    │       ├─> Intent classification (local model, 100ms)
    │       ├─> Similarity search in memory (vector DB, 50ms)
    │       └─> Route decision (heuristics + ML)
    │
    ├─> 2. Agent Selection
    │       │
    │       ├─> Match to agent profile
    │       ├─> Check skill library for existing solution
    │       └─> Spawn agent instance OR execute skill
    │
    ├─> 3. Agent Execution
    │       │
    │       ├─> Load agent context (system prompt + tools)
    │       ├─> Model inference (local or cloud)
    │       ├─> Tool calls (if needed)
    │       │   ├─> Sandbox validation
    │       │   ├─> Approval check (if required)
    │       │   └─> Execute tool
    │       └─> Return result
    │
    ├─> 4. Post-Processing
    │       │
    │       ├─> Save to task history (SQLite)
    │       ├─> Update vector memory (ChromaDB)
    │       ├─> Update skill usage stats
    │       └─> Check for self-improvement triggers
    │
    └─> 5. Return to User
            └─> Format response + metadata
```

#### Self-Improvement Flow

```
Cron Trigger (every 6 hours)
    │
    ├─> 1. Analysis Phase
    │       │
    │       ├─> Query task history (last 6 hours)
    │       ├─> Aggregate statistics
    │       │   ├─> Success/failure rates per agent
    │       │   ├─> Novel task patterns
    │       │   └─> Repeated struggles
    │       └─> Generate analysis (local model)
    │
    ├─> 2. Proposal Phase
    │       │
    │       ├─> If findings warrant improvement:
    │       │   ├─> Spawn CodeAgent
    │       │   ├─> Generate skill code
    │       │   └─> Write rationale
    │       └─> Create ProposedChange object
    │
    ├─> 3. Validation Phase
    │       │
    │       ├─> Lint code (ruff/black)
    │       ├─> Security scan
    │       │   ├─> Check for file access violations
    │       │   ├─> Check for network calls
    │       │   └─> Check for shell injections
    │       └─> Generate test cases
    │
    ├─> 4. Queue for Approval
    │       │
    │       ├─> Insert into approval_queue table
    │       ├─> Trigger notification
    │       └─> Wait for human decision
    │
    └─> 5. Application (after approval)
            │
            ├─> Git commit (version control)
            ├─> Deploy to skills/ directory
            ├─> Reload skill registry
            └─> Log approved change
```

---

## Data Models

### Core Models

#### Task

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Represents a single task execution"""
    
    task_id: str                    # Unique identifier
    user_input: str                 # Original user request
    status: TaskStatus              # Current status
    
    # Execution details
    agent_type: Optional[str]       # Which agent handled it
    model_used: str                 # Which LLM model
    
    # Results
    output: Optional[str]           # Final output
    error: Optional[str]            # Error message if failed
    
    # Metrics
    input_tokens: int = 0
    output_tokens: int = 0
    execution_time_ms: int = 0
    
    # Metadata
    tool_calls: List[Dict] = []     # Tools that were invoked
    context_sources: List[str] = []  # Memory sources used
    
    # Timestamps
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            "task_id": self.task_id,
            "user_input": self.user_input,
            "status": self.status.value,
            "agent_type": self.agent_type,
            "model_used": self.model_used,
            "output": self.output,
            "error": self.error,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "execution_time_ms": self.execution_time_ms,
            "tool_calls": self.tool_calls,
            "context_sources": self.context_sources,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
```

#### Agent

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Agent configuration loaded from YAML"""
    
    name: str                       # Agent identifier
    description: str                # What this agent does
    model_tier: str                 # "local-fast", "local-smart", "cloud-smart"
    
    tools: List[str]                # Tool names available to agent
    max_iterations: int = 5         # Max reasoning loops
    approval_required: bool = False # Require human approval
    
    system_prompt: str              # Agent instructions
    
    # Optional constraints
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    timeout_seconds: Optional[int] = None

@dataclass  
class AgentInstance:
    """Runtime instance of an agent"""
    
    instance_id: str
    config: AgentConfig
    conversation_history: List[Dict]
    
    # State
    iterations_used: int = 0
    tools_called: List[str] = []
    
    # Metrics
    tokens_consumed: int = 0
    start_time: datetime
    
    def can_continue(self) -> bool:
        """Check if agent can make another iteration"""
        return self.iterations_used < self.config.max_iterations
```

#### Skill

```python
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Skill:
    """Represents a reusable skill (script/function)"""
    
    skill_id: str                   # Unique identifier
    name: str                       # Human-readable name
    description: str                # What it does
    
    # Code
    filepath: Path                  # Path to skill file
    language: str                   # "python", "javascript", "bash"
    entry_point: str                # Function/class to execute
    
    # Metadata
    created_by: str                 # Which agent created it
    version: str                    # Semantic version
    tags: List[str]                 # Categorization tags
    
    # Usage tracking
    times_used: int = 0
    success_rate: float = 0.0
    avg_execution_time_ms: int = 0
    
    # Requirements
    dependencies: List[str] = []    # Python packages, etc.
    required_tools: List[str] = []  # Tools skill needs access to
    
    # Validation
    has_tests: bool = False
    last_tested: Optional[datetime] = None
    
    def load_code(self) -> str:
        """Read skill code from file"""
        return self.filepath.read_text()
```

#### ProposedChange

```python
from enum import Enum
from dataclasses import dataclass

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
    """Represents a self-improvement proposal"""
    
    proposal_id: str
    type: ChangeType
    status: ApprovalStatus = ApprovalStatus.PENDING
    
    # Content
    title: str                      # Short description
    rationale: str                  # Why this improvement
    code: Optional[str] = None      # Code if new/modified skill
    config: Optional[Dict] = None   # Config if agent/system change
    
    # Context
    triggered_by: str               # "cron", "user_request", "error"
    analysis_data: Dict = {}        # Supporting data
    
    # Review
    validation_results: Dict = {}   # Linter, tests, security scan
    reviewer_notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None
    
    # Rollback
    rollback_available: bool = True
    previous_version: Optional[str] = None
```

---

## API Specifications

### REST API (FastAPI)

Base URL: `http://localhost:8000/api`

#### Tasks

**POST /api/tasks**

Execute a new task.

Request:
```json
{
  "input": "Write a Python script to parse CSV files",
  "tier": "smart",  // optional: "fast" or "smart"
  "context": {      // optional: additional context
    "files": ["data.csv"],
    "preferences": {}
  }
}
```

Response:
```json
{
  "task_id": "task_1234567890",
  "status": "completed",
  "output": "Here's a Python script...",
  "model_used": "ollama/qwen3:8b",
  "tokens": {
    "input": 45,
    "output": 312
  },
  "execution_time_ms": 2341,
  "agent_type": "CodeAgent"
}
```

**GET /api/tasks/{task_id}**

Get task status and results.

Response:
```json
{
  "task_id": "task_1234567890",
  "status": "completed",
  "user_input": "Write a Python script...",
  "output": "...",
  "created_at": "2026-02-16T10:30:00Z",
  "completed_at": "2026-02-16T10:30:02Z"
}
```

**GET /api/tasks**

List recent tasks.

Query params:
- `limit` (default: 20)
- `status` (optional)
- `agent_type` (optional)

#### Approvals

**GET /api/approvals**

List pending approvals.

Response:
```json
{
  "pending": [
    {
      "proposal_id": "prop_123",
      "type": "new_skill",
      "title": "CSV Parser Skill",
      "rationale": "Repeated requests for CSV parsing detected",
      "created_at": "2026-02-16T08:00:00Z",
      "validation": {
        "linter": "passed",
        "security": "passed",
        "tests": "passed"
      }
    }
  ]
}
```

**POST /api/approvals/{proposal_id}/approve**

Approve a proposed change.

Request:
```json
{
  "notes": "Looks good, approved"
}
```

**POST /api/approvals/{proposal_id}/reject**

Reject a proposed change.

Request:
```json
{
  "reason": "Security concern: accesses /etc/passwd"
}
```

#### Statistics

**GET /api/stats**

Get usage statistics.

Query params:
- `days` (default: 7)

Response:
```json
{
  "period": {
    "start": "2026-02-09T00:00:00Z",
    "end": "2026-02-16T00:00:00Z"
  },
  "tasks": {
    "total": 342,
    "successful": 318,
    "failed": 24,
    "success_rate": 0.93
  },
  "by_model": {
    "ollama/qwen3:8b": {
      "tasks": 280,
      "tokens_in": 45000,
      "tokens_out": 120000
    },
    "claude-sonnet-4": {
      "tasks": 62,
      "tokens_in": 18000,
      "tokens_out": 45000,
      "cost_usd": 2.85
    }
  },
  "by_agent": {
    "CodeAgent": 89,
    "ResearchAgent": 145,
    "FileOpsAgent": 108
  }
}
```

### Python SDK

```python
from agent import Agent, Task

# Initialize
agent = Agent(workspace_path="/home/user/agent-workspace")

# Execute task (synchronous)
result = agent.execute("Write a haiku about coding")
print(result.output)

# Execute task (async)
task = await agent.execute_async("Research quantum computing")
print(task.task_id)

# Check task status
status = agent.get_task_status(task.task_id)

# Get statistics
stats = agent.get_stats(days=30)
print(f"Success rate: {stats['success_rate']:.1%}")

# List approvals
approvals = agent.list_approvals()
for proposal in approvals:
    print(f"{proposal.title}: {proposal.rationale}")

# Approve change
agent.approve_proposal("prop_123", notes="Looks good")
```

---

## Agent Specifications

### Base Agent Interface

All agents must implement:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, config: AgentConfig, orchestrator: Orchestrator):
        self.config = config
        self.orchestrator = orchestrator
        self.model = orchestrator.router.get_model(config.model_tier)
        self.tools = self._load_tools(config.tools)
        self.conversation_history = []
    
    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResult:
        """Execute the agent's task"""
        pass
    
    @abstractmethod
    def validate_result(self, result: Any) -> bool:
        """Validate agent output meets requirements"""
        pass
    
    def _load_tools(self, tool_names: List[str]) -> Dict[str, Tool]:
        """Load tool implementations"""
        tools = {}
        for name in tool_names:
            tools[name] = self.orchestrator.tool_manager.get_tool(name)
        return tools
```

### Agent Profiles

#### CodeAgent

**Purpose**: Write Python/JavaScript/Shell scripts and skills

**Model Tier**: smart (complex reasoning required)

**Tools**:
- `file_write` - Write to /skills directory (requires approval)
- `bash_execution` - Run shell commands (sandboxed)
- `skill_validator` - Lint and test code
- `package_search` - Search PyPI, npm

**Validation**:
- Must include docstring
- Must handle errors
- Must have type hints (Python)
- Passes ruff/black/mypy

#### ResearchAgent

**Purpose**: Web research, documentation reading, synthesis

**Model Tier**: fast (bulk reading, summarization)

**Tools**:
- `web_search` - Search engine API
- `web_fetch` - Retrieve web pages
- `document_parser` - Extract text from PDFs, DOCX
- `summarizer` - Local model summarization

**Validation**:
- Cites sources
- Distinguishes fact from opinion
- Handles 404s gracefully

#### FileOpsAgent

**Purpose**: File system operations within sandbox

**Model Tier**: local-fast (simple, private)

**Tools**:
- `file_read` - Read files (sandbox only)
- `file_list` - List directory contents
- `file_search` - Ripgrep wrapper
- `metadata_extract` - Get file metadata

**Validation**:
- Never accesses paths outside workspace
- Returns structured data (JSON)

---

## Security Model

### Threat Model

**Assets to protect**:
1. User's personal files (home directory, documents, photos)
2. System integrity (OS files, installed applications)
3. Network security (prevent unauthorized connections)
4. API credentials (prevent exfiltration)

**Threat actors**:
1. Malicious skills (from self-improvement or user installation)
2. Prompt injection (adversarial input in documents/emails)
3. Model hallucination (agent makes unsafe decisions)
4. Dependency vulnerabilities (third-party packages)

### Defense Layers

#### Layer 1: Filesystem Sandboxing

```python
# Allowed paths (whitelist)
ALLOWED_PATHS = {
    Path("/home/user/agent-workspace/skills"),
    Path("/home/user/agent-workspace/memory"),
    Path("/home/user/agent-workspace/temp"),
    Path("/home/user/agent-workspace/outputs"),
}

def validate_path(requested_path: str) -> Path:
    """Ensure path is within allowed directories"""
    requested = Path(requested_path).resolve()
    
    for allowed in ALLOWED_PATHS:
        if str(requested).startswith(str(allowed)):
            return requested
    
    raise SecurityError(f"Access denied: {requested_path}")
```

#### Layer 2: Tool Permissions

Each tool declares required capabilities:

```yaml
# tools/web_search.yaml
name: web_search
description: Search the web
permissions:
  - network.http.get
  - network.dns.resolve
dangerous: false
rate_limit: 10/minute
```

Agents can only use tools they're explicitly granted.

#### Layer 3: Approval Gates

Operations requiring human approval:
- Writing to `/outputs` directory
- Creating new skills
- Modifying agent configs
- Running shell commands (configurable)
- Making network requests to new domains (first time)

#### Layer 4: Code Validation

Before applying any self-generated code:

```python
def validate_skill_code(code: str) -> ValidationResult:
    """Security scan for proposed skill"""
    
    issues = []
    
    # 1. Static analysis
    if "os.system" in code:
        issues.append("Direct shell execution detected")
    
    if "eval(" in code or "exec(" in code:
        issues.append("Dynamic code execution detected")
    
    # 2. Path validation
    for match in re.findall(r'["\']([/~][^"\']+)["\']', code):
        if not is_within_workspace(match):
            issues.append(f"Illegal path access: {match}")
    
    # 3. Network access
    suspicious_domains = ["api.attacker.com", "evil.net"]
    for domain in suspicious_domains:
        if domain in code:
            issues.append(f"Suspicious domain: {domain}")
    
    # 4. Secrets detection
    if re.search(r'(password|secret|api_key)\s*=\s*["\'][^"\']+["\']', code):
        issues.append("Hardcoded secret detected")
    
    return ValidationResult(
        passed=len(issues) == 0,
        issues=issues
    )
```

---

## Performance Requirements

### Response Time Targets

| Operation | Target | Maximum |
|-----------|--------|---------|
| Simple task routing | < 100ms | 500ms |
| Local model inference (fast) | < 5s | 15s |
| Local model inference (smart) | < 30s | 60s |
| Cloud API call | < 5s | 15s |
| Database query | < 50ms | 200ms |
| Vector search | < 100ms | 500ms |
| Skill execution | < 10s | 60s |

### Throughput Targets

| Metric | Target |
|--------|--------|
| Concurrent tasks | 5 |
| Tasks per minute | 10 |
| API requests per day | 1000 |

### Resource Limits

**NAS (Intel i3-10100F)**:
- Memory: < 4GB total
- CPU: < 50% average
- Disk: < 10GB for workspace

**Mac Mini M4 Pro**:
- Memory: < 24GB total
- GPU: < 80% average
- Disk: < 50GB for models + workspace

---

## Database Schema

### SQLite Schema

```sql
-- Task execution history
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    user_input TEXT NOT NULL,
    status TEXT NOT NULL,
    agent_type TEXT,
    model_used TEXT NOT NULL,
    
    -- Results
    output TEXT,
    error TEXT,
    
    -- Metrics
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    execution_time_ms INTEGER DEFAULT 0,
    
    -- JSON fields
    tool_calls TEXT,  -- JSON array
    context_sources TEXT,  -- JSON array
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_completed ON tasks(completed_at DESC);
CREATE INDEX idx_tasks_agent ON tasks(agent_type);

-- Skills registry
CREATE TABLE skills (
    skill_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    filepath TEXT NOT NULL,
    language TEXT NOT NULL,
    
    -- Metadata
    created_by TEXT,
    version TEXT DEFAULT '1.0.0',
    tags TEXT,  -- JSON array
    
    -- Usage stats
    times_used INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    avg_execution_time_ms INTEGER DEFAULT 0,
    
    -- Validation
    has_tests BOOLEAN DEFAULT FALSE,
    last_tested TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approval queue
CREATE TABLE approval_queue (
    proposal_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    
    title TEXT NOT NULL,
    rationale TEXT,
    code TEXT,
    config TEXT,  -- JSON
    
    -- Context
    triggered_by TEXT,
    analysis_data TEXT,  -- JSON
    
    -- Validation
    validation_results TEXT,  -- JSON
    
    -- Review
    reviewer_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    applied_at TIMESTAMP
);

-- Agent performance metrics
CREATE TABLE agent_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_type TEXT NOT NULL,
    
    -- Aggregated metrics (updated hourly)
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

### ChromaDB Collections

```python
# Vector memory for semantic search
collection = chroma_client.create_collection(
    name="task_memory",
    metadata={
        "description": "Semantic memory of past tasks",
        "hnsw:space": "cosine"
    }
)

# Document structure
{
    "id": "task_1234567890",
    "embedding": [0.123, 0.456, ...],  # 1536-dim vector
    "document": "User asked: ... Agent responded: ...",
    "metadata": {
        "task_id": "task_1234567890",
        "agent_type": "CodeAgent",
        "success": True,
        "timestamp": "2026-02-16T10:30:00Z",
        "tags": ["python", "csv", "parsing"]
    }
}
```

---

## Configuration Format

### LiteLLM Configuration

```yaml
# config/litellm.yaml
model_list:
  # Local models via Ollama
  - model_name: local-fast
    litellm_params:
      model: ollama/qwen3:1.7b
      api_base: http://localhost:11434
      temperature: 0.3
      max_tokens: 1024
    
  - model_name: local-smart
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://localhost:11434
      temperature: 0.5
      max_tokens: 4096
  
  # Cloud fallback (optional)
  - model_name: cloud-smart
    litellm_params:
      model: claude-sonnet-4-20250514
      api_key: ${ANTHROPIC_API_KEY}
      temperature: 0.7
      max_tokens: 8192

# Routing configuration
router_settings:
  routing_strategy: "usage-based-routing"
  
  # Cost limits
  budget_manager:
    enabled: true
    monthly_budget_usd: 50
    alert_threshold: 0.8
  
  # Caching
  cache_responses: true
  cache_ttl_seconds: 3600
  
  # Fallback chains
  fallbacks:
    - model: local-smart
      fallback: cloud-smart
      conditions:
        - error_type: timeout
        - confidence_score: < 0.7
```

### Agent Configuration

```yaml
# config/agents/code_agent.yaml
name: CodeAgent
description: Writes Python/JavaScript/Shell skills

# Model selection
model_tier: smart  # Maps to local-smart or cloud-smart

# Behavior
max_iterations: 3
timeout_seconds: 300
approval_required: true

# Tools available to this agent
tools:
  - file_write
  - bash_execution
  - skill_validator
  - package_search

# LLM parameters
temperature: 0.3
max_tokens: 4096

# System prompt
system_prompt: |
  You are a code generation specialist. Your job is to write high-quality,
  tested, documented skills for the agent system.
  
  Follow these rules:
  1. Include comprehensive docstrings with examples
  2. Add type hints for all function parameters
  3. Implement error handling for edge cases
  4. Write deterministic, testable code
  5. Never access files outside /skills directory
  6. Use standard libraries when possible
  
  Output format:
  - Skill code with SKILL.md header
  - Usage examples
  - Test cases

# Validation rules
validation:
  required_docstring: true
  require_type_hints: true
  max_file_size_kb: 100
  allowed_imports:
    - re
    - json
    - pathlib
    - typing
    - dataclasses
  blocked_imports:
    - os.system
    - eval
    - exec
```

---

## Testing Requirements

### Unit Tests

Minimum coverage: 80%

```python
# tests/unit/test_orchestrator.py
import pytest
from agent.orchestrator import Orchestrator

def test_task_routing_simple():
    """Test that simple tasks route to fast model"""
    orchestrator = Orchestrator()
    task = "Summarize this article"
    
    tier = orchestrator.router.decide_tier(task)
    assert tier == "fast"

def test_task_routing_complex():
    """Test that complex tasks route to smart model"""
    orchestrator = Orchestrator()
    task = "Write a comprehensive analysis of quantum computing"
    
    tier = orchestrator.router.decide_tier(task)
    assert tier == "smart"
```

### Integration Tests

```python
# tests/integration/test_agent_execution.py
import pytest
from agent import Agent

@pytest.mark.integration
async def test_code_agent_skill_creation():
    """Test CodeAgent can create a valid skill"""
    agent = Agent()
    
    result = await agent.execute(
        "Create a skill that parses CSV files"
    )
    
    assert result.success
    assert "def parse_csv" in result.output
    assert result.agent_type == "CodeAgent"
```

### Performance Tests

```python
# tests/performance/test_response_time.py
import pytest
import time

@pytest.mark.performance
def test_routing_latency():
    """Ensure routing decision is fast"""
    orchestrator = Orchestrator()
    
    start = time.time()
    tier = orchestrator.router.decide_tier("Write code")
    latency_ms = (time.time() - start) * 1000
    
    assert latency_ms < 100  # Must be under 100ms
```

---

## Deployment

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...  # Optional if using local-only

# Optional
WORKSPACE_PATH=/home/user/agent-workspace
DATABASE_PATH=/home/user/agent-workspace/memory/tasks.db
OLLAMA_HOST=http://localhost:11434
LOG_LEVEL=INFO
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy application
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create workspace
RUN mkdir -p /workspace/{skills,memory,temp,outputs}

# Run
CMD ["python", "-m", "agent.api"]
```

---

## Monitoring & Observability

### Metrics to Track

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Task metrics
tasks_total = Counter('tasks_total', 'Total tasks executed', ['agent', 'status'])
task_duration = Histogram('task_duration_seconds', 'Task execution time')
active_tasks = Gauge('active_tasks', 'Currently executing tasks')

# Model metrics
model_requests = Counter('model_requests', 'LLM requests', ['model', 'tier'])
model_tokens = Counter('model_tokens', 'Tokens used', ['model', 'direction'])
model_cost = Counter('model_cost_usd', 'Estimated cost in USD', ['model'])

# Agent metrics
agent_iterations = Histogram('agent_iterations', 'Iterations per task', ['agent'])
agent_tool_calls = Counter('agent_tool_calls', 'Tool calls made', ['agent', 'tool'])
```

### Logging

```python
import structlog

logger = structlog.get_logger()

# Structured logging
logger.info(
    "task_completed",
    task_id=task.task_id,
    agent_type=task.agent_type,
    execution_time_ms=task.execution_time_ms,
    success=task.status == TaskStatus.COMPLETED
)
```

---

This specification provides the technical foundation for building the system. Each section can be expanded as implementation progresses.
