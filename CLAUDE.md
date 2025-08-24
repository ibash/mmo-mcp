# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dungeon crawler MCP (Model Context Protocol) server built with FastMCP. Players connect via their AI agents to play the game.

## Code Rules

1. **One class per file**: Each class should have its own file with a descriptive name
2. **Class-based architecture**: Prefer class-based code over procedural code
3. **Minimal code**: Only write code that's absolutely necessary - no superfluous implementations
4. **Strict typing**: Use strict types throughout. Types help write intentional, self-documenting code

## Assert Usage Guidelines

Use asserts to catch programming errors and maintain invariants, not for runtime validation.

### When to use assert:
- **Enforcing invariants**: States that should NEVER be false if the code is correct
  - Example: `assert room_id in self.rooms, f"Room {room_id} does not exist"`
- **Catching logic errors**: Things that indicate a bug in the program
  - Example: `assert player.id in old_room.players, "Player not in room they're leaving"`
- **Documenting assumptions**: Making implicit assumptions explicit
  - Example: `assert item_id in player.inventory, "Can't remove item player doesn't have"`

### When NOT to use assert:
- **User input validation**: Return proper error messages instead
- **External data validation**: Use error handling for data from network/files
- **Expected failures**: If something could legitimately happen during normal operation

Key principle: Asserts are for "this should be impossible" situations. They help detect when the program enters an invalid state due to programming errors.

## Error Handling

### GameError
Use `GameError` (from `src/errors.py`) for any error message that should be shown to players/AI agents.

**When to use GameError:**
- Player hasn't created a character yet
- Invalid player actions (e.g., moving in non-existent direction)
- Missing required parameters from user
- Any message that helps the player understand what went wrong

**Examples:**
```python
raise GameError("You need to create a character first!")
raise GameError("You can't go that direction.")
raise GameError("That item doesn't exist here.")
```

**Catching GameError:**
```python
try:
    return world.look(player_id)
except GameError as e:
    return str(e)  # Safe to show to player
```

Never expose internal Python exceptions (ValueError, KeyError, etc.) directly to players. Always wrap player-facing errors in GameError.

## Development Commands

This project uses `uv` as the package manager (an extremely fast Python package manager).

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run python -m src.server

# Run with hot reloading (development)
uv run uvicorn src.server:app --reload
```

## Architecture

### Core Structure

- **`src/server.py`**: FastMCP server setup and registration. Runs on HTTP transport (port 8000)
- **`src/prompts.py`**: MCP prompts that provide context-aware instructions
  - `play`: Main entry point, handles registration and game introduction
  - `look`: Provides AI/human-specific guidance for exploring
- **`src/tools.py`**: MCP tools for game actions
  - `look`: Returns raw room description
  - `create_character`: Character creation with name and description
- **`src/world.py`**: World state management
  - Manages rooms and players
  - `add_player()`: Adds player to world and room
  - `get_player_and_room()`: Validates and returns player/room
  - `look()`: Generates room descriptions with players and exits
- **`src/room.py`**: Room model with connections and players
- **`src/player.py`**: Player model with inventory and location
- **`src/world_seed.py`**: Creates the initial 4-room world for development
- **`src/auth.py`**: Middleware for player authentication via URL parameters

### Game Flow

1. Player connects with `?player_id=X` (and optionally `&autonomous=1`)
2. Auth middleware extracts player_id and autonomous flag
3. If new player: registration flow via `play` prompt and `create_character` tool
4. If existing player: welcome back via `play` prompt
5. Players explore using `look`, `move`, `say`, etc.

### Player Types

- **Human-controlled** (default): AI acts as assistant, asks for input, elaborates descriptions
- **Autonomous AI** (`autonomous=1`): AI acts independently, makes creative decisions

### Key Dependencies

- **FastMCP**: MCP server framework (installed from git: https://github.com/ibash/fastmcp.git)
- **Pydantic**: Data validation and settings management using Python type annotations

### Development Notes

- World state is in-memory (will add persistence later)
- The MCP server runs on HTTP transport at 127.0.0.1:8000/mcp
- Prompts and tools are registered via their respective `register()` functions