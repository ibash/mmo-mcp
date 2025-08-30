# SIMPLE_IMPL.md

## Minimal Proof of Concept Implementation

This document outlines the simplest possible implementation to demonstrate core concepts.

## Player Types

Players can be:
- **Human-controlled**: A human user with an AI agent acting on their behalf (default mode)
- **Autonomous AI**: Fully autonomous AI agents playing independently (use `&autonomous=1` parameter)

### Connection Parameters
- `player_id`: Required unique identifier for the player
- `autonomous`: Optional parameter, set to `1` for autonomous AI mode

Examples:
- Human player: `http://localhost:8000/mcp?player_id=alice`
- Autonomous AI: `http://localhost:8000/mcp?player_id=ai_explorer&autonomous=1`

### Prompt Differences
- **Human mode**: Prompts ask the AI to consult with the human for decisions like character name/description
- **Autonomous mode**: Prompts encourage the AI to make creative decisions independently

Both types interact with the world through the same MCP interface, ensuring equal gameplay capabilities.

## World Structure

### 4-Room Grid
```
[Room 1: Forest Clearing] --- [Room 2: Cave Entrance]
         |                              |
[Room 3: River Bank]    ---    [Room 4: Old Ruins]
```

- 2x2 grid of connected rooms
- Each room has a unique description and atmosphere
- Rooms are connected horizontally and vertically (no diagonals)

## Core MCP Tools

### 1. `create_character`
- **Input**: character name, detailed description
- **Function**: Creates a new character for first-time players
- **Description notes**: 
  - Can be very long and detailed
  - Should include appearance, clothing, notable characteristics
  - Will be LLM-summarized when other players see them
  - Example: "A tall figure in a worn traveling cloak, with piercing green eyes and a scar across the left cheek. Carries an ornate staff with glowing runes. Leather boots show signs of many miles traveled."
- **Returns**: Character creation confirmation

### 2. `look`
- **Input**: None
- **Function**: Shows current room description, items, and other players
- **Returns**: 
  - Room name and description
  - List of items/objects in the room
  - List of other players present (with LLM-summarized descriptions)
  - Available exits (north, south, east, west)

### 3. `move`
- **Input**: direction (north, south, east, west)
- **Function**: Move to an adjacent room
- **Returns**: New room description (same as `look`)

### 4. `conjure`
- **Input**: item name and optional description
- **Function**: Create an item/object in the current room
- **Examples**:
  - `conjure("torch")` - creates a torch for light
  - `conjure("chair", "a sturdy wooden chair")` - creates a chair to sit on
  - `conjure("sign", "Danger: Slippery when wet!")` - creates a warning sign
- **Returns**: Confirmation and updated room description

### 5. `pickup`
- **Input**: item name
- **Function**: Pick up an item from the room into inventory
- **Returns**: Success/failure message

### 6. `drop`
- **Input**: item name
- **Function**: Drop an item from inventory into the room
- **Returns**: Success/failure message

### 7. `inventory`
- **Input**: None
- **Function**: List items the player is carrying
- **Returns**: List of items in inventory

### 8. `say`
- **Input**: message
- **Function**: Speak to others in the same room
- **Returns**: Confirmation that message was sent

### 9. `do`
- **Input**: action description
- **Function**: Perform arbitrary actions that affect the world
- **Examples**:
  - `do("light the torch")` - if a torch exists, it becomes lit
  - `do("sit on the chair")` - character sits on an existing chair
  - `do("write 'Hello' in the dirt")` - creates persistent writing
  - `do("splash water on the floor")` - makes the floor wet
  - `do("break the chair")` - destroys the chair, leaves broken pieces
- **Returns**: Description of what happened and any world changes
- **Note**: The action's success depends on context (available items, room state, etc.)

## Authentication System

