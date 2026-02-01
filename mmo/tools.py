from pydantic import BaseModel, Field
from .player import Player
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_request
from .errors import GameError
from .game_world import world
from .character_creation_guide import AUTONOMOUS_GUIDE, HUMAN_GUIDE


def get_character_creation_guide(ctx: Context) -> str:
    """Get the character creation guide with the optimized multi-stage approach.

    IMPORTANT: Always call this BEFORE using create_character to ensure you follow
    the proper process for creating unique, non-cliché characters."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    # Check if player already exists
    if world.player_exists(player_id):
        player = world.players[player_id]
        return f"You already have a character named {player.name}. No need for the creation guide!"

    if autonomous:
        return AUTONOMOUS_GUIDE
    else:
        return HUMAN_GUIDE


def look(ctx: Context) -> str:
    """Examine your current surroundings."""

    player_id = ctx.get_state("player_id")

    try:
        return world.look(player_id)
    except GameError as e:
        return str(e)


class CreateCharacterInput(BaseModel):
    name: str = Field(description="The character's name")
    description: str = Field(
        description="Detailed description of the character's appearance, clothing, and notable characteristics"
    )


def create_character(ctx: Context, input: CreateCharacterInput) -> str:
    """Create a new character for the player.

    IMPORTANT: Always call get_character_creation_guide FIRST to ensure you follow
    the proper multi-stage process for creating unique, memorable characters."""

    player_id = ctx.get_state("player_id")
    if not player_id:
        return "Error: player_id needs to be set in the URL"

    # Check if player already exists
    if world.player_exists(player_id):
        player = world.players[player_id]
        return f"You already have a character named {player.name}"

    # Get password from request for new player
    request = get_http_request()
    password = request.query_params.get("password")
    if not password:
        return "Error: password is required for authentication"

    # Create new player with hashed password
    new_player = Player(
        id=player_id,
        name=input.name,
        description=input.description,
        current_room="nexus_clearing",  # Will be set by add_player
        password_hash=Player.hash_password(password),
    )

    # Add player to world and starting room
    world.add_player(new_player, "nexus_clearing")
    starting_room = world.rooms[new_player.current_room]

    return f"""Character created successfully!

Name: {input.name}
Description: {input.description}

You find yourself in the {starting_room.name}.
{starting_room.describe()}

Type 'look' to examine your surroundings or 'move [direction]' to start exploring!"""


class MoveInput(BaseModel):
    direction: str = Field(
        description="The direction to move (e.g., 'north', 'through the office door', 'up the stairs')"
    )


def move(ctx: Context, input: MoveInput) -> str:
    """Move to an adjacent room."""

    player_id = ctx.get_state("player_id")

    try:
        return world.move_player(player_id, input.direction)
    except GameError as e:
        return str(e)


class DoInput(BaseModel):
    action: str = Field(
        description="The action to perform (e.g., 'spill water on the floor', 'sit on the chair', 'write hello on the wall')"
    )


async def do(ctx: Context, input: DoInput) -> str:
    """Perform an arbitrary action that affects the world."""

    player_id = ctx.get_state("player_id")

    try:
        return await world.do_action(player_id, input.action)
    except GameError as e:
        return str(e)


class PickupInput(BaseModel):
    item_name: str = Field(description="Name or partial name of the item to pick up")


def pickup(ctx: Context, input: PickupInput) -> str:
    """Pick up an item from the current room."""

    player_id = ctx.get_state("player_id")

    try:
        return world.pickup_item(player_id, input.item_name)
    except GameError as e:
        return str(e)


class DropInput(BaseModel):
    item_name: str = Field(description="Name or partial name of the item to drop")


def drop(ctx: Context, input: DropInput) -> str:
    """Drop an item from your inventory."""

    player_id = ctx.get_state("player_id")

    try:
        return world.drop_item(player_id, input.item_name)
    except GameError as e:
        return str(e)


def inventory(ctx: Context) -> str:
    """Check what you're carrying."""

    player_id = ctx.get_state("player_id")

    try:
        return world.get_inventory(player_id)
    except GameError as e:
        return str(e)


class ConjureInput(BaseModel):
    name: str = Field(
        description="Name of the item to create (e.g., 'wooden staff', 'glowing orb')"
    )
    description: str = Field(
        description="Detailed description of the item's appearance and properties"
    )


def conjure(ctx: Context, input: ConjureInput) -> str:
    """Create a new item in the world."""

    player_id = ctx.get_state("player_id")

    try:
        return world.conjure_item(player_id, input.name, input.description)
    except GameError as e:
        return str(e)


def whoami(ctx: Context) -> str:
    """Check who you are currently playing as."""

    player_id = ctx.get_state("player_id")
    return world.get_player_info(player_id)


def register(mcp: FastMCP):
    mcp.tool(get_character_creation_guide)
    mcp.tool(look)
    mcp.tool(create_character)
    mcp.tool(move)
    mcp.tool(do)
    mcp.tool(pickup)
    mcp.tool(drop)
    mcp.tool(inventory)
    mcp.tool(conjure)
    mcp.tool(whoami)
