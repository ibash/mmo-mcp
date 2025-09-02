#!/usr/bin/env python
"""CLI tool for inspecting and managing the game world."""

import argparse
import asyncio
import traceback

from mmo.persist import Persist
from mmo.world import World


class CLI:
    """CLI for managing and inspecting the game world."""

    def __init__(self):
        self.persist = Persist()

    async def load_world(self) -> World:
        """Load the world from persistence."""
        return await self.persist.load()

    async def inspect_world(self) -> None:
        """Load and display the world state in a formatted way."""
        try:
            world = await self.load_world()

            print("\n=== World Inspection ===\n")

            # Display Rooms
            print("Rooms:")
            for room_id, room in world.rooms.items():
                print(f"  {room_id}: {room.name}")
                print(f"    Description: {room.description}")
                if room.exits:
                    exits_str = ", ".join(
                        [
                            f"{exit.keyword} -> {exit.target_room_id}"
                            for exit in room.exits
                        ]
                    )
                    print(f"    Exits: {exits_str}")
                if room.players:
                    print(f"    Players: {', '.join(room.players)}")
                if room.items:
                    print(f"    Items: {', '.join(room.items)}")
                if room.effects:
                    print(f"    Effects: {', '.join(room.effects)}")
                print()

            # Display Players
            print("Players:")
            if world.players:
                for player_id, player in world.players.items():
                    print(f"  {player_id}: {player.name}")
                    print(f"    Description: {player.description}")
                    print(f"    Location: {player.current_room}")
                    if player.inventory:
                        print(f"    Inventory: {', '.join(player.inventory)}")
                    if player.effects:
                        print(f"    Effects: {', '.join(player.effects)}")
                    print()
            else:
                print("  No players in the world")
                print()

            # Display Items
            print("Items:")
            if world.items:
                for item_id, item in world.items.items():
                    print(f"  {item_id}: {item.name}")
                    print(f"    Description: {item.description}")
                    if item.effects:
                        print(f"    Effects: {', '.join(item.effects)}")
                    print(f"    Portable: {item.portable}")
                    print()
            else:
                print("  No items in the world")
                print()

            print(
                f"Summary: {len(world.rooms)} rooms, {len(world.players)} players, {len(world.items)} items"
            )

        except FileNotFoundError:
            print(
                "Error: World file not found. Make sure the game has been run and world has been saved."
            )
        except Exception as e:
            print(f"Error loading world: {e}")
            print("\nFull traceback:")
            traceback.print_exc()

    async def generate_mermaid(self) -> None:
        """Generate a Mermaid chart of the world."""
        try:
            world = await self.load_world()

            print("\n=== Mermaid Graph ===\n")
            print("```mermaid")
            print("graph TD")

            # Add nodes with room names
            for room_id, room in world.rooms.items():
                # Escape special characters and indicate if players are present
                label = room.name.replace('"', "'")
                if room.players:
                    players = ", ".join(room.players)
                    print(f'    {room_id}["{label}<br/>👤 {players}"]')
                else:
                    print(f'    {room_id}["{label}"]')

            # Add edges with direction labels
            seen_connections = set()
            for room_id, room in world.rooms.items():
                for exit in room.exits:
                    # Avoid duplicate edges in undirected graph
                    edge = tuple(sorted([room_id, exit.target_room_id]))
                    if edge not in seen_connections:
                        print(
                            f"    {room_id} ---|{exit.keyword}| {exit.target_room_id}"
                        )
                        seen_connections.add(edge)

            print("```")

        except FileNotFoundError:
            print(
                "Error: World file not found. Make sure the game has been run and world has been saved."
            )
        except Exception as e:
            print(f"Error loading world: {e}")
            print("\nFull traceback:")
            traceback.print_exc()

    async def generate_dot(self) -> None:
        """Generate a Graphviz DOT chart of the world."""
        try:
            world = await self.load_world()

            print("\n=== Graphviz DOT ===\n")
            print("digraph world {")
            print("    rankdir=TB;")
            print("    node [shape=box];")

            # Add nodes with room names
            for room_id, room in world.rooms.items():
                label = room.name.replace('"', '\\"')
                if room.players:
                    players = ", ".join(room.players)
                    print(
                        f'    {room_id} [label="{label}\\n[{players}]", style=filled, fillcolor=lightblue];'
                    )
                else:
                    print(f'    {room_id} [label="{label}"];')

            # Add edges with direction labels
            for room_id, room in world.rooms.items():
                for exit in room.exits:
                    print(
                        f'    {room_id} -> {exit.target_room_id} [label="{exit.keyword}"];'
                    )

            print("}")
            print("\n# To render: dot -Tpng -o world_map.png <filename>.dot")

        except FileNotFoundError:
            print(
                "Error: World file not found. Make sure the game has been run and world has been saved."
            )
        except Exception as e:
            print(f"Error loading world: {e}")
            print("\nFull traceback:")
            traceback.print_exc()


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="CLI for the MMO MCP game")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add inspect world command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect the world state")
    inspect_parser.add_argument("target", choices=["world"], help="What to inspect")

    # Add map command with format options
    map_parser = subparsers.add_parser("map", help="Generate a map of the world")
    map_parser.add_argument(
        "format", choices=["mermaid", "dot"], help="Output format for the map"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = CLI()

    if args.command == "inspect" and args.target == "world":
        asyncio.run(cli.inspect_world())
    elif args.command == "map":
        if args.format == "mermaid":
            asyncio.run(cli.generate_mermaid())
        elif args.format == "dot":
            asyncio.run(cli.generate_dot())
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
