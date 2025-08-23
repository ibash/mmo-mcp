# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dungeon crawler MCP (Model Context Protocol) server built with FastMCP. Players connect via their AI agents to play the game.

## Code Rules

1. **One class per file**: Each class should have its own file with a descriptive name
2. **Class-based architecture**: Prefer class-based code over procedural code
3. **Minimal code**: Only write code that's absolutely necessary - no superfluous implementations
4. **Strict typing**: Use strict types throughout. Types help write intentional, self-documenting code

## Development Commands

This project uses `uv` as the package manager (an extremely fast Python package manager).

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run python server.py

# Run the main application
uv run python main.py
```

## Architecture

### Core Components

- **`server.py`**: FastMCP server implementation that runs on HTTP transport (port 8000). Contains the MCP tool endpoints for game interactions. Currently has a `play()` tool stub.

- **`character.py`**: Defines the `Character` model using Pydantic BaseModel for data validation. Characters have a name attribute.

- **`world.py`**: Contains the `World` class that manages a list of `Character` objects. This represents the game world state.

- **`main.py`**: Entry point for the application (currently just a placeholder).

### Key Dependencies

- **FastMCP**: MCP server framework (installed from git: https://github.com/ibash/fastmcp.git)
- **Pydantic**: Data validation and settings management using Python type annotations

### Development Notes

- The server has a TODO for implementing user authentication (server.py:5)
- The project uses Python 3.10+ with type hints
- The MCP server runs on HTTP transport at 127.0.0.1:8000