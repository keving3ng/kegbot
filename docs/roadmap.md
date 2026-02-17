# Implementation Roadmap

> Step-by-step guide to building the Personal AI Agent System from scratch

**Current Version**: 0.1.0  
**Target**: Production-ready v1.0.0

---

## Phase 0: Foundation (Week 1) ✅

**Goal**: Basic CLI agent that routes to cloud API

**Status**: COMPLETED (basic version provided)

### Tasks

- [x] Project structure setup
- [x] Basic orchestrator class
- [x] Claude API integration
- [x] CLI interface with Click
- [x] SQLite task history
- [x] Simple routing (fast vs smart)
- [x] Statistics command
- [x] Cost tracking

**Deliverable**: `python agent.py "your task"` works

---

## Phase 1: Local Models (Week 2) 🚧

**Goal**: Add Ollama for local inference, reduce API costs by 30-40%

### Tasks

#### 1.1 Ollama Integration

- [ ] Install Ollama on NAS
- [ ] Pull models: `qwen3:1.7b`, `qwen3:8b`
- [ ] Test inference speed
- [ ] Document hardware-specific performance

```bash
# Acceptance criteria
ollama run qwen3:1.7b "Classify this: ..."
# Response in < 15 seconds
```

#### 1.2 LiteLLM Router

- [ ] Install LiteLLM: `pip install litellm`
- [ ] Create `config/litellm.yaml`
- [ ] Add Ollama models to config
- [ ] Add Claude fallback models
- [ ] Implement `ModelRouter` class

```python
# Acceptance criteria
from litellm import Router
router = Router(model_list=config)
response = router.completion(
    model="local-fast",
    messages=[...]
)
```

#### 1.3 Routing Logic

- [ ] Implement intent classification with local model
- [ ] Add confidence scoring
- [ ] Route low-confidence to cloud
- [ ] Update orchestrator to use router

```python
# Acceptance criteria
# Simple task → local model (0 API cost)
# Complex task → cloud model (API cost)
# Log which model handled each task
```

#### 1.4 Cost Optimization

- [ ] Track local vs cloud usage
- [ ] Add cost comparison stats
- [ ] Implement response caching
- [ ] Add semantic deduplication

**Deliverable**: 30-40% reduction in API costs

**Testing Checklist**:
- [ ] 10 simple tasks → all local
- [ ] 10 complex tasks → all cloud
- [ ] 10 medium tasks → mixed routing
- [ ] Cost tracking shows savings

---

## Phase 2: Agents & Sandboxing (Week 3-4)

**Goal**: Specialized agents with sandboxed file operations

### Tasks

#### 2.1 Base Agent Framework

- [ ] Create `BaseAgent` abstract class
- [ ] Implement agent lifecycle methods
- [ ] Add tool loading system
- [ ] Create agent registry

```python
# agent/agents/base.py
class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, task, context) -> AgentResult:
        pass
```

#### 2.2 Agent Profiles

- [ ] Create `config/agents/` directory
- [ ] Write `code_agent.yaml`
- [ ] Write `research_agent.yaml`
- [ ] Write `fileops_agent.yaml`
- [ ] Implement YAML loader

#### 2.3 CodeAgent

- [ ] Implement `CodeAgent` class
- [ ] Add file_write tool (sandboxed)
- [ ] Add code validation tool
- [ ] Add skill template generator

```python
# Acceptance criteria
result = await code_agent.execute(
    "Write a Python function to parse JSON"
)
assert "def parse_json" in result.output
```

#### 2.4 ResearchAgent

- [ ] Implement `ResearchAgent` class
- [ ] Add web_search tool
- [ ] Add web_fetch tool
- [ ] Add summarization with local model

#### 2.5 FileOpsAgent

- [ ] Implement `FileOpsAgent` class
- [ ] Add file_read tool
- [ ] Add file_list tool
- [ ] Add file_search tool (ripgrep)

#### 2.6 File Sandboxing

- [ ] Create `SandboxedFileSystem` class
- [ ] Implement path validation
- [ ] Add allowed/blocked path lists
- [ ] Implement approval gates

```python
# Acceptance criteria
fs = SandboxedFileSystem("/home/user/workspace")

# These work:
fs.read_file("skills/my_skill.py")
fs.write_file("outputs/result.txt", "...")

# These fail:
fs.read_file("/etc/passwd")  # SecurityError
fs.write_file("../../secrets.txt", "...")  # SecurityError
```

#### 2.7 Orchestrator Integration

- [ ] Update orchestrator to spawn agents
- [ ] Implement agent selection logic
- [ ] Add agent result synthesis
- [ ] Track which agent handled each task

**Deliverable**: Orchestrator routes tasks to specialized agents

**Testing Checklist**:
- [ ] "Write code" → CodeAgent spawned
- [ ] "Research topic" → ResearchAgent spawned
- [ ] "Find files" → FileOpsAgent spawned
- [ ] Sandbox prevents /etc access
- [ ] Sandbox allows workspace access

---

## Phase 3: Skill System (Week 5)

**Goal**: Agents can create and execute reusable skills

