#!/usr/bin/env python3
"""Test multi-provider setup with TensorZero."""

import os
from dotenv import load_dotenv
from tensorzero import TensorZeroGateway

# Load environment variables
load_dotenv()

def test_all_providers():
    """Test all configured providers."""
    print("🔄 Testing Multi-Provider Setup")
    print("=" * 50)
    
    # Check API keys
    api_keys = {
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "Anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "xAI": os.getenv("XAI_API_KEY")
    }
    
    for provider, key in api_keys.items():
        status = "✅" if key else "❌"
        print(f"{status} {provider} API key: {'Set' if key else 'Missing'}")
    
    # Connect to gateway
    client = TensorZeroGateway("http://localhost:3000")
    print("\n✅ Connected to gateway")
    
    # Test variants
    variants_to_test = [
        ("gpt4", "OpenAI GPT-4"),
        ("gpt4_mini", "OpenAI GPT-4o Mini"),
        ("claude3_opus", "Anthropic Claude 3 Opus"),
        ("claude3_sonnet", "Anthropic Claude 3 Sonnet"),
        ("claude3_haiku", "Anthropic Claude 3 Haiku"),
        ("grok_beta", "xAI Grok Beta"),
    ]
    
    test_prompt = "Explain what TensorZero is in exactly one sentence."
    results = []
    
    print(f"\\n🧪 Testing prompt: {test_prompt}")
    print("=" * 50)
    
    for variant_name, display_name in variants_to_test:
        print(f"\\n🤖 Testing {display_name}...")
        
        try:
            response = client.inference(
                function_name="chat",
                variant_name=variant_name,
                input={
                    "messages": [
                        {"role": "user", "content": test_prompt}
                    ]
                }
            )
            
            # Extract content
            content = ""
            if hasattr(response, 'content') and response.content:
                if isinstance(response.content, list) and len(response.content) > 0:
                    content = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
                else:
                    content = str(response.content)
            
            print(f"   ✅ Success!")
            print(f"   📝 {content[:100]}{'...' if len(content) > 100 else ''}")
            print(f"   🆔 Inference ID: {response.inference_id}")
            
            results.append({
                "variant": variant_name,
                "provider": display_name,
                "success": True,
                "content": content,
                "inference_id": response.inference_id
            })
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append({
                "variant": variant_name,
                "provider": display_name,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\\n📊 Results Summary")
    print("=" * 30)
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print("\\n🎉 Working Providers:")
        for result in successful:
            print(f"   • {result['provider']}")
    
    if failed:
        print("\\n⚠️  Failed Providers:")
        for result in failed:
            print(f"   • {result['provider']}: {result.get('error', 'Unknown error')}")
    
    return results

if __name__ == "__main__":
    results = test_all_providers()
    print(f"\\n🌐 View results in TensorZero UI: http://localhost:4000")