"""Global game world instance management."""

import asyncio
import logging

from .persist import Persist
from .world import World
from .world_seed import create_seed_world

logger = logging.getLogger(__name__)


def load_world() -> World:
    """Load the world synchronously at import time."""
    persist = Persist()
    world_id = 1  # Default world

    try:
        # Try to load existing world
        world = persist.load_sync(world_id)
        logger.info(f"Loaded existing world (id={world_id})")
    except (FileNotFoundError, ValueError) as e:
        # No saved world found, create from seed
        logger.info(f"No saved world found: {e}")
        logger.info("Creating new world from seed...")
        world = create_seed_world()

        # Save the initial world
        persist.save_sync(world, world_id)
        logger.info(f"Saved initial world (id={world_id})")

    return world


# Load world at import time
world = load_world()


async def save_world_async(world_id: int = 1) -> None:
    """Save the current world state asynchronously."""
    persist = Persist()
    await persist.save(world, world_id)
    logger.info(f"World saved async (id={world_id})")


def start_periodic_save(interval_seconds: int = 300) -> asyncio.Task:
    """Start the periodic save background task.

    Args:
        interval_seconds: Seconds between saves (default: 300 = 5 minutes)

    Returns:
        The asyncio Task object for the background save task
    """
    persist = Persist()
    task = asyncio.create_task(
        persist.start_periodic_save(world, interval_seconds=interval_seconds)
    )
    return task
