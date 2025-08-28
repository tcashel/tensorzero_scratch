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
    client = TensorZeroGateway.build_http(gateway_url="http://localhost:3000")
    print("\n✅ Connected to gateway")
    
    # Test variants
    variants_to_test = [
        ("gpt4", "OpenAI GPT-4"),
        ("gpt4_mini", "OpenAI GPT-4o Mini"),
        ("claude3_opus", "Anthropic Claude 3 Opus"),
        ("claude3_sonnet", "Anthropic Claude 3 Sonnet"),
        ("claude3_haiku", "Anthropic Claude 3 Haiku"),
        ("grok3_mini", "xAI Grok-3 Mini"),
        ("grok_code_fast", "xAI Grok Code Fast"),
        ("grok4", "xAI Grok-4"),
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
            error_msg = str(e)
            # Extract cleaner error message if it's a verbose error
            if "TensorZeroError" in error_msg:
                try:
                    # Try to extract the actual error message
                    import json
                    error_start = error_msg.find('{"error":')
                    if error_start != -1:
                        error_json = json.loads(error_msg[error_start:error_msg.rfind('}')+1])
                        if "error" in error_json:
                            # Further parse nested errors
                            inner_error = error_json["error"]
                            if "Error 403 Forbidden" in inner_error:
                                error_msg = "403 Forbidden (check API key/credits)"
                            elif "max_tokens" in inner_error:
                                error_msg = "max_tokens required in config"
                            else:
                                error_msg = inner_error.split(": ")[-1][:100]
                except:
                    pass
            
            print(f"   ❌ Failed: {error_msg}")
            results.append({
                "variant": variant_name,
                "provider": display_name,
                "success": False,
                "error": error_msg
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