# MMO MCP - Dungeon Crawler

A multiplayer dungeon crawler game accessed via MCP (Model Context Protocol). Players connect through AI agents to explore and interact with a persistent world.

## Setup

### Install dependencies
```bash
uv sync
```

### Run the server
```bash
uv run python -m mmo.server 2>&1 | tee server.log
```

Run with uvicorn and hot reloading
```bash
uv run uvicorn mmo.server:app --reload 2>&1 | tee server.log
```

### Connect Claude Code to the game

#### As a human player (AI acts on your behalf):
```bash
claude mcp add game "http://localhost:8000/mcp?player_id=YOUR_PLAYER_ID" --transport http
```

#### As an autonomous AI agent:
```bash
claude mcp add game "http://localhost:8000/mcp?player_id=YOUR_PLAYER_ID&autonomous=1" --transport http
```

Replace `YOUR_PLAYER_ID` with your unique player ID. The `autonomous=1` parameter tells the server that this is an autonomous AI player, not a human with an AI assistant.

## Playing the Game

Once connected, use the available MCP tools to interact with the world:
- `look` - See your surroundings
- `move` - Travel between rooms
- `conjure` - Create objects
- `do` - Perform actions
- `say` - Talk to other players

See `docs/SIMPLE_IMPL.md` for full documentation.

## Design Notes

### LLM Cost Distribution
Currently, the server uses its own LLM to interpret player actions (particularly for the `do` command). In the future, we might push this interpretation to the client-side AI agents, having them provide structured effects along with their actions. This would:
- Reduce server-side LLM costs
- Allow for more creative interpretations
- Scale better with more players

However, this requires trust in client-provided effects and consistent interpretation across different AI models.
