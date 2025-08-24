from pydantic import BaseModel


# A player is a character in the game
class Player(BaseModel):
    id: str  # Unique player ID (could be token/auth ID)
    name: str
    description: str  # Detailed appearance, clothing, notable items, characteristics
    current_room: str  # Room ID where player is located
    inventory: list[str] = []  # List of item IDs in inventory
    effects: list[
        str
    ] = []  # Effects on the player ("Your clothes are wet", "You're covered in mud")
