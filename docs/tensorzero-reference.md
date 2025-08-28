# TensorZero Reference

A living document capturing our learnings about TensorZero as we explore the platform.

## Overview

TensorZero is an open-source platform for building industrial-grade LLM applications. It provides a unified gateway for multiple LLM providers with built-in observability, experimentation, and optimization capabilities.

**Key Components:**
1. Gateway - Unified API for LLM providers
2. Observability - Metrics and tracing
3. Optimization - Prompt and model tuning
4. Evaluations - Benchmarking and testing
5. Experimentation - A/B testing and routing

## Architecture

### Gateway
- Written in Rust for high performance (<1ms p99 latency)
- Supports OpenAI, Anthropic, Azure, Google AI, xAI, and more
- OpenAI-compatible API support for custom providers
- GitOps-friendly configuration via TOML files

### Configuration Structure
```toml
# Basic function definition
[functions.function_name]
type = "chat"

# Variant configuration
[functions.function_name.variants.variant_name]
type = "chat_completion"
model = "provider::model-name"
```

## Configuration Gotchas (Lessons Learned)

### Invalid Configuration Fields
- ❌ `[experiments]` section is **not supported** in current version
- ❌ `[model_routing]` section causes configuration errors
- ✅ Keep configuration minimal and follow official examples

### Working Configuration Pattern
```toml
# Minimal working configuration
[functions.chat]
type = "chat"

[functions.chat.variants.gpt4]
type = "chat_completion"
model = "openai::gpt-4"

[functions.chat.variants.gpt4_mini]
type = "chat_completion"
model = "openai::gpt-4o-mini"
```

## Providers

### Supported Providers
- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Anthropic**: Claude models
- **xAI**: Grok models
- **Azure OpenAI**: Enterprise deployments
- **Google AI**: Gemini models
- **AWS Bedrock**: Various models
- **Others**: Any OpenAI-compatible API

### Provider Configuration
```toml
# Example: Multiple providers for same function
[functions.generate_text.variants.gpt4]
type = "chat_completion"
model = "openai::gpt-4"

[functions.generate_text.variants.claude]
type = "chat_completion"
model = "anthropic::claude-3-opus-20240229"

[functions.generate_text.variants.grok]
type = "chat_completion"
model = "xai::grok-beta"
```

## API Structure

### Python Client
```python
from tensorzero import TensorZeroGateway

# Standalone gateway
client = TensorZeroGateway("http://localhost:3000")

# Embedded gateway
with TensorZeroGateway.build_embedded(
    clickhouse_url="http://localhost:8123/tensorzero",
    config_file="config/tensorzero.toml",
) as client:
    response = client.inference(
        function_name="function_name",
        input={"messages": [...]},
    )
```

### Inference API
- Endpoint: `/inference`
- Method: POST
- Input: Function-specific schema
- Output: Structured response with content and metadata

## Observability

### ClickHouse Integration
- All inferences stored in ClickHouse
- Default credentials: `chuser`/`chpassword` (development)
- Database: `tensorzero`
- Enables analytics and optimization
- Supports custom queries and dashboards

### UI Access
- TensorZero UI runs on port 4000 (updated from docs)
- Access at http://localhost:4000
- Shows inference history, metrics, and experiments
- Real-time monitoring of gateway activity

### Metrics Collected
- Latency (request, model, total)
- Token usage
- Cost estimates
- Error rates
- A/B test results
- Inference IDs for tracking

### Feedback Collection
```python
# Collect user feedback
client.feedback(
    inference_id=response.inference_id,
    feedback={"score": 0.9, "helpful": True}
)
```

### Python Client Modes
1. **Standalone Gateway**: Connects to running gateway service
   ```python
   # Deprecated constructor (shows warning)
   client = TensorZeroGateway("http://localhost:3000")
   
   # Preferred method
   client = TensorZeroGateway.build_http("http://localhost:3000")
   ```

2. **Embedded Gateway**: Runs gateway in-process (no separate service needed)
   ```python
   client = TensorZeroGateway.build_embedded(
       clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
       config_file="config/tensorzero.toml",
   )
   ```

### Response Format
Responses include structured content:
```python
response = client.inference(function_name="chat", input={"messages": [...]})

# Response attributes
response.inference_id      # Unique identifier
response.variant_name      # Which variant was used
response.content          # List of Text objects
response.content[0].text  # Actual text content
```

## Experimentation

### A/B Testing
- Configure multiple variants per function
- Automatic traffic splitting
- Statistical significance testing
- Performance comparison

### Routing Strategies
- Random selection
- Weighted distribution
- Model-based routing
- Fallback chains

## Best Practices

### Configuration Management
1. Use version control for TOML files
2. Separate configs by environment
3. Document variant purposes
4. Test configurations locally first

### Performance Optimization
1. Use connection pooling
2. Enable request batching where supported
3. Configure appropriate timeouts
4. Monitor latency metrics

### Cost Management
1. Set up usage alerts
2. Use cheaper models for development
3. Implement caching strategies
4. Monitor token usage

## Common Patterns

### Fallback Chain
```toml
# Primary expensive model
[functions.analyze.variants.primary]
type = "chat_completion"
model = "openai::gpt-4"

# Fallback to cheaper model
[functions.analyze.variants.fallback]
type = "chat_completion"
model = "openai::gpt-3.5-turbo"
```

### Multi-Provider Redundancy
```toml
# Use different providers for resilience
[functions.generate.variants.openai]
model = "openai::gpt-4"

[functions.generate.variants.anthropic]
model = "anthropic::claude-3-opus-20240229"

[functions.generate.variants.google]
model = "google::gemini-pro"
```

## Integration Examples

### With LangGraph
*To be documented after Phase 5 implementation*

### With Agno
*To be documented after Phase 5 implementation*

## Troubleshooting

### Common Issues
1. **Connection refused**: Check Docker services are running
2. **Invalid configuration**: Validate TOML syntax
3. **Provider errors**: Verify API keys and quotas
4. **High latency**: Check network and provider status

### Debug Tips
1. Enable verbose logging
2. Use TensorZero UI for request inspection
3. Check ClickHouse for stored data
4. Monitor Docker logs

## References

- [Official Docs](https://www.tensorzero.com/docs)
- [GitHub Repository](https://github.com/tensorzero/tensorzero)
- [API Reference](https://www.tensorzero.com/docs/gateway/api)
- Our examples: `notebooks/` and `examples/`

---

*This document will be updated as we learn more about TensorZero through hands-on exploration.*