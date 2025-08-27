# TensorZero Exploration Plan

## Overview
This project explores TensorZero, an open-source platform for building industrial-grade LLM applications. We'll understand its gateway functionality, multi-provider support, observability features, and integration with agent frameworks.

## Tech Stack
- **Python Environment**: uv + poethepoet for task automation
- **Documentation**: Jupyter notebooks for experiments, markdown for reference
- **Infrastructure**: Docker Compose for service orchestration
- **Languages**: Primary focus on Python, with examples in Go, Rust, C++ as needed

## Phase 1: Setup & Basic Gateway

### Goals
- Understand basic TensorZero architecture
- Set up development environment
- Create minimal working gateway

### Tasks
1. ✅ Add TensorZero as git submodule in `vendors/`
2. ✅ Create project directory structure
3. Set up Python environment with uv
4. Configure gateway with multiple providers:
   - OpenAI (GPT-4, GPT-3.5)
   - Anthropic (Claude)
   - xAI (Grok)
5. Create basic inference examples

### Deliverables
- Working docker-compose.yml
- Basic tensorzero.toml configuration
- `notebooks/01_basic_gateway.ipynb` demonstrating simple inference

## Phase 2: Multi-Provider Testing

### Goals
- Compare provider capabilities
- Understand fallback mechanisms
- Benchmark performance

### Tasks
1. Configure functions using different providers
2. Implement provider-specific prompts
3. Test automatic fallback scenarios
4. Measure latency and costs

### Deliverables
- `notebooks/02_multi_provider.ipynb` with comparisons
- Performance metrics documentation
- Cost analysis table

## Phase 3: Observability & Tracing

### Goals
- Set up complete observability stack
- Understand data collection patterns
- Explore TensorZero UI

### Tasks
1. Configure ClickHouse for metrics
2. Enable full request tracing
3. Implement feedback collection
4. Explore built-in UI features

### Deliverables
- `notebooks/03_observability.ipynb` with tracing examples
- Observability best practices guide
- Custom dashboard examples

## Phase 4: Prompt Management

### Goals
- Master prompt versioning
- Implement A/B testing
- Use structured schemas

### Tasks
1. Create prompt variants
2. Set up A/B tests
3. Define input/output schemas
4. Implement prompt optimization workflow

### Deliverables
- `notebooks/04_prompt_management.ipynb`
- Prompt template library
- A/B testing results

## Phase 5: Agent Integration

### Goals
- Integrate with agent frameworks
- Build multi-step workflows
- Enable agent observability

### Tasks
1. Create LangGraph agent using TensorZero
2. Explore Agno integration
3. Build complex multi-step workflows
4. Add agent-specific tracing

### Deliverables
- `notebooks/05_agents.ipynb`
- Agent examples in `examples/agents/`
- Integration patterns guide

## Project Structure
```
tensorzero_scratch/
├── PLAN.md                    # This file
├── README.md                  # Project overview
├── pyproject.toml             # Python dependencies (uv)
├── .python-version            # Python version
├── docker-compose.yml         # Service orchestration
├── CLAUDE.md                  # AI assistant reference
├── config/
│   └── tensorzero.toml        # Gateway configuration
├── docs/
│   └── tensorzero-reference.md # Living document of learnings
├── notebooks/
│   ├── 01_basic_gateway.ipynb
│   ├── 02_multi_provider.ipynb
│   ├── 03_observability.ipynb
│   ├── 04_prompt_management.ipynb
│   └── 05_agents.ipynb
├── examples/
│   ├── python/                # Python examples
│   ├── go/                    # Go examples
│   ├── rust/                  # Rust examples
│   └── agents/                # Agent framework examples
└── vendors/
    └── tensorzero/            # Submodule

```

## Poethepoet Tasks
- `poe setup` - Initialize environment and install dependencies
- `poe up` - Start all Docker services
- `poe down` - Stop all services
- `poe notebook` - Launch Jupyter Lab
- `poe test` - Run test suite
- `poe lint` - Run code quality checks
- `poe format` - Format all code
- `poe gateway` - Start only TensorZero gateway
- `poe ui` - Open TensorZero UI

## Success Criteria
1. Complete understanding of TensorZero gateway operation
2. Working examples with 3+ LLM providers
3. Full observability pipeline
4. Agent integration patterns documented
5. Clean, reusable code examples
6. Comprehensive reference documentation

## Timeline
- Phase 1: 1 day (Setup)
- Phase 2: 1 day (Providers)
- Phase 3: 1 day (Observability)
- Phase 4: 1 day (Prompts)
- Phase 5: 2 days (Agents)

Total: ~1 week for comprehensive exploration