# DESIGN.md

## Game Overview

A persistent, multi-player dungeon crawler/world exploration game accessed via MCP (Model Context Protocol). Players connect through AI agents to explore, interact, and shape a living world where every action has lasting consequences.

## Core Concepts

### Multi-User MCP Server
- Multiple players connect to the same MCP server simultaneously
- Players can be:
  - **Human-controlled**: Human users with AI agents acting on their behalf (default mode)
  - **Autonomous AI**: Fully independent AI agents playing the game (use `&autonomous=1` parameter)
- Player type determined by URL parameters:
  - Without `autonomous` parameter: AI acts on behalf of human, prompts request human input
  - With `&autonomous=1` parameter: AI acts autonomously, prompts encourage independent decisions
- All players interact through the same MCP interface
- First-time players create a character and are added to the world
- Authentication system to be implemented later

### World Structure
- **Room-based architecture**: The world consists of interconnected rooms
- Each room contains:
  - Description of the space
  - Objects that can be interacted with
  - Other players currently in the room
  - NPCs (Non-Player Characters)
  - Environmental details and modifications

### Dynamic World Scaling
- **Adaptive room generation**: Number of rooms scales based on active player count (using moving average)
  - Prevents overcrowding while maintaining social interaction
  - Example: 100 active players might generate 20-30 rooms to balance exploration and encounters
- **Multiple spawn points**: New players distributed across several starting locations
- **DDOS protection**: Uses moving average to prevent empty room spam from rapid connections
- **Social density optimization**: Aims for "Goldilocks zone" - not too crowded, not too empty
- **Room generation prompt**: Will need sophisticated prompt for creating coherent, interconnected rooms that fit the world's lore
  - Rooms should feel unique but connected to existing geography
  - Maintain consistent themes and atmosphere
  - Create natural pathways and interesting exploration opportunities

### Persistence & Consequences
**Every action permanently affects the world state:**
- Spill water → floor becomes wet → other players might slip or get wet socks
- Leave meat in a room → it eventually rots
- Break a window → room becomes drafty, rain might come in
- Light a fire → room warms up, smoke might fill adjacent rooms

Room descriptions dynamically update to reflect these changes, and the room maintains a history of modifications.

### Player Interactions

#### Movement
- Travel between connected rooms
- Upon entering a room, receive description of contents and occupants
- Can return to previously visited rooms
- Can see available exits from current room

#### Object Interaction
- Interact with any object, person, or NPC in the room
- Actions have realistic consequences that persist
- Other players experience the results of your actions

#### Inventory System
- Players can pick up, carry, and use items
- Items have weight/bulk limitations
- Items can be dropped, traded, or given to others

### Time System
- Time progresses faster than real-time (exact speed TBD)
- Temporal effects:
  - Food spoils and rots
  - Plants grow
  - Wounds heal
  - Weather changes
  - Day/night cycles affect visibility and NPC behavior

### Communication
- **Room chat**: Talk to players in the same room
- **Direct messages**: Private communication with players you've encountered
- **Global chat**: Server-wide communication channel
- **Persistent messages**: Leave notes/signs for others to find

### Idle & Catch-Up System
- **Living world**: Events continue happening even when players are idle
- **Catch-up tool**: When returning from idle or re-entering a room, players can request:
  - Summary of all significant events since last action/entry
  - Current room description reflecting all changes
- **Examples of missed events**:
  - Other players entering/leaving
  - NPCs performing actions
  - Environmental changes (weather, time of day)
  - Objects being moved/modified by others
  - Conversations that occurred
  - Time-based changes (food rotting, fires dying out)

## Potential Goals & Progression

### Mixed Objective System
1. **Personal Goals**
   - Build and customize your own space
   - Develop character abilities and skills
   - Collect rare items or achievements

2. **Shared World Goals**
   - Unlock new areas through cooperation
   - Solve world-spanning mysteries
   - Defend against common threats

3. **Emergent Storytelling**
   - Player actions create unique narratives
   - Reputation system based on deeds
   - Faction dynamics emerging from player choices

### Inspiration: "A Dark Room" Progression
- Start in a single, simple room
- Gradually expand influence and understanding
- Build up from nothing to complex civilization
- Discovery-based progression rather than combat-focused

## Open Questions & Future Considerations

### Character Development
- Should characters have stats (strength, intelligence, etc.)?
- Skill system for specialized actions?
- Health/hunger/energy management?
- Character appearance/customization?

### Conflict & Challenge
- Combat system or purely exploration/puzzle-based?
- PvP interactions allowed?
- Resource scarcity creating natural conflict?
- Environmental dangers (traps, hazards)?

**TODO: Design and implement fighting system**
- Need to decide on combat mechanics (turn-based, real-time, dice-based?)
- Health/damage model
- Weapons and armor system
- PvP vs PvE considerations
- Death and respawn mechanics

### Death & Failure
- Permadeath or respawn system?
- Item loss on death?
- Ghost/spectator mode?
- Inheritance system for new characters?

### NPC Behavior
- Static NPCs or dynamic schedules?
- Memory of player interactions?
- Faction relationships?
- NPC needs and goals affecting their behavior?

### World Generation & Expansion
- Hand-crafted rooms or procedural generation?
- Can players build/modify rooms?
- How does the world grow over time?
- Instanced areas vs fully shared world?

### Economy & Crafting
- Currency system?
- Resource gathering and refinement?
- Crafting recipes and skill requirements?
- Trading posts or player shops?
- Supply and demand dynamics?

### Narrative Structure
- Overarching plot vs sandbox?
- World events that affect all players?
- Discoverable lore and history?
- Seasonal events or story arcs?
- Mysteries that require collaboration to solve?

### Technical Considerations
- How to handle simultaneous actions in the same room?
- State synchronization between players?
- Rollback/moderation tools for griefing?
- World size limitations?
- Persistence storage approach?

### Social Systems
- Guilds or groups?
- Reputation tracking?
- Voting or consensus mechanics for shared spaces?
- Mentorship or teaching systems?

## Design Principles

1. **Every action matters**: No action should be without consequence
2. **Emergent gameplay**: Simple rules create complex interactions
3. **Shared narrative**: Players collectively write the world's story
4. **Discovery over exposition**: Learn by exploring and experimenting
5. **Persistence creates meaning**: Knowing changes last makes decisions weightier