### Tasks

#### 3.1 Skill Data Model

- [ ] Create `Skill` dataclass
- [ ] Design skills table schema
- [ ] Implement skill serialization

#### 3.2 Skill Registry

- [ ] Create `SkillRegistry` class
- [ ] Implement skill loading from disk
- [ ] Add skill search/matching
- [ ] Track usage statistics

```python
# Acceptance criteria
registry = SkillRegistry("workspace/skills")
skill = registry.find_match("parse CSV files")
if skill:
    result = registry.execute_skill(skill, params)
```

#### 3.3 Skill Templates

- [ ] Create SKILL.md template
- [ ] Add Python skill template
- [ ] Add JavaScript skill template
- [ ] Add Bash skill template

#### 3.4 Skill Validation

- [ ] Implement linting (ruff/black)
- [ ] Add security scanning
- [ ] Check for illegal imports
- [ ] Validate file paths

#### 3.5 Skill Execution

- [ ] Implement safe Python execution
- [ ] Add timeout handling
- [ ] Capture stdout/stderr
- [ ] Log execution metrics

**Deliverable**: Agent creates skill, skill is reusable

**Testing Checklist**:
- [ ] CodeAgent creates CSV parser skill
- [ ] Skill saved to workspace/skills/
- [ ] Skill appears in registry
- [ ] Can execute skill directly
- [ ] Skill fails validation if unsafe

---

## Phase 4: Self-Improvement (Week 6)

**Goal**: Proactive analysis and improvement proposals

### Tasks

#### 4.1 Cron Scheduler

- [ ] Install APScheduler
- [ ] Create scheduler service
- [ ] Add configuration for intervals
- [ ] Implement graceful shutdown

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    self_improve,
    'interval',
    hours=6
)
scheduler.start()
```

#### 4.2 Analysis Logic

- [ ] Query recent task history
- [ ] Identify novel tasks
- [ ] Detect repeated failures
- [ ] Find optimization opportunities

```python
# Acceptance criteria
analysis = analyze_recent_tasks(hours=6)
assert "novel_tasks" in analysis
assert "repeated_failures" in analysis
assert "suggestions" in analysis
```

#### 4.3 Proposal Generation

- [ ] Spawn CodeAgent for proposals
- [ ] Generate improvement code
- [ ] Write rationale/explanation
- [ ] Create test cases

#### 4.4 Approval Queue

- [ ] Create approval_queue table
- [ ] Implement `ProposedChange` model
- [ ] Add approval queue manager
- [ ] Implement notifications

#### 4.5 Validation Pipeline

- [ ] Run linter on proposals
- [ ] Security scan
- [ ] Test execution (if tests provided)
- [ ] Generate validation report

#### 4.6 Application Logic

- [ ] Implement git commit workflow
- [ ] Deploy approved skills
- [ ] Update skill registry
- [ ] Log applied changes
- [ ] Support rollback

**Deliverable**: System proposes improvements automatically

**Testing Checklist**:
- [ ] Cron triggers after 6 hours
- [ ] Analysis detects novel patterns
- [ ] Proposal created and queued
- [ ] Validation runs successfully
- [ ] Approval applies change
- [ ] Skill is usable immediately

---

## Phase 5: Web Interface (Week 7)

**Goal**: Web dashboard for approvals and monitoring

### Tasks

#### 5.1 FastAPI Setup

- [ ] Create FastAPI app
- [ ] Define API routes
- [ ] Add CORS middleware
- [ ] Implement error handling

#### 5.2 API Endpoints

- [ ] `POST /api/tasks` - Execute task
- [ ] `GET /api/tasks/{id}` - Get task status
- [ ] `GET /api/approvals` - List approvals
- [ ] `POST /api/approvals/{id}/approve`
- [ ] `GET /api/stats` - Usage statistics

#### 5.3 Frontend (Simple)

- [ ] Create static HTML template
- [ ] Add JavaScript for API calls
- [ ] Style with Tailwind CSS
- [ ] Make responsive

```html
<!-- Simple approval interface -->
<div id="approvals">
  <!-- List of pending proposals -->
  <!-- Approve/Reject buttons -->
  <!-- Code diff viewer -->
</div>
```

#### 5.4 WebSocket Support

- [ ] Add WebSocket endpoint
- [ ] Stream task progress
- [ ] Real-time approval notifications
- [ ] Live stats updates

**Deliverable**: Web UI at `http://localhost:8000`

**Testing Checklist**:
- [ ] Can execute task via web UI
- [ ] Approvals list appears
- [ ] Can approve/reject proposals
- [ ] Stats page shows metrics
- [ ] WebSocket updates work

---

## Phase 6: Memory & RAG (Week 8)

**Goal**: Semantic memory and learning from experience

### Tasks

#### 6.1 Vector Database

- [ ] Install ChromaDB
- [ ] Create collection schema
- [ ] Implement embedding generation
- [ ] Add semantic search

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("task_memory")

# Store task
collection.add(
    ids=[task_id],
    embeddings=[embedding],
    documents=[task.output],
    metadatas=[{"success": True}]
)

