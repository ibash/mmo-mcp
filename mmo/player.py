import re
import bcrypt
from datetime import datetime
from pydantic import BaseModel, Field
from mmo.errors import GameError


# A player is a character in the game
class Player(BaseModel):
    id: str  # Unique player ID (could be token/auth ID)
    created_at: datetime = Field(
        default_factory=datetime.now
    )  # When player was first created
    name: str
    description: str  # Detailed appearance, clothing, notable items, characteristics
    current_room: str  # Room ID where player is located
    inventory: list[str] = []  # List of item IDs in inventory
    password_hash: str  # Bcrypt hash of the player's password
    effects: list[
        str
    ] = []  # Effects on the player ("Your clothes are wet", "You're covered in mud")
    last_action_at: datetime = Field(
        default_factory=datetime.now
    )  # When player last did something

    @staticmethod
    def validate_id(player_id: str) -> str:
        """
        Validates and normalizes a player ID.

        Rules:
        - 3-20 characters long
        - Only alphanumeric, underscore, and hyphen
        - Must start with alphanumeric character
        - Returns normalized (lowercase) version

        Raises:
            GameError: If player_id is invalid
        """
        if not player_id:
            raise GameError("Player ID is required")

        # Check length
        if len(player_id) < 3:
            raise GameError("Player ID must be at least 3 characters long")
        if len(player_id) > 20:
            raise GameError("Player ID must be 20 characters or less")

        # Check pattern: must start with alphanumeric, then alphanumeric/underscore/hyphen
        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$", player_id):
            raise GameError(
                "Player ID must start with a letter or number and contain only "
                "letters, numbers, underscores, and hyphens"
            )

        # Return normalized (lowercase) version
        return player_id.lower()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt with rounds=6 for ~4ms latency."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=6)).decode(
            "utf-8"
        )

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def touch(self) -> None:
        """Update last_action_at to current time."""
        self.last_action_at = datetime.now()

    def describe_self(self, world) -> str:
        """Describe yourself - includes private information like inventory."""
        info = f"**You are: {self.name}**\n\n"
        info += f"**Player ID:** {self.id}\n\n"
        info += f"**Description:** {self.description}\n"

        if self.effects:
            effects_text = " ".join(self.effects)
            info += f"**Current effects:** {effects_text}\n"

        current_room = world.rooms.get(self.current_room)
        if current_room:
            info += f"\n**Current location:** {current_room.name}\n"

        if self.inventory:
            info += f"\n**Inventory ({len(self.inventory)} items):**\n"
            for item_id in self.inventory:
                item = world.items.get(item_id)
                if item:
                    info += f"- {item.name}: {item.description}\n"
        else:
            info += "\n**Inventory:** Empty"

        return info

    def describe_for_others(self) -> str:
        """Describe this player as seen by others - public information only."""
        desc = f"{self.name}: {self.description}"
        if self.effects:
            effects_text = " ".join(self.effects)
            desc += f" {effects_text}"
        return desc
