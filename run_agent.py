#!/usr/bin/env python3
"""
Simple runner script for the TensorZero LangGraph Agent.

This script provides an easy way to run the TensorZero LangGraph agent
with proper setup and error handling.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path to import our package
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from tensorzero_scratch import TensorZeroLangGraphAgent


async def main():
    """Main function to run the TensorZero LangGraph agent."""
    try:
        print("🚀 Starting TensorZero LangGraph Agent...")
        print("Make sure TensorZero gateway is running on http://localhost:3000")
        print("Run 'poe gateway' in another terminal if not already running.\n")

        agent = TensorZeroLangGraphAgent()

        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            print("🎭 Running demo conversation...")
            await agent.run_demo_conversation()
        else:
            print("💬 Starting interactive chat...")
            print("Type 'demo' to run the demo conversation")
            print("Type 'quit' to exit\n")
            await agent.interactive_chat()

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Make sure TensorZero gateway is running: poe gateway")
        print("2. Check your environment variables: poe env-check")
        print("3. Verify Docker services are up: poe ps")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
