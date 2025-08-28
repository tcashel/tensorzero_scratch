#!/usr/bin/env python3
"""Quick test of TensorZero gateway functionality."""

import os
from dotenv import load_dotenv
from tensorzero import TensorZeroGateway

# Load environment variables
load_dotenv()

def test_gateway():
    """Test basic gateway functionality."""
    print("🧪 Testing TensorZero Gateway")
    print("=" * 40)
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY not set!")
        return False
    
    print(f"✅ OpenAI API key loaded: {openai_key[:8]}...")
    
    # Connect to gateway
    try:
        client = TensorZeroGateway.build_http(gateway_url="http://localhost:3000")
        print("✅ Connected to gateway at localhost:3000")
    except Exception as e:
        print(f"❌ Failed to connect to gateway: {e}")
        return False
    
    # Test haiku generation (from official example)
    try:
        print("\n🎋 Testing haiku generation...")
        response = client.inference(
            function_name="generate_haiku",
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": "Write a haiku about artificial intelligence."
                    }
                ]
            }
        )
        
        print(f"✅ Inference ID: {response.inference_id}")
        print(f"✅ Variant: {response.variant_name}")
        print(f"✅ Content:\n{response.content}")
        
    except Exception as e:
        print(f"❌ Inference failed: {e}")
        return False
    
    # Test chat function
    try:
        print("\n💬 Testing chat function...")
        response = client.inference(
            function_name="chat",
            variant_name="gpt4_mini",
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": "What is TensorZero in one sentence?"
                    }
                ]
            }
        )
        
        print(f"✅ Inference ID: {response.inference_id}")
        print(f"✅ Variant: {response.variant_name}")
        print(f"✅ Content: {response.content}")
        
    except Exception as e:
        print(f"❌ Chat failed: {e}")
        return False
    
    print(f"\n🎉 All tests passed!")
    print(f"🌐 TensorZero UI: http://localhost:4000")
    return True

if __name__ == "__main__":
    success = test_gateway()
    exit(0 if success else 1)