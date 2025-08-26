from dotenv import load_dotenv

load_dotenv()

from fastmcp import FastMCP  # noqa: E402

from .auth import AuthMiddleware  # noqa: E402
from . import tools  # noqa: E402
from . import prompts  # noqa: E402

mcp = FastMCP(
    name="Dungeon Crawler MCP",
    instructions="""A persistent multiplayer text-based dungeon crawler where AI agents and humans explore together.

Connect your AI agent to play as either:
- An autonomous adventurer (set autonomous=1 in URL)
- An assistant helping a human player navigate the world

Every action has lasting consequences in this living world. Create objects, modify rooms, 
interact with other players, and leave your mark on the dungeon.

Use the 'play' prompt to get started and create your character.""",
)
mcp.add_middleware(AuthMiddleware())

app = mcp.http_app()

tools.register(mcp)
prompts.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
