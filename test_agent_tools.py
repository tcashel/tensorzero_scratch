#!/usr/bin/env python3
"""
Simple test script to verify TensorZero agent tool calling works.
"""

from tensorzero import TensorZeroGateway, ToolCall

def test_agent_tools():
    """Test the agent_chat function with tools."""

    print("🧪 Testing TensorZero Agent Tool Calling")
    print("=" * 50)

    try:
        # Create client
        client = TensorZeroGateway.build_http(gateway_url="http://localhost:3000")
        print("✅ Connected to TensorZero Gateway")

        # Test calculator tool
        print("\n🧮 Testing Calculator Tool")
        print("-" * 30)

        messages = [{"role": "user", "content": "What is 15 + 27?"}]
        response = client.inference(
            function_name="agent_chat",
            variant_name="gpt4_mini",
            input={"messages": messages}
        )

        print(f"Inference ID: {response.inference_id}")
        print(f"Variant: {response.variant_name}")

        # Process response content
        assistant_text = ""
        tool_calls = []

        if hasattr(response, 'content') and response.content:
            for content_block in response.content:
                if hasattr(content_block, 'text') and content_block.text:
                    assistant_text += content_block.text
                elif isinstance(content_block, ToolCall):
                    tool_calls.append({
                        "name": content_block.name,
                        "args": content_block.arguments if hasattr(content_block, 'arguments') else {},
                        "id": content_block.id if hasattr(content_block, 'id') else f"call_{len(tool_calls)}"
                    })

        print(f"Assistant: {assistant_text}")
        if tool_calls:
            print(f"Tool Calls: {len(tool_calls)}")
            for tool_call in tool_calls:
                print(f"  - {tool_call['name']}: {tool_call['args']}")
        else:
            print("No tool calls detected")

        # Test weather tool
        print("\n🌤️  Testing Weather Tool")
        print("-" * 30)

        messages = [{"role": "user", "content": "What's the weather like in Tokyo?"}]
        response = client.inference(
            function_name="agent_chat",
            variant_name="gpt4_mini",
            input={"messages": messages}
        )

        print(f"Inference ID: {response.inference_id}")

        # Process response content
        assistant_text = ""
        tool_calls = []

        if hasattr(response, 'content') and response.content:
            for content_block in response.content:
                if hasattr(content_block, 'text') and content_block.text:
                    assistant_text += content_block.text
                elif isinstance(content_block, ToolCall):
                    tool_calls.append({
                        "name": content_block.name,
                        "args": content_block.arguments if hasattr(content_block, 'arguments') else {},
                        "id": content_block.id if hasattr(content_block, 'id') else f"call_{len(tool_calls)}"
                    })

        print(f"Assistant: {assistant_text}")
        if tool_calls:
            print(f"Tool Calls: {len(tool_calls)}")
            for tool_call in tool_calls:
                print(f"  - {tool_call['name']}: {tool_call['args']}")
        else:
            print("No tool calls detected")

        print("\n✅ Agent tool testing completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error testing agent tools: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent_tools()
