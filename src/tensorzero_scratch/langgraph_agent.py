#!/usr/bin/env python3
"""
LangGraph Agent with TensorZero Integration

This module demonstrates how to use TensorZero as a proxy for LLM provider calls
within a LangGraph agent using the create_react_agent() function from LangChain.

The agent uses xAI's Grok model through TensorZero and can call various tools
defined in Python. It outputs a predefined conversation to demonstrate tool calling
with proper formatting and pretty printing.
"""

import asyncio
from typing import Any

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage

from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict

from rich.console import Console
from rich.panel import Panel


# Define Python-based tools (our custom tools)
@tool
def python_calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions using Python's built-in calculator.

    This is a custom Python tool that provides advanced mathematical capabilities
    including complex expressions and error handling.

    Args:
        expression: A mathematical expression like '2 + 2' or 'sqrt(16)'

    Returns:
        The result of the mathematical expression as a string
    """
    try:
        # Import math for advanced functions
        import math
        # Use eval with restricted globals for safety but allow math functions
        allowed_names = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "pow": pow,
            "min": min,
            "max": max,
        }

        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Python Calculator Result: {expression} = {result}"
    except Exception as e:
        return f"Error in Python calculator: '{expression}' - {str(e)}"


@tool
def current_time(timezone: str = "UTC") -> str:
    """
    Get the current time in a specified timezone.

    This is a Python-only tool that provides current time information
    not available in TensorZero's configuration.

    Args:
        timezone: The timezone to get time for (UTC, EST, PST, etc.)

    Returns:
        Current time in the specified timezone
    """
    try:
        from datetime import datetime
        import pytz

        # Get current UTC time
        utc_now = datetime.now(pytz.UTC)

        # Handle common timezone abbreviations
        timezone_map = {
            "UTC": "UTC",
            "EST": "US/Eastern",
            "PST": "US/Pacific",
            "CST": "US/Central",
            "MST": "US/Mountain",
            "GMT": "GMT",
            "CET": "Europe/Paris",
            "JST": "Asia/Tokyo",
        }

        tz_name = timezone_map.get(timezone.upper(), timezone)
        try:
            tz = pytz.timezone(tz_name)
            local_time = utc_now.astimezone(tz)
            return f"Current time in {timezone}: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except pytz.exceptions.UnknownTimeZoneError:
            return f"Unknown timezone: {timezone}. Available: {', '.join(timezone_map.keys())}"

    except ImportError:
        # Fallback if pytz is not available
        from datetime import datetime
        utc_now = datetime.utcnow()
        return f"Current UTC time: {utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')} (timezone conversion not available)"


@tool
def text_analyzer(text: str) -> str:
    """
    Analyze text for various properties.

    This is a Python-only tool that provides text analysis capabilities
    including word count, character count, and basic sentiment analysis.

    Args:
        text: The text to analyze

    Returns:
        Analysis results of the input text
    """
    try:
        # Basic text analysis
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        char_no_spaces = len(text.replace(" ", ""))

        # Simple sentiment analysis based on keywords
        positive_words = ["good", "great", "excellent", "awesome", "fantastic", "wonderful", "amazing"]
        negative_words = ["bad", "terrible", "awful", "horrible", "worst", "hate", "disappointed"]

        positive_count = sum(1 for word in words if word.lower() in positive_words)
        negative_count = sum(1 for word in words if word.lower() in negative_words)

        sentiment = "neutral"
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"

        analysis = f"""
