from .world import World
from .room import Room


def create_expanded_seed_world() -> World:
    """Create a seed world with the Forest Clearing as a surreal nexus to various districts."""

    world = World()

    # ============================================
    # CENTRAL HUB - The Nexus Forest Clearing
    # ============================================
    nexus = Room(
        id="nexus_clearing",
        name="The Nexus Clearing",
        description=(
            "A serene forest clearing with soft grass and wildflowers. Strangely, there are "
            "several doors standing freely among the trees: a revolving glass door, a metal "
            "office door marked 'Suite 200', a rusty subway entrance, a neon-lit arcade entrance, "
            "and an ornate museum door. None of them should exist here, yet they do."
        ),
        connections={
            "office": "office_lobby",
            "subway": "subway_platform_1",
            "arcade": "mall_arcade",
            "museum": "museum_lobby",
            "forest": "forest_grove",
            "revolving": "cyber_street",
        },
    )

    # ============================================
    # OFFICE COMPLEX DISTRICT
    # ============================================
    office_lobby = Room(
        id="office_lobby",
        name="Corporate Lobby",
        description=(
            "A sterile corporate lobby with marble floors and a reception desk. Motivational "
            "posters line the walls. Elevator music plays softly. A forest clearing is "
            "visible through the glass doors."
        ),
        connections={
            "glass": "nexus_clearing",
            "elevator": "office_floor_7",
            "stairs": "office_basement",
        },
    )

    office_floor_7 = Room(
        id="office_floor_7",
        name="7th Floor - Cubicle Farm",
        description=(
            "An endless maze of grey cubicles. The fluorescent lights hum oppressively. "
            "Someone's printer is jammed. There's a birthday cake in the break room, but "
            "nobody knows whose birthday it is."
        ),
        connections={
            "elevator": "office_lobby",
            "break": "office_break_room",
            "fire": "office_roof",
        },
    )

    office_break_room = Room(
        id="office_break_room",
        name="Break Room",
        description=(
            "A small break room with a microwave that beeps incessantly. The coffee is "
            "eternally stale. Someone labeled their yogurt 'DO NOT STEAL' in the fridge. "
            "A window overlooks the parking lot."
        ),
        connections={
            "cubicles": "office_floor_7",
            "window": "office_parking",  # Surprisingly, it opens
        },
    )

    office_basement = Room(
        id="office_basement",
        name="IT Basement",
        description=(
            "A dimly lit basement full of server racks and tangled cables. The air is "
            "cold from the AC. Multiple monitors show scrolling green text. A suspicious "
            "door marked 'Authorized Personnel Only' leads somewhere unexpected."
        ),
        connections={
            "up": "office_lobby",
            "suspicious": "subway_tunnel",  # Secret connection!
        },
    )

    office_roof = Room(
        id="office_roof",
        name="Office Rooftop",
        description=(
            "The building's rooftop with AC units and a small garden someone started but "
            "abandoned. You can see other districts from here - a forest, neon lights, "
            "and what looks like... a beach?"
        ),
        connections={"fire": "office_floor_7", "escape": "office_parking"},
    )

    office_parking = Room(
        id="office_parking",
        name="Corporate Parking Lot",
        description=(
            "A vast parking lot with designated spots for employees of the month. "
            "Most cars look identical. A shopping cart from the mall sits abandoned "
            "in a parking space."
        ),
        connections={
            "building": "office_lobby",
            "window": "office_break_room",
            "escape": "office_roof",
            "hedge": "mall_loading",  # Another secret!
        },
    )

    # ============================================
    # CYBERPUNK DISTRICT
    # ============================================
    cyber_street = Room(
        id="cyber_street",
        name="The Sprawl - Sector 7",
        description=(
            "Perpetual acid rain corrodes everything. Junkies twitch in doorways, their "
            "neural implants sparking. A street doc sells black market cyberware from a "
            "shopping cart. Corporate arcology towers loom overhead, their residents never "
            "coming down. A revolving door stands bizarrely pristine among the decay."
        ),
        connections={
            "revolving": "nexus_clearing",
            "ramen": "cyber_ramen",
            "fire": "cyber_apartment",
            "alley": "cyber_back_alley",
        },
    )

    cyber_ramen = Room(
        id="cyber_ramen",
        name="Matsuda's Black Clinic",
        description=(
            "A ramen shop that's really a street clinic. The chef is missing an eye - "
            "the socket glows red when he scans customers. Yakuza soldiers get patched up "
            "in the back while salary men slurp synthetic noodles up front. The smell of "
            "antiseptic mixes with soy sauce."
        ),
        connections={"street": "cyber_street", "kitchen": "cyber_back_alley"},
    )

    cyber_apartment = Room(
        id="cyber_apartment",
        name="Coffin Hotel - Unit 3847",
        description=(
            "A 2x3 meter coffin apartment, 47 floors up. The previous tenant's blood is "
            "still on the wall - suicide or murder unclear. Stolen corporate data decks "
            "are stacked like pizza boxes. Through the grimy window, you see a thousand "
            "identical units. Someone's screaming three coffins over."
        ),
        connections={
            "fire": "cyber_street",
            "vent": "cyber_rooftop",  # Because why not
        },
    )

    cyber_back_alley = Room(
        id="cyber_back_alley",
        name="Night Market - Organ Row",
        description=(
            "They sell everything here - kidneys, eyes, neural tissue, all 'ethically sourced'. "
            "A surgeon operates in the open, no anesthetic. Data pirates hawk mind recordings "
            "of dead celebrities. The Triad runs protection; bodies of those who didn't pay "
            "hang from the data cables overhead."
        ),
        connections={
            "street": "cyber_street",
            "kitchen": "cyber_ramen",
            "dumpster": "subway_tunnel",  # Everything connects!
        },
    )

    cyber_rooftop = Room(
        id="cyber_rooftop",
        name="Rooftop Shantytown",
        description=(
            "A squatter camp built from shipping containers and scavenged corp-tech. "
            "Refugees grow vat-meat in repurposed server racks. Armed gangs control "
            "the water collectors. Below, the city burns; above, surveillance drones "
            "circle endlessly. Through the smog, impossibly, you glimpse trees."
        ),
        connections={
            "vent": "cyber_apartment",
            "bridge": "museum_roof",  # Rooftop network!
        },
    )

    # ============================================
    # ABANDONED MALL DISTRICT
    # ============================================
    mall_arcade = Room(
        id="mall_arcade",
        name="Retro Arcade",
        description=(
            "An arcade frozen in the 1990s. Most machines still work, playing their "
            "attract mode sounds in an endless loop. The carpet has that distinct "
            "arcade smell. Prize tickets litter the floor."
        ),
        connections={
            "forest": "nexus_clearing",
            "mall": "mall_food_court",
            "staff": "mall_backrooms",
        },
    )

    mall_food_court = Room(
        id="mall_food_court",
        name="Abandoned Food Court",
        description=(
            "A vast food court with empty stalls and overturned chairs. The fountain "
            "in the center still runs somehow. Muzak echoes eerily. One restaurant's "
            "sign still flickers: 'Pizza by the Slice'."
        ),
        connections={
            "arcade": "mall_arcade",
            "up": "mall_upper",
            "parking": "mall_loading",
        },
    )

    mall_upper = Room(
        id="mall_upper",
        name="Upper Mall Level",
        description=(
            "The upper level with a defunct department store and empty boutiques. "
            "Mannequins in outdated fashion stand frozen in windows. A skylight "
            "shows the sky, though you're not sure which sky it is."
        ),
        connections={
            "down": "mall_food_court",
            "store": "mall_store",
            "skylight": "mall_roof",  # If you can reach it
        },
    )

    mall_store = Room(
        id="mall_store",
        name="Department Store",
        description=(
            "Racks of clothes from a bygone era. The escalators are frozen. "
            "Soft jazz plays from hidden speakers. The perfume section is "
            "overwhelming even after all this time."
        ),
        connections={"mall": "mall_upper", "service": "mall_backrooms"},
    )

    mall_backrooms = Room(
        id="mall_backrooms",
        name="Mall Backrooms",
        description=(
            "Endless beige hallways with fluorescent lighting. Boxes of old "
            "merchandise gather dust. You hear the hum of ventilation but "
            "can't tell where it's coming from. Doors lead everywhere and nowhere."
        ),
        connections={
            "arcade": "mall_arcade",
            "elevator": "mall_store",
            "loading": "mall_loading",
            "unmarked": "office_basement",  # Connected to office!
        },
    )

    mall_loading = Room(
        id="mall_loading",
        name="Loading Dock",
        description=(
            "The mall's loading area with abandoned trucks and shipping containers. "
            "Weeds grow through cracks in the concrete. A gap in the fence leads to "
            "what looks like a corporate parking lot."
        ),
        connections={
            "mall": "mall_food_court",
            "backrooms": "mall_backrooms",
            "fence": "office_parking",  # District crossing!
        },
    )

    mall_roof = Room(
        id="mall_roof",
        name="Mall Rooftop",
        description=(
            "The mall's flat rooftop with old AC units and a surprisingly good view. "
            "You can see the forest clearing from here, with its impossible doors. "
            "Birds nest in the old neon signs."
        ),
        connections={"skylight": "mall_upper"},
    )

    # ============================================
    # SUBWAY SYSTEM DISTRICT
    # ============================================
    subway_platform_1 = Room(
        id="subway_platform_1",
        name="Central Platform",
        description=(
            "A subway platform that shouldn't exist. Tiles on the walls show "
            "destinations that don't make sense. A train arrives and departs on "
            "its own schedule. The stairs lead up to... a forest?"
        ),
        connections={
            "up": "nexus_clearing",
            "tunnel": "subway_tunnel",
            "across": "subway_platform_2",
        },
    )

    subway_platform_2 = Room(
        id="subway_platform_2",
        name="Ghost Platform",
        description=(
            "An abandoned platform lit by flickering lights. Old advertisements "
            "from the 1950s still hang on the walls. You hear trains but never "
            "see them. A maintenance door is slightly ajar."
        ),
        connections={
            "across": "subway_platform_1",
            "maintenance": "subway_control",
            "dark": "subway_tunnel",
        },
    )

    subway_tunnel = Room(
        id="subway_tunnel",
        name="Service Tunnel",
        description=(
            "Dark tunnels with pipes and cables running along the walls. "
            "You hear dripping water and distant train sounds. Multiple passages "
            "branch off, leading to unexpected places."
        ),
        connections={
            "platform": "subway_platform_1",
            "ghost": "subway_platform_2",
            "grate": "office_basement",  # To office!
            "pipes": "cyber_back_alley",  # To cyberpunk!
        },
    )

    subway_control = Room(
        id="subway_control",
        name="Control Room",
        description=(
            "An old control room with switches and track diagrams. Half the "
            "lights on the board are red, half green, but nothing seems to "
            "change when you flip switches. Coffee cups suggest someone was here recently."
        ),
        connections={"platform": "subway_platform_2", "emergency": "subway_surface"},
    )

    subway_surface = Room(
        id="subway_surface",
        name="Subway Entrance",
        description=(
            "You emerge at street level, but it's unclear which street. "
            "The entrance is covered in graffiti. Somehow, you can see both "
            "neon signs and office buildings from here."
        ),
        connections={
            "down": "subway_control",
            "neon": "cyber_street",  # To cyberpunk!
            "offices": "office_parking",  # To office!
        },
    )

    # ============================================
    # FOREST DISTRICT (Natural expansion of the nexus)
    # ============================================
    forest_grove = Room(
        id="forest_grove",
        name="Ancient Grove",
        description=(
            "Massive trees that seem older than they should be. Soft moss covers "
            "everything. Mushrooms glow faintly in the shadows. The path splits "
            "in multiple directions."
        ),
        connections={
            "clearing": "nexus_clearing",
            "deeper": "forest_deep",
            "stream": "forest_stream",
        },
    )

    forest_deep = Room(
        id="forest_deep",
        name="Deep Woods",
        description=(
            "The forest is thick here, canopy blocking most light. You hear "
            "strange sounds - birds that don't sound quite right. An old stone "
            "structure is visible through the trees."
        ),
        connections={
            "grove": "forest_grove",
            "ruins": "forest_ruins",
            "hollow": "museum_storage",  # Secret passage!
        },
    )

    forest_stream = Room(
        id="forest_stream",
        name="Babbling Brook",
        description=(
            "A clear stream runs through the forest. Smooth stones make natural "
            "stepping stones. The water is impossibly clear. You swear you can see "
            "subway tiles at the bottom of the deeper pools."
        ),
        connections={
            "grove": "forest_grove",
            "upstream": "forest_waterfall",
            "downstream": "forest_pond",
        },
    )

    forest_waterfall = Room(
        id="forest_waterfall",
        name="Hidden Waterfall",
        description=(
            "A small waterfall cascades into a pool. Behind the water, you can "
            "make out what looks like a cave entrance. The mist creates rainbows "
            "in the filtered sunlight."
        ),
        connections={"stream": "forest_stream", "behind": "forest_cave"},
    )

    forest_cave = Room(
        id="forest_cave",
        name="Cave Behind the Falls",
        description=(
            "A small cave hidden by the waterfall. Someone has been here - "
            "there's modern camping equipment and... is that a WiFi router? "
            "A narrow passage leads deeper."
        ),
        connections={
            "waterfall": "forest_waterfall",
            "squeeze": "cyber_apartment",  # Why not!
        },
    )

    forest_pond = Room(
        id="forest_pond",
        name="Reflection Pond",
        description=(
            "A serene pond that perfectly reflects the sky. Lily pads float "
            "on the surface. When you look closely at your reflection, the "
            "background shows a different place each time."
        ),
        connections={"stream": "forest_stream", "around": "forest_ruins"},
    )

    forest_ruins = Room(
        id="forest_ruins",
        name="Forgotten Ruins",
        description=(
            "Ancient stone ruins overtaken by nature. Vines cover most surfaces. "
            "The architecture doesn't match any known civilization. A doorway "
            "still stands, though it should lead nowhere."
        ),
        connections={
            "woods": "forest_deep",
            "pond": "forest_pond",
            "doorway": "museum_ancient",  # To museum!
        },
    )

    # ============================================
    # MUSEUM DISTRICT
    # ============================================
    museum_lobby = Room(
        id="museum_lobby",
        name="Museum Grand Entrance",
        description=(
            "A grand marble entrance with high ceilings and a information desk "
            "that's unmanned. Banners advertise exhibitions that seem to change "
            "when you're not looking. A door leads back to... a forest?"
        ),
        connections={
            "forest": "nexus_clearing",
            "exhibits": "museum_main",
            "stairs": "museum_upper",
            "staff": "museum_storage",
        },
    )

    museum_main = Room(
        id="museum_main",
        name="Main Exhibition Hall",
        description=(
            "A vast hall with exhibits from different eras that shouldn't exist "
            "together. A T-Rex skeleton stands next to a space shuttle. Medieval "
            "armor faces off against robot prototypes."
        ),
        connections={
            "lobby": "museum_lobby",
            "ancient": "museum_ancient",
            "future": "museum_future",
        },
    )

    museum_ancient = Room(
        id="museum_ancient",
        name="Ancient History Wing",
        description=(
            "Artifacts from civilizations both real and impossible. Some exhibits "
            "are behind glass, others invite touching. A doorway that looks like "
            "it belongs in ruins leads somewhere unexpected."
        ),
        connections={
            "main": "museum_main",
            "doorway": "forest_ruins",  # Back to forest!
        },
    )

    museum_future = Room(
        id="museum_future",
        name="Future Tech Wing",
        description=(
            "Gleaming displays of technology that might exist someday. Interactive "
            "holograms demonstrate impossible inventions. One exhibit is just a "
            "door labeled 'Staff Only' that hums with electricity."
        ),
        connections={
            "main": "museum_main",
            "humming": "cyber_apartment",  # To cyberpunk!
        },
    )

    museum_upper = Room(
        id="museum_upper",
        name="Upper Gallery",
        description=(
            "A quiet gallery with paintings that seem to move when you're not "
            "looking directly at them. Large windows show views of different "
            "places - a forest, a city, an office building."
        ),
        connections={"stairs": "museum_lobby", "roof": "museum_roof"},
    )

    museum_storage = Room(
        id="museum_storage",
        name="Museum Storage",
        description=(
            "Countless artifacts in various states of cataloging. Crates labeled "
            "with impossible dates. A hollow tree trunk is marked 'Forest Exhibit' "
            "but seems to have depth beyond its size."
        ),
        connections={
            "lobby": "museum_lobby",
            "tree": "forest_deep",  # To forest!
        },
    )

    museum_roof = Room(
        id="museum_roof",
        name="Museum Rooftop Sculpture Garden",
        description=(
            "A rooftop garden with modern sculptures that might be art or might be "
            "leftover AC units. A makeshift bridge of planks leads to another building's "
            "roof. The view shows all the impossible geography."
        ),
        connections={
            "gallery": "museum_upper",
            "planks": "cyber_rooftop",  # Rooftop network!
        },
    )

    # Add all rooms to world
    world.rooms = {
        # Hub
        "nexus_clearing": nexus,
        # Office District
        "office_lobby": office_lobby,
        "office_floor_7": office_floor_7,
        "office_break_room": office_break_room,
        "office_basement": office_basement,
        "office_roof": office_roof,
        "office_parking": office_parking,
        # Cyberpunk District
        "cyber_street": cyber_street,
        "cyber_ramen": cyber_ramen,
        "cyber_apartment": cyber_apartment,
        "cyber_back_alley": cyber_back_alley,
        "cyber_rooftop": cyber_rooftop,
        # Mall District
        "mall_arcade": mall_arcade,
        "mall_food_court": mall_food_court,
        "mall_upper": mall_upper,
        "mall_store": mall_store,
        "mall_backrooms": mall_backrooms,
        "mall_loading": mall_loading,
        "mall_roof": mall_roof,
        # Subway District
        "subway_platform_1": subway_platform_1,
        "subway_platform_2": subway_platform_2,
        "subway_tunnel": subway_tunnel,
        "subway_control": subway_control,
        "subway_surface": subway_surface,
        # Forest District
        "forest_grove": forest_grove,
        "forest_deep": forest_deep,
        "forest_stream": forest_stream,
        "forest_waterfall": forest_waterfall,
        "forest_cave": forest_cave,
        "forest_pond": forest_pond,
        "forest_ruins": forest_ruins,
        # Museum District
        "museum_lobby": museum_lobby,
        "museum_main": museum_main,
        "museum_ancient": museum_ancient,
        "museum_future": museum_future,
        "museum_upper": museum_upper,
        "museum_storage": museum_storage,
        "museum_roof": museum_roof,
    }

    return world
