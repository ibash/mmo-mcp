from pydantic import BaseModel, Field
from .exit import Exit


class Room(BaseModel):
    id: str
    name: str
    description: str
    exits: list[Exit] = Field(default_factory=list)  # List of exits to other rooms
    items: list[str] = []  # List of item IDs
    players: list[str] = []  # List of player IDs currently in room
    effects: list[
        str
    ] = []  # Effects that modify the room ("The floor is wet", "Scorch marks on the wall")

    def describe(self) -> str:
        """Return a text description of the room, including any effects."""
        base_description = self.description

        if self.effects:
            effects_text = " ".join(self.effects)
            return f"{base_description} {effects_text}"

        return base_description