Text Analysis Results:
- Words: {word_count}
- Characters (with spaces): {char_count}
- Characters (no spaces): {char_no_spaces}
- Sentiment: {sentiment}
- Positive indicators: {positive_count}
- Negative indicators: {negative_count}
        """.strip()

        return analysis

    except Exception as e:
        return f"Error analyzing text: {str(e)}"


# Tool mapping: Our agent tool names -> TensorZero tool names
TOOL_NAME_MAPPING = {
    "math_solver": "calculator",           # Our custom name -> TensorZero name
    "weather_info": "get_weather",         # Our custom name -> TensorZero name
    "docs_search": "search_tensorzero_docs" # Our custom name -> TensorZero name
}





class TensorZeroLangGraphAgent:
    """
    LangGraph Agent that uses TensorZero as the LLM provider.

    This agent uses TensorZero's OpenAI-compatible API endpoint to work
    seamlessly with LangChain's create_react_agent function.
    """

    def __init__(self, gateway_url: str = "http://localhost:3000"):
        """Initialize the agent."""
        self.console = Console()

        # Configure HTTP client for TensorZero
        http_client = None
        if HTTPX_AVAILABLE:
            http_client = httpx.Client()

        # Use TensorZero's OpenAI-compatible endpoint
        self.llm = init_chat_model(
            "tensorzero::model_name::openai::gpt-4o-mini",  # Use our agent_chat function through TensorZero
            model_provider="openai",
            base_url=f"{gateway_url}/openai/v1",
            api_key="dummy",  # TensorZero ignores the API key
            http_client=http_client
        )

        # Define all available tools (both TensorZero and Python-only)
        self.tools = [
            # TensorZero tools (will be mapped to different names)
            # These correspond to tools defined in tensorzero.toml
            # But we'll use our custom names in the agent

            # Python-only tools (defined in this file)
            python_calculator,
           # current_time,
            text_analyzer
        ]

        # Create the agent using create_react_agent with our custom tools
        tool_descriptions = """
