from pydantic import BaseModel, Field
from fastmcp import FastMCP, Context
from .errors import GameError
from .world import World
import json


# Input models for tools
class HandOfGodInput(BaseModel):
    target_type: str = Field(
        description="Type of object to modify: 'room', 'player', or 'item'"
    )
    target_id: str = Field(description="ID of the object to modify")
    field: str = Field(
        description="Field to modify (e.g., 'name', 'description', 'effects')"
    )
    value: str = Field(
        description="New value for the field (JSON string for complex types)"
    )


class Admin:
    """Admin tools for managing and debugging the game world."""

    def __init__(self, world: World):
        self.world = world

    def world_state(self, ctx: Context) -> str:
        """Get the complete state of the world (admin only)."""
        self._require_admin(ctx)

        # Get full world state using Pydantic's model_dump
        state = self.world.model_dump()

        # Add summary
        summary = {
            "total_rooms": len(self.world.rooms),
            "total_players": len(self.world.players),
            "total_items": len(self.world.items),
            "online_players": len(
                [p for p in self.world.players.values()]
            ),  # TODO: track online status
        }

        return f"""**WORLD STATE**

**Summary:**
- Rooms: {summary["total_rooms"]}
- Players: {summary["total_players"]}
- Items: {summary["total_items"]}

**Full State:**
```json
{json.dumps(state, indent=2)}
```"""

    def show_map(self, ctx: Context) -> str:
        """Display an ASCII map of the world (admin only)."""
        self._require_admin(ctx)

        # Build a grid representation of rooms
        room_coords = {}
        visited = set()

        def map_rooms(room_id, x=0, y=0):
            """Recursively map room positions."""
            if room_id in visited:
                return
            visited.add(room_id)
            room_coords[room_id] = (x, y)

            room = self.world.rooms.get(room_id)
            if not room:
                return

            # Map connected rooms
            if "north" in room.connections:
                map_rooms(room.connections["north"], x, y - 1)
            if "south" in room.connections:
                map_rooms(room.connections["south"], x, y + 1)
            if "east" in room.connections:
                map_rooms(room.connections["east"], x + 1, y)
            if "west" in room.connections:
                map_rooms(room.connections["west"], x - 1, y)

        # Start mapping from room_1
        if "room_1" in self.world.rooms:
            map_rooms("room_1")

        if not room_coords:
            return "No rooms to map!"

        # Find bounds
        min_x = min(x for x, y in room_coords.values())
        max_x = max(x for x, y in room_coords.values())
        min_y = min(y for x, y in room_coords.values())
        max_y = max(y for x, y in room_coords.values())

        # Build the map
        lines = []
        for y in range(min_y, max_y + 1):
            room_line = ""
            conn_line = ""
            player_line = ""

            for x in range(min_x, max_x + 1):
                # Find room at this position
                room_id = None
                for rid, (rx, ry) in room_coords.items():
                    if rx == x and ry == y:
                        room_id = rid
                        break

                if room_id:
                    room = self.world.rooms[room_id]
                    # Room box
                    room_num = room_id.replace("room_", "R")
                    player_count = len(room.players)
                    player_indicator = (
                        f"[{player_count}]" if player_count > 0 else "   "
                    )

                    room_line += f"[{room_num:^7}]"
                    player_line += f" {player_indicator:^7} "

                    # Connections
                    east_conn = "---" if "east" in room.connections else "   "
                    room_line += east_conn
                    player_line += "   "

                    south_conn = " | " if "south" in room.connections else "   "
                    conn_line += f"    {south_conn}     "
                else:
                    room_line += "            "
                    player_line += "            "
                    conn_line += "            "

            lines.append(room_line)
            lines.append(player_line)
            if y < max_y:
                lines.append(conn_line)

        # Add legend
        legend = """
**Legend:**
[R#] = Room number
[#] = Number of players in room
--- = East/West connection
 |  = North/South connection"""

        # List rooms with names
        room_list = "\n**Rooms:**\n"
        for room_id in sorted(self.world.rooms.keys()):
            room = self.world.rooms[room_id]
            players_here = [
                self.world.players[pid].name
                for pid in room.players
                if pid in self.world.players
            ]
            players_str = f" ({', '.join(players_here)})" if players_here else ""
            room_list += f"- {room_id}: {room.name}{players_str}\n"

        return f"""**WORLD MAP**

```
{chr(10).join(lines)}
```
{legend}
{room_list}"""

    def hand_of_god(self, ctx: Context, input: "HandOfGodInput") -> str:
        """Directly modify any data in the world (admin only)."""
        self._require_admin(ctx)

        # Find and modify the target
        if input.target_type == "room":
            if input.target_id not in self.world.rooms:
                raise GameError(f"Room {input.target_id} does not exist.")
            target = self.world.rooms[input.target_id]
            old_value = getattr(target, input.field, None)
        elif input.target_type == "player":
            if input.target_id not in self.world.players:
                raise GameError(f"Player {input.target_id} does not exist.")
            target = self.world.players[input.target_id]
            old_value = getattr(target, input.field, None)
        elif input.target_type == "item":
            if input.target_id not in self.world.items:
                raise GameError(f"Item {input.target_id} does not exist.")
            target = self.world.items[input.target_id]
            old_value = getattr(target, input.field, None)
        else:
            raise GameError(f"Invalid target type: {input.target_type}")

        # Parse value if it's JSON
        try:
            new_value = json.loads(input.value)
        except:
            new_value = input.value

        # Apply the modification
        try:
            setattr(target, input.field, new_value)
        except Exception as e:
            raise GameError(f"Failed to modify {input.field}: {str(e)}")

        return f"""**HAND OF GOD**

Modified {input.target_type} '{input.target_id}':
- Field: {input.field}
- Old value: {old_value}
- New value: {new_value}

The world has been altered."""

    # TODO: Implement room_editor method
    # def room_editor(self, ctx: Context, input: RoomEditorInput) -> str:
    #     """Create or edit rooms in the world (admin only)."""
    #     pass

    def register(self, mcp: FastMCP):
        """Register all admin tools with the MCP server."""
        mcp.tool(self.world_state)
        mcp.tool(self.show_map)
        mcp.tool(self.hand_of_god)

    def _require_admin(self, ctx: Context) -> None:
        """Check if the current player has admin privileges."""
        player_id = ctx.get_state("player_id")

        if player_id not in self.world.players:
            raise GameError("You need to create a character first!")

        player = self.world.players[player_id]
        if not player.is_admin():
            raise GameError("This command requires admin privileges.")
