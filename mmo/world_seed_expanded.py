from .world import World
from .room import Room
from .exit import Exit


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
        exits=[
            Exit(
                keyword="office",
                target_room_id="office_lobby",
                movement_phrase="enter the office door",
            ),
            Exit(
                keyword="subway",
                target_room_id="subway_platform_1",
                movement_phrase="descend into the subway",
            ),
            Exit(
                keyword="arcade",
                target_room_id="mall_arcade",
                movement_phrase="step into the neon arcade",
            ),
            Exit(
                keyword="museum",
                target_room_id="museum_lobby",
                movement_phrase="enter the museum",
            ),
            Exit(
                keyword="forest",
                target_room_id="forest_grove",
                movement_phrase="follow the forest path",
            ),
            Exit(
                keyword="revolving",
                target_room_id="cyber_street",
                movement_phrase="push through the revolving door",
            ),
        ],
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
        exits=[
            Exit(
                keyword="glass",
                target_room_id="nexus_clearing",
                movement_phrase="pass through the glass doors",
            ),
            Exit(
                keyword="elevator",
                target_room_id="office_floor_7",
                movement_phrase="take the elevator",
            ),
            Exit(
                keyword="stairs",
                target_room_id="office_basement",
                movement_phrase="descend the stairs",
            ),
        ],
    )

    office_floor_7 = Room(
        id="office_floor_7",
        name="7th Floor - Cubicle Farm",
        description=(
            "An endless maze of grey cubicles. The fluorescent lights hum oppressively. "
            "Someone's printer is jammed. There's a birthday cake in the break room, but "
            "nobody knows whose birthday it is."
        ),
        exits=[
            Exit(
                keyword="elevator",
                target_room_id="office_lobby",
                movement_phrase="take the elevator down",
            ),
            Exit(
                keyword="break",
                target_room_id="office_break_room",
                movement_phrase="head to the break room",
            ),
            Exit(
                keyword="fire",
                target_room_id="office_roof",
                movement_phrase="take the fire escape up",
            ),
        ],
    )

    office_break_room = Room(
        id="office_break_room",
        name="Break Room",
        description=(
            "A small break room with a microwave that beeps incessantly. The coffee is "
            "eternally stale. Someone labeled their yogurt 'DO NOT STEAL' in the fridge. "
            "A window overlooks the parking lot."
        ),
        exits=[
            Exit(
                keyword="cubicles",
                target_room_id="office_floor_7",
                movement_phrase="return to the cubicles",
            ),
            Exit(
                keyword="window",
                target_room_id="office_parking",
                movement_phrase="climb through the window",
            ),
        ],
    )

    office_basement = Room(
        id="office_basement",
        name="IT Basement",
        description=(
            "A dimly lit basement full of server racks and tangled cables. The air is "
            "cold from the AC. Multiple monitors show scrolling green text. A suspicious "
            "door marked 'Authorized Personnel Only' leads somewhere unexpected."
        ),
        exits=[
            Exit(
                keyword="up",
                target_room_id="office_lobby",
                movement_phrase="climb back up the stairs",
            ),
            Exit(
                keyword="suspicious",
                target_room_id="subway_tunnel",
                movement_phrase="investigate the suspicious door",
            ),
        ],
    )

    office_roof = Room(
        id="office_roof",
        name="Office Rooftop",
        description=(
            "The building's rooftop with AC units and a small garden someone started but "
            "abandoned. You can see other districts from here - a forest, neon lights, "
            "and what looks like... a beach?"
        ),
        exits=[
            Exit(
                keyword="fire",
                target_room_id="office_floor_7",
                movement_phrase="descend the fire escape",
            ),
            Exit(
                keyword="escape",
                target_room_id="office_parking",
                movement_phrase="take the exterior fire escape down",
            ),
        ],
    )

    office_parking = Room(
        id="office_parking",
        name="Corporate Parking Lot",
        description=(
            "A vast parking lot with designated spots for employees of the month. "
            "Most cars look identical. A shopping cart from the mall sits abandoned "
            "in a parking space."
        ),
        exits=[
            Exit(
                keyword="building",
                target_room_id="office_lobby",
                movement_phrase="enter the building",
            ),
            Exit(
                keyword="window",
                target_room_id="office_break_room",
                movement_phrase="climb up through the window",
            ),
            Exit(
                keyword="escape",
                target_room_id="office_roof",
                movement_phrase="climb the fire escape",
            ),
            Exit(
                keyword="hedge",
                target_room_id="mall_loading",
                movement_phrase="squeeze through the hedge",
            ),
        ],
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
        exits=[
            Exit(
                keyword="revolving",
                target_room_id="nexus_clearing",
                movement_phrase="push through the revolving door",
            ),
            Exit(
                keyword="ramen",
                target_room_id="cyber_ramen",
                movement_phrase="duck into the ramen shop",
            ),
            Exit(
                keyword="fire",
                target_room_id="cyber_apartment",
                movement_phrase="climb the fire escape",
            ),
            Exit(
                keyword="alley",
                target_room_id="cyber_back_alley",
                movement_phrase="slip into the dark alley",
            ),
        ],
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
        exits=[
            Exit(
                keyword="street",
                target_room_id="cyber_street",
                movement_phrase="return to the street",
            ),
            Exit(
                keyword="kitchen",
                target_room_id="cyber_back_alley",
                movement_phrase="slip through the kitchen",
            ),
        ],
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
        exits=[
            Exit(
                keyword="fire",
                target_room_id="cyber_street",
                movement_phrase="descend the fire escape",
            ),
            Exit(
                keyword="vent",
                target_room_id="cyber_rooftop",
                movement_phrase="crawl through the vent",
            ),
        ],
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
        exits=[
            Exit(
                keyword="street",
                target_room_id="cyber_street",
                movement_phrase="return to the main street",
            ),
            Exit(
                keyword="kitchen",
                target_room_id="cyber_ramen",
                movement_phrase="enter through the kitchen door",
            ),
            Exit(
                keyword="dumpster",
                target_room_id="subway_tunnel",
                movement_phrase="squeeze behind the dumpster",
            ),
        ],
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
        exits=[
            Exit(
                keyword="vent",
                target_room_id="cyber_apartment",
                movement_phrase="drop back through the vent",
            ),
            Exit(
                keyword="bridge",
                target_room_id="museum_roof",
                movement_phrase="cross the makeshift bridge",
            ),
        ],
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
        exits=[
            Exit(
                keyword="forest",
                target_room_id="nexus_clearing",
                movement_phrase="exit to the forest",
            ),
            Exit(
                keyword="mall",
                target_room_id="mall_food_court",
                movement_phrase="enter the mall proper",
            ),
            Exit(
                keyword="staff",
                target_room_id="mall_backrooms",
                movement_phrase="slip through the staff door",
            ),
        ],
    )

    mall_food_court = Room(
        id="mall_food_court",
        name="Abandoned Food Court",
        description=(
            "A vast food court with empty stalls and overturned chairs. The fountain "
            "in the center still runs somehow. Muzak echoes eerily. One restaurant's "
            "sign still flickers: 'Pizza by the Slice'."
        ),
        exits=[
            Exit(
                keyword="arcade",
                target_room_id="mall_arcade",
                movement_phrase="return to the arcade",
            ),
            Exit(
                keyword="up",
                target_room_id="mall_upper",
                movement_phrase="take the escalator up",
            ),
            Exit(
                keyword="parking",
                target_room_id="mall_loading",
                movement_phrase="head to the loading dock",
            ),
        ],
    )

    mall_upper = Room(
        id="mall_upper",
        name="Upper Mall Level",
        description=(
            "The upper level with a defunct department store and empty boutiques. "
            "Mannequins in outdated fashion stand frozen in windows. A skylight "
            "shows the sky, though you're not sure which sky it is."
        ),
        exits=[
            Exit(
                keyword="down",
                target_room_id="mall_food_court",
                movement_phrase="take the escalator down",
            ),
            Exit(
                keyword="store",
                target_room_id="mall_store",
                movement_phrase="enter the department store",
            ),
            Exit(
                keyword="skylight",
                target_room_id="mall_roof",
                movement_phrase="climb through the skylight",
            ),
        ],
    )

    mall_store = Room(
        id="mall_store",
        name="Department Store",
        description=(
            "Racks of clothes from a bygone era. The escalators are frozen. "
            "Soft jazz plays from hidden speakers. The perfume section is "
            "overwhelming even after all this time."
        ),
        exits=[
            Exit(
                keyword="mall",
                target_room_id="mall_upper",
                movement_phrase="return to the mall",
            ),
            Exit(
                keyword="service",
                target_room_id="mall_backrooms",
                movement_phrase="take the service elevator",
            ),
        ],
    )

    mall_backrooms = Room(
        id="mall_backrooms",
        name="Mall Backrooms",
        description=(
            "Endless beige hallways with fluorescent lighting. Boxes of old "
            "merchandise gather dust. You hear the hum of ventilation but "
            "can't tell where it's coming from. Doors lead everywhere and nowhere."
        ),
        exits=[
            Exit(
                keyword="arcade",
                target_room_id="mall_arcade",
                movement_phrase="return to the arcade",
            ),
            Exit(
                keyword="elevator",
                target_room_id="mall_store",
                movement_phrase="take the service elevator up",
            ),
            Exit(
                keyword="loading",
                target_room_id="mall_loading",
                movement_phrase="go to the loading dock",
            ),
            Exit(
                keyword="unmarked",
                target_room_id="office_basement",
                movement_phrase="open the unmarked door",
            ),
        ],
    )

    mall_loading = Room(
        id="mall_loading",
        name="Loading Dock",
        description=(
            "The mall's loading area with abandoned trucks and shipping containers. "
            "Weeds grow through cracks in the concrete. A gap in the fence leads to "
            "what looks like a corporate parking lot."
        ),
        exits=[
            Exit(
                keyword="mall",
                target_room_id="mall_food_court",
                movement_phrase="enter the mall",
            ),
            Exit(
                keyword="backrooms",
                target_room_id="mall_backrooms",
                movement_phrase="enter the backrooms",
            ),
            Exit(
                keyword="fence",
                target_room_id="office_parking",
                movement_phrase="squeeze through the fence",
            ),
        ],
    )

    mall_roof = Room(
        id="mall_roof",
        name="Mall Rooftop",
        description=(
            "The mall's flat rooftop with old AC units and a surprisingly good view. "
            "You can see the forest clearing from here, with its impossible doors. "
            "Birds nest in the old neon signs."
        ),
        exits=[
            Exit(
                keyword="skylight",
                target_room_id="mall_upper",
                movement_phrase="drop back through the skylight",
            ),
        ],
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
        exits=[
            Exit(
                keyword="up",
                target_room_id="nexus_clearing",
                movement_phrase="climb the stairs up",
            ),
            Exit(
                keyword="tunnel",
                target_room_id="subway_tunnel",
                movement_phrase="enter the dark tunnel",
            ),
            Exit(
                keyword="across",
                target_room_id="subway_platform_2",
                movement_phrase="cross to the opposite platform",
            ),
        ],
    )

    subway_platform_2 = Room(
        id="subway_platform_2",
        name="Ghost Platform",
        description=(
            "An abandoned platform lit by flickering lights. Old advertisements "
            "from the 1950s still hang on the walls. You hear trains but never "
            "see them. A maintenance door is slightly ajar."
        ),
        exits=[
            Exit(
                keyword="across",
                target_room_id="subway_platform_1",
                movement_phrase="cross back to the main platform",
            ),
            Exit(
                keyword="maintenance",
                target_room_id="subway_control",
                movement_phrase="enter the maintenance door",
            ),
            Exit(
                keyword="dark",
                target_room_id="subway_tunnel",
                movement_phrase="venture into the dark tunnel",
            ),
        ],
    )

    subway_tunnel = Room(
        id="subway_tunnel",
        name="Service Tunnel",
        description=(
            "Dark tunnels with pipes and cables running along the walls. "
            "You hear dripping water and distant train sounds. Multiple passages "
            "branch off, leading to unexpected places."
        ),
        exits=[
            Exit(
                keyword="platform",
                target_room_id="subway_platform_1",
                movement_phrase="return to the central platform",
            ),
            Exit(
                keyword="ghost",
                target_room_id="subway_platform_2",
                movement_phrase="find the ghost platform",
            ),
            Exit(
                keyword="grate",
                target_room_id="office_basement",
                movement_phrase="squeeze through the grate",
            ),
            Exit(
                keyword="pipes",
                target_room_id="cyber_back_alley",
                movement_phrase="squeeze behind the pipes",
            ),
        ],
    )

    subway_control = Room(
        id="subway_control",
        name="Control Room",
        description=(
            "An old control room with switches and track diagrams. Half the "
            "lights on the board are red, half green, but nothing seems to "
            "change when you flip switches. Coffee cups suggest someone was here recently."
        ),
        exits=[
            Exit(
                keyword="platform",
                target_room_id="subway_platform_2",
                movement_phrase="return to the ghost platform",
            ),
            Exit(
                keyword="emergency",
                target_room_id="subway_surface",
                movement_phrase="take the emergency exit",
            ),
        ],
    )

    subway_surface = Room(
        id="subway_surface",
        name="Subway Entrance",
        description=(
            "You emerge at street level, but it's unclear which street. "
            "The entrance is covered in graffiti. Somehow, you can see both "
            "neon signs and office buildings from here."
        ),
        exits=[
            Exit(
                keyword="down",
                target_room_id="subway_control",
                movement_phrase="descend back to the control room",
            ),
            Exit(
                keyword="neon",
                target_room_id="cyber_street",
                movement_phrase="head toward the neon lights",
            ),
            Exit(
                keyword="offices",
                target_room_id="office_parking",
                movement_phrase="walk toward the office buildings",
            ),
        ],
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
        exits=[
            Exit(
                keyword="clearing",
                target_room_id="nexus_clearing",
                movement_phrase="return to the clearing",
            ),
            Exit(
                keyword="deeper",
                target_room_id="forest_deep",
                movement_phrase="venture deeper into the woods",
            ),
            Exit(
                keyword="stream",
                target_room_id="forest_stream",
                movement_phrase="follow the sound of water",
            ),
        ],
    )

    forest_deep = Room(
        id="forest_deep",
        name="Deep Woods",
        description=(
            "The forest is thick here, canopy blocking most light. You hear "
            "strange sounds - birds that don't sound quite right. An old stone "
            "structure is visible through the trees."
        ),
        exits=[
            Exit(
                keyword="grove",
                target_room_id="forest_grove",
                movement_phrase="return to the grove",
            ),
            Exit(
                keyword="ruins",
                target_room_id="forest_ruins",
                movement_phrase="approach the stone ruins",
            ),
            Exit(
                keyword="hollow",
                target_room_id="museum_storage",
                movement_phrase="crawl through the hollow tree",
            ),
        ],
    )

    forest_stream = Room(
        id="forest_stream",
        name="Babbling Brook",
        description=(
            "A clear stream runs through the forest. Smooth stones make natural "
            "stepping stones. The water is impossibly clear. You swear you can see "
            "subway tiles at the bottom of the deeper pools."
        ),
        exits=[
            Exit(
                keyword="grove",
                target_room_id="forest_grove",
                movement_phrase="return to the grove",
            ),
            Exit(
                keyword="upstream",
                target_room_id="forest_waterfall",
                movement_phrase="walk upstream",
            ),
            Exit(
                keyword="downstream",
                target_room_id="forest_pond",
                movement_phrase="follow the stream downstream",
            ),
        ],
    )

    forest_waterfall = Room(
        id="forest_waterfall",
        name="Hidden Waterfall",
        description=(
            "A small waterfall cascades into a pool. Behind the water, you can "
            "make out what looks like a cave entrance. The mist creates rainbows "
            "in the filtered sunlight."
        ),
        exits=[
            Exit(
                keyword="stream",
                target_room_id="forest_stream",
                movement_phrase="return to the stream",
            ),
            Exit(
                keyword="behind",
                target_room_id="forest_cave",
                movement_phrase="slip behind the waterfall",
            ),
        ],
    )

    forest_cave = Room(
        id="forest_cave",
        name="Cave Behind the Falls",
        description=(
            "A small cave hidden by the waterfall. Someone has been here - "
            "there's modern camping equipment and... is that a WiFi router? "
            "A narrow passage leads deeper."
        ),
        exits=[
            Exit(
                keyword="waterfall",
                target_room_id="forest_waterfall",
                movement_phrase="exit through the waterfall",
            ),
            Exit(
                keyword="squeeze",
                target_room_id="cyber_apartment",
                movement_phrase="squeeze through the narrow passage",
            ),
        ],
    )

    forest_pond = Room(
        id="forest_pond",
        name="Reflection Pond",
        description=(
            "A serene pond that perfectly reflects the sky. Lily pads float "
            "on the surface. When you look closely at your reflection, the "
            "background shows a different place each time."
        ),
        exits=[
            Exit(
                keyword="stream",
                target_room_id="forest_stream",
                movement_phrase="follow the stream back",
            ),
            Exit(
                keyword="around",
                target_room_id="forest_ruins",
                movement_phrase="walk around the pond",
            ),
        ],
    )

    forest_ruins = Room(
        id="forest_ruins",
        name="Forgotten Ruins",
        description=(
            "Ancient stone ruins overtaken by nature. Vines cover most surfaces. "
            "The architecture doesn't match any known civilization. A doorway "
            "still stands, though it should lead nowhere."
        ),
        exits=[
            Exit(
                keyword="woods",
                target_room_id="forest_deep",
                movement_phrase="return to the deep woods",
            ),
            Exit(
                keyword="pond",
                target_room_id="forest_pond",
                movement_phrase="walk to the pond",
            ),
            Exit(
                keyword="doorway",
                target_room_id="museum_ancient",
                movement_phrase="step through the ancient doorway",
            ),
        ],
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
        exits=[
            Exit(
                keyword="forest",
                target_room_id="nexus_clearing",
                movement_phrase="exit to the forest",
            ),
            Exit(
                keyword="exhibits",
                target_room_id="museum_main",
                movement_phrase="enter the main exhibits",
            ),
            Exit(
                keyword="stairs",
                target_room_id="museum_upper",
                movement_phrase="climb the grand staircase",
            ),
            Exit(
                keyword="staff",
                target_room_id="museum_storage",
                movement_phrase="slip through the staff door",
            ),
        ],
    )

    museum_main = Room(
        id="museum_main",
        name="Main Exhibition Hall",
        description=(
            "A vast hall with exhibits from different eras that shouldn't exist "
            "together. A T-Rex skeleton stands next to a space shuttle. Medieval "
            "armor faces off against robot prototypes."
        ),
        exits=[
            Exit(
                keyword="lobby",
                target_room_id="museum_lobby",
                movement_phrase="return to the lobby",
            ),
            Exit(
                keyword="ancient",
                target_room_id="museum_ancient",
                movement_phrase="visit the ancient wing",
            ),
            Exit(
                keyword="future",
                target_room_id="museum_future",
                movement_phrase="explore the future wing",
            ),
        ],
    )

    museum_ancient = Room(
        id="museum_ancient",
        name="Ancient History Wing",
        description=(
            "Artifacts from civilizations both real and impossible. Some exhibits "
            "are behind glass, others invite touching. A doorway that looks like "
            "it belongs in ruins leads somewhere unexpected."
        ),
        exits=[
            Exit(
                keyword="main",
                target_room_id="museum_main",
                movement_phrase="return to the main hall",
            ),
            Exit(
                keyword="doorway",
                target_room_id="forest_ruins",
                movement_phrase="step through the ancient doorway",
            ),
        ],
    )

    museum_future = Room(
        id="museum_future",
        name="Future Tech Wing",
        description=(
            "Gleaming displays of technology that might exist someday. Interactive "
            "holograms demonstrate impossible inventions. One exhibit is just a "
            "door labeled 'Staff Only' that hums with electricity."
        ),
        exits=[
            Exit(
                keyword="main",
                target_room_id="museum_main",
                movement_phrase="return to the main hall",
            ),
            Exit(
                keyword="humming",
                target_room_id="cyber_apartment",
                movement_phrase="investigate the humming door",
            ),
        ],
    )

    museum_upper = Room(
        id="museum_upper",
        name="Upper Gallery",
        description=(
            "A quiet gallery with paintings that seem to move when you're not "
            "looking directly at them. Large windows show views of different "
            "places - a forest, a city, an office building."
        ),
        exits=[
            Exit(
                keyword="stairs",
                target_room_id="museum_lobby",
                movement_phrase="descend the grand staircase",
            ),
            Exit(
                keyword="roof",
                target_room_id="museum_roof",
                movement_phrase="climb to the roof access",
            ),
        ],
    )

    museum_storage = Room(
        id="museum_storage",
        name="Museum Storage",
        description=(
            "Countless artifacts in various states of cataloging. Crates labeled "
            "with impossible dates. A hollow tree trunk is marked 'Forest Exhibit' "
            "but seems to have depth beyond its size."
        ),
        exits=[
            Exit(
                keyword="lobby",
                target_room_id="museum_lobby",
                movement_phrase="return to the lobby",
            ),
            Exit(
                keyword="tree",
                target_room_id="forest_deep",
                movement_phrase="crawl through the hollow tree trunk",
            ),
        ],
    )

    museum_roof = Room(
        id="museum_roof",
        name="Museum Rooftop Sculpture Garden",
        description=(
            "A rooftop garden with modern sculptures that might be art or might be "
            "leftover AC units. A makeshift bridge of planks leads to another building's "
            "roof. The view shows all the impossible geography."
        ),
        exits=[
            Exit(
                keyword="gallery",
                target_room_id="museum_upper",
                movement_phrase="return to the gallery",
            ),
            Exit(
                keyword="planks",
                target_room_id="cyber_rooftop",
                movement_phrase="balance across the planks",
            ),
        ],
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
