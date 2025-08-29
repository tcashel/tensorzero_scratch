"""
TensorZero Chat Model for LangChain

This module provides a LangChain-compatible chat model that uses TensorZero
as the backend LLM provider. It follows the same patterns as OpenAI's ChatOpenAI
implementation and integrates seamlessly with LangChain/LangGraph agents.

Usage:
    from tensorzero_scratch import TensorZeroChatModel

    # Initialize with default settings
    chat_model = TensorZeroChatModel()

    # Or with custom configuration
    chat_model = TensorZeroChatModel(
        gateway_url="http://localhost:3000",
        function_name="agent_chat",
        variant_name="gpt4_mini"
    )

    # Use in LangGraph agents
    from langgraph.prebuilt import create_react_agent
    agent = create_react_agent(chat_model, tools)
"""

import asyncio
from typing import Any, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.utils import from_env
from pydantic import Field, model_validator
from typing_extensions import Self

from tensorzero import TensorZeroGateway, Message, Text, ToolCall, ToolResult


class TensorZeroChatModel(BaseChatModel):
    """
    Custom LangChain Chat Model wrapper for TensorZero Gateway.

    This class allows TensorZero to be used as a drop-in replacement
    for any LangChain chat model, enabling the use of TensorZero's
    multi-provider capabilities within LangChain/LangGraph agents.

    Follows the same pattern as OpenAI's ChatOpenAI implementation.
    """

    # Client management (private fields)
    gateway: TensorZeroGateway = Field(default=None, exclude=True)

    # Model configuration
    function_name: str = Field(default="agent_chat", description="TensorZero function name to use")
    variant_name: str = Field(default="gpt4_mini", description="TensorZero variant name to use")
    gateway_url: Optional[str] = Field(
        default_factory=lambda: from_env("TENSORZERO_GATEWAY_URL", default="http://localhost:3000"),
        description="TensorZero gateway URL"
    )

    # Episode management
    episode_id: Optional[str] = Field(default=None, description="Current episode ID for conversation continuity")

    model_name: str = Field(default="tensorzero", description="Model identifier for LangChain")

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        """Validate and initialize TensorZero gateway."""
        if self.gateway is None:
            self.gateway = TensorZeroGateway.build_http(gateway_url=self.gateway_url)
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response using TensorZero."""

        # Convert messages and make inference call
        tensorzero_messages = self._convert_messages_to_tensorzero(messages)
        response = self.gateway.inference(
            function_name=self.function_name,
            variant_name=self.variant_name,
            input={"messages": tensorzero_messages},
            episode_id=self.episode_id
        )

        # Store episode ID for future calls
        if hasattr(response, 'episode_id'):
            self.episode_id = response.episode_id

        # Extract content and create response
        content, tool_calls = self._extract_response_content(response)
        ai_message = self._create_ai_message(content, tool_calls)

        generation = ChatGeneration(message=ai_message)
        return ChatResult(generations=[generation])

    def _convert_messages_to_tensorzero(self, messages: list[BaseMessage]) -> list[Message]:
        """Convert LangChain messages to TensorZero format."""
        tensorzero_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                tensorzero_messages.append(self._convert_human_message(msg))
            elif isinstance(msg, AIMessage):
                tensorzero_messages.append(self._convert_ai_message(msg))
            elif isinstance(msg, ToolMessage):
                tensorzero_messages.append(self._convert_tool_message(msg))

        return tensorzero_messages

    def _convert_human_message(self, msg: HumanMessage) -> Message:
        """Convert HumanMessage to TensorZero format."""
        content = msg.content
        if isinstance(content, str):
            return Message(role="user", content=content)
        else:
            return Message(role="user", content=str(content))

    def _convert_ai_message(self, msg: AIMessage) -> Message:
        """Convert AIMessage to TensorZero format."""
        content = msg.content
        if isinstance(content, str):
            return Message(role="assistant", content=content)
        else:
            return Message(role="assistant", content=str(content))

    def _convert_tool_message(self, msg: ToolMessage) -> Message:
        """Convert ToolMessage to TensorZero format."""
        # Create a proper tool message format that matches OpenAI's expectations
        tool_result = ToolResult(
            name=msg.name or "unknown_tool",
            result=msg.content,
            id=msg.tool_call_id or "unknown_id"
        )

        # For TensorZero, we need to send this as a user message containing the tool result
        # This matches the pattern used in the TensorZero examples
        return Message(
            role="user",
            content=[tool_result]
        )

    def _extract_response_content(self, response) -> tuple[str, list[dict]]:
        """Extract content and tool calls from TensorZero response."""
        content = ""
        tool_calls = []

        if not (hasattr(response, 'content') and response.content):
            return content, tool_calls

        for content_block in response.content:
            if isinstance(content_block, Text):
                content += content_block.text
            elif isinstance(content_block, ToolCall):
                tool_call = self._create_tool_call_dict(content_block, len(tool_calls))
                tool_calls.append(tool_call)

        return content, tool_calls

    def _create_tool_call_dict(self, content_block: ToolCall, call_index: int) -> dict:
        """Create a tool call dictionary from a ToolCall object."""
        return {
            "name": content_block.name,
            "args": content_block.arguments if hasattr(content_block, 'arguments') else {},
            "id": content_block.id if hasattr(content_block, 'id') else f"call_{call_index}"
        }

    def _create_ai_message(self, content: str, tool_calls: list[dict]) -> AIMessage:
        """Create AIMessage with optional tool calls."""
        if tool_calls:
            return AIMessage(
                content=content,
                tool_calls=[
                    {
                        "name": tc["name"],
                        "args": tc["args"],
                        "id": tc["id"]
                    }
                    for tc in tool_calls
                ]
            )
        else:
            return AIMessage(content=content)

    def bind_tools(self, tools: list, **kwargs: Any):
        """Bind tools to the model for tool calling."""
        # For TensorZero, tools are configured at the function level
        # in the tensorzero.toml file, not dynamically bound
        # So we just return self with tool information stored
        self._bound_tools = tools
        return self

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "tensorzero"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Get identifying parameters."""
        return {
            "function_name": self.function_name,
            "variant_name": self.variant_name,
            "gateway_url": self.gateway_url,
            "episode_id": self.episode_id
        }
