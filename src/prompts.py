from fastmcp import FastMCP, Context
from .world_seed import seed_world
from .errors import GameError

# Use the seed world as our game world (in-memory for now)
world = seed_world


def play(ctx: Context) -> str:
    """Main entry point for the game - introduces the game and handles player registration."""

    # Check if player_id is set
    player_id: str = ctx.get_state("player_id")
    if not player_id:
        return "Error: player_id needs to be set in the URL (e.g., ?player_id=YOUR_ID)"

    autonomous: bool = ctx.get_state("autonomous")

    # Look up player in the world
    player = world.players.get(player_id)

    # Check if player is registered
    if player and player.name and player.description:
        # Player is already registered
        if autonomous:
            # Direct instructions for autonomous AI
            return f"""Welcome back, {player.name}!

You are in: {world.rooms[player.current_room].name}

This is a persistent multiplayer text-based dungeon crawler where every action has lasting consequences.
You are playing as an autonomous AI adventurer. The world continues evolving even when you're away.

Your role as an autonomous player:
- Explore the interconnected rooms and discover the world
- Interact with other players (both human-controlled and AI)
- Create objects using 'conjure' to enhance the environment
- Perform creative actions with 'do' that permanently change rooms
- Build your own story and leave your mark on the world

Available actions:
- look: Examine your surroundings and see other players
- move [direction]: Travel north, south, east, or west
- conjure [item] [description]: Create objects in the world
- do [action]: Perform actions with objects or the environment
- pickup [item]: Take an item
- drop [item]: Drop an item from your inventory
- inventory: See what you're carrying
- say [message]: Speak to others in the room

Start by using 'look' to understand your surroundings, then begin your adventure!
Be creative and memorable - other players will experience the results of your actions."""
        else:
            # Instructions for AI helping a human
            return f"""Welcome back to the Dungeon Crawler!

The player {player.name} is currently in: {world.rooms[player.current_room].name}

This is a persistent multiplayer text-based dungeon crawler where every action has lasting consequences.
You are helping a human player navigate and interact with this living world.

Your role as their assistant:
- Ask the human what they'd like to do
- Suggest interesting actions they might take
- Execute their choices using the available tools
- Describe what happens in an engaging way
- Keep them informed about other players and changes in the environment

Available actions for the player:
- look: Examine surroundings
- move [direction]: Travel to adjacent rooms
- conjure [item] [description]: Create objects
- do [action]: Perform actions with the environment
- pickup/drop: Manage inventory
- say: Talk to others in the room

Ask the human what they'd like to do next, and help them explore this world where their actions permanently shape the environment!"""

    else:
        # Player needs to register
        # TODO: Add a character creation tool to help AI/humans create rich character descriptions
        if autonomous:
            # Registration for autonomous AI
            return """Welcome to the Dungeon Crawler!

This is a persistent multiplayer text-based adventure where you explore interconnected rooms, 
interact with objects and other players, and shape the world through your actions.

As an autonomous AI player, you need to create your character:

1. Choose a creative and unique character name
2. Write a detailed description including:
   - Physical appearance and distinctive features
   - Clothing and equipment
   - Personality traits and quirks
   - Brief backstory or motivation for adventuring

Be creative! Your character will interact with both human players and other AIs.
Your description is what others will see when they encounter you.

Use the create_character tool with your chosen name and description to begin your adventure!"""
        else:
            # Registration for human player
            return """Welcome to the Dungeon Crawler!

This is a persistent multiplayer text-based adventure where you explore interconnected rooms, 
interact with objects and other players, and shape the world through your actions.

You're helping a human player join the game. Please:

1. Ask them for their character's name
2. Ask for basic details about their character (appearance, clothing, personality)
3. Take their input and elaborate it into a rich, detailed description that includes:
   - Vivid physical details and distinctive features
   - Clothing described with textures, colors, and wear
   - Equipment or notable items with character
   - Personality quirks or mannerisms
   - Hints of backstory or motivation

Your role: Transform their simple ideas into an immersive character description that will captivate other players.
For example, if they say "a warrior with a sword", you might elaborate into "a battle-scarred warrior with weathered leather armor, carrying an ancient blade etched with mysterious runes..."

Once you've crafted the enhanced description, confirm it with them, then use create_character to begin!"""


def look(ctx: Context) -> str:
    """Look around and observe your surroundings."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        room_description = world.look(player_id)

        if autonomous:
            # For autonomous AI - full description and encourage action
            return f"""{room_description}

You are an autonomous AI adventurer. Consider your surroundings carefully:
- Who else is here that you could interact with?
- What objects could you create to enhance this space?
- Which direction seems most interesting to explore?
- What creative action could leave your mark here?

Think about what you want to do next, then take action! Use the available tools to:
- 'say' something to other players
- 'move' to explore new areas
- 'conjure' items to add to the world
- 'do' creative actions that change the environment"""
        else:
            # For human player - summarize and suggest
            return f"""**Full room details:**
{room_description}

**Summary for the human player:**
Please provide a 3-4 sentence summary of the surroundings, highlighting:
- The atmosphere of the current location
- Any other players present
- Anything unusual, notable, or out of place that would immediately catch someone's eye
- Available directions to explore

Focus on what someone would naturally notice first when entering the room - the obvious, the odd, or the interesting.

**Suggested actions:**
Based on the surroundings, suggest 3-4 interesting actions the player could take, such as:
- Talking to specific players if present
- Exploring a particular direction that sounds intriguing
- Creating objects that would fit the setting
- Performing actions that would be fun or useful

Ask the human what they'd like to do next!"""

    except GameError as e:
        return str(e)


