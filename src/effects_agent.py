from pydantic import BaseModel, Field
from typing import List, Literal

from pydantic_ai import Agent


class Effect(BaseModel):
    target_id: str = Field(
        description="The ID of the target (room_id, player_id, or item_id)"
    )
    target_type: Literal["room", "player", "item"] = Field(
        description="The type of entity being affected"
    )
    effect: str = Field(
        description="A concise description of the effect/change (e.g., 'The floor is wet.', 'Your clothes are soaked.')"
    )


class ActionEffects(BaseModel):
    effects: List[Effect] = Field(
        description="List of effects that result from the action"
    )
    response: str = Field(
        description="What to tell the player about their action (e.g., 'You splash water on Alice. She is now soaked!')"
    )


SYSTEM_PROMPT = """You are interpreting actions in a multiplayer dungeon crawler game.
Given an action, determine what effects it should have on the world.

Consider:
- The room where the action takes place
- Who is performing the action
- Other players who might be affected
- Objects mentioned in the action
- Realistic consequences

Return effects as specific changes to rooms, players, or items.
Keep effects concise and descriptive.

Examples:
- Action: "splash water on Alice" 
  Effects: room gets "The floor is wet.", Alice gets "Your clothes are soaked."
- Action: "write 'hello' on the wall"
  Effects: room gets "Someone has written 'hello' on the wall."
- Action: "sit down"
  Effects: player gets "You are sitting down."
"""

effects_agent = Agent(
    "anthropic:claude-3-7-sonnet-latest",
    system_prompt=SYSTEM_PROMPT,
    output_type=ActionEffects,
)


async def get_action_effects(
    action: str,
    actor_id: str,
    actor_name: str,
    room_id: str,
    room_description: str,
    other_players: dict[str, str],  # player_id -> player_name
    room_items: dict[str, str],  # item_id -> item_name
) -> ActionEffects:
    """Interpret an action and return its effects on the world."""

    # TODO(ibash) the names of the other players, items, etc are first in the
    # prompt, but we never specify which item name maps to which id... check on
    # this

    # TODO: Handle items getting destroyed (e.g., "burn the book", "smash the vase")
    # This will need a new effect type or a special effect like "DESTROYED" that
    # the World class can interpret to remove the item from existence
    context = f"""
Action: {action}
Actor: {actor_name} (ID: {actor_id})
Room: {room_description} (ID: {room_id})
Other players in room: {", ".join(other_players.values()) if other_players else "None"}
Items in room: {", ".join(room_items.values()) if room_items else "None"}

Determine the effects of this action. Consider:
1. Effects on the room itself
2. Effects on the actor
3. Effects on other players mentioned in the action
4. Effects on items mentioned in the action

Available player IDs: {list(other_players.keys()) if other_players else []}
Available item IDs: {list(room_items.keys()) if room_items else []}
"""

    result = await effects_agent.run(context)
    return result.output
