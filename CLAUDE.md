# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a TensorZero exploration project focused on understanding and demonstrating the capabilities of the TensorZero platform for building industrial-grade LLM applications.

## Key Commands

### Development Setup
```bash
# Install Python dependencies using uv
poe setup

# Start all services (TensorZero gateway, ClickHouse, UI)
poe up

# Launch Jupyter notebooks
poe notebook

# Check service status
poe ps
```

### Code Quality
```bash
# Run linting
poe lint

# Format code
poe format

# Type checking
poe typecheck

# Run all checks
poe check
```

### Testing
```bash
# Run tests
poe test
```

## Architecture

### TensorZero Components
1. **Gateway** (port 3000) - Unified API for LLM providers
2. **ClickHouse** (port 8123) - Metrics and observability storage  
3. **UI** (port 3001) - Web interface for monitoring
4. **Configuration** - `config/tensorzero.toml` defines functions and variants

### Project Structure
- `notebooks/` - Jupyter notebooks demonstrating features
- `examples/` - Clean code examples in multiple languages
- `config/` - TensorZero and service configurations
- `docs/` - Reference documentation
- `vendors/tensorzero/` - TensorZero source (submodule)

### Key Concepts
- **Functions**: Named operations (chat, analyze_sentiment, etc.)
- **Variants**: Different model/provider implementations of functions
- **Providers**: LLM services (OpenAI, Anthropic, xAI, etc.)
- **Experiments**: A/B testing and routing configurations

## Development Workflow

1. Configuration changes go in `config/tensorzero.toml`
2. Use notebooks for exploration and prototyping
3. Extract clean examples to `examples/` directory
4. Document learnings in `docs/tensorzero-reference.md`
5. Use poethepoet (`poe`) for all common tasks

## Environment Variables
Required API keys (set in `.env` file):
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `XAI_API_KEY`

## Testing Approach
- Unit tests for utility functions
- Integration tests using mock providers
- Notebook-based exploratory testing
- Performance benchmarking in dedicated notebooks

## Common Tasks

### Adding a New Provider
1. Update `config/tensorzero.toml` with new variants
2. Add API key to environment variables
3. Create test notebook in `notebooks/`
4. Document in reference guide

### Creating Examples
1. Start with notebook prototype
2. Extract to standalone script in `examples/`
3. Add appropriate error handling
4. Include usage documentation

### Debugging
1. Check Docker logs: `poe logs`
2. Verify configuration: Review `config/tensorzero.toml`
3. Check ClickHouse data: Use UI at http://localhost:3001
4. Enable debug logging in gateway