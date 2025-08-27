# TensorZero Scratch

A hands-on exploration of TensorZero - an open-source platform for building industrial-grade LLM applications.

## Quick Start

```bash
# Install dependencies
poe setup

# Start all services
poe up

# Launch Jupyter notebooks
poe notebook
```

## What is TensorZero?

TensorZero provides:
- **Unified Gateway**: Single API for multiple LLM providers (OpenAI, Anthropic, xAI, etc.)
- **Observability**: Built-in tracing and metrics collection
- **Experimentation**: A/B testing, routing, and fallbacks
- **Performance**: <1ms p99 latency overhead (written in Rust)
- **Flexibility**: GitOps-friendly configuration

## Project Goals

1. Understand TensorZero's gateway architecture
2. Test multi-provider support (OpenAI, Anthropic, xAI)
3. Explore observability and tracing features
4. Learn prompt management and A/B testing
5. Integrate with agent frameworks (LangGraph, Agno)

## Project Structure

- `notebooks/` - Jupyter notebooks exploring different features
- `examples/` - Clean code examples in Python, Go, Rust
- `config/` - TensorZero configuration files
- `docs/` - Reference documentation and learnings
- `vendors/tensorzero/` - TensorZero source (submodule)

## Available Tasks

Run `poe` to see all available tasks:
- `poe setup` - Initialize environment
- `poe up/down` - Start/stop services
- `poe notebook` - Launch Jupyter Lab
- `poe test` - Run tests
- `poe lint` - Code quality checks

## Documentation

- [PLAN.md](PLAN.md) - Detailed exploration plan
- [docs/tensorzero-reference.md](docs/tensorzero-reference.md) - Our learnings
- [TensorZero Docs](https://www.tensorzero.com/docs) - Official documentation

## Requirements

- Docker & Docker Compose
- Python 3.11+ (managed by uv)
- API keys for LLM providers (OpenAI, Anthropic, xAI)