from datetime import datetime
from pydantic import BaseModel, Field


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
    effects: list[
        str
    ] = []  # Effects on the player ("Your clothes are wet", "You're covered in mud")
    last_action_at: datetime = Field(
        default_factory=datetime.now
    )  # When player last did something

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
