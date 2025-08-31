from pydantic import BaseModel
from .room import Room
from .player import Player
from .item import Item
from .errors import GameError
from .effects_agent import get_action_effects
import uuid
import re


class World(BaseModel):
    rooms: dict[str, Room] = {}  # room_id -> Room
    players: dict[str, Player] = {}  # player_id -> Player
    items: dict[str, Item] = {}  # item_id -> Item

    def add_player(self, player: Player, room_id: str) -> None:
        """Add a player to the world and place them in a specific room."""
        assert room_id in self.rooms, f"Room {room_id} does not exist"

        # Add player to world
        self.players[player.id] = player

        # Set player's current room
        player.current_room = room_id

        # Add player to the room
        self.rooms[room_id].players.append(player.id)

    def get_player_and_room(self, player_id: str) -> tuple[Player, Room]:
        """Get a player and their current room, with validation."""
        if not player_id:
            raise GameError("player_id needs to be set in the URL")

        if player_id not in self.players:
            raise GameError(
                "You need to create a character first! Use the play prompt to get started."
            )

        player = self.players[player_id]
        current_room = self.rooms[player.current_room]

        return player, current_room

    def look(self, player_id: str) -> str:
        """Get a description of what the player can see."""
        player, current_room = self.get_player_and_room(player_id)

        # Build the response
        response = f"**{current_room.name}**\n\n"
        response += f"{current_room.describe()}\n\n"

        # List other players in the room
        other_players = [pid for pid in current_room.players if pid != player_id]
        if other_players:
            response += "**Players here:**\n"
            for pid in other_players:
                other = self.players.get(pid)
                if other:
                    response += f"- {other.describe_for_others()}\n"
            response += "\n"

        # List items in the room
        if current_room.items:
            response += "**Items here:**\n"
            for item_id in current_room.items:
                item = self.items.get(item_id)
                if item:
                    response += f"- {item.describe()}\n"
            response += "\n"

        # Show available exits and adjacent rooms
        if current_room.connections:
            response += "**Exits:**\n"
            for direction, room_id in current_room.connections.items():
                adjacent_room = self.rooms.get(room_id)
                if adjacent_room:
                    # Brief preview of adjacent room
                    preview = adjacent_room.description.split(".")[0]  # First sentence
                    response += f"- {direction.capitalize()}: {adjacent_room.name} ({preview}...)\n"
        else:
            response += "There are no visible exits.\n"

        return response

    def move_player(self, player_id: str, direction: str) -> str:
        """Move a player to an adjacent room."""
        player, current_room = self.get_player_and_room(player_id)

        # Normalize direction to lowercase
        direction = direction.lower()

        # Check if direction exists
        if direction not in current_room.connections:
            available = list(current_room.connections.keys())
            if available:
                raise GameError(
                    f"You can't go {direction}. Available directions: {', '.join(available)}"
                )
            else:
                raise GameError("There are no exits from this room.")

        # Get the destination room
        new_room_id = current_room.connections[direction]
        if new_room_id not in self.rooms:
            # This shouldn't happen with valid data, but check anyway
            # TODO(ibash) send an error to an error tracker
            raise GameError(f"The path {direction} leads nowhere...")

        new_room = self.rooms[new_room_id]

        # Move the player
        current_room.players.remove(player_id)
        player.current_room = new_room_id
        new_room.players.append(player_id)

        # Return description of new room
        return f"You move {direction} to {new_room.name}.\n\n{self.look(player_id)}"

    async def do_action(self, player_id: str, action: str) -> str:
        """Perform an arbitrary action that may affect the world."""
        player, current_room = self.get_player_and_room(player_id)

        # Build context for the AI
        other_players = {}
        for other_id in current_room.players:
            if other_id != player_id:
                other = self.players.get(other_id)
                if other:
                    other_players[other_id] = other.name

        # Build items context
        room_items = {}
        for item_id in current_room.items:
            item = self.items.get(item_id)
            if item:
                room_items[item_id] = item.name

        # Get effects from the AI agent
        try:
            action_effects = await get_action_effects(
                action=action,
                actor_id=player_id,
                actor_name=player.name,
                room_id=current_room.id,
                room_description=current_room.describe(),
                other_players=other_players,
                room_items=room_items,
            )

            # Apply the effects
            for effect in action_effects.effects:
                if effect.target_type == "room" and effect.target_id in self.rooms:
                    self.rooms[effect.target_id].effects.append(effect.effect)
                elif (
                    effect.target_type == "player" and effect.target_id in self.players
                ):
                    self.players[effect.target_id].effects.append(effect.effect)
                elif effect.target_type == "item" and effect.target_id in self.items:
                    self.items[effect.target_id].effects.append(effect.effect)

            return action_effects.response

        except Exception as e:
            # Fallback to basic response if AI fails
            print(f"Effects agent failed: {e}")
            current_room.effects.append(f"Signs of recent activity: {action}.")
            return f"You {action}."

    def pickup_item(self, player_id: str, item_name: str) -> str:
        """Handle picking up an item from the current room."""
        player, current_room = self.get_player_and_room(player_id)

        # Find matching item in room
        matching_item = self._find_item_by_name(current_room.items, item_name)

        if not matching_item:
            raise GameError(f"There's no '{item_name}' here to pick up.")

        if not matching_item.portable:
            raise GameError(f"The {matching_item.name} cannot be picked up.")

        # Move item from room to player inventory
        current_room.items.remove(matching_item.id)
        player.inventory.append(matching_item.id)

        return f"You pick up the {matching_item.name}."

    def drop_item(self, player_id: str, item_name: str) -> str:
        """Handle dropping an item from inventory."""
        player, current_room = self.get_player_and_room(player_id)

        # Find matching item in inventory
        matching_item = self._find_item_by_name(player.inventory, item_name)

        if not matching_item:
            raise GameError(f"You don't have '{item_name}' in your inventory.")

        # Move item from inventory to room
        player.inventory.remove(matching_item.id)
        current_room.items.append(matching_item.id)

        return f"You drop the {matching_item.name}."

    def get_inventory(self, player_id: str) -> str:
        """Get formatted inventory listing for a player."""
        if player_id not in self.players:
            raise GameError("You need to create a character first!")

        player = self.players[player_id]

        if not player.inventory:
            return "You're not carrying anything."

        response = "**Your inventory:**\n"
        for item_id in player.inventory:
            item = self.items.get(item_id)
            if item:
                response += f"- {item.describe()}\n"

        return response

    def conjure_item(self, player_id: str, name: str, description: str) -> str:
        """Create a new item in the world."""
        player, current_room = self.get_player_and_room(player_id)

        # Generate unique item ID - replace non-alphanumeric chars with underscore
        safe_name = re.sub(r"[^a-zA-Z0-9]+", "_", name.lower()).strip("_")
        item_id = f"{safe_name}_{uuid.uuid4().hex[:8]}"

        # Create the item
        new_item = Item(
            id=item_id,
            name=name,
            description=description,
            # Most conjured items should be portable by default
            # TODO(ibash) set this intelligently
            portable=True,
        )

        # Add to world and current room
        self.items[item_id] = new_item
        current_room.items.append(item_id)

        return f"You conjure {name} into existence. {description}"

    def player_exists(self, player_id: str) -> bool:
        """Check if a player with this ID exists."""
        return player_id in self.players if player_id else False

    def get_player_info(self, player_id: str) -> str:
        """Get information about the current player."""
        if not player_id:
            return "No player_id set. You need to connect with ?player_id=YOUR_ID in the URL."

        if not self.player_exists(player_id):
            return f"You are connected as '{player_id}' but haven't created a character yet. Use the 'play' prompt to get started!"

        player = self.players[player_id]
        return player.describe_self(self)

    def _find_item_by_name(self, item_ids: list[str], partial_name: str) -> Item | None:
        """Find an item by partial name match in a list of item IDs."""
        for item_id in item_ids:
            item = self.items.get(item_id)
            if item and partial_name.lower() in item.name.lower():
                return item
        return None
