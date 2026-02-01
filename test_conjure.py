#!/usr/bin/env python3
"""Test conjure and destruction."""
import asyncio
import os
from fastmcp import Client

PLAYER_ID = os.environ.get("MMO_PLAYER_ID", "geodude")
PASSWORD = os.environ.get("MMO_PASSWORD", "REDACTED")
SERVER_URL = f"https://mcp.summon.app/mcp?player_id={PLAYER_ID}&password={PASSWORD}&autonomous=1"

async def main():
    async with Client(SERVER_URL) as client:
        # Conjure an actual item
        print("Conjuring a test vase...")
        result = await client.call_tool("conjure", {
            "input": {
                "name": "test vase",
                "description": "A fragile ceramic vase, clearly meant to be smashed for testing purposes."
            }
        })
        print(result.data)
        print()
        
        # Look to confirm it exists
        print("Looking to confirm item exists...")
        result = await client.call_tool("look", {})
        if "test vase" in result.data.lower():
            print("✓ Test vase found in items!")
        else:
            print("✗ Test vase NOT found")
        print()
        
        # Try to smash it
        print("Attempting to smash the test vase...")
        result = await client.call_tool("do", {"input": {"action": "smash the test vase into pieces"}})
        print(result.data)
        print()
        
        # Look again to see if it's gone
        print("Looking to confirm destruction...")
        result = await client.call_tool("look", {})
        if "test vase" in result.data.lower():
            print("✗ Test vase STILL exists - destruction failed")
        else:
            print("✓ Test vase is GONE - destruction worked!")

if __name__ == "__main__":
    asyncio.run(main())
