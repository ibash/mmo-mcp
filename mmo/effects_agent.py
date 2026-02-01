from typing import List, Literal
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from .settings import settings


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
    destroyed: bool = Field(
        default=False,
        description="Set to true if an item is completely destroyed/consumed by the action (only valid for target_type='item')"
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

ITEM DESTRUCTION:
When an action would completely destroy, consume, or eliminate an item, set destroyed=true.
Examples of destructive actions: burning, smashing, eating, dissolving, throwing into a void.
When destroyed=true, also provide an effect describing what happened (e.g., "shattered into pieces").
The item will be permanently removed from the game.

Examples:
- Action: "splash water on Alice" 
  Effects: room gets "The floor is wet.", Alice gets "Your clothes are soaked."
- Action: "write 'hello' on the wall"
  Effects: room gets "Someone has written 'hello' on the wall."
- Action: "sit down"
  Effects: player gets "You are sitting down."
- Action: "smash the vase"
  Effects: item (vase) gets effect "shattered into countless pieces" with destroyed=true,
           room gets "Broken pottery shards litter the floor."
- Action: "burn the book"
  Effects: item (book) gets effect "consumed by flames, now just ashes" with destroyed=true,
           room gets "The smell of burnt paper lingers."
"""

effects_agent = Agent(
    AnthropicModel(
        "claude-3-7-sonnet-latest",
        provider=AnthropicProvider(api_key=settings.anthropic_api_key),
    ),
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

    # Build item and player mappings with clear ID associations
    items_with_ids = [f"{name} (ID: {id})" for id, name in room_items.items()] if room_items else []
    players_with_ids = [f"{name} (ID: {id})" for id, name in other_players.items()] if other_players else []

    context = f"""
Action: {action}
Actor: {actor_name} (ID: {actor_id})
Room: {room_description} (ID: {room_id})
Other players in room: {", ".join(players_with_ids) if players_with_ids else "None"}
Items in room: {", ".join(items_with_ids) if items_with_ids else "None"}

Determine the effects of this action. Consider:
1. Effects on the room itself (use room ID: {room_id})
2. Effects on the actor (use player ID: {actor_id})
3. Effects on other players mentioned in the action (use their IDs)
4. Effects on items mentioned in the action (use their IDs)

IMPORTANT: When targeting items for effects (especially destruction), use the exact item ID shown above.
"""

    result = await effects_agent.run(context)
    return result.output
