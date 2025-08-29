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
- **xAI**: Grok models (grok-3-mini, grok-code-fast-1, grok-4-0709)
  - All Grok models support structured output, reasoning, and function calling
  - grok-4-0790 supports image input + text output
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
**Working Integration Pattern:**

TensorZero handles tools differently from OpenAI:
- **Configuration-based**: Tools are defined in `tensorzero.toml`, not sent in requests
- **ToolCall objects**: TensorZero returns `ToolCall` objects instead of OpenAI's tool_calls format
- **Structured responses**: Response content is a list of Text and ToolCall objects

**Key Differences:**
```python
# ❌ OpenAI-style (doesn't work with TensorZero)
input_data = {
    "messages": messages,
    "tools": tool_definitions  # Not supported
}

# ✅ TensorZero-style
input_data = {
    "messages": messages
    # Tools configured in tensorzero.toml
}

# Handle ToolCall objects
for content_block in response.content:
    if isinstance(content_block, ToolCall):
        # Process tool call
        tool_name = content_block.name
        tool_args = content_block.arguments
```

**Working Agent Example:**
```python
class SimpleTensorZeroAgent:
    def chat(self, user_message: str):
        response = client.inference(
            function_name="agent_chat",  # Function with tools configured
            input={"messages": [{"role": "user", "content": user_message}]}
        )

        # Process response content blocks
        for content_block in response.content:
            if isinstance(content_block, ToolCall):
                # Handle tool call
                pass
            elif hasattr(content_block, 'text'):
                # Handle text response
                pass
```

**Configuration:**
```toml
[functions.agent_chat]
type = "chat"
tools = ["calculator", "get_weather", "search_tensorzero_docs"]

[tools.calculator]
description = "Safely evaluate mathematical expressions"
parameters = "functions/calculator.json"
strict = true
```

### With Agno
*To be documented after Phase 5 implementation*

## Troubleshooting

### Common Issues
1. **Connection refused**: Check Docker services are running
2. **Invalid configuration**: Validate TOML syntax
3. **Provider errors**: Verify API keys and quotas
4. **High latency**: Check network and provider status
5. **Tool calling errors**: See Tool Calling Issues section below

### Tool Calling Issues
**Error: "tools: unknown field `tools`, expected `system` or `messages`"**

**Cause:** TensorZero doesn't support sending tools in the request payload like OpenAI does.

**Solution:**
1. **Configure tools in `tensorzero.toml`:**
   ```toml
   [functions.agent_chat]
   type = "chat"
   tools = ["calculator", "get_weather"]

   [tools.calculator]
   description = "Calculate mathematical expressions"
   parameters = "functions/calculator.json"
   strict = true
   ```

2. **Remove tools from request payload:**
   ```python
   # ❌ Wrong
   input_data = {
       "messages": messages,
       "tools": tool_definitions  # Remove this
   }

   # ✅ Correct
   input_data = {
       "messages": messages
       # Tools configured in tensorzero.toml
   }
   ```

3. **Handle ToolCall objects in response:**
   ```python
   for content_block in response.content:
       if isinstance(content_block, ToolCall):
           tool_name = content_block.name
           tool_args = content_block.arguments
   ```

### Debug Tips
1. Enable verbose logging
2. Use TensorZero UI for request inspection
3. Check ClickHouse for stored data
4. Validate TOML configuration syntax
5. Test with simple requests before adding tools
4. Monitor Docker logs

## References

- [Official Docs](https://www.tensorzero.com/docs)
- [GitHub Repository](https://github.com/tensorzero/tensorzero)
- [API Reference](https://www.tensorzero.com/docs/gateway/api)
- Our examples: `notebooks/` and `examples/`

---

*This document will be updated as we learn more about TensorZero through hands-on exploration.*