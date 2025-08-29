# TensorZero LangGraph Agent

A demonstration of integrating TensorZero with LangGraph's `create_react_agent()` function to build AI agents with tool calling capabilities.

## Overview

This agent showcases how TensorZero can act as a proxy for LLM provider calls within LangGraph agents. It uses:

- **xAI's Grok model** through TensorZero
- **LangGraph's `create_react_agent()`** for agent orchestration
- **Python-based tools** for calculations, weather lookup, and documentation search
- **Rich console output** with beautiful formatting

## Features

### 🤖 Agent Capabilities
- **Tool Calling**: Uses calculator, weather, and documentation search tools
- **Multi-Provider Support**: Leverages TensorZero's provider abstraction
- **Interactive Chat**: Real-time conversation with the agent
- **Demo Mode**: Predefined conversation demonstrating all features

### 🛠️ Tools Available
- **Calculator**: Safe mathematical expression evaluation
- **Weather**: Mock weather data for major cities
- **Documentation Search**: TensorZero documentation lookup

## Quick Start

### Prerequisites
1. **TensorZero Gateway**: Running on `http://localhost:3000`
2. **Environment Variables**: Set up API keys for providers
3. **Dependencies**: Install with `poe setup`

### Running the Agent

#### Interactive Mode (Default)
```bash
poe agent
```

#### Demo Mode (Predefined Conversation)
```bash
poe agent-demo
```

#### Direct Python Execution
```bash
python run_agent.py          # Interactive
python run_agent.py --demo   # Demo mode
```

## Architecture

### TensorZeroLLM Class
Custom LangChain LLM wrapper that:
- Translates LangChain messages to TensorZero format
- Handles tool call conversion
- Manages episode IDs for conversation continuity
- Provides seamless integration with LangChain ecosystem

### Agent Flow
1. **User Input** → LangGraph Agent
2. **Agent Reasoning** → TensorZero (via custom LLM wrapper)
3. **Tool Calls** → Python tool functions
4. **Tool Results** → Back to agent for final response
5. **Final Output** → Rich console formatting

## Example Conversation

```
🤖 TensorZero LangGraph Agent Demo

User: What's the weather like in Tokyo?

Assistant: I'd be happy to help you check the weather in Tokyo. Let me look that up for you.

Tool Calls:
• get_weather({"location":"Tokyo"})

Assistant: The current weather in Tokyo is Rainy, 22°C.
```

## Configuration

The agent uses TensorZero's `agent_chat` function with the `grok4` variant:

```toml
[functions.agent_chat]
type = "chat"
tools = ["calculator", "get_weather", "search_tensorzero_docs"]

[functions.agent_chat.variants.grok4]
type = "chat_completion"
model = "xai::grok-4-0709"
```

## Development

### Project Structure
```
src/tensorzero_scratch/
├── langgraph_agent.py    # Main agent implementation
├── __init__.py          # Package exports
└── ...

run_agent.py             # Simple runner script
```

### Extending the Agent

#### Adding New Tools
```python
@tool
def my_new_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return result
```

#### Customizing the LLM
```python
# Use different TensorZero function/variant
llm = TensorZeroLLM(
    function_name="my_custom_function",
    variant_name="claude3_sonnet"
)
```

## Troubleshooting

### Common Issues

1. **"Connection refused" Error**
   - Ensure TensorZero gateway is running: `poe gateway`
   - Check gateway URL: `http://localhost:3000`

2. **"Tool not found" Error**
   - Verify tool definitions in `config/tensorzero.toml`
   - Check tool function names match configuration

3. **Import Errors**
   - Install dependencies: `poe setup`
   - Verify Python path includes `src/`

### Debug Mode
Run with verbose output:
```bash
python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('run_agent.py').read())"
```

## Integration Points

This agent demonstrates key integration patterns:

1. **LangChain ↔ TensorZero**: Custom LLM wrapper
2. **LangGraph Tools**: Python function to tool conversion
3. **Async Operations**: Proper async/await handling
4. **Error Handling**: Graceful degradation and user feedback
5. **UI/UX**: Rich console output for better user experience

## Next Steps

- [ ] Add more sophisticated tools (web search, file operations)
- [ ] Implement memory and conversation persistence
- [ ] Add streaming responses
- [ ] Integrate with external APIs (real weather data)
- [ ] Add evaluation and metrics collection
- [ ] Deploy as a web service

## Related Files

- `src/tensorzero_scratch/langgraph_agent.py` - Main agent implementation
- `config/tensorzero.toml` - TensorZero configuration
- `config/functions/` - Tool definitions
- `run_agent.py` - Runner script
- `pyproject.toml` - Project configuration and tasks
