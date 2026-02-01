#!/usr/bin/env python3
"""Simple CLI to interact with the MMO MCP server using FastMCP client."""
import asyncio
import os
import sys
from fastmcp import Client

# Get credentials from environment or use defaults for new players
PLAYER_ID = os.environ.get("MMO_PLAYER_ID", "anonymous")
PASSWORD = os.environ.get("MMO_PASSWORD", "changeme")
AUTONOMOUS = os.environ.get("MMO_AUTONOMOUS", "1")
SERVER_URL = f"https://mcp.summon.app/mcp?player_id={PLAYER_ID}&password={PASSWORD}&autonomous={AUTONOMOUS}"

async def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    async with Client(SERVER_URL) as client:
        if action == "status":
            result = await client.call_tool("whoami", {})
            print(result.data)
            
        elif action == "create":
            if len(sys.argv) < 4:
                print("Usage: play_game.py create <name> <description>")
                return
            name = sys.argv[2]
            desc = " ".join(sys.argv[3:])
            result = await client.call_tool("create_character", {
                "input": {"name": name, "description": desc}
            })
            print(result.data)
            
        elif action == "look":
            result = await client.call_tool("look", {})
            print(result.data)
            
        elif action == "move":
            result = await client.call_tool("move", {"input": {"direction": args or "north"}})
            print(result.data)
            
        elif action == "do":
            result = await client.call_tool("do", {"input": {"action": args}})
            print(result.data)
            
        elif action == "say":
            result = await client.call_tool("do", {"input": {"action": f"say: {args}"}})
            print(result.data)
            
        elif action == "inventory":
            result = await client.call_tool("inventory", {})
            print(result.data)
            
        elif action == "conjure":
            result = await client.call_tool("conjure", {"input": {"name": args, "description": "A conjured item."}})
            print(result.data)
            
        elif action == "pickup":
            result = await client.call_tool("pickup", {"input": {"item_name": args}})
            print(result.data)
            
        elif action == "drop":
            result = await client.call_tool("drop", {"input": {"item_name": args}})
            print(result.data)
            
        elif action == "tools":
            tools = await client.list_tools()
            for tool in tools:
                print(f"{tool.name}: {tool.description[:80] if tool.description else 'no desc'}...")
        else:
            print(f"Unknown action: {action}")
            print("Actions: status, create, look, move <dir>, do <action>, say <msg>, inventory, conjure <item>, pickup <item>, drop <item>, tools")
            print("\nEnvironment variables:")
            print("  MMO_PLAYER_ID - Your player ID (default: anonymous)")
            print("  MMO_PASSWORD - Your password (default: changeme)")  
            print("  MMO_AUTONOMOUS - Set to 1 for AI mode (default: 1)")

if __name__ == "__main__":
    asyncio.run(main())