Available tools:
- python_calculator: Advanced mathematical calculations with math functions
- current_time: Get current time in different timezones
- text_analyzer: Analyze text properties and sentiment
- math_solver: Basic mathematical calculations (via TensorZero)
- weather_info: Get weather information for locations (via TensorZero)
- docs_search: Search TensorZero documentation (via TensorZero)
        """.strip()

        self.agent = create_react_agent(
            self.llm,
            self.tools,
            prompt=f"You are a helpful assistant powered by TensorZero. {tool_descriptions}\n\nYou have access to both TensorZero-configured tools and custom Python tools. Use the appropriate tool for each task."
        )

        # Initialize conversation history
        self.conversation_history = []



    def _format_message(self, message: BaseMessage, message_type: str) -> Panel:
        """Format a message for display."""
        if isinstance(message, AIMessage):
            if message.tool_calls:
                content = f"{message.content}\n\n[bold cyan]Tool Calls:[/bold cyan]\n"
                for tool_call in message.tool_calls:
                    content += f"• {tool_call['name']}({tool_call['args']})\n"
                content = content.strip()
            else:
                content = message.content
            border_color = "blue"
        elif isinstance(message, HumanMessage):
            content = message.content
            border_color = "green"
        elif isinstance(message, ToolMessage):
            content = f"Tool Result: {message.content}"
            border_color = "yellow"
        else:
            content = str(message.content)
            border_color = "white"

        return Panel(
            content,
            title=f"[bold]{message_type}[/bold]",
            border_style=border_color,
            title_align="left"
        )

    def _display_message(self, message: BaseMessage, message_type: str):
        """Display a message with formatting."""
        panel = self._format_message(message, message_type)
        self.console.print(panel)
        self.console.print()  # Add spacing

    async def run_demo_conversation(self):
        """
        Run a predefined conversation demonstrating tool calling capabilities.

        This method executes a series of predefined interactions to showcase
        how the agent uses TensorZero and calls various tools.
        """
        self.console.print("\n[bold magenta]🤖 TensorZero LangGraph Agent Demo[/bold magenta]\n")
        self.console.print("[dim]This demo shows how TensorZero acts as a proxy for LLM calls in a LangGraph agent[/dim]\n")

        # Predefined conversation testing all tools
        demo_messages = [
            "Hello! I'm exploring TensorZero. Can you help me understand what it is?",
            "What's the weather like in Tokyo?",  # Uses weather_info (TensorZero)
            "Can you calculate sqrt(144) + 5?",  # Uses python_calculator (Python-only)
            "What time is it in Tokyo right now?",  # Uses current_time (Python-only)
            "Tell me more about TensorZero functions and tools",  # Uses docs_search (TensorZero)
            "Can you analyze this text: 'This is an amazing product, I love it!'",  # Uses text_analyzer (Python-only)
            "What's 2 ** 8?",  # Uses math_solver (TensorZero)
            "How's the weather in Paris?"  # Uses weather_info (TensorZero)
        ]

        for user_message in demo_messages:
            self._display_message(HumanMessage(content=user_message), "User")

            # Show processing indicator
            with self.console.status("[bold green]Processing with TensorZero...", spinner="dots"):
                try:
                    # Add user message to conversation history
                    user_msg = HumanMessage(content=user_message)
                    self.conversation_history.append(user_msg)

                    # Run the agent with full conversation history
                    response = self.agent.invoke({"messages": self.conversation_history})

                    # Update conversation history with new messages
                    if response and "messages" in response:
                        # Add new messages to history (skip the user message we already added)
                        for message in response["messages"]:
                            if message not in self.conversation_history:
                                self.conversation_history.append(message)

                        # Display all new messages in the response
                        for message in response["messages"]:
                            if hasattr(message, 'type'):
                                if message.type == 'ai':
                                    self._display_message(message, "Assistant")
                                elif message.type == 'tool':
                                    self.console.print(f"[dim]🔧 Tool Result: {message.content}[/dim]")
                            else:
                                self.console.print(f"[dim]{message.type}: {getattr(message, 'content', str(message))}[/dim]")

                except Exception as e:
                    self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue

    async def interactive_chat(self):
        """
        Start an interactive chat session with the agent.

        Users can type messages and the agent will respond using TensorZero
        and tool calling capabilities.
        """
        self.console.print("\n[bold magenta]🤖 Interactive TensorZero Chat[/bold magenta]\n")
        self.console.print("[dim]Type 'quit' to exit, 'demo' to run demo conversation[/dim]\n")

        while True:
            try:
                user_input = await asyncio.to_thread(input, "You: ")
                user_input = user_input.strip()

                if user_input.lower() == 'quit':
                    self.console.print("[bold blue]Goodbye! 👋[/bold blue]")
                    break
                elif user_input.lower() == 'demo':
                    await self.run_demo_conversation()
                    continue
                elif not user_input:
                    continue

                # Show processing indicator
                with self.console.status("[bold green]Processing with TensorZero...", spinner="dots"):
                    try:
                        # Add user message to conversation history
                        user_msg = HumanMessage(content=user_input)
                        self.conversation_history.append(user_msg)

                        # Run the agent with full conversation history
                        response = self.agent.invoke({"messages": self.conversation_history})

                        # Update conversation history with new messages
                        if response and "messages" in response:
                            # Add new messages to history (skip the user message we already added)
                            for message in response["messages"]:
                                if message not in self.conversation_history:
                                    self.conversation_history.append(message)

                            # Display all new messages in the response
                            for message in response["messages"]:
                                if hasattr(message, 'type'):
                                    if message.type == 'ai':
                                        self._display_message(message, "Assistant")
                                    elif message.type == 'tool':
                                        self.console.print(f"[dim]🔧 Tool Result: {message.content}[/dim]")
                                else:
                                    self.console.print(f"[dim]{message.type}: {getattr(message, 'content', str(message))}[/dim]")

                    except Exception as e:
                        self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
                        continue

            except KeyboardInterrupt:
                self.console.print("\n[bold blue]Goodbye! 👋[/bold blue]")
                break
            except Exception as e:
                self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
                continue


async def main():
    """
    Main function to demonstrate the TensorZero LangGraph agent.

    This function creates an agent and runs either a demo conversation
    or starts an interactive chat session.
    """
    try:
        agent = TensorZeroLangGraphAgent()

        # Check if we should run demo or interactive mode
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            await agent.run_demo_conversation()
        else:
            await agent.interactive_chat()

    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error initializing agent:[/bold red] {str(e)}")
        console.print("[dim]Make sure TensorZero gateway is running on http://localhost:3000[/dim]")


if __name__ == "__main__":
    asyncio.run(main())
