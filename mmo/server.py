import atexit
import logging
import threading
import time

from fastmcp import FastMCP

from . import prompts, tools
from .auth import AuthMiddleware
from .game_world import world
from .persist import Persist

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


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


def main():
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        path="/mcp",
    )


if __name__ == "__main__":
    main()
