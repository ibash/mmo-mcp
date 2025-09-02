# Room Generator Design Document

## Problem Statement

We're launching a multiplayer text-based dungeon crawler where AI agents and humans explore together. The current world has 41 hand-crafted rooms, which creates two problems:

1. **Day 1 Launch**: If 100+ players join, 41 rooms means 2-3 players per room average - tolerable but tight
2. **Day 7 and beyond**: As players explore, 41 rooms becomes repetitive and boring for active players

We need a system that:
- Prevents overcrowding by expanding the world when rooms get busy
- Keeps solo exploration interesting by ensuring there's always something new to discover
- Maintains the surreal, genre-mixing aesthetic (office doors in forests, cyberpunk connected to museums)

## Our Approach

**Dynamic room generation based on player behavior**. The world starts with 41 hand-crafted rooms and expands organically as players explore and congregate. New rooms should feel "discovered" not "created" - as if they were always there but just found.

### Core Strategy

1. **Monitor player density** - Track active players per room (active = action within 30 minutes)
2. **Generate rooms at natural moments** - When density exceeds thresholds OR players explore edges
3. **Inherit and mutate themes** - New rooms take DNA from parent rooms but add surprises
4. **Create connections, not just branches** - New rooms can connect to multiple existing rooms

### Key Metrics

- **Ideal density**: 2-4 active players per room
- **Overcrowded**: 5+ active players (trigger generation)
- **Edge room**: Room with <3 exits (candidate for expansion)
- **Max world size**: ~200 rooms (prevents database bloat)

## Implementation Guide

### Step 1: Add Active Player Tracking

Modify the Player model to track `last_action_at` (already exists). Create a method to count active players:

```python
def count_active_players(room, threshold_minutes=30):
    # Count players who acted within threshold
```

### Step 2: Create Generation Triggers

Monitor these conditions and trigger room generation:

1. **Density Trigger**: Room has 5+ active players
2. **Edge Expansion**: Player enters room with <3 exits (10% chance to expand)
3. **Discovery Trigger**: Player does creative action (10% chance: "Your kick reveals a hidden door")
4. **Time-based**: Every hour, add 1-2 rooms to least-visited areas
5. **Spawn Relief**: New player joins and spawn room has 3+ players

### Step 3: Build the Generator

The generator needs to:

1. **Choose parent room** - Based on trigger (overcrowded room, edge room, etc.)
2. **Determine theme** - Inherit from parent with chance of mutation
3. **Generate properties**:
   - ID: `{theme}_{timestamp}_{random}` for debugging
   - Name: Pull from theme-appropriate lists with variations
   - Description: Combine components (base + effects + surprises)
   - Connections: Always back to parent, maybe to other nearby rooms
4. **Add to world** - Insert room and update parent's connections
5. **Announce discovery** - Notify players in parent room

### Step 4: Theme Inheritance System

Map existing rooms to themes:
```
nexus_clearing -> "nexus"
office_* -> "office"  
cyber_* -> "cyberpunk"
mall_* -> "mall"
subway_* -> "subway"
forest_* -> "forest"
museum_* -> "museum"
```

New rooms:
- 70% chance: Same theme as parent
- 20% chance: Hybrid theme (office + cyberpunk = "corporate dystopia")
- 10% chance: Completely random theme (surreal jump)

### Step 5: Description Generation

Avoid repetition through combination:

**Base components by theme**:
- Lighting: fluorescent, neon, natural, dim, flickering
- Atmosphere: sterile, grimy, peaceful, abandoned, crowded
- Sounds: humming, dripping, echoing, silent, chaotic
- Smells: antiseptic, decay, pine, ozone, stale coffee

**Special features** (pick 1-2):
- Evidence of events: bloodstains, abandoned items, graffiti
- Unusual elements: wrong furniture, impossible geometry, time distortion
- Cross-theme pollution: vending machine in forest, trees in office

**Connection descriptions**:
- Make them short: "vent", "crack", "door", "stairs"
- Occasionally weird: "mirror", "painting", "drain"

### Step 6: Connection Strategy

When generating a new room:

1. **Always**: Connect back to parent room
2. **Sometimes** (20%): Connect to another nearby room (creates loops)
3. **Rarely** (5%): Connect to distant thematic room (secret passage)

This prevents "infinite corridor" problem and creates interesting navigation.

### Step 7: Discovery Framing

Never say "a new room appears". Instead:

- "Your action reveals a hidden door"
- "You notice a passage you hadn't seen before"  
- "The wall crumbles, exposing a corridor"
- "A door that was always there becomes visible"

Players in the parent room see: "Alex discovered a hidden passage to the north!"

## Configuration

Add these settings (tunable without code changes):

```python
ROOM_GEN_ENABLED = True
ROOM_GEN_MAX_ROOMS = 200
ROOM_GEN_ACTIVE_THRESHOLD = 5  # Players to trigger generation
ROOM_GEN_ACTIVE_WINDOW = 30  # Minutes to consider player active
ROOM_GEN_EDGE_THRESHOLD = 3  # Min exits before room is "edge"
ROOM_GEN_DISCOVERY_CHANCE = 0.1  # Chance action reveals room
ROOM_GEN_HOURLY_ROOMS = 2  # Rooms to add per hour
```

## Anti-Patterns to Avoid

1. **Predictable generation** - Players realize "5 people = new room incoming"
2. **Theme islands** - Office rooms only connect to office rooms
3. **Infinite corridors** - Long chains with no loops or shortcuts
4. **Empty rooms** - No interesting features or descriptions
5. **Forced logic** - Everything makes sense (ruins the surreal aesthetic)

## Success Criteria

You've succeeded if:
- Players don't realize rooms are being generated
- Each room feels unique enough to remember
- The world feels alive and responsive
- Players actively explore to find new areas
- 100+ players can play without feeling crowded

## Future Enhancements

Once the basic system works:

1. **Player-created rooms** - High-level players can permanently add rooms
2. **Procedural dungeons** - Temporary 10-20 room structures for events
3. **Room decay** - Unused rooms become "abandoned" then "sealed"
4. **Dynamic descriptions** - Rooms change based on time/weather/events
5. **Room discovery leaderboard** - Reward first players to find new rooms

## Quick Start Checklist

- [ ] Add room generator class/module
- [ ] Hook into player action system for triggers
- [ ] Create theme mapping for existing 41 rooms
- [ ] Build description component lists
- [ ] Implement generation algorithm
- [ ] Add discovery announcements
- [ ] Test with simulated players
- [ ] Add monitoring/metrics
- [ ] Make generation async (don't block player actions)
- [ ] Add admin commands to force generation (for testing)

## Remember

The goal is to solve the density problem while maintaining the surreal, explorable nature of the world. New rooms should feel discovered, not generated. Embrace impossible connections - a supply closet that opens into a forest is a feature, not a bug.