def move(ctx: Context, direction: str) -> str:
    """Move in a specific direction and describe the journey."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        # Attempt to move the player
        result = world.move_player(player_id, direction)

        if autonomous:
            # For autonomous AI - describe the move and encourage exploration
            return f"""{result}

You've entered a new area! As an autonomous adventurer:
- Look around carefully at this new environment
- Consider what objects might be useful to conjure here
- Think about how you could modify this space
- Decide if you want to explore further or interact with what's here

What will you do in this new location?"""
        else:
            # For human player - describe the move and ask for input
            return f"""{result}

**For the human player:**
Please describe to them:
1. The feeling of moving {direction}
2. What they notice first as they enter
3. Any immediate sensations (sounds, smells, temperature)

Then ask what they'd like to do in this new location. Suggest a few options based on what's available here."""

    except GameError as e:
        # Movement failed
        if autonomous:
            return f"""{str(e)}

You cannot move {direction} from here. Consider:
- Checking available directions with 'look'
- Exploring a different direction
- Interacting with the current room instead"""
        else:
            return f"""{str(e)}

Let the human know they cannot go {direction}. Suggest they:
- Look around to see available exits
- Try a different direction
- Explore their current location more thoroughly"""


async def do(ctx: Context, action: str) -> str:
    """Perform an action and describe its effects."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        # Perform the action
        result = await world.do_action(player_id, action)

        if autonomous:
            # For autonomous AI - acknowledge and encourage creativity
            return f"""{result}

Your action has affected the world! Consider:
- How did this change the environment?
- Did it affect other players?
- What new possibilities has this created?
- What would be an interesting follow-up action?

The world is dynamic and responsive to your creativity. Continue shaping it!"""
        else:
            # For human player - describe vividly and prompt for next action
            return f"""{result}

**For the human player:**
Describe the action vividly, including:
- The physical motions involved
- Any sounds or sensations
- How the environment changed
- Reactions from other players if affected

Then ask what they'd like to do next. The world has permanently changed from their action!"""

    except GameError as e:
        # Action failed
        if autonomous:
            return f"""{str(e)}

Your action couldn't be performed. Consider:
- Are you trying something impossible?
- Do you need to be more specific?
- Is there a different approach?"""
        else:
            return f"""{str(e)}

Let the human know their action couldn't be performed. Suggest:
- Being more specific about what they want to do
- Trying a different approach
- Checking their surroundings first with 'look'"""


# TODO: Update this prompt to mention trading once give/trade tools are implemented
def pickup(ctx: Context, item_name: str) -> str:
    """Pick up an item from the current room."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        result = world.pickup_item(player_id, item_name)

        if autonomous:
            return f"""{result}

You now have this item in your inventory. Consider:
- Using it in creative ways with 'do'
- Dropping it in strategic locations"""
        else:
            return f"""{result}

Tell the human player they've successfully picked up the item.
It's now in their inventory and they can:
- Drop it elsewhere
- Use it with the 'do' command
- Check their inventory to see all carried items"""

    except GameError as e:
        if autonomous:
            return f"""{str(e)}

Try looking around to see what items are available."""
        else:
            return f"""{str(e)}

Let the human know they couldn't pick up that item. Suggest they:
- Look around to see available items
- Check if they typed the name correctly"""


def drop(ctx: Context, item_name: str) -> str:
    """Drop an item from your inventory."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        result = world.drop_item(player_id, item_name)

        if autonomous:
            return f"""{result}

The item is now in this room for others to find. Consider:
- The strategic value of leaving items in certain locations
- Creating item caches or gifts for other players
- How this changes the room's character"""
        else:
            return f"""{result}

Tell the human they've dropped the item here.
Other players will be able to see and pick it up.
The item remains in this room permanently unless someone takes it."""

    except GameError as e:
        if autonomous:
            return f"""{str(e)}

Check your inventory to see what you're carrying."""
        else:
            return f"""{str(e)}

Let the human know they don't have that item. Suggest checking their inventory."""


# TODO: Update this prompt to mention trading once give/trade tools are implemented
def inventory(ctx: Context) -> str:
    """Check what you're carrying."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        result = world.get_inventory(player_id)

        if autonomous:
            if "not carrying anything" in result:
                return f"""{result}

Your inventory is empty. Consider:
- Looking for items in rooms
- Conjuring new items to carry"""
            else:
                return f"""{result}

These are your current possessions. Think about:
- Which items might be useful here
- Where strategic placement might help others"""
        else:
            return f"""{result}

**For the human player:**
Show them their inventory and explain they can:
- Drop items to leave them in rooms
- Pick up items they find while exploring
- Use items in creative ways with the 'do' command"""

    except GameError as e:
        return str(e)


def conjure(ctx: Context, name: str, description: str) -> str:
    """Create a new item in the world."""

    player_id = ctx.get_state("player_id")
    autonomous = ctx.get_state("autonomous")

    try:
        result = world.conjure_item(player_id, name, description)

        if autonomous:
            return f"""{result}

You've added a permanent object to the world! Consider:
- How this item might be used by others
- Whether to leave it here or carry it elsewhere
- What other items might complement this one"""
        else:
            return f"""{result}

**For the human player:**
Explain that they've created a permanent item that:
- Will exist forever in the game world
- Can be picked up, dropped, and used by anyone
- Adds to the collaborative storytelling

Suggest they might:
- Pick it up to carry with them
- Leave it for others to discover
- Create more items to build up the world"""

    except GameError as e:
        return str(e)


def register(mcp: FastMCP):
    mcp.prompt(play)
    mcp.prompt(look)
    mcp.prompt(move)
    mcp.prompt(do)
    mcp.prompt(pickup)
    mcp.prompt(drop)
    mcp.prompt(inventory)
    mcp.prompt(conjure)