# Search similar
results = collection.query(
    query_texts=["How do I parse CSV?"],
    n_results=5
)
```

#### 6.2 Memory Integration

- [ ] Hook into task completion
- [ ] Generate embeddings
- [ ] Store in vector DB
- [ ] Update on deletions

#### 6.3 Context Assembly

- [ ] Search for similar past tasks
- [ ] Rank by relevance
- [ ] Include in agent context
- [ ] Limit token usage

```python
# Before executing task:
similar_tasks = memory.search(user_input, top_k=5)
context = build_context(similar_tasks)
# Include context in agent prompt
```

#### 6.4 Learning Loops

- [ ] Track skill success rates
- [ ] Identify underperforming skills
- [ ] Trigger retraining proposals
- [ ] Update skill rankings

**Deliverable**: Agent learns from past tasks

**Testing Checklist**:
- [ ] Ask same question twice
- [ ] Second response uses first as context
- [ ] Similar questions get similar answers
- [ ] Context relevance improves over time

---

## Phase 7: Production Ready (Week 9)

**Goal**: Polish, documentation, deployment

### Tasks

#### 7.1 Error Handling

- [ ] Add retry logic with exponential backoff
- [ ] Implement circuit breakers
- [ ] Add graceful degradation
- [ ] Log all errors properly

#### 7.2 Monitoring

- [ ] Add Prometheus metrics
- [ ] Create Grafana dashboard
- [ ] Set up alerts (optional)
- [ ] Add health check endpoint

#### 7.3 Documentation

- [ ] Complete API documentation
- [ ] Write user guide
- [ ] Create video walkthrough
- [ ] Add troubleshooting guide

#### 7.4 Docker Support

- [ ] Create Dockerfile
- [ ] Add docker-compose.yml
- [ ] Test container deployment
- [ ] Document Docker setup

#### 7.5 CI/CD

- [ ] GitHub Actions workflow
- [ ] Automated testing
- [ ] Code quality checks
- [ ] Automated releases

**Deliverable**: Production-ready v1.0.0

---

## Future Enhancements (Post-1.0)

### Performance Optimizations

- [ ] Model quantization experiments
- [ ] Response streaming
- [ ] Parallel agent execution
- [ ] Database connection pooling

### Advanced Features

- [ ] Multi-agent collaboration
- [ ] Voice interface
- [ ] Mobile app companion
- [ ] Browser extension

### Enterprise Features

- [ ] Multi-user support
- [ ] RBAC (role-based access control)
- [ ] SSO integration
- [ ] Audit log export
- [ ] Compliance reports (SOC2, GDPR)

### Model Upgrades

- [ ] Support for Mac Mini M4 Pro
- [ ] Qwen3-30B-A3B integration
- [ ] Model hot-swapping
- [ ] A/B testing framework

---

## Success Criteria

### Technical Metrics

- [ ] 80%+ test coverage
- [ ] < 5s average response time
- [ ] < 5% error rate
- [ ] Zero critical security issues

### User Metrics

- [ ] 30-40% cost reduction (Phase 1)
- [ ] 70%+ approval rate for proposals
- [ ] 90%+ task success rate
- [ ] Positive user feedback

### Documentation

- [ ] All APIs documented
- [ ] User guide complete
- [ ] Architecture documented
- [ ] Contribution guide ready

---

## Timeline Summary

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 0 - Foundation | 1 week | Working CLI agent |
| 1 - Local Models | 1 week | 30% cost reduction |
| 2 - Agents | 2 weeks | Specialized agents |
| 3 - Skills | 1 week | Skill system |
| 4 - Self-Improve | 1 week | Auto-improvement |
| 5 - Web UI | 1 week | Dashboard |
| 6 - Memory | 1 week | RAG system |
| 7 - Production | 1 week | v1.0.0 release |
| **Total** | **9 weeks** | **Production ready** |

---

## Risk Mitigation

### Technical Risks

**Risk**: Local models too slow on NAS  
**Mitigation**: Start with smallest models, upgrade hardware if needed

**Risk**: API costs too high  
**Mitigation**: Phase 1 adds local routing, reduces costs 30-40%

**Risk**: Security vulnerability in sandbox  
**Mitigation**: Multiple validation layers, human approval gates

### Schedule Risks

**Risk**: Complexity underestimated  
**Mitigation**: Each phase independently useful, can ship early

**Risk**: Blocked on dependencies  
**Mitigation**: Can skip optional phases (web UI, memory)

---

## Getting Started

**Start here**:
1. Read README.md for overview
2. Follow QUICKSTART.md to run Phase 0
3. Use this roadmap to plan Phase 1
4. Read DEVELOPMENT.md when you start coding

**Questions to answer before Phase 1**:
- [ ] What's your NAS CPU? (verify i3-10100F)
- [ ] How much RAM? (determines model size)
- [ ] How much are you spending on Claude API now?
- [ ] What tasks do you want to automate first?

**Ready to begin?** 

Start with Phase 1, Task 1.1: Install Ollama on your NAS.
