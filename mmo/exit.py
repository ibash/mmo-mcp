from pydantic import BaseModel, Field


class Exit(BaseModel):
    """Represents an exit from one room to another."""

    keyword: str = Field(
        description="Short keyword for the movement command (e.g., 'mall', 'stairs', 'vent')"
    )
    target_room_id: str = Field(description="ID of the room this exit leads to")
    movement_phrase: str = Field(
        description="How to describe moving through this exit (e.g., 'enter the mall', 'climb the stairs')"
    )
