#!/usr/bin/env python3
"""
Test script to verify that our custom tools are working correctly.
"""

import sys
from pathlib import Path

# Add src to path to import our package
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.tensorzero_scratch.langgraph_agent import (
    python_calculator,
    current_time,
    text_analyzer
)

def test_tools():
    """Test each of our custom tools."""
    print("🧪 Testing Custom Tools")
    print("=" * 40)

    # Test python_calculator
    print("\n🧮 Testing Python Calculator:")
    try:
        result = python_calculator.invoke({"expression": "sqrt(16) + 5"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test current_time
    print("\n🕐 Testing Current Time:")
    try:
        result = current_time.invoke({"timezone": "PST"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test text_analyzer
    print("\n📝 Testing Text Analyzer:")
    try:
        result = text_analyzer.invoke({"text": "This is an amazing product, I love it!"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n✅ Tool testing completed!")

if __name__ == "__main__":
    test_tools()
