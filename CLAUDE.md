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
Use `GameError` (from `mmo/errors.py`) for any error message that should be shown to players/AI agents.

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
uv run python -m mmo.server

# Run with hot reloading (development)
uv run uvicorn mmo.server:app --reload
```

## Architecture

### Core Structure

- **`mmo/server.py`**: FastMCP server setup and registration. Runs on HTTP transport (port 8000)
- **`mmo/prompts.py`**: MCP prompts that provide context-aware instructions
  - `play`: Main entry point, handles registration and game introduction
  - `look`: Provides AI/human-specific guidance for exploring
- **`mmo/tools.py`**: MCP tools for game actions
  - `look`: Returns raw room description
  - `create_character`: Character creation with name and description
- **`mmo/world.py`**: World state management
  - Manages rooms and players
  - `add_player()`: Adds player to world and room
  - `get_player_and_room()`: Validates and returns player/room
  - `look()`: Generates room descriptions with players and exits
- **`mmo/room.py`**: Room model with connections and players
- **`mmo/player.py`**: Player model with inventory and location
- **`mmo/world_seed.py`**: Creates the initial 4-room world for development
- **`mmo/auth.py`**: Middleware for player authentication via URL parameters

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

## Prompt Engineering Process

When improving prompts or LLM interactions:

### Core Principles

1. **LLMs must write to "think"**: LLMs don't have internal mental processes. Any complex reasoning must be externalized into written steps. "Think about X then do Y" doesn't work - instead use "Write out X, then based on what you wrote, do Y".

2. **Test empirically, not intuitively**: Create test files comparing multiple approaches in parallel. Use LLM judges with harsh scoring criteria (30-50 normal, 70+ exceptional). Counter-intuitive approaches often win (e.g., 5 concepts beat 20).

### Testing Process

1. Create a test file with multiple approaches
2. Run them in parallel with consistent evaluation 
3. Use LLM judges with specific scoring criteria
4. Test counter-intuitive approaches (less might be more)
5. Focus on process/method, not content/examples
6. Make all steps explicit and observable
7. Include anti-patterns (what NOT to do)
8. Iterate based on empirical results

### Key Techniques

- **Constraint breeds creativity**: Specific requirements ("EXACTLY 5, COMPLETELY different") beat vague guidance
- **Process over examples**: Teaching the method beats providing content
- **Anti-patterns matter**: Explicitly state what to avoid (e.g., "NOT Shadow, Storm, Raven")
- **Observable steps**: Make each step visible (list concepts, show reasoning, list avoided patterns)
- **Specific beats vague**: "$27.43 in pocket" beats "some money"

### Example: Character Creation Optimization

Our character creation went from 35/100 (baseline) to 70/100 (optimized) by:
- Reducing from 20 to 5 concepts (forced diversity)
- Making LLM write out all steps explicitly
- Adding specific mundane details
- Listing clichés to avoid
- Using harsh LLM scoring

Remember: Small wording changes can have huge impacts. "Mentally generate" vs "Write out" was the difference between 48/100 and 65/100 scores.