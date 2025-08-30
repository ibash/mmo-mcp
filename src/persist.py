import asyncio
import json
import logging
import os

import psycopg

from .world import World

logger = logging.getLogger(__name__)

# Persistence mode: "disk" for local JSON files, "postgres" for PostgreSQL
PERSIST_MODE = os.environ.get("PERSIST_MODE", "disk").lower()


class Persist:
    """Handle saving and loading world state to various backends."""

    def _get_filename(self, world_id: int) -> str:
        """Get the filename for a given world ID."""
        if world_id == 1:
            return "world.json"
        else:
            return f"world_{world_id}.json"

    def save_sync(self, world: World, world_id: int = 1) -> None:
        """Synchronously save world state using the configured backend."""
        filename = self._get_filename(world_id)

        if PERSIST_MODE == "postgres":
            self.save_to_postgres_sync(world, world_id)
        elif PERSIST_MODE == "disk":
            self.save_to_disk(world, filename)
        else:
            raise ValueError(
                f"Unknown PERSIST_MODE: {PERSIST_MODE}. Use 'disk' or 'postgres'"
            )

    def load_sync(self, world_id: int = 1) -> World:
        """Synchronously load world state using the configured backend."""
        filename = self._get_filename(world_id)

        if PERSIST_MODE == "postgres":
            return self.load_from_postgres_sync(world_id)
        elif PERSIST_MODE == "disk":
            return self.load_from_disk(filename)
        else:
            raise ValueError(
                f"Unknown PERSIST_MODE: {PERSIST_MODE}. Use 'disk' or 'postgres'"
            )

    async def save(self, world: World, world_id: int = 1) -> None:
        """Save world state using the configured backend (disk or postgres)."""
        filename = self._get_filename(world_id)

        if PERSIST_MODE == "postgres":
            await self.save_to_postgres(world, world_id)
        elif PERSIST_MODE == "disk":
            self.save_to_disk(world, filename)
        else:
            raise ValueError(
                f"Unknown PERSIST_MODE: {PERSIST_MODE}. Use 'disk' or 'postgres'"
            )

    async def load(self, world_id: int = 1) -> World:
        """Load world state using the configured backend (disk or postgres)."""
        filename = self._get_filename(world_id)

        if PERSIST_MODE == "postgres":
            return await self.load_from_postgres(world_id)
        elif PERSIST_MODE == "disk":
            return self.load_from_disk(filename)
        else:
            raise ValueError(
                f"Unknown PERSIST_MODE: {PERSIST_MODE}. Use 'disk' or 'postgres'"
            )

    def save_to_disk(self, world: World, filename: str = "world.json") -> None:
        """Save the world state to a JSON file."""
        # Write to a temp file first, then rename for atomicity
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, "w") as f:
            json.dump(world.model_dump(), f, indent=2)

        # Atomic rename
        os.replace(temp_filename, filename)
        logger.info(f"World saved to {filename}")

    def load_from_disk(self, filename: str = "world.json") -> World:
        """Load world state from a JSON file."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Save file {filename} not found")

        with open(filename, "r") as f:
            world_data = json.load(f)

        # Reconstruct the World from the saved data
        world = World(**world_data)

        logger.info(f"World loaded from {filename}")
        return world

    async def save_to_postgres(self, world: World, world_id: int) -> None:
        """Save the world state to PostgreSQL."""
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        async with await psycopg.AsyncConnection.connect(database_url) as conn:
            world_json = json.dumps(world.model_dump())

            # Upsert - insert or update if exists
            await conn.execute(
                """
                INSERT INTO worlds (id, payload, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                ON CONFLICT (id) 
                DO UPDATE SET 
                    payload = EXCLUDED.payload,
                    updated_at = NOW()
            """,
                (world_id, world_json),
            )

            logger.info(f"World saved to PostgreSQL (id={world_id})")

    async def load_from_postgres(self, world_id: int) -> World:
        """Load world state from PostgreSQL."""
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        async with (
            await psycopg.AsyncConnection.connect(database_url) as conn,
            conn.cursor() as cur,
        ):
            await cur.execute(
                "SELECT payload, updated_at FROM worlds WHERE id = %s", (world_id,)
            )
            row = await cur.fetchone()

            if not row:
                raise ValueError(f"World with id={world_id} not found in database")

            # row is a tuple: (payload, updated_at)
            payload, updated_at = row
            world_data = json.loads(payload)
            world = World(**world_data)

            logger.info(
                f"World loaded from PostgreSQL (id={world_id}, updated={updated_at})"
            )
            return world

    def save_to_postgres_sync(self, world: World, world_id: int) -> None:
        """Synchronously save the world state to PostgreSQL."""
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        with psycopg.connect(database_url) as conn:
            world_json = json.dumps(world.model_dump())

            # Upsert - insert or update if exists
            conn.execute(
                """
                INSERT INTO worlds (id, payload, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
                ON CONFLICT (id) 
                DO UPDATE SET 
                    payload = EXCLUDED.payload,
                    updated_at = NOW()
            """,
                (world_id, world_json),
            )

            logger.info(f"World saved to PostgreSQL sync (id={world_id})")

    def load_from_postgres_sync(self, world_id: int) -> World:
        """Synchronously load world state from PostgreSQL."""
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        with psycopg.connect(database_url) as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT payload, updated_at FROM worlds WHERE id = %s", (world_id,)
            )
            row = cur.fetchone()

            if not row:
                raise ValueError(f"World with id={world_id} not found in database")

            # row is a tuple: (payload, updated_at)
            payload, updated_at = row
            world = World(**payload)

            logger.info(
                f"World loaded from PostgreSQL sync (id={world_id}, updated={updated_at})"
            )
            return world

    async def start_periodic_save(
        self, world: World, world_id: int = 1, interval_seconds: int = 300
    ):
        """Start a background task that periodically saves the world.

        Args:
            world: The world instance to save
            world_id: ID of the world (default: 1)
            interval_seconds: Seconds between saves (default: 300 = 5 minutes)
        """
        logger.info(
            f"Starting periodic save every {interval_seconds} seconds for world {world_id}"
        )

        while True:
            await asyncio.sleep(interval_seconds)
            try:
                await self.save(world, world_id)
                logger.info(f"Periodic save completed for world {world_id}")
            except Exception as e:
                logger.error(f"Periodic save failed: {e}")
