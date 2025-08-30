import atexit
import logging
import threading
import time

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from fastmcp import FastMCP  # noqa: E402

from . import prompts  # noqa: E402
from . import tools  # noqa: E402
from .auth import AuthMiddleware  # noqa: E402
from .game_world import world  # noqa: E402
from .persist import Persist  # noqa: E402
from .admin import Admin  # noqa: E402

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

# Register game tools and prompts
tools.register(mcp)
prompts.register(mcp)

# Register admin tools
admin = Admin(world)
admin.register(mcp)


# Simple background thread for periodic saves


def periodic_save():
    """Save world every 5 minutes."""
    persist = Persist()
    while True:
        time.sleep(300)  # 5 minutes
        persist.save_sync(world)
        logging.info("Periodic save completed")


# Start background thread as daemon so it exits with main program
thread = threading.Thread(target=periodic_save, daemon=True)
thread.start()
logging.info("Started periodic save thread")


# Save on exit
def save_on_exit():
    """Save world when program exits."""
    logging.info("Saving world on exit...")
    Persist().save_sync(world)
    logging.info("World saved")


atexit.register(save_on_exit)

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        path="/mcp",
    )
