from .world import World
from .room import Room


def create_seed_world() -> World:
    """Create a seed world with 4 rooms in a 2x2 grid for development."""

    world = World()

    # Create 4 rooms
    room_1 = Room(
        id="room_1",
        name="Forest Clearing",
        description="A peaceful clearing in the forest. Sunlight filters through the canopy above.",
        connections={"east": "room_2", "south": "room_3"},
    )

    room_2 = Room(
        id="room_2",
        name="Cave Entrance",
        description="A dark cave entrance looms before you. Cool air flows from within.",
        connections={"west": "room_1", "south": "room_4"},
    )

    room_3 = Room(
        id="room_3",
        name="River Bank",
        description="A gentle river flows by. You can hear the water babbling over smooth stones.",
        connections={"north": "room_1", "east": "room_4"},
    )

    room_4 = Room(
        id="room_4",
        name="Old Ruins",
        description="Ancient stone ruins covered in moss. There's an air of mystery here.",
        connections={"north": "room_2", "west": "room_3"},
    )

    # Add rooms to world
    world.rooms = {
        "room_1": room_1,
        "room_2": room_2,
        "room_3": room_3,
        "room_4": room_4,
    }

    return world


# Create global instance for development
seed_world = create_seed_world()
