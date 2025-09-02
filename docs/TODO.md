# TODO

## Error Handling

- [ ] **Fix error masking for GameError**: Currently fastmcp has internal error masking logic that we need to work around
  - We want to mask internal errors for security (don't expose stack traces, etc.)
  - EXCEPT for `GameError` exceptions - these are meant to be user-facing and should be shown to players
  - Need to ensure GameErrors are properly propagated through fastmcp's error handling

## High Priority for Launch

### Add "Go Home" / Teleport Command
**Problem**: With 41+ rooms, players might get lost and unable to find others, especially during low-population times.

**Solution**: Add a command to return to the Nexus Clearing (central hub).

**Implementation Options**:
1. **Simple "home" command** - Instantly teleports player to nexus_clearing
   - Pros: Easy to implement, always works
   - Cons: Might be abused to escape danger (if we add that later)
   
2. **"Recall stone" item** - Item that teleports you home when used
   - Pros: More immersive, can be limited (consumable or cooldown)
   - Cons: New players might not have one
   
3. **"Find others" command** - Teleports to room with most players
   - Pros: Directly solves the "can't find anyone" problem
   - Cons: Could break immersion, might overwhelm popular rooms

**Recommended Approach**:
- Start with simple "home" command for launch
- Command: `home` or `return` 
- Message: "You focus on the memory of the Nexus Clearing and find yourself back among the impossible doors."
- Consider cooldown (5 minutes?) to prevent abuse
- Always works from anywhere

**Code Location**:
- Add to `mmo/tools.py` as new tool
- No input needed, just uses player context
- Update player location to "nexus_clearing"

This ensures players can always:
- Return to a known meeting spot
- Escape if they get lost in confusing areas  
- Regroup with others at the central hub
- Start fresh if they're stuck

Consider adding flavor text that makes it feel intentional:
- "The strange doors of the Nexus call to you..."
- "Reality shifts and you're back where you started..."
- "You wake up in the clearing, unsure if you ever left..."

## Prompt Adjustments

- [ ] **Reduce fantasy bias in prompts**: Update prompts to tone down how much "fantasy" AIs inject when interacting with the world. Currently AIs are over-indexing on "dungeon crawler" to mean only dungeons/fantasy characters (wizards, knights, etc.). We want more of an open world exploration game - magic exists but the constant medieval fantasy tropes are becoming cliche. Consider:
  - Emphasizing modern, sci-fi, mundane, or surreal elements as equally valid
  - Removing or rephrasing "dungeon crawler" terminology
  - Adding examples that show non-fantasy interactions
  - Encouraging diverse character types and settings

- [ ] **Tone down exaggerated interactions**: Not every action needs to be dramatic or over-the-top. Encourage more natural, varied responses:
  - Simple actions should have simple effects
  - Not everything needs to be "epic" or "mysterious"
  - Mundane interactions are perfectly valid
  - Reserve dramatic descriptions for truly significant events

## Items System

- [ ] Implement Item model (`mmo/item.py`)
- [ ] Add inventory system to Player
- [ ] Add items list to Room
- [ ] Implement pickup/drop/inventory tools
- [ ] Implement conjure tool for creating items
- [ ] Update look command to show items
- [ ] Allow item interactions in do command

## Item Trading & Economy

- [ ] Update prompts to mention trading after implementing give/trade features

- [ ] Implement `give` tool to transfer items between players
- [ ] Implement `trade` system for mutual item exchanges
- [ ] Add item value/rarity system
- [ ] Create marketplace/bazaar room type
- [ ] Implement market stalls or vendor system
- [ ] Add currency system (gold, coins, credits, etc.)
- [ ] Allow players to set up shops or trading posts

## Dynamic World Generation

### Dynamic Room Generation
- [ ] **Automatic room creation based on player actions**: When players discover new areas (e.g., crawl through a vent, find a hidden door), automatically generate new rooms
  - Trigger room generation on specific actions (explore, search, use items)
  - Create rooms contextually based on the action (vent → maintenance tunnel, door → new chamber)
  - Connect new rooms to existing world graph
  - Consider room templates or procedural generation
  - Maintain world coherence and prevent infinite expansion

### Dynamic NPC/Player Generation  
- [ ] **Automatic NPC/player creation from player actions**: When players conjure/summon/create entities (e.g., conjure a family, summon a creature), generate them as new players/NPCs
  - Allow players to create NPCs through roleplay actions
  - Generated NPCs should have appropriate names, descriptions, behaviors
  - NPCs could be controlled by AI or become available for other players to embody
  - Consider limits to prevent spam/abuse
  - NPCs should persist and have their own agency

## Character Creation Improvements

- [ ] **Allow non-human character types**: Update character creation prompt to support diverse character types
  - Remove human-centric assumptions from prompts
  - Allow animals, robots, aliens, abstract entities, etc.
  - Adjust character description guidance to be species-agnostic
  - Ensure game mechanics work for non-humanoid forms
  - Update room descriptions to handle diverse character types gracefully

## Notifications

**Implementation Note:** Will need to use MCP resources and resource change notifications to push updates to connected clients.

- [ ] Set up MCP resource for player state/room state
- [ ] Implement MCP resource change notifications
- [ ] When another player enters/exits the room the user should be notified
- [ ] When significant events happen in the room a player is in, the player
      should be notified (but not for small / hard to notice events)
- [ ] When big observable events (e.g. an explosion happen in adjacent room the player
      should be notified)
- [ ] When a chat message is received or "say" message is received, the player
      is notified
