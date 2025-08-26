# TODO

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

- [ ] Implement Item model (`src/item.py`)
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
