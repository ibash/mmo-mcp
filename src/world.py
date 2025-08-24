from pydantic import BaseModel
from .room import Room
from .player import Player
from .errors import GameError
from .effects_agent import get_action_effects


class World(BaseModel):
    rooms: dict[str, Room] = {}  # room_id -> Room
    players: dict[str, Player] = {}  # player_id -> Player

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
                    # Show full description
                    player_desc = f"- {other.name}: {other.description}"
                    if other.effects:
                        effects_text = " ".join(other.effects)
                        player_desc += f" {effects_text}"
                    response += f"{player_desc}\n"
            response += "\n"

        # List items in the room (placeholder for now)
        # TODO: Implement items
        # if current_room.items:
        #     response += "**Items here:**\n"
        #     for item in current_room.items:
        #         response += f"- {item}\n"
        #     response += "\n"

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

        # Get effects from the AI agent
        try:
            action_effects = await get_action_effects(
                action=action,
                actor_id=player_id,
                actor_name=player.name,
                room_id=current_room.id,
                room_description=current_room.describe(),
                other_players=other_players,
            )

            # Apply the effects
            for effect in action_effects.effects:
                if effect.target_type == "room" and effect.target_id in self.rooms:
                    self.rooms[effect.target_id].effects.append(effect.effect)
                elif (
                    effect.target_type == "player" and effect.target_id in self.players
                ):
                    self.players[effect.target_id].effects.append(effect.effect)
                # TODO: Handle items when we implement them

            return action_effects.response

        except Exception as e:
            # Fallback to basic response if AI fails
            print(f"Effects agent failed: {e}")
            current_room.effects.append(f"Signs of recent activity: {action}.")
            return f"You {action}."
