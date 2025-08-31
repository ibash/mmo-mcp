from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str = Field(description="Unique identifier for the item (e.g., 'sword_1234')")
    name: str = Field(description="Display name of the item (e.g., 'rusty sword')")
    description: str = Field(
        description="Detailed description of the item's appearance and characteristics"
    )
    effects: list[str] = Field(
        default=[],
        description="Dynamic effects applied to the item (e.g., 'The blade gleams', 'It's covered in mud')",
    )
    portable: bool = Field(
        default=True, description="Whether the item can be picked up and carried"
    )

    def describe(self) -> str:
        """Return formatted description including name, description, and effects."""
        result = f"{self.name}: {self.description}"
        if self.effects:
            effects_text = " ".join(self.effects)
            result += f" {effects_text}"
        return result