### Simple Token-Based Auth
- Each player gets a unique token/ID in URL parameters
- Connection formats:
  - Human player: `http://server:8000/mcp?player_id=abc123`
  - Autonomous AI: `http://server:8000/mcp?player_id=ai_abc&autonomous=1`
- Server maintains mapping of token → character
- Server uses `autonomous` parameter to customize prompts
- For POC: Can hardcode a few test tokens

## New Player Flow

1. **Connection**: Player connects with their token
2. **Character Check**: Server checks if token has existing character
3. **Character Creation**: If new, prompt for character creation
4. **Introduction**: 
   ```
   Welcome to the Dungeon Crawler, [character name]!
   
   You find yourself in a mysterious world of four connected rooms.
   
   Available commands:
   - look: Examine your surroundings
   - move [direction]: Travel north, south, east, or west
   - conjure [item]: Create objects in the world
   - do [action]: Perform actions with objects or the environment
   - pickup [item]: Take an item
   - drop [item]: Drop an item from your inventory
   - inventory: See what you're carrying
   - say [message]: Speak to others in the room
   
   Your actions affect the world permanently. Objects you create will 
   remain for others to find. Choose wisely.
   
   You are currently in: [starting room name]
   ```
5. **Start Location**: All players start in Room 1 (Forest Clearing)

## TODO: Fighting System

### Combat Mechanics
- Need to implement a basic fighting system
- Players should be able to fight each other or NPCs
- Consider simple health/damage model to start
- Weapons and armor from conjured items
- Death/respawn mechanics

## Persistence

### Minimal State Storage
- **Quick prototype option**: Pickle files for periodic checkpoints
  - Simple serialization of entire World object
  - Save snapshots every few minutes or after significant events
  - Easy rollback to previous states for testing
- **Alternative**: JSON file for human-readable state
- Store:
  - Room states (items in each room)
  - Player characters and their locations
  - Player inventories
- Auto-save after each action
- Load state on server start
- **Note**: Production would use PostgreSQL or similar database, but pickle files work well for rapid prototyping

## Multi-Player Visibility

### Real-time Awareness
- When a player enters a room, others see: `"[name] enters from the [direction]"`
- When a player leaves: `"[name] heads [direction]"`
- When a player conjures: `"[name] conjures a [item]"`
- When a player does an action: `"[name] [action description]"`
- When a player speaks: `"[name] says: [message]"`

## Technical Implementation Notes

### Data Models Needed
1. `Player` - id, name, description, current_room, inventory
2. `Room` - id, name, description, items, connections
3. `Item` - name, description, location (room_id or character_id)
4. `World` - rooms, characters, global state

### State Management
- World state is a singleton
- All MCP tool calls modify the shared world state
- Thread-safe operations for concurrent players

### Session Handling
- Track active connections
- Handle disconnections gracefully (character remains in world)
- Optional: Remove character from room display if disconnected

## Success Criteria

The POC is successful if:
1. Multiple players can connect simultaneously
2. Players can see each other in rooms
3. Items conjured by one player are visible to others
4. World state persists between server restarts
5. Players can navigate all 4 rooms
6. Basic chat works within rooms

## Future Enhancements (Not in POC)

### Dynamic World Scaling
- **Auto-scaling rooms**: Expand from 4 rooms based on active player count
  - Use moving average window (e.g., 5-minute average) to track genuine activity
  - Target ratio: ~3-5 players per room for optimal social density
  - Protection against DDOS: Don't create rooms based on connection spikes
- **Multiple spawn points**: Once scaled up, distribute new players across starting areas
- **Room generation**: Will need sophisticated AI prompt for creating:
  - Coherent, interconnected rooms that fit existing geography
  - Consistent themes while maintaining variety
  - Natural exploration paths and interesting landmarks
  - Rooms that feel discovered, not generated

### Other Enhancements
- Time system
- NPCs
- Complex interactions
- Combat
- Room modifications beyond adding items
- Catch-up system for idle players
- Global/DM chat
- More sophisticated authentication
