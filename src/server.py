import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from fastmcp import FastMCP  # noqa: E402

from .auth import AuthMiddleware  # noqa: E402
from . import tools  # noqa: E402
from . import prompts  # noqa: E402
from .game_world import start_periodic_save  # noqa: E402

mcp = FastMCP(
    name="Dungeon Crawler MCP",
    instructions="""A persistent multiplayer text-based dungeon crawler where AI agents and humans explore together.

Connect your AI agent to play as either:
- An autonomous adventurer (set autonomous=1 in URL)
- An assistant helping a human player navigate the world

Every action has lasting consequences in this living world. Create objects, modify rooms, 
interact with other players, and leave your mark on the dungeon.

First use 'whoami' to check if you have a character. If not, use the 'play' prompt to get started and create your character.""",
)
mcp.add_middleware(AuthMiddleware())

app = mcp.http_app()

tools.register(mcp)
prompts.register(mcp)


# Start periodic save on startup
@app.on_event("startup")
def startup_event():
    """Start background tasks when the server starts."""
    # Start periodic save (every 5 minutes by default)
    start_periodic_save()
    logging.info("Started periodic world save task")


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
